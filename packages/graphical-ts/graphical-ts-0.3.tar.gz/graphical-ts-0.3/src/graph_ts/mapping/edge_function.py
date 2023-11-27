import numpy as np
from inspect import signature
from functools import wraps
import copy
from ..structure.edge_id import EdgeID
from ..misc.utils import *


## TODO: do this in the simulation


        

## ASSUMPTIONS: mappings from the same source with different lags can be combined into a single mapping, so an edge function should not take a variable input more than
class EdgeFunction:
    VAR_SET = {'continuous', 'binary', 'categorical'}
    MODES = {'add', 'value', 'grad', 'diff'}
    """ d
    A class representing an edge function for generating signal transformations along directed edges.

    EdgeFunction encapsulates a function that describes how a signal is transformed along an edge in a
    dynamic graph. It allows for various signal transformations and optionally adds Gaussian noise to the
    output. Edge functions can be matched with EdgeIDs to ensure compatibility with the edge's temporal
    structure.

    Parameters:
        function (callable, optional): The edge transformation function. If not provided, the EdgeFunction
                                      will be created with an empty function.
        indim (int or dict, optional): The input dimensionality of the function. An integer represents the
                                       input dimension for uniform functions, while a dictionary specifies
                                       input dimensions for functions with multiple inputs. Default is None.
        outdim (int, optional): The output dimensionality of the function (default is 1).
        gauss_loc (float, optional): The mean (loc) of the Gaussian noise (default is 0).
        gauss_scl (float, optional): The scale (standard deviation) of the Gaussian noise (default is 1).
        rng (numpy.random.Generator or int, optional): The random number generator to use for noise
                                                      generation. If an integer is provided, a new
                                                      generator will be created with that seed. If not
                                                      provided, the default generator will be used.

    Attributes:
        indim (int or dict): The input dimensionality of the function.
        outdim (int): The output dimensionality of the function.
        gauss_loc (float): The mean (loc) of the Gaussian noise.
        gauss_scl (float): The scale (standard deviation) of the Gaussian noise.
        rng (numpy.random.Generator): The random number generator used for noise generation.

    Methods:
        __call__(self, with_noise=False, **kwargs): Apply the edge function to input data with optional noise.
        match_with(self, eid): Check if the EdgeFunction is compatible with an EdgeID.
        __str__(self): Get a string representation of the EdgeFunction.

    Class Methods:
        Identity(cls): Create an EdgeFunction that represents an identity transformation.
        Sweep(cls): Create an EdgeFunction that sweeps to zero (sets all values to zero).
        Step(cls, scale, up=np.inf, low=-np.inf): Create an EdgeFunction for a step function with optional bounds.
        Scale(cls, scl): Create an EdgeFunction for scaling input values.
        Grad(cls, length): Create an EdgeFunction for computing the gradient of input signals.
        SawtoothFromStep(cls, height=1, length=1): Create an EdgeFunction to convert step signals to sawtooth.

    Example Usage:
        # Create an EdgeFunction for an identity transformation
        identity_function = EdgeFunction.Identity()

        # Apply the function to input data
        output_signal = identity_function(with_noise=True, input_data=[1, 2, 3])

        # Create an EdgeFunction for scaling input values
        scaling_function = EdgeFunction.Scale(scl=2)

        # Check compatibility with an EdgeID
        edge_id = EdgeID([(0, 'A'), (1, 'B')])  # Example EdgeID
        is_compatible = scaling_function.match_with(edge_id)
    """

    def __init__(self, function=None, indim=1, outdim=1, mode='add', 
                 gauss_loc=0, gauss_scl=1, random_seed=None, rng=None, **fn_params):
        self._signature = signature(function) if function else None
        self._function = function
        self._indim = indim
        self._outdim = outdim
        self._default_fn_params = fn_params
        
        assert mode in EdgeFunction.MODES, f"Only f{', '.join(EdgeFunction.MODES)}"
        self._mode = mode
        


        self.__config_random(gauss_loc, gauss_scl, random_seed, rng)

    def __config_random(self, gauss_loc, gauss_scl, random_seed, rng):

        self.gauss_loc = gauss_loc
        self.gauss_scl = gauss_scl
        
        ## set by priority rng > random_seed 
        if rng is not None:
            self.rng = rng
        elif random_seed is not None:
            self.rng = np.random.default_rng(random_seed)
        else:
            self.rng = np.random.default_rng()
        

    def __call__(self, with_noise=False, rng=None, **kwargs):
        """
        Apply the edge function to input data with optional Gaussian noise.
        All parent values are passed as keyword arguments because a relation is defined with context

        Parameters:
            with_noise (bool, optional): If True, Gaussian noise will be added to the output (default is False).
            **kwargs: Keyword arguments representing input data for the function.

        Returns:
            numpy.ndarray: The transformed output data.

        Example Usage:
            # Apply the function to input data
            output_signal = edge_function(with_noise=True, v_seq=[1, 2, 3], u_seq=[0, 0.1, 3, 4], ...)
        """
        if isinstance(self._indim, int): # when there's only one input variable, place the value sequence as POSITIONAL argument
            eff = self._function(list(kwargs.values())[0], **self._default_fn_params)
        else: # when there are multiple parents, bind them according to argument names
            bound_args = self._signature.bind_partial(**kwargs)
            bound_args.apply_defaults()

            merged_params = self._default_fn_params.copy()
            merged_params.update(bound_args.kwargs)
            eff = self._function(**merged_params)

        eff = np.array(eff).reshape((-1))

        if with_noise and self._mode != "grad":
            _rng = self.rng if rng==None else rng
            eff += _rng.normal(self.gauss_loc, self.gauss_scl, eff.shape)
            
        return eff

    def __str__(self):
        """
        Get a string representation of the EdgeFunction.

        Returns:
            str: A string representing the EdgeFunction.

        Example Usage:
            # Get a string representation of the EdgeFunction
            function_string = str(edge_function)
        """
        return f'EdgeFunction: {self._function.__name__}'

    def match_with(self, eid):
        """
        Check if the EdgeFunction is compatible with an EdgeID.

        The EdgeFunction is considered compatible if it can operate on the temporal structure described by
        the EdgeID.

        Parameters:
            eid (EdgeID): The EdgeID to check compatibility with.

        Returns:
            bool: True if the EdgeFunction is compatible with the EdgeID; otherwise, False.

        Example Usage:
            # Check compatibility with an EdgeID
            edge_id = EdgeID([(0, 'A'), (1, 'B')])  # Example EdgeID
            is_compatible = edge_function.match_with(edge_id)
        """
        assert isinstance(eid, EdgeID), "Only EdgeID is supported"
        if isinstance(self._indim, int):
            return len(eid.lag_origins) == 1 and self._indim <= 1 + eid.lag_origins[0][0]  # 1 extra for the instantaneous value
        else:
            origins = {item[1] for item in eid.lag_origins}
            if origins != self._indim.keys():
                return False
            else:
                return all(self._indim[lo_item[1]] <= 1 + lo_item[0] for lo_item in eid.lag_origins)

    @property
    def indim(self):
        """
        Get a deep copy of the input dimensionality of the EdgeFunction.

        Returns:
            int or dict: The input dimensionality of the EdgeFunction.

        Example Usage:
            # Get the input dimensionality of the EdgeFunction
            input_dimension = edge_function.indim
        """
        return copy.deepcopy(self._indim)

    @property
    def outdim(self):
        """
        Get the output dimensionality of the EdgeFunction.

        Returns:
            int: The output dimensionality of the EdgeFunction.

        Example Usage:
            # Get the output dimensionality of the EdgeFunction
            output_dimension = edge_function.outdim
        """
        return self._outdim

    @property
    def mode(self):
        return self._mode

    ################################################################
    #region static
    @classmethod
    def copy(cls, **params):
        """
        Create an EdgeFunction that represents an identity transformation.

        Returns:
            EdgeFunction: An EdgeFunction instance representing an identity transformation.

        Example Usage:
            identity_function = EdgeFunction.Identity()
        """
        return cls(identity, **params)

    @classmethod
    def sweep(cls,  **params):
        """
        Create an EdgeFunction that sweeps to zero (sets all values to zero).

        Returns:
            EdgeFunction: An EdgeFunction instance representing a sweep to zero.

        Example Usage:
            sweep_function = EdgeFunction.Sweep()
        """
        return cls(np.zeros_like, **params)

    @classmethod
    def step(cls, scale, up=np.inf, low=-np.inf, **params):
        """
        Create an EdgeFunction for a step function with optional bounds.

        Parameters:
            scale (float): The scaling factor for the step function.
            up (float, optional): The upper bound for the step function (default is positive infinity).
            low (float, optional): The lower bound for the step function (default is negative infinity).

        Returns:
            EdgeFunction: An EdgeFunction instance representing a step function.

        Example Usage:
            step_function = EdgeFunction.Step(scale=2, up=5, low=0)
        """
        return cls(bound_it, scale=scale, up=up, low=low,  **params)

    @classmethod
    def simple_scale(cls, scale, **params):
        """
        Create an EdgeFunction for scaling input values.

        Parameters:
            scl (float): The scaling factor for input values.

        Returns:
            EdgeFunction: An EdgeFunction instance representing a scaling transformation.

        Example Usage:
            scaling_function = EdgeFunction.Scale(scl=2)
        """
        return cls(scale_it, scale=scale,  **params)

    @classmethod
    @block_params('indim', 'outdim')
    def grad(cls, length,  **params):
        """
        Create an EdgeFunction for computing the gradient of input signals.

        Parameters:
            length (int): The input dimensionality and the length of the gradient output.

        Returns:
            EdgeFunction: An EdgeFunction instance representing a gradient computation.

        Example Usage:
            gradient_function = EdgeFunction.Grad(length=3)
        """
        return cls(np.gradient, indim=length, outdim=length, **params)

    @classmethod
    @block_params('indim', 'outdim')
    def step_to_sawtooth(cls, height=1, length=1, **params):
        """
        Create an EdgeFunction to convert step signals to sawtooth signals.

        Parameters:
            height (float, optional): The height of the sawtooth wave (default is 1).
            length (int, optional): The length of the input and output signals (default is 1).

        Returns:
            EdgeFunction: An EdgeFunction instance representing the conversion.

        Example Usage:
            sawtooth_function = EdgeFunction.SawtoothFromStep(height=2, length=3)
        """
        return cls(step2sawtooth, indim=length, outdim=length, height=height, **params)
    
    @classmethod
    def expert_edge(cls, type_x, type_y, **params):
        assert type_x in EdgeFunction.VAR_SET and type_y in EdgeFunction.VAR_SET, 'invalid variable type'
        
        if type_x == 'continuous' and type_y == 'continuous':
            # source gives a rise/fall signal to the target
            return cls(cont2cont, mode='diff', **params) ## need scale
        if type_x == 'continuous' and type_y == 'binary':
            # 
            return cls(bound_it, mode='value', **params) ## need upper and lower
        
        if type_x == 'continous' and type_y == 'categorical':
            return cls(cont2cat, mode='value', **params) # need spectrum
        
        if type_x == 'binary' and type_y == 'continuous':
            return cls(bin2cont, mode='diff', **params) ## need scale
        
        if type_x == 'binary' and type_y == 'binary':
            return cls(bin2bin, mode='value', **params)
        
        if type_x == 'binary' and type_y == 'categorical':
            return cls(bin2cat, mode='value', **params) # need target value
        
        if type_x == 'categorical' and type_y == 'continuous':
            return cls(cat2cont, mode='diff', **params) ## need scale
        
        if type_x == 'categorical' and type_y == 'binary':
            return cls(cat2bin, mode='vote', **params) 

        
        # give the child a signal to increase by a value within a window 
    

        
    #endregion
    ################################################################





