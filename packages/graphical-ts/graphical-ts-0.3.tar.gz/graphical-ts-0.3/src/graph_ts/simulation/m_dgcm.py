from .dgcm import DGCM
from ..mapping.edge_function import EdgeFunction
from ..misc.utils import block_params

import numpy as np


class MDGCM(DGCM):
    
    def __init__(self, m_ratio=None, *args, **kwargs):
        self.m_ratio = m_ratio
        super().__init__(*args, **kwargs)
        # Additional initialization for handling missing values, if necessary

    def add_node(self, node, **attr):
        if node.startswith('r_'):
            # Reject node names that are "r_<any existing node>" or "v_<any existing node>"
            raise ValueError(f"Node name '{node}' is forbidden, as it matches the pattern 'r_<node>'")
        else:
            super().add_node(node, **attr)

    ## TODO: hard mnar
    def enable_missing(self, *node):
        for n in node:
            # First check if the node exists
            if not self.has_node(n):
                raise ValueError(f"Node '{n}' does not exist")

            # Add an r_node for the existing node called n, with type "binary"
            r_node = f"r_{n}"
            super().add_node(r_node, type="binary")
            
    def add_missing_cause(self, cause_node, node_to, lag=0, edge_attr={}, ef_attr={}):
        node_to = f"r_{node_to}"
        if not self.has_node(node_to): 
            raise TypeError(f"node {node_to} doesn't exist!")
        source_type = self.nodes[cause_node].get('type', 'continuous')
        
        ef_x2bin = EdgeFunction.expert_edge(source_type, 'binary', **ef_attr)
        
        self._add_edge(cause_node, node_to, lag=lag, **edge_attr)
        self.assign_edge_with_fn(cause_node, node_to, ef_x2bin, lag)
        
    def _generate_independent_signal(self, sfs, val_seq, Tp, *args, **kwargs):
        
        super()._generate_independent_signal(sfs, val_seq, Tp, *args, **kwargs)
        
        r_variables = [var for var in self.nodes if var.startswith('r_') and self.in_degree(var) == 0]
        for r_var in r_variables:
            if r_var in sfs: 
                continue
            # Extract the variable name after 'r_'
            var_name = r_var[2:]
            # Determine the mutation ratio for this variable
            if isinstance(self.m_ratio, dict):
                mutation_ratio = self.m_ratio.get(var_name, 0)
            else:
                mutation_ratio = self.m_ratio

            val_seq[r_var] = np.random.choice([0, 1], size=Tp, p=[1-mutation_ratio, mutation_ratio])

    @block_params('post_process')
    def simulate_process(self, T, safe_mode=True, **kwargs):
        return super().simulate_process(T, safe_mode, post_process=self.__masking, **kwargs)
    
    def __masking(self, generated_df): 
        """ this is simply for masking 
        """
        # Step 1: Get all the columns with naming pattern "r_<something>"
        r_xs = [col for col in generated_df.columns if col.startswith('r_')]
       
        if len(r_xs) == 0:
            return generated_df

        # Step 2: Create a copy of the dataframe to avoid modifying the original one
        modified_df = generated_df.copy()

        # Iterate over the r_columns and set <something> to missing (e.g., NaN) where r_<something> = 1
        for r_x in r_xs:
            x = r_x.split('r_')[1]  # Extracting <something> from r_<something>
            # Set <something> to NaN where r_<something> is 1
            modified_df.loc[modified_df[r_x] == 1, x] = np.nan  # or use np.nan

        # Step 3: Optionally return the r_columns subdataframe
        return modified_df
