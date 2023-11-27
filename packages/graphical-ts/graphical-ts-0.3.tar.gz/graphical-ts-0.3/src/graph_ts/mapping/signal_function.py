from graph_ts.misc.utils import *
import numpy as np
from inspect import signature

class SignalFunction:
    """
    A class representing a signal generator function with optional Gaussian noise.

    SignalFunction allows you to encapsulate a signal generator function, such as a mathematical function or a
    custom signal generator. It can apply the function to generate signals over a specified time range and
    frequency. Additionally, you can add Gaussian noise to the generated signals if needed.

    Parameters:
        function (callable): The signal generator function. It should accept a time array as its first argument
                            and may have additional parameters.
        freq (float, optional): The frequency of the signal (default is 1).
        gauss_loc (float, optional): The mean (loc) of the Gaussian noise (default is 0).
        gauss_scl (float, optional): The scale (standard deviation) of the Gaussian noise (default is 1).
        rng (numpy.random.Generator, optional): The random number generator to use for noise generation. If not
                                                provided, the default generator will be used.
        **params: Additional keyword parameters to be passed to the signal generator function.

    Attributes:
        freq (float): The frequency of the signal.
        gauss_loc (float): The mean (loc) of the Gaussian noise.
        gauss_scl (float): The scale (standard deviation) of the Gaussian noise.
        rng (numpy.random.Generator): The random number generator used for noise generation.

    Methods:
        __call__(self, T, with_noise=False): Generate a signal over a time range T.
        ConstantSignal(cls, height=0): Create a SignalFunction for a constant signal.
        BasselProcess(cls): Create a SignalFunction for a Bessel process.
        MultifractionalBrownianMotion(cls): Create a SignalFunction for multifractional Brownian motion.
        Sinuoid(cls): Create a SignalFunction for a sinusoidal signal.

    Example Usage:
        # Create a SignalFunction for a sine wave
        sine_wave = SignalFunction(np.sin, freq=2)

        # Generate a sine wave signal over a time range T
        signal = sine_wave(T=100, with_noise=True)

        # Create a SignalFunction for a constant signal
        constant_signal = SignalFunction.ConstantSignal(height=5)
    """

    def __init__(self, function, freq=1, gauss_loc=0, gauss_scl=1, rng=None, **params):
        self._function = function
        self._signature = signature(function)
        self._freq = freq
        self._params = params
        self.gauss_loc = gauss_loc
        self.gauss_scl = gauss_scl

        # Random Gaussian noise generator
        if not rng:
            self.rng = np.random.default_rng()
        else:
            self.rng = rng

    @property
    def freq(self):
        return self._freq

    def __call__(self, T, with_noise=False):
        ts = np.arange(T)
        if 'rng' in self._signature.parameters and 'rng' not in self._params:
            result = self._function(ts * self._freq, rng=self.rng, **self._params)
        else:
            result = self._function(ts * self._freq, **self._params)

        if with_noise:
            return result + self.rng.normal(self.gauss_loc, self.gauss_scl, result.shape)
        else:
            return result

    @classmethod
    def const_signal(cls, height=0):
        """
        Create a SignalFunction for a constant signal.

        Parameters:
            height (float, optional): The height of the constant signal (default is 0).

        Returns:
            SignalFunction: A SignalFunction instance representing a constant signal.

        Example Usage:
            constant_signal = SignalFunction.ConstantSignal(height=5)
        """
        return cls(constant_signal, height=height)

    @classmethod
    def bessel_process_signal(cls):
        """
        Create a SignalFunction for a Bessel process.

        Returns:
            SignalFunction: A SignalFunction instance representing a Bessel process.

        Example Usage:
            bessel_process = SignalFunction.BasselProcess()
        """
        return cls(bessel_process)

    @classmethod
    def mf_brownian_signal(cls):
        """
        Create a SignalFunction for multifractional Brownian motion.

        Returns:
            SignalFunction: A SignalFunction instance representing multifractional Brownian motion.

        Example Usage:
            mfbm = SignalFunction.MultifractionalBrownianMotion()
        """
        return cls(mfbm)

    @classmethod
    def sinuoid_signal(cls):
        """
        Create a SignalFunction for a sinusoidal signal.

        Returns:
            SignalFunction: A SignalFunction instance representing a sinusoidal signal.

        Example Usage:
            sine_wave = SignalFunction.Sinuoid()
        """
        return cls(np.sin)


class DiscreteSignal(SignalFunction):
    """
    A class representing a discrete signal generator function without Gaussian noise.

    DiscreteSignal extends the functionality of SignalFunction by ensuring that no Gaussian noise is added
    to the generated signals. It allows you to generate discrete signals over a specified time range and
    frequency.

    Parameters:
        function (callable): The signal generator function. It should accept a time array as its first argument
                            and may have additional parameters.
        freq (float, optional): The frequency of the signal (default is 1).
        **params: Additional keyword parameters to be passed to the signal generator function.

    Methods:
        __call__(self, T, **kwargs): Generate a discrete signal over a time range T.
        UniformDiscrete(cls, values, **kwargs): Create a DiscreteSignal for a uniform discrete signal.

    Example Usage:
        # Create a DiscreteSignal for a uniform discrete signal
        uniform_signal = DiscreteSignal.UniformDiscrete(values=[0, 1, 2, 3])
    """

    def __call__(self, T, **kwargs):
        result = super(DiscreteSignal, self).__call__(T, with_noise=False)
        return result

    @classmethod
    def uniform_categorical(cls, values, **kwargs):
        """
        Create a DiscreteSignal for a uniform discrete signal.

        Parameters:
            values (list): The list of possible values for the discrete signal.
            **kwargs: Additional keyword parameters to be passed to the signal generator function.

        Returns:
            DiscreteSignal: A DiscreteSignal instance representing a uniform discrete signal.

        Example Usage:
            uniform_signal = DiscreteSignal.UniformDiscrete(values=[0, 1, 2, 3])
        """
        return cls(uniform_categorical, values=values, **kwargs)
