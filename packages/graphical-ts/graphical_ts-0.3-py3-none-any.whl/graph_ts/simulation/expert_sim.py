## Expert Simulation

# 1. the future value is last value / average of historical values + positive/negative effect as VELOCITY!

# 2. requiement: 
    # implement the mode "velcity" for edge function
    
from .dgcm import DGCM
from ..mapping.edge_function import EdgeFunction
from ..mapping.signal_function import SignalFunction
from ..structure.edge_id import EdgeID
from ..misc.utils import *
import inspect
import copy

## TODO: wave form based expert Knowledge
## TODO: wave form as finer granularity

def extract_args(func):
    """Extract arguments of a function except 'x'"""
    args = inspect.getfullargspec(func).args
    return [arg for arg in args if arg != 'x']

class ExpertSim(DGCM):
    """Difference than its parent:
    * Only stores the edge information
    * Occp is not important 
    """
    
    CONT = 'continuous'
    CAT = 'categorical'
    BIN = 'binary'
    TYP_SET = {'continuous', 'categorical', 'binary'}
    
    MATCH_TYPE = {
        (CONT, CONT): {
            'fn': cont2cont, 
            'arg_names': extract_args(cont2cont)
        },
        (CONT, BIN): {
            'fn': cont2bin,
            'arg_names': extract_args(cont2bin)
        },
        (CONT, CAT): {
            'fn': cont2cat,
            'arg_names': extract_args(cont2cat)
        },
        (BIN, CONT): {
            'fn': bin2cont,
            'arg_names': extract_args(bin2cont)
        },
        (BIN, BIN): {
            'fn': bin2bin,
            'arg_names': extract_args(bin2bin)
        },
        (BIN, CAT): {
            'fn': bin2cat,
            'arg_names': extract_args(bin2cat)
        },
        (CAT, CONT): {
            'fn': cat2cont,
            'arg_names': extract_args(cat2cont)
        },
        (CAT, BIN): {
            'fn': cat2bin,
            'arg_names': extract_args(cat2bin)
        },
        (CAT, CAT): {
            'fn': cat2cat,
            'arg_names': extract_args(cat2cat)
        }
    }

    def add_node(self, 
                 node, 
                 **attr):
        
        assert 'type' in attr, "please specify the type of this node"
        
        if attr['type'] == 'categorical':
            self._justify_attr_for_cat_var(attr)
            
        super().add_node(node, **attr)

    def _justify_attr_for_cat_var(self, attr):
        values = attr.get('values', None)
        val_encode = attr.get('val_encode', None)
        has_vals = values is not None
        has_encode = val_encode is not None
            
        if has_vals and has_encode: 
                # 1. vals << enc: just update vals
                # 2. enc << vals: update encode the vals with left-over encodings
                # 3. intersect: union and fills the non-encoded values
                # collect all the values
            _vals = list(set(values) | val_encode.keys())
                
                # check if any values needs encoding 
            n_todo = len(_vals) - len(values)
                
                # collect the used encoding and get the maximum encoding, for calculating the left-over encodings
            occp_enc = {int(v) for v in val_encode.values()}
            max_enc = max(occp_enc)
            pool_enc = (set(range(max_enc+1)) - occp_enc) | set(range(max_enc+1, max_enc+1+n_todo)) 
                
                # fill the missing encodings 
            _val_enc = { k: val_encode.setdefault(k, pool_enc.pop()) for k in _vals} # pool_enc might not be empty after this
                
                
        elif has_vals and not has_encode:
            _vals = copy.deepcopy(values)
            _val_enc = { k: i for i, k in enumerate(_vals) }
                
                
        elif not has_vals and has_encode:
            _vals = list(val_encode.keys())
            _val_enc = copy.deepcopy(val_encode)
            
        else:
            raise AssertionError("A list of possible values should be specified")
            
        attr.update({
            'values': _vals,
            'val_encode': _val_enc
        })
            

        

    
    def simulate_process(self, T, safe_mode=True, post_process=None, **kwargs):
        
        eids_for_node = self._analyse_node_occp(silent=True)
        
        pre_len, efs = self._fill_edges_with_expert_info(eids_for_node)
        
        sfs = self._fill_signals_with_expert_info(self.nodes(data=True))
                
        traverse_order = self.static_order()
        
        return self._step_based_generation(T, 
                                           sfs, 
                                           efs, 
                                           eids_for_node, 
                                           pre_len, 
                                           traverse_order, 
                                           safe_mode=safe_mode, 
                                           post_process=post_process,
                                           fill_offset=False,
                                           **kwargs)

    def _fill_signals_with_expert_info(self, nodes):
        sfs = copy.deepcopy(self._sfs)
        for u, data in nodes:
            if u in sfs: 
                continue
            else: 
                if 'offset' in data:
                    offset = data['offset']
                    sfs[u] = SignalFunction.const_signal(offset)
                    
                elif 'range' in data:
                    a, b = data['range']
                    assert b > a, "upper range of a node should be greater than its lower range"
                    offset = self.rng.normal(loc=(a+b)/2, scale=(b-a)/6)
                    sfs[u] = SignalFunction.const_signal(offset)
                    
                else:
                    continue
        return sfs

    def _fill_edges_with_expert_info(self, eids_for_node, G=None):
        pre_len = self._pre_len
        efs = copy.deepcopy(self._efs)
        
        ## FILL the null edges with expert information
        ## ASSUMPTION: all null edges are isolated and not chunked into a multi-parent edge id
        G = self if G is None else G
        for v, eids in eids_for_node.items():
            for eid in eids:
                if eid in efs: # that means a non-expert edge is assigned 
                    continue
                
                else:
                    assert len(eid.lag_origins) == 1, "Not supported: Multi-Parent Edge for Expert Knowledge"
                    lag, u = eid.lag_origins[0]
                    
                    
                    u_type = self.nodes[u]['type']
                    v_type = self.nodes[v]['type']
                    
                    fn_info = ExpertSim.MATCH_TYPE[(u_type, v_type)]
                    fn = fn_info['fn']
                    
                    fn_args = {}
                    e_attr = G[u][v][lag]
                    fn_args['gauss_loc'] = e_attr.get('guass_loc', 0)
                    fn_args['gauss_scl'] = e_attr.get('gauss_scl', 1)
                    fn_args['rng'] = e_attr.get('rng', None)

                    if v_type in {ExpertSim.CAT, ExpertSim.BIN}:
                        fn_args['mode'] = 'value'
                        
                    if v_type == ExpertSim.CONT:
                        fn_args['indim'] = e_attr.get('input_len', 1) # the default value is intentionally wrong here
                        fn_args['outdim'] = e_attr.get('effect_len', 1)
                        fn_args['effect_len'] = e_attr.get('effect_len', 1)
                        fn_args['mode'] = e_attr.get('mode', e_attr.get('effect_type', DGCM.SET_GRAD))
                        

                    fn_args.update({k: e_attr[k] for k in e_attr if k in fn_info['arg_names']})
                    
                    efn = EdgeFunction(function=fn, **fn_args)
                    
                    efs[eid] = efn
                    
                    pre_len = max(pre_len, efn.indim)
        return pre_len,efs
                    
                    
    def null_edges(self, *args, **kwargs):
        raise NotImplementedError("non-applicable method for expert graph") 