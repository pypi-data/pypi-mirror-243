from pathlib import Path
import json
from graph_ts.errors import InvalidEdgeError

import networkx as nx
import warnings



class DynGraph(nx.MultiDiGraph):
    """
    A dynamic directed graph that represents temporal relationships between nodes.

    DynGraph extends the functionality of NetworkX's MultiDiGraph by adding support for temporal dynamics.
    It allows the representation of directed edges with associated time lags.

    Parameters:
        *args: Variable-length arguments accepted by MultiDiGraph.
        out_graph (dict, optional): A dictionary representing the out-graph structure.
        in_graph (dict, optional): A dictionary representing the in-graph structure.
        **kwargs: Additional keyword arguments accepted by MultiDiGraph.

    Attributes:
        lags (list): A list of unique time lags present in the graph.
        out_graph (dict): A compact representation of the out-graph structure.
        in_graph (dict): A compact representation of the in-graph structure.

    Methods:
        has_edge(u, v, lag=0): Check if an edge exists from node u to node v with the specified lag.
        has_edge_id(eid): Check if an edge with a specific EdgeID exists in the graph.
        add_node(node, **attr): Add a node to the graph.
        add_edge(node_from, node_to, lag=0, **attr): Add an edge from node_from to node_to with the specified lag.
        static_order(): Determine a topological order of nodes for the instantaneous view of the graph.
        save_json(path, graph_name='graph'): Save the out-graph structure as a JSON file.

    Class Methods:
        from_json(path): Create a DynGraph instance from a JSON file containing the out-graph structure.

    Private Methods:
        __parse_graph(graph, mode): Convert a dictionary representation of a graph to a list of edges.
        __compact_graph(mode): Create a compact graph representation (in or out) for visualization.
        __check_loop(): Check for the presence of loops in the instantaneous view of the graph.
        __get_instantaneous(): Get the instantaneous view of the graph.
        __static_filter(a, b, k): A static filter function used for subgraph view creation.

    Raises:
        ValueError: If there are duplicate nodes or edges in the graph, or if adding an edge would result in a loop.

    Note:
        This class extends NetworkX's MultiDiGraph and provides additional functionality for temporal graph analysis.

    Example Usage:
        # Create a DynGraph instance
        graph = DynGraph()

        # Add nodes and edges
        graph.add_node("A")
        graph.add_node("B")
        graph.add_edge("A", "B", lag=2)

        # Get the list of time lags in the graph
        lags = graph.lags

        # Save the graph to a JSON file
        graph.save_json("my_graph.json")

        # Load the graph from a JSON file
        loaded_graph = DynGraph.from_json("my_graph.json")
    """

    def __init__(self, *args, out_graph=None, in_graph=None, **kwargs):
        super(DynGraph, self).__init__(*args, **kwargs)
        # self._parents_with_lags = {}
        
        num_graph_args = (out_graph is not None) + (in_graph is not None) 
        assert num_graph_args < 2, "only one of the graph type is allowed"
        
        if num_graph_args == 1:
            if out_graph is not None:
                edge_list = self.__parse_graph(out_graph, "out")
            if in_graph is not None: 
                edge_list = self.__parse_graph(in_graph, "in")
                
            super().add_edges_from(edge_list)
    
    ################################################################
    # region private methods (not for overriding)
    def __parse_graph(self, graph, mode):
        edge_list = []
        for node_a, edict in graph.items():
            for lag, node_bs in edict.items():
                for node_b in node_bs:
                    if mode == "in":
                        edge_list.append((node_b, node_a, lag))
                    if mode == "out":
                        edge_list.append((node_a, node_b, lag))
        return edge_list
    
    def __compact_graph(self, mode):
        graph = {}
        for u, v, lag in self.edges(keys=True):
            if mode == "out":
                graph.setdefault(u, {}).setdefault(lag, []).append(v)
            if mode == "in":
                graph.setdefault(v, {}).setdefault(lag, []).append(u)
        return graph
                                
    def __check_loop(self):
        instant_view = self.__get_instananeous()
        try: 
            nx.find_cycle(instant_view, self)
            raise ValueError("Your graph must not contain loops!")
        except nx.NetworkXNoCycle:
            pass
        
    def __get_instananeous(self):
        return nx.subgraph_view(self, filter_edge=DynGraph.__static_filter)
    
    # endregion private methods (not for overriding)
    ################################################################

    
    ################################################################
    # region overridden from nx
    def has_edge(self, u, v, lag=0):
        edge_ind = super().has_edge(u, v)
        return edge_ind and lag in self[u][v]
    
    # TODO: use generic methods
    def has_edge_id(self, eid):
        """
        Check if an edge with a specific EdgeID exists in the graph.

        An EdgeID represents a sequence of directed edges with their associated time lags, forming a temporal path
        from a source node to a target node. This method checks if all the edges in the specified EdgeID exist in
        the graph.

        Parameters:
            eid (EdgeID): An EdgeID object representing the sequence of edges to check.

        Returns:
            bool: True if all edges in the EdgeID exist in the graph; otherwise, False.
        """
        target = eid.target
        for lag, source in eid._pairs:
            if not self.has_edge(source, target, lag):
                return False
        return True
    
    def add_node(self, node, **attr):
        node = str(node)
        if not self.has_node(node):
            super().add_node(node, **attr)
        else:
            warnings.warn("Node already exists")
    
    def add_edge(self, node_from, node_to, lag=0, **attr):
        """
        Add an edge from one node to another with an associated time lag.

        This method adds a directed edge from `node_from` to `node_to` with the specified time `lag`. The edges
        represent temporal relationships in the graph, where `lag` indicates the time delay or duration of the effect.

        Parameters:
            node_from: The source node from which the edge originates.
            node_to: The target node to which the edge points.
            lag (int, optional): The time lag associated with the edge (default is 0).
            **attr: Additional attributes to be assigned to the edge.

        Returns:
            int: The unique key assigned to the added edge.

        Raises:
            InvalidEdgeError: If an edge attempts to create an instantaneous effect from a node to itself (lag=0).
            ValueError: If an edge with the same source, target, and lag already exists, or if adding the edge
                        would result in a loop in the graph.
        """
        lag = int(lag)
        if node_from == node_to and lag == 0: 
            raise InvalidEdgeError("Instantaneous effect from a node itself to itself is not allowed")
        if self.has_edge(node_from, node_to, lag):
            raise ValueError("Duplicate edge")
        
        key = super().add_edge(node_from, node_to, lag, **attr)
        
        if lag == 0:
            try:
                self.__check_loop()
            except Exception as e:
                super().remove_edge(node_from, node_to, lag)
                raise type(e)(f"Could not add edge for: \"{e}\", aborted")
            
        return key
        
    # endregion overridden from nx
    ################################################################
    
    
    ################################################################
    # region custonmized functions
    def static_order(self):
        instant_view = self.__get_instananeous()
        in_deg = instant_view.in_degree
        roots = [k for k, v in in_deg if v==0]
        traverse_list = []
        for s in roots:
            if s not in traverse_list:
                traverse_list.append(s)
            for u, v, _ in nx.edge_bfs(instant_view, s):
                if u not in traverse_list:
                    traverse_list.append(u)
                if v not in traverse_list:
                    traverse_list.append(v)
        return traverse_list
    
    # endregion
    ################################################################
    
    ################################################################
    # region properties
    @property
    def lags(self):
        """
        Get a sorted list of unique time lags present in the graph.

        This property returns a list of all unique time lags associated with the edges in the graph. The list is
        sorted in ascending order.

        Returns:
            list: A sorted list of unique time lags in the graph.
        """
        result = {lag for u, v, lag in self.edges}
        result = list(result)
        result.sort()
        return result
        
    @property
    def out_graph(self):
        """
        Get a compact representation of the out-graph structure.

        This property returns a dictionary representation of the out-graph structure, where each node is
        associated with its outgoing edges and time lags. 

        Returns:
            dict: A compact representation of the out-graph structure.
        """
        return self.__compact_graph(mode="out")

    @property
    def in_graph(self):
        """
        Get a compact representation of the in-graph structure.

        This property returns a dictionary representation of the in-graph structure, where each node is
        associated with its incoming edges and time lags. 
        Returns:
            dict: A compact representation of the in-graph structure.
        """
        return self.__compact_graph(mode="in")
    
    # endregion
    ################################################################
    
    
    def save_json(self, path, mode="out", graph_name='graph'):
        # NEVER SPECIFY graph_name when called inside the class
        p = Path(path)
        with open(p / f'{graph_name}.json', 'w') as f:
            if mode == 'out':
                json.dump(self.out_graph, f)
            if mode == 'in':
                json.dump(self.in_graph, f)
                
    
    @staticmethod
    def __static_filter(a, b, k):
        return k == 0
    
    @classmethod
    def from_json(cls, path):
        with open(path, 'r') as f:
            graph = json.load(f)
        return cls(graph)    
    