import numpy as np
import torch
from qunet import MLP


class AI_RL:
    def __init__(self) -> None:
        nS, nA = 17, 5

        #  moving_targets=False                             reset,rest_period    times:    rew:
        #state = torch.load("models/01/model_v0_s17a5_014_-62.24.pt") # (0)     [2.51|130 ]s   -62
        #state = torch.load("models/01/model_v0_s17a5_013_-128.38.pt")# (1)     [2.54|6.02]s  -128
        #state = torch.load("models/01/model_v0_s17a5_012_-76.72.pt") # (2,100) [1.79|7.23]s   -77 <-- лучший для неподвижных целей
    
        #  moving_targets=True    (2,100)                                       moving_targets=True   =False
        #state = torch.load("models/01/model_v0_s17a5_012_-76.72.pt")  #           # [4.11|6.38]  [1.80|6.80]s для сравнения
        #state = torch.load("models/01/model_v20p100_s17a5_029_r-86.45_e25700.pt") # [3.57|4.73]   [inf|inf]        
        #state = torch.load("models/01/model_v20p50_s17a5_020_r-82.69_e6600.pt")   # [2.33|3.93]   [5.95|6.23] но лучше (3 их 4х застряли)
        state = torch.load("models/01/model_v20p20_s17a5_025_r-80.56_e12100.pt")   # [2.33|4.38]   [1.84|7.10]                                  

        print('reward:', state['reward'])
        self.model = MLP(input=nS, output=nA,  hidden=[256, 64]) 
        self.model.load_state_dict(state['model'])
        print(self.model)

        self.device  = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)
        #self.actions = np.array([[-1.,-1.],[-1.,0.],[-1.,1.], [ 0.,-1],[ 0.,0],[ 0.,1.], [1.,-1.],[1.,0],[1.,1.]])
        self.actions = np.array([[-1.,-1.], [-1.,1.], [1.,-1.], [1.,0], [1.,1.]])

    def reset(self, init_state, state):
        """ Receives initial state """
        self.ai_kind = init_state['ai_kind']
        self.kinds   = init_state['kind']
        self.N       = init_state['n_cars']
        self.seg_p1  = torch.tensor(init_state['string'][:,0,:])  # begin and end
        self.seg_p2  = torch.tensor(init_state['string'][:,1,:])  # of segment


    #---------------------------------------------------------------------------

    def step(self, state, reward, done):
        """
        Receives state and reward, returns simple actions.
        """    
        state = self.features(state)
        with torch.no_grad():
            state = torch.tensor(state, device=self.device)
            Q = self.model(state)
            a = torch.argmax(Q, dim=-1).cpu().numpy() 

        action = np.zeros((len(a), 2))
        for i in range(len(a)):
            action[i] = self.actions[a[i]]        
        
        return action
    #------------------------------------------------------------------------------------

    def features(self, state, vel_scale=20, dist_scale=10, eps=1e-6):
        """
        Начнём с преследования цели. Фичи - простые скаляры
        """
        pos, vel, dir1 = state['pos'], state['vel'], state['dir'] 
        whe  = state['wheels'] 
        t_pos, t_vel = state['target_pos'],  state['target_vel']

        vel   = vel   / vel_scale
        t_vel = t_vel / vel_scale

        v_len = np.linalg.norm(vel, axis=-1, keepdims=True)
        dir2= np.zeros_like(dir1)
        dir2[:, 0] = dir1[:, 1];   dir2[:, 1] = -dir1[:, 0];

        R = t_pos - pos
        V = t_vel - vel
        R_len = np.linalg.norm(R, axis=-1, keepdims=True)
        V_len = np.linalg.norm(V, axis=-1, keepdims=True)        

        tar1    = R / (R_len + eps)
        tar2    = np.zeros_like(tar1)
        tar2[:, 0] = tar1[:, 1];   tar2[:, 1] = -tar1[:, 0]

        K     = t_vel - tar1*(tar1*t_vel).sum(axis=-1).reshape(-1,1)

        state = np.hstack([
            v_len,
            (vel*dir1).sum(axis=-1).reshape(-1,1),
            (vel*dir2).sum(axis=-1).reshape(-1,1),
            whe,

            (tar1*dir1).sum(axis=-1).reshape(-1,1),
            (tar1*dir2).sum(axis=-1).reshape(-1,1),            

            np.tanh( R_len / dist_scale ),
            np.linalg.norm(t_vel, axis=-1, keepdims=True),
            V_len,            
            np.linalg.norm(t_vel, axis=-1, keepdims=True),
            (V * tar1).sum(axis=-1).reshape(-1, 1),
            (V * tar2).sum(axis=-1).reshape(-1, 1),
            (t_vel * dir1).sum(axis=-1).reshape(-1, 1),
            (t_vel * dir2).sum(axis=-1).reshape(-1, 1),
            (K * dir1).sum(axis=-1).reshape(-1, 1),
            (K * dir2).sum(axis=-1).reshape(-1, 1),
        ])
        return state
    #------------------------------------------------------------------------------------

    def features2(self, state, vel_scale=20, dist_scale=10, eps=1e-6):
        """
        Начнём с преследования цели. Фичи - простые скаляры
        """
        pos, vel, dir1 = state['pos'], state['vel'], state['dir'] 
        whe  = state['wheels'] 
        t_pos, t_vel = state['target_pos'],  state['target_vel']

        vel   = vel   / vel_scale
        t_vel = t_vel / vel_scale

        v_len = np.linalg.norm(vel, axis=-1, keepdims=True)
        dir2= np.zeros_like(dir1)
        dir2[:, 0] = dir1[:, 1];   dir2[:, 1] = -dir1[:, 0];

        R = t_pos - pos
        V = t_vel - vel
        R_len = np.linalg.norm(R, axis=-1, keepdims=True)
        V_len = np.linalg.norm(V, axis=-1, keepdims=True)        

        n1    = R / (R_len + eps)
        n2    = np.zeros_like(n1)
        n2[:, 0] = n1[:, 1];   n2[:, 1] = -n1[:, 0]

        K     = t_vel - n1*(n1*t_vel).sum(axis=-1).reshape(-1,1)

        state = np.hstack([
            v_len,
            (vel*dir1).sum(axis=-1).reshape(-1,1),
            (vel*dir2).sum(axis=-1).reshape(-1,1),
            whe,

            (n1*dir1).sum(axis=-1).reshape(-1,1),
            (n1*dir2).sum(axis=-1).reshape(-1,1),            

            np.tanh( R_len / dist_scale ),
            np.linalg.norm(t_vel, axis=-1, keepdims=True),
            V_len,            
            np.linalg.norm(t_vel, axis=-1, keepdims=True),
            (V * n1).sum(axis=-1).reshape(-1, 1),
            (V * n2).sum(axis=-1).reshape(-1, 1),
            (t_vel * dir1).sum(axis=-1).reshape(-1, 1),
            (t_vel * dir2).sum(axis=-1).reshape(-1, 1),
            (K * dir1).sum(axis=-1).reshape(-1, 1),
            (K * dir2).sum(axis=-1).reshape(-1, 1),
        ])
        return state
