import numpy as np
from functools import wraps
from stochastic.processes import continuous
from collections.abc import Iterable

def block_params(*params):
    def inner(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            intersection = set(params).intersection(kwargs.keys())
            if len(intersection) > 0:
                raise TypeError(f"{intersection} are implied internally in {fn.__name__}'")
            return fn(*args, **kwargs)
        return wrapper
    return inner


def check_len(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        x = args[0]
        assert hasattr(x, '__getitem__'), "input should be indexable"
        assert len(x) >= 2, "input should be longer than 2"
        return fn(*args, **kwargs)
        
    return wrapper

def check_binary(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        x = args[0]
        if isinstance(x, Iterable):
            assert all((item == 0 or item == 1) for item in x), "all x values should be binaries"
        else:
            assert x == 0 or x == 1, "all x values should be binaries"
            
        return fn(*args, **kwargs)
    return wrapper






# region the set relation for expert sim
@check_len
@check_binary
def bin2cont(x, effect_len, scale=1, effect_type='grad'):
    diff = x[-1] - x[0] # -1, 0, 1
    if effect_type in {'value'  'add', 'diff'}:
        return diff * rise(scale, effect_len)    
    if effect_type == 'grad':
        return diff * scale * np.ones(effect_len)
    
    
@check_len
def cat2cont(x, effect_len, scale=1, effect_type='grad'):
    end_state = x[-1]
    scl = scale[end_state]
    
    return bin2cont(x, scl, effect_len, effect_type)    

def cont2cont(x, effect_len, scale=1, effect_type='grad'):
    if effect_type in {'grad', 'diff'}:
        return np.ones(effect_len) * mean_grad(x, scale)
    if effect_type in {'value',  'add'}:  # WARNING: this is only for self loop 
        return scale * np.ones(effect_len) * np.mean(x)


def cat2cat(x, mapping): # indim = outdim = 1
    return mapping[x]

def cont2cat(x, spectrum):
    return group_it(x, spectrum) # indim = outdim = 1

@check_binary
def bin2bin(x, flip=False): # indim = outdim = 1
    if flip:
        return 1 - x
    else: 
        return x

def cat2bin(x, catogory):
    return np.isin(x, catogory)

def cont2bin(x, up=np.inf, low=-np.inf):
    return bound_it(x, up, low)

# endregion







def rsigmoid(x):
    return 1.0 / (1.0 + np.exp(-5*(2*x-1)))

def rise(scale, T):
    ts = np.arange(T)
    xs = ts / (T-1)
    y = scale * rsigmoid(xs)
    return y

@check_binary
def bin2cat(x, target_value):
    return x * target_value


@check_len
def mean_grad(x, scale):
    grad = np.mean(np.gradient(x))
    return scale * grad

def bound_it(x, up=np.inf, low=-np.inf, scale=1):
    return scale * ((x>low) and (x<up))

def group_it(x, spectrum):
    bins = np.digitize(x, spectrum)
    return bins

def to_camel_case(s):
    s = s.replace("-", " ")  # replace "-" with space
    words = s.split()  # split string into words
    words = [word.capitalize() for word in words]  # capitalize each word
    return "".join(words)  # join words without space

def identity(x):
    return x

def bin2bin(x, flip=False):
    return x if not flip else 1-x


## basic functions
def step2sawtooth(x, height):
    dx = np.where(np.diff(x)==1.0)[0] + 1
    incremental_seq = np.hstack([
        np.arange(1, b-a+1) for a, b in 
        zip([0] + dx.tolist(), dx.tolist() + [len(x)])
    ])
    y = x.copy()
    y[x == 1] = incremental_seq[x == 1]
    return height*y

def scale_it(x, scale):
    return scale*x

def constant_signal(ts, height):
    return np.ones_like(ts)*height

def bessel_process(ts):
    return continuous.BesselProcess().sample_at(ts)

def mfbm(ts):
    return continuous.MultifractionalBrownianMotion(t=max(ts)).sample(len(ts)-1)


def uniform_categorical(ts, values, trans_freq=0.008, start_val=None, end_val=None, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    
    n_trans = max(round(len(ts)*trans_freq), 1)
    
    trans_pt = np.sort(rng.choice(ts, size=n_trans, replace=False))
    
    trans_v = rng.choice(values, size=n_trans-1)
    
    if start_val is None:
        start_val = rng.choice(values, 1)
    
    if end_val is None:
        end_val = rng.choice(values, 1)
        
    trans_v = np.concatenate([start_val, trans_v, end_val])
    
    result = np.zeros_like(ts)
    for i in range(n_trans):
        start_idx = 0 if i == 0 else trans_pt[i-1]
        result[start_idx:trans_pt[i]] = trans_v[i]
        
    return result




## validate if the aggregation is compatible with the node type 
def node_agg_compatible(node_type, agg_type):
    if node_type == 'continuous':
        to_check = [agg_type] if isinstance(agg_type,str) else agg_type.keys()
        return all(typ in {'average', 'sum', 'weighted'} for typ in to_check) 
    
    elif node_type in {'categorical', 'binary'}:
        return agg_type == 'vote' 
    
    else:
        return True
    
# value mode cannot be together with gradient or add
def validate_mixture_eff(all_effs):
    if 'value' in all_effs:
        return len(all_effs.keys()) == 1
    
    return True




## FOR MISSINGNESS
def get_v_est(v, r, repl=np.nan):
    # Check if v and r are both single values or both arrays of the same length
    if not (np.isscalar(v) and np.isscalar(r)):
        if len(v) != len(r):
            raise ValueError("v and r must be the same length")

    # Assert that all elements in r are either 0 or 1
    if not np.all(np.isin(r, [0, 1])):
        raise ValueError("All elements in r must be either 0 or 1")

    return (1 - r) * v + r * repl



