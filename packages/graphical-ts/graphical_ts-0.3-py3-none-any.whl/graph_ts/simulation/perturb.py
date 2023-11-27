from ..structure.edge_id import *
from ..mapping.signal_function import *
from ..structure.dyn_graph import DynGraph
from .expert_sim import *

from copy import deepcopy
import warnings



# TODO: post processing in node data
class PerturbSampler(ExpertSim):
    
    def simulate_perturb(self, T, n_max=5, pgv=None, keep_lag=False):
        assert self.number_of_edges() > 2*n_max, "graph is too small for perturbation, lower `n_max` or grow bigger graph"
        
        pgv = self.random_perturb_graph(n_max, keep_lag=keep_lag) if pgv is None else pgv
        
        sfs, efs, eids_for_nodes, pre_len = self.infer_from_view(pgv)
        traverse_order = pgv.static_order()
        
        data = self._step_based_generation(T, sfs, efs, eids_for_nodes, pre_len, traverse_order, 
                                           safe_mode=False, 
                                           noisy_signal=True, 
                                           fill_offset=False)
        return data, pgv
        

    def random_perturb_graph(self, n_max, n_min=0, keep_lag=False, rm_only=True):
        
        E = self.number_of_edges()
        
        # number of operation steps
        N_op = self.rng.integers(n_min, n_max+1, 1)[0]
        if N_op > E//2:
            warnings.warn("Too many edges will be removed, using E//2 steps perturbation")
            N_op = E//2
            
        # infer number of adding step and number of removing step
        if rm_only:
            N_rm = N_op
        else:
            N_rm = self.rng.binomial(N_op, 0.5)
        N_add = N_op - N_rm
        
        # Step 1: Use a new graph for the return
        pgv = DynGraph() 
        
        # Step 2: decide which edges to keep
        keep_idc = self.rng.choice(range(E), E-N_rm, replace=False)
        
        for i, (u, v, lag, e_attr) in enumerate(self.edges(keys=True, data=True)):
            if i not in keep_idc:
                continue
            else:
                if lag == 0 or keep_lag: # don't mess around with instantaneous edges
                    pgv.add_edge(u, v, lag, **e_attr)
                else:
                    new_lag = self.rng.binomial(2 * lag, 0.5) + 1
                    pgv.add_edge(u, v, new_lag, **e_attr)
                    # print(f"edge lag from {u} to {v} changes from {lag} to {new_lag}.")
        
        # print("starting to add edges")
        for i in range(N_add):
            raise NotImplementedError
            done = False
            while not done:
                try:
                    u, v = self.rng.choice(list(self.nodes), 2, replace=False)
                    if self.in_degree(v) != 0: # don't add new edge to source
                        lag = self.rng.binomial(2 * int(np.mean(self.lags)), 0.5) # integer guaranteed
                        pgv.add_edge(u, v, lag)
                        done = True
                        # print(f"new edge added from {u} to {v} with lag {lag}")
                except ValueError as e:
                    continue
                
        return pgv
    
        
    def infer_from_view(self, pgv):
        pre_len = 1 
        efs = {}
        sfs = {}
        # ASSUMPTION: since perturbation is allowed, so all edges should be isolated
        temp_d = {}
        for u, v, lag in pgv.edges(keys=True):
            temp_d.setdefault(v, []).append(EdgeID(v, (lag, u)))
        eids_for_node = {v: list(set(l)) for v, l in temp_d.items()}
        
        pre_len, efs = self._fill_edges_with_expert_info(eids_for_node, G=pgv)
        sfs = self._fill_signals_with_expert_info(pgv.nodes(data=True))
            
        return sfs, efs, eids_for_node, pre_len
        
    