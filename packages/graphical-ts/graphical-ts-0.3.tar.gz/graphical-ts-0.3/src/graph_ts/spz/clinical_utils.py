import numpy as np

TAU_MAX = 4
TU = 1
BLD_FILLED = np.random.uniform(250, 420)

def init_bld(ts, *, bld_filled=BLD_FILLED, tau_max=TAU_MAX, tu=TU):
    T = len(ts)
    
    bld_pt = [0, T-1]
    for i in range(3):
        bld_pt.append(np.random.randint(i * T / 3 + 3 *tau_max - tu, (i + 1) * T / 3 + 3 * tau_max - tu))  # recrording needs to be one hour longer
    bld_pt.sort()
    
    bld = np.zeros(T)
    bld[T-1] = 0
    
    bld[bld_pt[-2]] = bld_filled
    
    for i in range(len(bld_pt) - 1):
        if i % 2 == 0:
            bld[bld_pt[i]] = 0
        elif i % 2 != 0:
            bld[bld_pt[i]] = bld_filled
        for j in range(1, bld_pt[i + 1] - bld_pt[i]):
            if i % 2 == 0:
                bld[j + bld_pt[i]] = j * bld_filled / (
                            bld_pt[i + 1] - bld_pt[i]) + np.random.normal(0, 2)
            else:
                bld[j + bld_pt[i]] = -(j + bld_pt[i] - bld_pt[i + 1]) * bld_filled / (
                            bld_pt[i + 1] - bld_pt[i]) + np.random.normal(0, 2)
    return bld




def init_bldv2(ts, *, bld_filled=BLD_FILLED, tau_max=TAU_MAX):
    T = len(ts)
    bld = np.zeros_like(ts)
    
    for i in range(T):
        bld[i] = bld_filled/(T + tau_max)*(i - tau_max)
    return bld


def init_act(ts, *, nr_act):
    T = len(ts)
    act = np.zeros_like(ts)
    switch_pt = np.random.randint(0, T, nr_act)
    
    act[:switch_pt[0]] = 5  # can be hard-fixed to transport --> wash --> ...
    act[switch_pt[-1]:] = 9  # np.random.randint(0,10) #can be hard-fixed to wash --> transport --> sleep
    cur_act = None
    for i in range(nr_act - 1):
        temp_act = np.random.randint(0, 10)
        if temp_act == cur_act:
            temp_act = np.random.randint(0, 10)
        act[switch_pt[i]:switch_pt[i + 1]] = temp_act
        
    return act