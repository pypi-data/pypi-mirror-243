"""
import gym
from qunet import DQN, MLP

env = gym.make("LunarLander-v2")   # nS=8, nA=4
dqn = DQN( env )

model = MLP(input=env.observation_space.shape[0], outpput=env.action_space.n,  hidden=[256,64])

dqn.init(model)
print(dqn.params)
dqn.learn(episodes = 2000)

# Environment should have:
# s0 = env.reset()                 # s0.shape = (nS,)
# s1, r1, done, _ = env.step(a0)   # a0: int in (0...nA-1); r1: float; done: bool
# env.close()

"""
import math, time, copy, os
import numpy as np, matplotlib.pyplot as plt
import torch, torch.nn as nn

from ..config import Config

class MemoryBuffer:
    """
    Overwrite memory for storing the environment model.
    This implementation is not the most efficient, but it is needed for experimenting with sorting.
    """
    def __init__(self, capacity, n_states, n_actions):
        """
        capacity  - memory capacity (maximum number of stored items)
        n_states  - number of state variables
        n_actions - number of actions
        """
        self.capacity = capacity    # maximum number of stored elements
        self.count = 0              # how many items have already been saved
        self.index = 0              # index of element to be inserted
        self.nS = n_states          # dim of the state
        self.nA = n_actions         # number of actions

        self.memo = np.zeros( (capacity, self.nS*2 + 4), dtype = np.float32)
    #------------------------------------------------------------------------------------

    def add(self, s0, a0, s1, r1, done, rewrite = 0):
        """ Add example to memory """
        self.index = self.index % self.capacity

        norm = np.dot(s1,s1)**0.5
        self.memo[self.index] = np.concatenate(( s0, s1, [a0], [r1], [done], [norm]) )

        self.index += 1
        self.count += 1

        if  abs(rewrite) < 1.0 and (self.count == self.capacity
            or (self.count > self.capacity and self.index >= int(abs(rewrite)*self.capacity)) ):
            self.memo = self.memo[ self.memo[:, -1].argsort() ]
            if rewrite < 0:
                self.memo = self.memo[::-1]   # large norm at the beginig
            self.index = 0
    #------------------------------------------------------------------------------------

    def samples(self, count):
        """ Return count of random examples from memory """
        mem_max = min(self.count, self.capacity)
        indxs = np.random.choice(mem_max, count, replace=False)
        sample = self.memo[indxs]
        s0 = sample[:, 0:           self.nS]
        s1 = sample[:, self.nS:     2*self.nS]
        a0 = sample[:, 2*self.nS:   2*self.nS+1]
        r1 = sample[:, 2*self.nS+1: 2*self.nS+2]
        en = sample[:, 2*self.nS+2: 2*self.nS+3]
        return torch.tensor(s0), torch.tensor(a0, dtype = torch.int64), torch.tensor(s1), torch.tensor(r1), torch.tensor(en)
    #------------------------------------------------------------------------------------

    def stat(self):
        """ Statistic of s1 length and actions """
        num = min(self.count, self.capacity)
        if num == 0:
            return [],[],[],[]

        s1 = self.memo[:num, self.nS: 2*self.nS]
        hist_S, bins_S = np.histogram(s1, bins=np.linspace(0, math.sqrt(self.nS), 101), density=True)

        a = self.memo[:num, 2*self.nS: 2*self.nS+1],
        hist_A, bins_A = np.histogram(a, bins=np.linspace(-0.5, self.nA-0.5, self.nA+1), density=True)

        return hist_S, bins_S, hist_A, bins_A

#========================================================================================

class DQN:
    """ DQN метод для дискретных действий """
    def __init__(self):
        self.params = Config(             # default parameters
            env      = "Environment",
            ticks    = 200,
            timeout  = True,            # whether to consider reaching ticks as a terminal state
            method   = "DQN",           # kind of the method (DQN, DDQN)
            gamma    = 0.99,            # discount factor
            eps1     = 1.0,             # initial value epsilon
            eps2     = 0.001,           # final value   epsilon
            decays   = 1000,            # number of episodes to decay eps1 - > eps2
            update   = 10,              # target model update rate (in frames = time steps)
            best     = False,           # target model is best
            batch    = 100,             # batch size for training
            capacity = 100_000,         # memory size
            rewrite  = 1.0,             # rewrite memory (if < 1 - sorted)
            reset    = 1,               # reset i-th agent in muli-agent mode when done (1 or 2)            
            loss     = 'mse',           # loss function (mse, huber)
            optim    = 'adam',          # optimizer (sgd, adam)
            lm       = 0.001,           # learning rate
        )
        self.bounds= Config(low=None, high=None) # min and max observation values
        self.view = Config(ymin=None, ymax=None)

        self.last_loss = 0.             # last loss
        self.history   = {'episodes': [], 'bests': [] }
    #------------------------------------------------------------------------------------

    def init(self, env, model, nS, nA):
        """ Create a neural network and optimizer """
        self.env  = env                          # environment we work with
        self.nA   = nA                           # number of discrete actions
        self.nS   = nS                           # number of state components

        self.device =torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print("device:", self.device)

        self.model = Config(
            current = model.to(self.device),
            target  = copy.deepcopy(model).to(self.device))

        self.best = Config(
            model   = copy.deepcopy(model),
            reward  = -1000000,
            episode = -1,
            file_id = 0,
            fname   = None)

        if   self.params.loss == 'mse':
             self.loss  = nn.MSELoss()
        elif self.params.loss == 'huber':
             self.loss = nn.HuberLoss()
        else:
            print("ERROR: Unknown loss function!!!")

        if   self.params.optim == 'sgd':
             self.optim = torch.optim.SGD(self.model.current.parameters(), lr=self.params.lm, momentum=0.8)
        elif self.params.optim == 'adam':
             self.optim = torch.optim.Adam(self.model.current.parameters(), lr=self.params.lm)
        else:
            print("ERROR: Unknown optimizer!!!")

        self.memo = MemoryBuffer(self.params.capacity, self.nS, self.nA)

        self.epsilon     = self.params.eps1        # start value in epsilon greedy strategy
        self.decay_rate  = math.exp(math.log(self.params.eps2/self.params.eps1)/self.params.decays)

        self.episode = 0
        self.frame   = 1

        print(f"decay_rate: {self.decay_rate:.4f}")
        print(self.model.current)
        print("low :   ", self.bounds.low)
        print("high:   ", self.bounds.high)
    #------------------------------------------------------------------------------------

    def scale(self, obs):
        """ to [-1...1] """
        if self.bounds.low is None or self.bounds.high is None:
            return obs

        low, high = self.bounds.low, self.bounds.high
        if obs.ndim == 2:
            low, high = low.reshape(1, -1), high.reshape(1, -1)
        return -1. + 2.*(obs - low)/(high-low)
    #------------------------------------------------------------------------------------

    def policy(self, state):
        """ Return action according to epsilon greedy strategy """
        if np.random.random() < self.epsilon:
            return np.random.randint(self.nA)    # random action

        x = torch.tensor(state, dtype=torch.float32).to(self.device)
        with torch.no_grad():
            y = self.model.current(x).detach().to('cpu').numpy()
        return np.argmax(y)                      # best action
    #------------------------------------------------------------------------------------

    def run_episode(self, ticks = 200):
        """ Run one episode, keeping the environment model in memory """
        rew = 0                                  # total reward
        s0 = self.env.reset()                    # initial state
        s0 = self.scale (s0)                     # scale it
        a0 = self.policy(s0)                     # get action
        for t in range(1, ticks+1):
            s1, r1, done, _ = self.env.step(a0)
            s1 = self.scale (s1)
            a1 = self.policy(s1)

            dn = done and (self.params.timeout or t < ticks)
            #self.memo.add(s0, a0, s1, r1, float(dn), self.params.rewrite )
            self.memo.add(s0, a0, s1, r1, float(dn), 1. )

            if self.frame % self.params.update == 0:  # copy model to target
                if self.params.best and self.best.model is not None:
                    self.model.target.load_state_dict( self.best.model.state_dict() )    
                else:
                    self.model.target.load_state_dict( self.model.current.state_dict() )

            if self.memo.count >= self.params.batch:
                self.learn_model()

            rew += r1
            self.frame += 1

            if done:
                break

            s0, a0 = s1, a1
        return rew, t
    #------------------------------------------------------------------------------------

    def epsilon_decay(self):
            self.epsilon *= self.decay_rate                # epsilon-decay
            if self.epsilon < self.params.eps2:
                self.epsilon = 0.
    #------------------------------------------------------------------------------------

    def learn(self, episodes = 100000, stat1 = 10, stat2 = 100, plots = -1):
        """ Repeat episodes episodes times """
        self.frame = 1
        rews, lens, mean, beg   = [], [], 0, time.process_time()
        for episode in range(1, episodes+1):
            rew, t = self.run_episode( self.params.ticks )
            rews.append( rew )
            lens.append(t)

            self.epsilon_decay()

            if episode % stat1 == 0:
                self.history['episodes'].append([episode, np.mean(rews[-stat1:]), np.mean(rews[-stat2:])])

            if  episode % stat2 == 0:
                mean, std    = np.mean(rews[-stat2:]), np.std(rews[-stat2:])
                lensM, lensS = np.mean(lens[-stat2:]), np.std(lens[-stat2:])
                if mean > self.best.reward:
                    self.best.reward = mean
                    self.best.episode = episode
                    self.best.model.load_state_dict( self.model.current.state_dict() )
                    self.history['bests'].append([episode, mean])
                maxQ = self.maxQ.to('cpu')
                print(f"{episode:6d} rew:{mean:7.1f} ± {std/stat2**0.5:3.1f}, best:{self.best.reward:7.2f}, ticks:{lensM:3.0f}, eps:{self.epsilon:.3f}, Q:{maxQ.mean():8.2f} ±{maxQ.std():6.2f}, loss:{self.last_loss:7.3f}, {(time.process_time() - beg):3.0f}s")
                beg = time.process_time()

            if  plots > 0 and episode % plots == 0:
                self.plot(f"{self.params.env}  Episode: {episode}  best: {self.best.reward:7.1f} [{self.best.episode}]")
                #self.test(episodes = 1, ticks = self.params.ticks, render = True)
                #env.close()
    #------------------------------------------------------------------------------------

    def multi_agent_random_policy(self, state):
        """ random action """
        return np.random.randint(low=0, high=self.nA, size=(state.shape[0],))    
    #------------------------------------------------------------------------------------

    def multi_agent_policy(self, model, state):
        """
        Return action according to epsilon greedy strategy
        state: (N, nS)
        """        
        if np.random.random() < self.epsilon:
            return self.multi_agent_random_policy(state)    # random action            

        x = torch.tensor(state, dtype=torch.float32).to(self.device)
        with torch.no_grad():
            y = model(x).detach().to('cpu').numpy()
        return np.argmax(y,axis=-1)              # best action (N, )
    #------------------------------------------------------------------------------------

    def multi_agent_training(self, episodes = 100000, stat1 = 10, stat2 = 100, plots = -1, start_episode_check=-1, check_rate=1.1, fname=""):        
        episodes += self.episode
        rews, lens,  mean, beg   = [], [], 0, time.process_time()
        model = self.model.current

        s0 = self.env.reset()                    # initial state (N,nS)
        s0 = self.scale (s0)                     # scale it      (N,nS)
        a0 = self.multi_agent_policy(model, s0)  # get action    (N,)
        N  = len(s0)
        rew = np.zeros((N,))                     # total reward
        ticks = np.zeros((N,))                   # время эпизода i-го анента
        
        for tick in range(1, episodes*self.params.ticks + 1):
            s1, r1, done, _ = self.env.step(a0)
            s1 = self.scale (s1)
            a1 = self.multi_agent_policy(model, s1)

            for i in range(len(s0)):
                ticks[i] += 1
                expired = (ticks[i] >= self.params.ticks)

                dn = done[i] and (self.params.timeout or not expired)  # ??? для обычных сред done=True и при expired
                self.memo.add(s0[i], a0[i], s1[i], r1[i], float(dn), 1. )
                rew[i] += r1[i]
                if expired or done[i]:           # один из агентов закончил эпизод
                    self.episode  += 1
                    self.epsilon_decay()

                    rews.append( rew[i] )
                    lens.append( ticks[i])
                    ticks[i] = 0
                    rew[i]   = 0

                    if self.episode % stat1 == 0:
                        self.history['episodes'].append([self.episode, np.mean(rews[-stat1:]), np.mean(rews[-stat2:])])

                    if  self.episode >= stat2:
                        mean, std    = np.mean(rews[-stat2:]), np.std(rews[-stat2:])
                        lensM, lensS = np.mean(lens[-stat2:]), np.std(lens[-stat2:])
                        if mean > self.best.reward:
                            self.best.reward = mean
                            self.best.episode = self.episode
                            self.best.model.load_state_dict(model.state_dict() )
                            self.history['bests'].append([self.episode, mean])
                            self.best.file_id += 1
                            if len(fname) and start_episode_check > 0 and self.episode > start_episode_check:
                                name = fname + f"_s{self.nS}a{self.nA}_{self.best.file_id:04d}_r{self.best.reward:.2f}_e{self.best.episode}.pt"
                                self.save(self.best.model, self.best.reward, name)
                                self.best.fname = name
                        elif len(fname) and  start_episode_check > 0 and self.episode > start_episode_check and mean > self.best.reward * check_rate:
                            self.best.file_id += 1
                            name = fname + f"_s{self.nS}a{self.nA}_{self.best.file_id:04d}_r{mean:.2f}_e{self.episode}_chk.pt"
                            self.save(model, mean, name)

                    if  self.episode % stat2 == 0:
                        maxQ = self.maxQ.to('cpu')
                        print(f"{self.episode:6d} rew:{mean:7.1f} ± {std/stat2**0.5:3.1f}, best:{self.best.reward:7.2f}, ticks:{lensM:3.0f} ± {lensS/stat2**0.5:3.0f}, eps:{self.epsilon:.3f}, Q:{maxQ.mean():8.2f} ±{maxQ.std():6.2f}, loss:{self.last_loss:7.3f}, {(time.process_time() - beg):3.0f}s")
                        beg = time.process_time()

                    if  plots > 0 and self.episode % plots == 0:
                        self.plot(f"{self.params.env}  Episode: {self.episode}  best: {self.best.reward:7.1f} [{self.best.episode}]")

                    if self.episode > episodes:
                        return

                    if self.params.reset > 0:
                        si = self.env.reset(i)
                        if si is not None:
                            si = self.scale (si)
                            ai = self.multi_agent_policy(model, si)
                            if self.params.reset == 1:
                                s1[i], a1[i] = si[0], ai[0]
                            else:
                                s1, a1 = si, ai

            if self.frame % self.params.update == 0:  # copy model to target
                if self.params.best and self.best.model is not None:
                    self.model.target.load_state_dict( self.best.model.state_dict() )    
                else:
                    self.model.target.load_state_dict( self.model.current.state_dict() )

            if self.memo.count >= self.params.batch:
                self.learn_model()

            self.frame += 1

            s0, a0 = s1, a1
        return
    #------------------------------------------------------------------------------------

    def save(self, model, reward=0, fname="model"):
        state = {
            'model':  model.state_dict(),
            'reward': reward,
            'cfg':    model.cfg.get_str(),
            'hist':   self.history,
            'params': self.params,
        }                 
        torch.save(state, fname)                
    #------------------------------------------------------------------------------------

    def multi_agent_testing(self, model, episodes = 1000, reset_steps=-1, epsilon=0, info="", sufix="", verbose=1):   
        self.epsilon = epsilon
        episode = 0
        rews, lens,  mean, beg   = [], [], 0, time.process_time()

        s0 = self.env.reset()                    # initial state (N,nS)
        s0 = self.scale (s0)                     # scale it      (N,nS)
        a0 = self.multi_agent_policy(model, s0)  # get action    (N,)
        N  = len(s0)
        rew = np.zeros((N,))                     # total reward
        ticks = np.zeros((N,))                   # время эпизода i-го анента        
        for step in range(1, episodes*self.params.ticks + 1):
            s1, r1, done, _ = self.env.step(a0)
            s1 = self.scale (s1)
            a1 = self.multi_agent_policy(model, s1)

            for i in range(len(s0)):
                ticks[i] += 1
                expired = (ticks[i] >= self.params.ticks)                
                rew[i] += r1[i]
                if expired or done[i]:           # один из агентов закончил эпизод
                    episode  += 1                    
                    rews.append( rew[i] )
                    lens.append( ticks[i])
                    ticks[i] = 0
                    rew[i]   = 0
                    print(f"\r{episode:6d} {np.mean(rews):.2f}", end=" ")
                    if episode > episodes:
                        if verbose:
                            mean, std = np.mean(rews),    np.std(rews) / len(rews)**0.5
                            lensM, lensS = np.mean(lens), np.std(lens)/ len(lens)**0.5
                            print(f"{info}rew:{mean:7.1f} ± {std:3.1f}, ticks:{lensM:3.0f} ± {lensS:3.0f}, eps:{self.epsilon:.3f}, {(time.process_time() - beg):3.0f}s {sufix}")
                        return rews, lens                                            

                    if self.params.reset > 0:
                        si = self.env.reset(i)
                        if si is not None:
                            si = self.scale (si)
                            ai = self.multi_agent_policy(model, si)
                            if self.params.reset == 1:
                                s1[i], a1[i] = si[0], ai[0]
                            else:
                                s1, a1 = si, ai

            if reset_steps > 0 and step % reset_steps == 0:
                s1 = self.env.reset()  
                s1 = self.scale (s1)                     # scale it      (N,nS)
                a1 = self.multi_agent_policy(model, s1)  # get action    (N,)

            s0, a0 = s1, a1

    #------------------------------------------------------------------------------------

    def multi_agent_testing_dir(self, dir="", episodes = 1000, reset_steps=-1, epsilon=0, info="", verbose=1, count=10):   
        fnames = []
        for fname in os.listdir(dir):    
            path = os.path.join(dir, fname)
            if os.path.isfile(path) and path.endswith(".pt"):                
                fnames.append(path)              
        fnames = sorted(fnames)[-count: ]
        fnames.append(self.best.fname)
        fnames = sorted(list(set(fnames)))[::-1]

        model = copy.deepcopy(self.model.current)
        for fname in fnames:
            state = torch.load(fname)
            model.load_state_dict(state['model'])
            self.multi_agent_testing(model, episodes = episodes, reset_steps=reset_steps, epsilon=epsilon, info=info, sufix=fname)

    #------------------------------------------------------------------------------------

    def learn_model(self):
        """ Model Training """
        batch = self.params.batch

        S0, A0, S1, R1, Done = self.memo.samples(batch)
        S0 = S0.to(self.device); A0 = A0.to(self.device)
        S1 = S1.to(self.device); R1 = R1.to(self.device);  Done = Done.to(self.device)

        if self.params.method == 'DQN':
            with torch.no_grad():
                y = self.model.target(S1).detach()
            self.maxQ, _ = torch.max(y, 1)      # maximum Q values for S1
        elif self.params.method == 'DDQN':
            y = self.model.current(S1)
            a = torch.argmax(y,1).view(-1,1)   # a = arg max Q(s1,a; theta)
            with torch.no_grad():
                q = self.model.target(S1)
            self.maxQ = q.gather(1, a)         # Q(s1, a; theta')
        else:
            print("Unknown method")

        sum_loss = 0
        s0, a0   = S0, A0.view(-1,1)
        r1, done = R1.view(-1,1), Done.view(-1,1)
        q1       = self.maxQ.view(-1,1)

        yb = r1 + self.params.gamma * q1 * (1.0 - done)

        y = self.model.current(s0)     # forward
        y = y.gather(1, a0)
        L = self.loss(y, yb)

        self.optim.zero_grad()     # reset the gradients
        L.backward()                   # calculate gradients
        self.optim.step()          # adjusting parameters

        sum_loss += L.detach().item()

        self.last_loss = sum_loss
    #------------------------------------------------------------------------------------

    def plot(self, text):
        self.plot_all(text, self.history)
    #------------------------------------------------------------------------------------

    def plot_all(self, text, history):
        """ Plot histogram for states and actions """
        hist_S, bins_S, hist_A, bins_A = self.memo.stat()

        fig, ax = plt.subplots(1, 3, figsize=(12,5), gridspec_kw={'width_ratios': [2, 1, 5]})
        plt.suptitle(text, fontsize=18)

        ax[0].set_xlim(min(bins_S), max(bins_S))    # histogram for S1
        ax[0].grid(axis='x', alpha=0.75); ax[0].grid(axis='y', alpha=0.75)
        ax[0].set_xlabel('|s1|', fontsize=16)
        bins = [ (bins_S[i]+bins_S[i+1])/2 for i in range(len(bins_S)-1)]
        ax[0].bar(bins, hist_S, width=0.5, color='blue')

        ax[1].set_xlim(min(bins_A), max(bins_A))    # histogram for A
        ax[1].grid(axis='x', alpha=0.75); ax[1].grid(axis='y', alpha=0.75)
        ax[1].set_xlabel('actions', fontsize=16)
        ax[1].set_xticks(np.arange(self.nA));
        bins = [ (bins_A[i]+bins_A[i+1])/2 for i in range(len(bins_A)-1)]
        ax[1].bar(bins, hist_A, width=0.5, color='blue')

        if len(history['episodes']):
            hist = np.array(history['episodes'])   
            ax[2].plot(hist[:,0], hist[:,1], linewidth=1)
            ax[2].plot(hist[:,0], hist[:,2], linewidth=2)
            if len(history['bests']):
                hist = np.array(history['bests'])  
                ax[2].scatter(hist[:,0], hist[:,1], s=15, c='g', edgecolors='black', linewidths=0.5)

            if self.view.ymin is not None and self.view.ymax is not None:
                ax[2].set_ylim(self.view.ymin, self.view.ymax)
            ax[2].set_xlabel('episode', fontsize=16)
            ax[2].grid(axis='x', alpha=0.75); ax[2].grid(axis='y', alpha=0.75)
            params = self.params.get_str("\n")
            ax[2].text(0.05, 0.95, "".join(params), {'fontsize':12, 'fontname':'monospace'},  transform = ax[2].transAxes, ha='left',  va='top')

        plt.show()
    #------------------------------------------------------------------------------------

    def test(self, episodes = 1000, ticks = 1000, render = False):
        """ Q-Function Testing """
        rews = []
        for episode in range(1, episodes+1):
            tot = 0
            obs =  self.env.reset()
            for _ in range(ticks):
                action = self.policy( self.scale(obs) )
                obs, rew, done, _ = self.env.step(action)
                tot += rew
                if render:
                    self.env.render()
                if done:
                    break
            rews.append(tot)
            if episode % 100:
                print(f"\r {episode:4d}: Reward: {np.mean(rews):7.3f} ± {np.std(rews)/len(rews)**0.5:.3f}", end="")
        print()
