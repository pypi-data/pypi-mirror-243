import copy
import warnings
import pickle

import numpy as np
import pandas as pd

from pathlib import Path
from functools import wraps, cached_property
from collections.abc import Iterable
from collections import Counter

from graph_ts.structure.dyn_graph import *
from graph_ts.mapping.edge_function import *
from graph_ts.mapping.signal_function import SignalFunction
from graph_ts.structure.edge_id import *
from graph_ts.errors import *

# TODO: use a helper class to handle the aggregation and set mode logic

# this is governed by verbose flag, so there is no log level 
def verbose_info(template):
    def parameterized(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            vinfo = fn(*args, **kwargs)
            if 'verbose' in kwargs:
                if kwargs['verbose']:
                    msg = ""
                    for item in vinfo:
                        if not isinstance(item, Iterable):
                            item = [item]
                        msg += f"{template.format(*item)}\n"
                    print(msg)
        return wrapper
    return parameterized



"""
DGCM Class Definition

This module defines the DGCM (Dynamic Graph Causal Model) class, which is used to construct, manipulate, and simulate causal models represented as dynamic graphs. The class allows users to assign edge functions and signal functions to model the relationships between nodes in the graph and simulate processes over time.

Attributes:
    DGCM.DEFAULT_GRPAH (str): Default filename for saving the graph structure as JSON.
    DGCM.DEFAULT_EDGE_FOLDER (str): Default subfolder name for storing edge functions.
    DGCM.DEFAULT_NODE_FOLDER (str): Default subfolder name for storing signal functions.

Classes:
    DGCM: Represents a Dynamic Graph Causal Model.

"""
class DGCM(DynGraph):
    """
    DGCM Class

    Represents a Dynamic Graph Causal Model (DGCM) used to construct, manipulate, and simulate causal models.

    Args:
        graph (dict, optional): A dictionary representing the initial graph structure.
        edge_functions (dict, optional): A dictionary of edge functions assigned to specific edges.
        signals (dict, optional): A dictionary of signal functions assigned to nodes.
        data_folder (str, optional): Path to the folder where data will be stored.
        collision_mode (str, optional): Specifies collision resolution mode for nodes.
        null_cause (EdgeFunction or str, optional): Edge function used as a null cause.
        null_signal (SignalFunction or str, optional): Signal function used as a null signal.

    Methods:
        assign_eid_with_fn(eid, func): Assigns an EdgeID with an edge function.
        assign_edge_with_fn(node_from, node_to, func, lag=0): Assigns an edge with an edge function.
        assign_edges(func_dict, lag=None): Assigns multiple edges with edge functions.
        assign_node_with_fn(node, func): Assigns a node with a signal function.
        assign_nodes(signal_dict): Assigns multiple nodes with signal functions.
        remove_node(node, force=False, verbose=False): Removes a node and related data.
        remove_edge(node_from, node_to, lag, force=False, verbose=False): Removes an edge and related data.
        simulate_process(T, mode='step', safe_mode=True, post_process=None, **params): Simulates a process over time.
        load_all_nodes(): Loads all signal functions from disk.
        load_all_edges(): Loads all edge functions from disk.
        null_edges(node_to=None, in_group=True): Returns null edges for a specific node or all nodes.
        from_path(path, cached_same=True): Creates a DGCM instance from a given path.

    Properties:
        edge_functions: Dictionary of assigned edge functions.
        signal_functions: Dictionary of assigned signal functions.

    """
    
    DEFAULT_GRPAH = "graph.json"
    DEFAULT_EDGE_FOLDER = "edge_funcs"
    DEFAULT_NODE_FOLDER = "signals"
    SET_GRAD = "grad"
    SET_DIFF = "diff"
    SET_ADD = "add"
    SET_VAL = "value"
    
    
    ################################################################
    #region construction
    
    def __init__(self, *args, edge_functions=None, signals=None, null_cause=None, null_signal=None, rng=None, random_seed=None, **kwargs):  
        """
        Initialize DGCM instance with specified parameters.

        Args:
            graph (dict, optional): A dictionary representing the initial graph structure.
            edge_functions (dict, optional): A dictionary of edge functions assigned to specific edges.
            signals (dict, optional): A dictionary of signal functions assigned to nodes.
            data_folder (str, optional): Path to the folder where data will be stored.
            collision_mode (str, optional): Specifies collision resolution mode for nodes.
            null_cause (EdgeFunction or str, optional): Edge function used as a null cause.
            null_signal (SignalFunction or str, optional): Signal function used as a null signal.
        """
        
        # init before super init because add_xxx are overridden
        
        
        # TODO: throw to subclass
        self.m_ratio = 0.2
        # end TODO
        
        self._pre_len = 1 
        self._efn_path = {}
        self._sfn_path = {}
        self._sfs = {}
        self._efs = {}
        
        super(DGCM, self).__init__(*args, **kwargs) # !!!this will call the overridden add_edge
            
        self.__init_edges_functions(edge_functions, null_cause)
        self.__init_signals(signals, null_signal) 
        
        if rng:
            self.rng = rng
        else:
            seed = random_seed if random_seed is not None else 0
            self.rng = np.random.default_rng(seed)
        
        
    
    #endregion construction
    ################################################################
    
    
    
    ################################################################
    # region private methods
    def __init_edges_functions(self, edge_functions, null_cause=None):
        
        # handle null cause so it is a EdgeFunction
        if null_cause is None:
            null_cause = 'copy'

        # null cause will be stored in the memory
        if type(null_cause) == str:
            self.null_cause = getattr(EdgeFunction, null_cause)()
        else: 
            self.null_cause = null_cause
            

        self.assign_edges(edge_functions)
                
        return "null", self.null_cause
                
    def __init_signals(self, signals, null_signal):
        if not null_signal:
            null_signal = 'const'
        
        if type(null_signal) == str:
            self.null_signal = getattr(SignalFunction, f"{null_signal}_signal")()
        else:
            self.null_signal = null_signal
        

        self.assign_nodes(signals)
        
        return "null", self.null_signal
    
    def __assign_edge(self, eid, obj):
        if not self.has_edge_id(eid):
            raise EdgeNotExist(f"invalid EdgeID: {eid}")
        
        if not isinstance(obj, (EdgeFunction, str, Path)):
            raise TypeError("Invalid Edge Function assignment: Object must be an EdgeFunction or a Path")

        efn = None
        if isinstance(obj, EdgeFunction): 
            efn = obj
            assert efn.match_with(eid), f"Edge function with in dimension(s) {efn.indim} does not match the edge group {eid}"
            
        if isinstance(obj, (str, Path)):
            efn = self.__load_from_path(obj, EdgeFunction)
            assert efn.match_with(eid), f"Edge function with in dimension(s) {efn.indim} does not match the edge group {eid}"
            self._efn_path[eid] = obj
        
        self._efs[eid] = efn
        efindim = efn.indim if isinstance(efn.indim, dict) else {eid.lag_origins[0][1]: efn.indim}
        self.__update_occp(eid, efindim)
        self._pre_len = max(self._pre_len, eid.max_lag)
                    
                    
    def __assign_node(self, node, obj):
        if not self.has_node(node):
            raise NodeNotExist(f"Node {node} doesn't exist.")
    
        if not isinstance(obj, (SignalFunction, str, Path)):
            raise TypeError("Invalid Signal Function assignment: Object must be an SignalFunction or a Path")
        
        sfn = None
        if isinstance(obj, SignalFunction): 
            sfn = obj
            
        if isinstance(obj, (str, Path)):
            sfn = self.__load_from_path(obj, SignalFunction)
            self._sfn_path[node] = obj
            
        self._sfs[node] = sfn
        

    
    def __load_from_path(self, path, check_cls):
        with open(path, 'rb') as f:
            obj = pickle.load(f)
        if not isinstance(obj, check_cls):
            raise TypeError(f"The loaded object is invalid: {type(obj)}")
        return obj
    
    
    # TOOD: verbose replacement
    def __update_occp(self, eid: EdgeID, efindim=None):
        """
        Update edge occupancy information for a given EdgeID.

        This method updates the edge occupancy information for the specified EdgeID and its lag origins.
        The occupancy information is stored in the graph structure for efficient access.

        Args:
            eid (EdgeID): The EdgeID for which to update the occupancy information.
            efindim (Union[int, dict], optional): The input dimension(s) for the EdgeFunction associated with the EdgeID.

        """
        # Loop through each lag origin in the EdgeID
        for lag, origin in eid.lag_origins:
            # Update the occupancy information for the target node and lag
            self[origin][eid.target][lag]['occp'] = eid
            
            # Check if input dimension information is provided
            if efindim:
                # process the input dimension for the currect origin (or the only origin when the int is provided)
                if isinstance(efindim, int):
                    indim = efindim
                else:
                    indim = efindim[origin]
                    
                # Loop through each step within the input dimension (move ON along the history)
                for step in range(indim):
                    # Check if the graph has an edge between the origin and target nodes with the specified lag
                    if self.has_edge(origin, eid.target, lag - step):
                        # Update the occupancy information for the lag-affected edge 
                        if self[origin][eid.target][lag - step]['occp'] is None:
                            self[origin][eid.target][lag - step]['occp'] = eid

     
    @verbose_info(template="Edge from ({2}, {0}) to {1} is now a null cause")
    def __remove_occp(self, main_node, other_node=None, lag=None, verbose=False):
        arg_count = (other_node is not None) + (lag is not None)
        is_for_node = (arg_count  == 0)
        is_for_edge = (arg_count == 2)
        assert is_for_node or is_for_edge, "<inner logic T_T> wrong argument combination!"
        # delete the occupancies key for any edge involing node
        
        vinfo = []
        if is_for_node:
            for u, v, k, eid in self.edges(keys=True, data='occp'):
                if eid and eid.has_origin(main_node):
                    self[u][v][k]['occp'] = None
                    vinfo.append((u, v, k))
        
        if is_for_edge:
            eid = self[main_node][other_node][lag]['occp']
            if eid:
                for l, o in eid.lag_origins:
                    self[o][eid.target][l]['occp'] = None
                    vinfo.append((o, eid.target, l))
        
        return vinfo
    
    
    @verbose_info(template="Edge function deleted for {0}")
    def __clean_edge_fn(self, node_from, node_to=None, lag=None, verbose=False):
        assert (node_to is None and lag is None) or (node_to is not None and lag is not None)
        to_del = []
        for eid in self._efn_path.keys():
            node_match = lag is None and (eid.has_origin(node_from) or eid.target==node_from)
            edge_match = lag is not None and (eid.has_pair((lag, node_from)) and eid.target==node_to)
            if node_match or edge_match:
                to_del.append(eid)
        
        for eid in to_del:
            del self._efn_path[eid]
        return to_del
    
    def __get_null_edges(self, node_to, in_group=False, in_eid=False):
        def null_occp(u, v, k):
            return v == node_to and self[u][node_to][k]['occp'] is None
        edges = nx.subgraph_view(self, filter_edge=null_occp).edges(keys=True)
        
        if not in_eid: 
            return edges
        else:
            items = [(k, u) for (u, _, k) in edges]
        
            if not in_group:
                return [EdgeID(node_to, item) for item in items]
            else: 
                return EdgeID(node_to, *items)
            
            
    def _get_clean_gdict(self):
        gdict = copy.deepcopy(nx.to_dict_of_dicts(self))
        for u, u_item in gdict.items():
            for v, v_item in u_item.items():
                for lag in v_item.keys():
                    del gdict[u][v][lag]['occp']
        return gdict
    
    def _get_epath_dict(self, folder):
        ep_dict = {repr(eid): p for eid, p in self._efn_path.items()}
        save_folder = (Path(folder) / self.DEFAULT_EDGE_FOLDER)
        save_folder.mkdir(parents=True, exist_ok=True)
        for eid, efn in self._efs.items():
            if not eid in self._efn_path:
                target_path =  save_folder / f"{eid.filename}.pkl"
                with open(target_path, 'wb') as f:
                    pickle.dump(efn, f)
                ep_dict[repr(eid)] = str(target_path.resolve())
                
        with open(save_folder/"null.pkl", 'wb') as f:
            pickle.dump(self.null_cause, f)
            ep_dict['null'] = str((save_folder/"null.pkl").resolve())
            
        return ep_dict
    
    def _get_spath_dict(self, folder):
        sp_dict = copy.deepcopy(self._sfn_path)
        save_folder = (Path(folder) / self.DEFAULT_NODE_FOLDER)
        save_folder.mkdir(parents=True, exist_ok=True)
        for u, sfn in self._sfs.items():
            if not u in self._sfn_path:
                target_path = save_folder / f"{u}.pkl"
                with open(target_path, 'wb') as f:
                    pickle.dump(sfn, f)
                sp_dict[u] = str(target_path.resolve())
                
        with open(save_folder/"null.pkl", 'wb') as f:
            pickle.dump(self.null_signal, f)
            sp_dict['null'] = str((save_folder/"null.pkl").resolve())
            
        return sp_dict
        

    # endregion private methods
    ################################################################
    
    
    
    ##############################
    #region relation assingments

    def assign_eid_with_fn(self, eid, func):
        """
        Assigns an EdgeID with an edge function.

        Args:
            eid (EdgeID): The EdgeID to assign the edge function to.
            func (EdgeFunction): The edge function to assign.

        Raises:
            EdgeNotExist: If the provided EdgeID does not exist in the graph.

        Returns:
            str: File name of the assigned edge function.
        """
        self.__assign_edge(eid, func)    
        
    def assign_edges_with_fn(self, target, *lag_origins, func):
        """
        Assigns an edge function to a specified edge in the graph.

        Args:
            target (str): The target of the edge.
            *lag_origins (list of tuples): A list of tuples, each containing a lag (int) and an origin (str).
            func (EdgeFunction): The edge function to assign.

        Raises:
            ValueError: If the edge parameters are invalid or the edge does not exist in the graph.

        Returns:
            str: File name of the assigned edge function.
        """
        # Validate and create an EdgeID
        eid = EdgeID(target, *lag_origins)

        # Check if the edge exists in the graph
        if not self.has_edge(eid):
            raise ValueError("The specified edge does not exist in the graph.")

        # Assign the edge function to the EdgeID
        self.__assign_edge(eid, func)

        
    
    def assign_edge_with_fn(self, node_from, node_to, func, lag=0):
        """
        Assigns an edge with an edge function.

        Args:
            node_from (str): Source node of the edge.
            node_to (str): Target node of the edge.
            func (EdgeFunction): The edge function to assign.
            lag (int, optional): Lag value of the edge.

        Returns:
            None
        """
        eid = EdgeID(node_to, (lag, node_from))
        self.assign_eid_with_fn(eid, func)
             
    def assign_edges(self, func_dict, lag=None):
        """
        Assigns multiple edges with edge functions.

        Args:
            func_dict (dict): A dictionary where keys are EdgeIDs or edge tuples, and values are edge functions or paths.
            lag (int, optional): Lag value for assigning edge functions.

        Raises:
            ValueError: If the provided relation type is not valid.

        Returns:
            None
        """
        if not func_dict:
            return 
        assert all(type(next(iter(func_dict.keys()))) == type(k) for k in func_dict.keys()), "All keys should be the same type"
        
        # if lag is not speicified, assume user gives eid as keys
        if lag is None:
            for eid, efn in func_dict.items():
                try:
                    if isinstance(efn, (EdgeFunction, Path, str)):
                        self.assign_eid_with_fn(eid, efn)
                    else: 
                        raise ValueError(f"relation of type {type(efn)} is not valid")
                except EdgeNotExist as e:
                    warnings.warn(f"edge with {eid} was skipped for: {type(e)}: {e}", UserWarning)
        
        # if there is a lag, assume user use single edge with lag
        else:
            for edge, efn in func_dict.items():
                try: 
                    if isinstance(efn, (EdgeFunction, Path, str)):
                        self.assign_edge_with_fn(*edge, efn, lag=lag)
                    else: 
                        raise ValueError(f"relation of type {type(efn)} is not valid")
                except Exception as e:
                    warnings.warn(f"{edge} was skipped for: {e}", UserWarning)
  
    #endregion relation assingments
    ##############################
    
    
    
    #######################################
    #region independent signal assignments
    
    def assign_node_with_fn(self, node, func):
        """
        Assigns a node with a signal function.

        Args:
            node (str): The node to assign the signal function to.
            func (SignalFunction): The signal function to assign.

        Raises:
            NodeNotExist: If the provided node does not exist in the graph.

        Returns:
            str: File name of the assigned signal function.
        """
        self.__assign_node(node, func)
        
    def assign_nodes(self, signal_dict):
        """
        Assigns multiple nodes with signal functions.

        Args:
            signal_dict (dict): A dictionary where keys are nodes, and values are signal functions or paths.

        Raises:
            ValueError: If the provided signal function type is not valid.

        Returns:
            None
        """
        if signal_dict is None:
            return
        for node, signal in signal_dict.items():
            try: 
                if isinstance(signal, (str, Path, SignalFunction)):
                    self.assign_node_with_fn(node, signal)
                else: 
                    raise ValueError(f"signal function of type {type(signal)} is invalid")
            except Exception as e:
                warnings.warn(f"{node} was skipped for: {e}", UserWarning)
    
    #endregion independent signal assinments
    #######################################
    
    
    
    ########################################################
    #region overriding add node / edge
    

        

        
          
    def _add_edge(self, node_from, node_to, lag=0, **attr):
        key = super().add_edge(node_from, node_to, lag, occp=None, **attr) # new
        self._pre_len = max(self._pre_len, key)
        return key
    
    def add_edge(self, node_from, node_to, lag=0, **attr):
        # Check if node_to matches the forbidden pattern
        if any(node_to == f"r_{node}" for node in self.nodes):
            raise ValueError(f"Cannot add edge to the node '{node_to}' as it matches the forbidden pattern.")
        
        # Proceed with adding the edge if the pattern does not match
        return self._add_edge(node_from, node_to, lag, **attr)

    
    def remove_node(self, node, force=False, verbose=False):
        """
        Removes a node and related data from the graph.

        Args:
            node (str): The node to remove.
            force (bool, optional): Whether to forcefully remove edge functions related to the node.
            verbose (bool, optional): Whether to display verbose information.

        Returns:
            None
        """
        # force is for deciding whether to delete information from the disk
        # check multi function related to this node
        if force:  #TODO 
            raise NotImplementedError
        
        self.__remove_occp(node, verbose=verbose)

        self.__clean_edge_fn(node, verbose=verbose)
        
        super().remove_node(node)
        
        # delete the inhabitant signal for a node
        if node in self._sfn_path:
            del self._sfn_path[node]
            
    def remove_edge(self, node_from, node_to, lag, force=False, verbose=False):
        """
        Removes an edge and related data from the graph.

        Args:
            node_from (str): Source node of the edge.
            node_to (str): Target node of the edge.
            lag (int): Lag value of the edge.
            force (bool, optional): Whether to forcefully remove edge functions related to the edge.
            verbose (bool, optional): Whether to display verbose information.

        Returns:
            None
        """
        if force:  #TODO 
            raise NotImplementedError
        
        self.__remove_occp(node_from, node_to, lag, verbose=verbose) 
        
        self.__clean_edge_fn(node_from, node_to, lag, verbose=verbose)
        
        super().remove_edge(node_from, node_to, lag)
        
    #endregion overriding add node / edge
    ########################################################
    
    
    
    #####################
    # region properties
    @property
    def edge_functions(self):
        return copy.deepcopy(self._efs)
    
    @property
    def signal_functions(self):
        return copy.deepcopy(self._sfs)
    
    
    def null_edges(self, node_to=None, in_group=True, in_eid=True):
        self._analyse_node_occp()
        if node_to:
            return self.__get_null_edges(node_to, in_group, in_eid)
        else: 
            result = {}
            for node in self.nodes:
                result[node] = self.__get_null_edges(node, in_group, in_eid)
            return result
      
    def eids_with_node(self, node):
        incoming_eid = []
        outgoing_eid = []
        for eid in self._efn_path:
            if eid.target == node:
                incoming_eid.append(eid)
            if node in list(zip(*eid.lag_origins))[1]:
                outgoing_eid.append(eid)
        return incoming_eid, outgoing_eid
    
     
    def _analyse_node_occp(self, silent=False):
        """
        Loads all edge functions from disk to a memory (in return).

        This method loads edge functions from disk for each EdgeID in the graph,
        ensuring that they are stored in memory for efficient access during simulations.

        Returns:
            tuple: A tuple containing three elements:
                   - A dictionary of loaded edge functions, where keys are EdgeIDs and values are edge functions.
                   - A dictionary of lists of EdgeIDs for each target node.
                   - The maximum lag value among all edge functions.

        Raises:
            NotAEdgeFunctionError: If a loaded object is not an instance of EdgeFunction.
            AssertionError: If the loaded EdgeFunction does not match the specified EdgeID.
        """
        
        ### 1. init for returns 
        
            # Append the EdgeID to the list of EdgeIDs associated with the target node
        eids_for_node = {}
        warned = False
        
        for u, v, lag, eid in self.edges(keys=True, data='occp'):
            if eid is not None:
                eids_for_node.setdefault(v, []).append(eid)
            else: # that means the edge is a null edge
                eids_for_node.setdefault(v, []).append(EdgeID(v, (lag, u)))
                if not warned and not silent:
                    warnings.warn(f"there are null edges, use `DGCM.null_edges()` to check them")
                    warned = True
        
        return {v: list(set(eids)) for v, eids in eids_for_node.items()}

    # endregion
    #####################
    
    
    
    #####################
    #region Generation

    def simulate_process(self, T, safe_mode=True, post_process=None, **kwargs):
        ## TODO: allow post_process to be a list of functions
        eids_for_node = self._analyse_node_occp()
        traverse_order = self.static_order()
        
        # might look weird but it makes inheritance easier
        return self._step_based_generation(T, 
                                           self._sfs, 
                                           self._efs, 
                                           eids_for_node, 
                                           self._pre_len, 
                                           traverse_order, 
                                           safe_mode=safe_mode, 
                                           post_process=post_process, **kwargs)
          
          
    
    def _step_based_generation(self, 
                               T, 
                               sfs, # the prepared signal functions
                               efs, # ... edge functions
                               eids_for_node, #  parent relations for each node sorted by edge id
                               pre_len, # prepended length 
                               traverse_order, # static traverse order by BFS starting from the root node
                               safe_mode=True, # if enabled, will raise error when trying to access the future, otherwise truncate before the future TODO: wrap it to config
                               noisy_signal=False, # if true, gaussian noise will be added to independent signal 
                               noisy_edge=False, # if true, gaussian noise will be added to relation 
                               fill_offset=True, # if true, fill offset for the whole episode, that means the effects are only acting as the bias to offset
                               post_process=None,
                               return_gradient=False, # if true, return the gradient sequence. 
                               scale_check=False):
        
        ## NOTE: 
        ##  when the generation broadcasts to t+, we need to know if the effect will be accumulated. If superposition is performed, then the value at a time step will explode 
            
        # initialize the result
        Tp = pre_len + T
        val_seq = {k: np.zeros(Tp) for k in self.nodes}
        grad_seq = {k: np.ones(Tp) * np.nan for k in self.nodes}
        
        # generate independent signals
        self._generate_independent_signal(sfs, val_seq, Tp, pre_len, noisy_signal, fill_offset)

        # generate causal part of the signal
        for t in range(pre_len, Tp): 
            for v in traverse_order:
                # ASSUMPTION: the compatibility has been checked during initialization
                all_effs = {}
                for eid in eids_for_node.get(v, []):
                    edge_func = efs[eid] if eid in efs else self.null_cause
                    in_dim = edge_func.indim
                    out_dim = edge_func.outdim
                
                    edge_args = {}
                    # collect history snippets from variables
                    for lag, parent in eid.lag_origins:
                        piece = self.__get_parent_history(val_seq, parent, safe_mode, t, lag, in_dim)
                        piece = self.__random_fill_piece(piece, val_seq, parent)
                        edge_args[parent] = piece
                        
                    out_a, out_b = t, min(t+out_dim, Tp)
                    # TODO: this part is buggy
                    result_slice = edge_func(**edge_args, with_noise=noisy_edge)[:out_b - out_a]
                    all_effs.setdefault(edge_func.mode, []).append(result_slice)
                
                if t == pre_len: ## because this check is only needed once 
                    assert validate_mixture_eff(all_effs), "Could not aggregate \'value\' effect mode with other modes" 
                        
                self.__update_seqs_with_eff(pre_len, val_seq, grad_seq, t, v, all_effs, scale_chek=scale_check)
                        
        generated_df = pd.DataFrame(val_seq)[pre_len:].reset_index(drop=True)
        generated_grad = pd.DataFrame(grad_seq)[pre_len:].reset_index(drop=True)
        
        if post_process is not None:
            generated_df = post_process(generated_df)
            
            
        if not return_gradient:
            return generated_df
        else: 
            return generated_df, generated_grad
            

    def _generate_independent_signal(self, sfs, val_seq, Tp, pre_len, noisy_signal, fill_offset):
        for u in self.nodes:
            sfunc = sfs[u] if u in sfs else self.null_signal
            if fill_offset or self.in_degree(u) == 0: # root will fill offset
                val_seq[u] += sfunc(Tp, with_noise=noisy_signal)
            else:
                val_seq[u][:pre_len] = sfunc(pre_len, with_noise=noisy_signal)





    def __random_fill_piece(self, piece, val_seq, v):
        node_type = self.nodes[v].get('type', 'continuous')
        
        # For continuous values
        if node_type == 'continuous':
            a, b = self.nodes[v].get('range', [np.nanmin(val_seq[v]), np.nanmax(val_seq[v])])
            # Replace nan with a random number between a and b
            piece = np.where(np.isnan(piece), self.rng.uniform(a, b, size=piece.shape), piece)
        
        # For binary values
        elif node_type == 'binary':
            # Replace nan with a random choice between 0 and 1
            piece = np.where(np.isnan(piece), self.rng.choice([0, 1], size=piece.shape), piece)
        
        # For categorical values
        elif node_type == 'categorical':
            # Get all categorical values
            categories = list(self.nodes[v]['val_encode'].values())
            # Replace nan with a random choice from categories
            piece = np.where(np.isnan(piece), self.rng.choice(categories, size=piece.shape), piece)

        return piece

    def __update_seqs_with_eff(self, pre_len, val_seq, grad_seq, t, v, all_effs, scale_chek=False):
        """Aggregate effect sent to a node at time t, and set the effect to its value sequence or gradient sequence depending on the set mode

        Args:
            pre_len (int): the prepending length for warm-up generation
            val_seq (ref: np.1darray): the value sequence 
            grad_seq (ref: np.1darray): the gradient sequence 
            t (int): the current timestamp
            v s(str)): the name of the node
            all_effs (_type_): effects from each eid, grouped by their set mode
        """
        node_type = self.nodes[v].get('type', 'continuous')
        agg_typ_ref = self.nodes[v].get('agg_mode', 'vote' if node_type in {'categorical', 'binary'} else 'average') # dict or str
        pre_val = val_seq[v][t-1]
        # aggregation mode for each set mode
        # { 
        #   'grad': 'average',
        #   'diff': 'sum',
        # }
                
        if t == pre_len:
            assert node_agg_compatible(node_type, agg_typ_ref), "Incompatible node type and aggregation method!"
                    
        for set_mode, eff_set in all_effs.items():
            # {
            #   'grad': [eff_from_eid1, eff_from_eid3, ...],
            #   'diff': [eff_from_eid2, ...],
            #   'add': ...
            # }
            # ASSUMPTIONs:
            #  * 'value' CANNOT be mixed with other set_mode, because it set the value directly.
            
            agg_typ = agg_typ_ref[set_mode] if isinstance(agg_typ_ref, dict) else agg_typ_ref
            
                 
            ################################################   
            # 1. perform aggregation to get the total effect
            ################################################
            total_eff, max_len = self.__agg_eff_set(agg_typ_ref, eff_set, agg_typ)
            
            ###################################
            # 2. apply total effect by set_mode
            ###################################
            if set_mode == DGCM.SET_VAL:
                if node_type in {'categorical', 'binary'}:
                    val_seq[v][t] = total_eff
                if node_type == 'continuous': 
                    val_seq[v][t: t+max_len] = total_eff
                    
            if set_mode == DGCM.SET_ADD:
                val_seq[v][t: t+max_len] += total_eff
                    
            ## ASSUMPTION: the following two are only for continuous targets! 
            if set_mode == DGCM.SET_GRAD: 
                target_slice = grad_seq[v][t: t+max_len]
                nan_mask = np.isnan(target_slice)
                target_slice[nan_mask] = 0 # this changes the grad_seq
                target_slice += total_eff # this changes the grad_seq
                        
            if set_mode == DGCM.SET_DIFF:
                val_seq[v][t: t+max_len] = pre_val + total_eff
                
            if scale_chek:
                self.__perform_scale_check(v, set_mode, total_eff, pre_val, t)
        #######################################
        # 2. apply gradient effect if it exists
        #######################################
        # TODO: weighted gradient
        grad_val = grad_seq[v][t]
        if not np.isnan(grad_val):
            val_seq[v][t] += val_seq[v][t-1] * (1 + grad_val)

    def __agg_eff_set(self, agg_mode, eff_set, agg_typ):
        total_eff = None
        max_len = max(len(eff) for eff in eff_set)
        if len(eff_set) > 1:  
            if agg_typ in {'average', 'sum'}:
                    # For continuous target the edge function will pose an effect to the last value with a sequence of delta values
                total_eff = np.zeros(max_len)
                for arr in eff_set:
                    n_pads = max_len - len(arr)
                    total_eff += np.pad(arr, (0, n_pads), 'constant')
                if agg_mode == 'average':
                    total_eff /= len(eff_set)
                            
            if agg_typ == 'vote': ## ASSUMPTION: target node is a discete value and out_dim == 1
                    # For discrete target, the edge function will directly tell the current value. Multiple edges to a node will vote for the decision
                total_eff = Counter(eff_set).most_common(1)[0][0]
        else:
            total_eff = eff_set[0]
        return total_eff, max_len
            
        
    def __perform_scale_check(self, v, set_mode, total_eff, pre_val, t):
        """perform scale check during the generation to avoid explosion of values

        Args:
            v (string): the node for which we check scale
            set_mode (enumerate: string): the set mode for the node
            total_eff (1d): the effect sequence snippet subjected to the check
            pre_val (number): the previous value right before total effect 
            t (int): the type subjected to the check, only for msg here
        """
        
        if self.nodes[v]['type'] in {'categorical', 'binary'}: return 
        
        a, b = self.nodes[v]['range']
        mean_eff = np.mean(total_eff)
        abs_mean_eff = np.abs(mean_eff)
        
        warn_msg = ''
        if set_mode == DGCM.SET_DIFF:
            if abs_mean_eff > np.abs(pre_val):
                warn_msg += f"abrupt change: {100*abs_mean_eff/(np.abs(pre_val)+1e-6):.2f}%"
        if set_mode == DGCM.SET_GRAD:
            if abs_mean_eff > 1: 
                warn_msg += f"abrupt gradient: {100*abs_mean_eff:.2f}%"
        if set_mode == DGCM.SET_VAL:
            if mean_eff > b or mean_eff < a:
                warn_msg += f"value out-of-bound: {mean_eff:.2f} is outside of ({a}, {b})"
        if set_mode == DGCM.SET_ADD: # TODO: this mode is quite weird but my brain shuts down so todo
            if  mean_eff > 2 * np.abs(pre_val):
                warn_msg += f"abrupt change: {100*(mean_eff-np.abs(pre_val))/(np.abs(pre_val)+1e-6):.2f}%"
        if warn_msg == '':
            return
        else: 
            warn_msg += f" detected during setting with {set_mode} for node {v} at time {t}"
            warnings.warn(warn_msg)

    def __get_parent_history(self, val_seq, parent, safe_mode, t, lag, indim):
        cur_in_len = indim if isinstance(indim, int) else indim[parent]
        assert cur_in_len > 0, "invalid in dimension!"
        if lag == 0:
            if cur_in_len > 1 and safe_mode:
                raise ValueError("Tried to get information from the future")
            in_a, in_b = t, t+1
        else:
            if cur_in_len - lag > 0 and safe_mode:
                raise ValueError("Tried to get information from the future")
            in_a, in_b = t-lag, min(t-lag+cur_in_len, t)
            
            
        pad_len = max(0, cur_in_len - in_b + in_a)
        piece = np.pad(val_seq[parent][in_a: in_b], (0, pad_len))
        return piece

    #endregion generalization
    #####################


    ################################
    # region save to disk
    def to_path(self, path):
        # save the graph
        gdict = self._get_clean_gdict()

        # save the eid: epath json. This will also save the freshly made EdgeFunctions
        epdict = self._get_epath_dict(folder=path)
        
        # save the node: spath json. This will also save the freshly made SignalFunctions
        spdict = self._get_spath_dict(folder=path)
        
        final_dict = {
            'graph': gdict,
            'node_attr': {u: self.nodes[u] for u in self.nodes},
            'edge_fns': epdict,
            'signal_fns': spdict
        }
        
        with open(Path(path)/'graph_info.json', 'w') as f:
            json.dump(final_dict, f)
        
                
    # endregion 
    ################################
    


    ########################
    #region static methods
                           
    @classmethod
    def from_path(cls, folder):
        
        # load the graph from json file
        with open(Path(folder)/'graph_info.json', 'r') as f:
            final_dict = json.load(f)
        
        g_obj = nx.from_dict_of_dicts(final_dict['graph'], create_using=cls, multigraph_input=True)
        
        for eid_info, epath in final_dict['edge_fns'].items():
            if eid_info == 'null':
                with open(epath, 'rb') as f:
                    g_obj.null_cause = pickle.load(f)
            else: 
                eid = eval(eid_info)
                g_obj.assign_eid_with_fn(eid, epath)
            
        for u, spath in final_dict['signal_fns'].items():
            if u == 'null':
                with open(spath, 'rb') as f:
                    g_obj.null_signal = pickle.load(f)
            else:
                g_obj.assign_node_with_fn(u, spath)
                
        nx.set_node_attributes(g_obj, final_dict['node_attr'])
        
        return g_obj
        
        
                   

            
    #endregion static methods
    ########################
    
  
  
  # default node type:  undefined 
  # default aggregation: sum
  # default set mode: value