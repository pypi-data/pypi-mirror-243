import hashlib
import copy
import sys
import logging
from functools import cached_property
import re

class EdgeID:
    def __init__(self, target, *lag_origins):
        """Edge identifier for comparing and storing edge function in dynamic graph

        Args:
            destination (str): the target of an edge
            origins (str or list of str): a subset of origins of an edge
            lags (int or list of int): corresponding lags of the `origins` argument
        """
        assert all(isinstance(int(item[0]), int) for item in lag_origins), "all lags must be integer"
        # auto conversions for integer keys
        try:
            assert all(isinstance(item[1], str) for item in lag_origins) 
        except AssertionError:
            print("variables should be strings, converted")
            lag_origins = [(int(item[0]), str(item[1])) for item in lag_origins]
        assert all("-" not in item[1] and " " not in item[1] for item in lag_origins), "variables should not contain \"-\" or spaces"
        assert len(list(lag_origins)) == len(set(lag_origins)), "should not contain duplicates"
        
        # initialize
        self._target = target
        self._pairs = sorted(copy.deepcopy(lag_origins))
        self._origins = set(list(zip(*self._pairs))[1])
        
        
    def __repr__(self):
        info = list(self._pairs)
        return f"EdgeID('{self._target}', *{info})"
    
    def __hash__(self):
        obj_str = str(self)
        sha256 = hashlib.sha256()
        sha256.update(obj_str.encode())
        hash_int = int(sha256.hexdigest(), 16)
        return hash_int % sys.hash_info.modulus
         
    def __eq__(self, other):
        assert isinstance(other, self.__class__), "Should be an EdgeID"
        return (
            self._target == other._target
            and self._pairs == other._pairs
        )
        

    def __str__(self):
        return f"Edge ID: from {self._pairs} to {self._target}"
    
    @property
    def target(self):
        return self._target
    
    @property
    def max_lag(self):
        return max(self._pairs)[0]
    
    @property
    def min_lag(self):
        return min(self._pairs)[0]
    
    @property
    def lag_origins(self):
        return copy.deepcopy(self._pairs)
    
    @property
    def filename(self):
        return f"O%{'-'.join(x[1] for x in self._pairs)}%L%{'-'.join(str(x[0]) for x in self._pairs)}%D%{self._target}"
    
    def has_origin(self, node):
        return node in self._origins
    
    def has_pair(self, lag_origin):
        return lag_origin in self._pairs
    
    
    @classmethod
    def from_string(cls, string):
        # pattern to match elements separated by hyphens
        pattern = r"O%([\w+-]+)%L%([\w+-]+)%D%(\w+)"

        # Use re.search to find the match
        match = re.search(pattern, string)

        # The matched groups are the strings you want
        o_list = match.group(1).split('-')
        l_list = [int(t) for t in match.group(2).split('-')]
        d_string = match.group(3)[0]
        
        lo_pairs = list(zip(l_list, o_list))
    
        return cls(d_string, *lo_pairs)
    
    @classmethod
    def from_in_edges(cls, edges):
        """assume [(u, v, lag)]"""
        edges = [e for e in edges]
        
        lag_origins = [(lag, u) for u, _, lag in edges]
        
        return cls(edges[0][1], *lag_origins)