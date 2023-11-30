import array
import types
from functools import lru_cache
from typing import NamedTuple, Optional, Tuple

import numpy as np
from numpy.fft import fft, ifft, irfft, rfft

try:
    from numba import njit
except ImportError:
    def njit(f):
        return f

from hifiscan.io_ import Correction


class XY(NamedTuple):
    """XY coordinate data of arrays of the same length."""

    x: np.ndarray
    y: np.ndarray


class Analyzer:
    """
    Analyze the system response to a chirp stimulus.

    Args:
      f0: Start frequency of chirp [Hz].
      f1: End frequency of chirp [Hz].
      secs: Duration of chirp.
      rate: Audio sample rate [Hz].
      ampl: Amplitude of chirp.
      calibration: Microphone calibration.
      target: Target curve.

    Symbols that are used:

      x: stimulus
      y: response = x * h
      X = FT(x)
      Y = FT(y) = X . H
      H: system transfer function = X / Y
      h: system impulse response = IFT(H)
      h_inv: inverse system impulse response (which undoes h) = IFT(1 / H)

    with:
      *: convolution operator
      FT: Fourier transform
      IFT: Inverse Fourier transform
    """

    MAX_DELAY_SECS = 0.1
    TIMEOUT_SECS = 1.0
    CACHED_METHODS = [
        'X', 'Y', 'calcH', 'H', 'H2', 'h', 'h_inv', 'spectrum',
        'frequency', 'calibration', 'target']

    chirp: np.ndarray
    x: np.ndarray
    y: np.ndarray
    sumH: np.ndarray
    numMeasurements: int
    rate: int
    fmin: float
    fmax: float
    time: float

    def __init__(
            self, f0: int, f1: int, secs: float, rate: int, ampl: float,
            calibration: Optional[Correction] = None,
            target: Optional[Correction] = None):
        self.chirp = ampl * geom_chirp(f0, f1, secs, rate)
        self.x = np.concatenate([
            self.chirp,
            np.zeros(int(self.MAX_DELAY_SECS * rate))
        ])
        self.y = np.zeros(self.x.size)
        self.rate = rate
        self.fmin = min(f0, f1)
        self.fmax = max(f0, f1)
        self.time = 0
        self.sumH = np.zeros(self.X().size)
        self.numMeasurements = 0
        self._calibration = calibration
        self._target = target

    def __getstate__(self):
        return {k: v for k, v in self.__dict__.items()
                if k not in self.CACHED_METHODS}

    def setCaching(self):
        """
        Cache the main methods in a way that allows garbage collection of self.
        Calling this method again will in effect clear the previous caching.
        """
        for name in self.CACHED_METHODS:
            unbound = getattr(Analyzer, name)
            bound = types.MethodType(unbound, self)
            setattr(self, name, lru_cache(bound))

    def addMeasurements(self, analyzer):
        """Add measurements from other analyzer to this one."""
        if not self.isCompatible(analyzer):
            raise ValueError('Incompatible analyzers')
        self.sumH = self.sumH + analyzer.sumH
        self.numMeasurements += analyzer.numMeasurements
        self.setCaching()

    def isCompatible(self, analyzer):
        """
        See if other analyzer is compatible for adding measurement to this one.
        """
        return isinstance(analyzer, Analyzer) and np.array_equal(
            analyzer.x, self.x)

    def findMatch(self, recording: array.array) -> bool:
        """
        Use correlation to find a match of the chirp in the recording.
        If found, return True and store the system response as ``y``.
        """
        sz = len(recording)
        self.time = sz / self.rate
        if sz >= self.x.size:
            Y = fft(recording)
            X = fft(np.flip(self.x), n=sz)
            corr = ifft(X * Y).real
            idx = int(corr.argmax()) - self.x.size + 1
            if idx >= 0:
                self.y = np.array(recording[idx:idx + self.x.size])
                self.numMeasurements += 1
                self.sumH += self.calcH()
                self.setCaching()
                return True
        return False

    def timedOut(self) -> bool:
        """See if time to find a match has exceeded the timeout limit."""
        return self.time > self.x.size / self.rate + self.TIMEOUT_SECS

    def frequency(self) -> np.ndarray:
        """Frequency array, from 0 to the Nyquist frequency."""
        return np.linspace(0, self.rate // 2, self.X().size)

    def freqRange(self, size: int = 0) -> slice:
        """
        Return range slice of the valid frequency range for an array
        of given size.
        """
        size = size or self.X().size
        nyq = self.rate / 2
        i0 = min(size - 1, int(0.5 + size * self.fmin / nyq))
        i1 = min(size - 1, int(0.5 + size * self.fmax / nyq))
        return slice(i0, i1 + 1)

    def calibration(self) -> Optional[np.ndarray]:
        """Interpolated calibration curve."""
        return self.interpolateCorrection(self._calibration)

    def target(self) -> Optional[np.ndarray]:
        """Interpolated target curve."""
        return self.interpolateCorrection(self._target)

    def interpolateCorrection(
            self, corr: Optional[Correction]) -> Optional[np.ndarray]:
        """
        Logarithmically interpolate the correction to a full-sized array.
        """
        if not corr:
            return None
        corr = sorted(c for c in corr if c[0] > 0)
        a = np.array(corr, 'd').T
        logF = np.log(a[0])
        db = a[1]
        freq = self.frequency()
        interp = np.empty_like(freq)
        interp[0] = 0
        interp[1:] = np.interp(np.log(freq[1:]), logF, db)
        return interp

    def X(self) -> np.ndarray:
        return rfft(self.x)

    def Y(self) -> np.ndarray:
        return rfft(self.y)

    def calcH(self) -> np.ndarray:
        """
        Calculate transfer function H of the last measurement.
        """
        X = self.X()
        Y = self.Y()
        # H = Y / X
        H = Y * np.conj(X) / (np.abs(X) ** 2 + 1e-6)
        if self._calibration:
            H *= 10 ** (-self.calibration() / 20)
        H = np.abs(H)
        return H

    def H(self) -> XY:
        """
        Transfer function H averaged over all measurements.
        """
        freq = self.frequency()
        H = self.sumH / (self.numMeasurements or 1)
        return XY(freq, H)

    def H2(self, smoothing: float) -> XY:
        """Calculate smoothed squared transfer function |H|^2."""
        freq, H = self.H()
        r = self.freqRange()
        H2 = np.empty_like(H)
        # Perform smoothing on the squared amplitude.
        H2[r] = smooth(freq[r], H[r] ** 2, smoothing)
        H2[:r.start] = H2[r.start]
        H2[r.stop:] = H2[r.stop - 1]
        return XY(freq, H2)

    def h(self) -> XY:
        """Calculate impulse response ``h`` in the time domain."""
        _, H = self.H()
        h = irfft(H)
        h = np.hstack([h[h.size // 2:], h[0:h.size // 2]])
        t = np.linspace(0, h.size / self.rate, h.size)
        return XY(t, h)

    def spectrum(self, smoothing: float = 0) -> XY:
        """
        Calculate the frequency response in the valid frequency range,
        with optional smoothing.

        Args:
          smoothing: Determines the overall strength of the smoothing.
          Useful values are from 0 to around 30.
          If 0 then no smoothing is done.
        """
        freq, H2 = self.H2(smoothing)
        r = self.freqRange()
        return XY(freq[r], 10 * np.log10(H2[r]))

    def h_inv(
            self,
            secs: float = 0.05,
            dbRange: float = 24,
            kaiserBeta: float = 5,
            smoothing: float = 0,
            causality: float = 0) -> XY:
        """
        Calculate the inverse impulse response.

        Args:
            secs: Desired length of the response in seconds.
            dbRange: Maximum attenuation in dB (power).
            kaiserBeta: Shape parameter of the Kaiser tapering window.
            smoothing: Strength of frequency-dependent smoothing.
            causality: 0 = linear-phase a-causal, 1 = minimum-phase causal.
        """
        freq, H2 = self.H2(smoothing)
        # Apply target curve.
        if self._target:
            H2 = H2 * 10 ** (-self.target() / 10)
        # Re-sample to halve the number of samples needed.
        n = int(secs * self.rate / 2)
        H = resample(H2, n) ** 0.5
        # Accommodate the given dbRange from the top.
        H /= H.max()
        H = np.fmax(H, 10 ** (-dbRange / 20))

        # Calculate Z, the reciprocal transfer function with added
        # linear phase. This phase will shift and center z.
        Z = 1 / H
        phase = np.exp(Z.size * 1j * np.linspace(0, np.pi, Z.size))
        Z = Z * phase

        # Calculate the inverse impulse response z.
        z = irfft(Z)
        z = z[:-1]
        z *= window(z.size, kaiserBeta)
        if causality:
            z = transform_causality(z, causality)

        # Normalize using a fractal dimension for scaling.
        dim = 1.5 - 0.25 * causality
        norm = (np.abs(z) ** dim).sum() ** (1 / dim)
        z /= norm

        t = np.linspace(0, z.size / self.rate, z.size)
        return XY(t, z)

    def correctionFactor(self, h_inv: np.ndarray) -> XY:
        """
        Calculate correction factor for each frequency, given the
        inverse impulse response.
        """
        Z = np.abs(rfft(h_inv))
        Z /= Z.max()
        freq = np.linspace(0, self.rate / 2, Z.size)
        return XY(freq, Z)

    def correctedSpectrum(self, corrFactor: XY) -> Tuple[XY, XY]:
        """
        Simulate the frequency response of the system when it has
        been corrected with the given transfer function.
        """
        freq, H2 = self.H2(0)
        H = H2 ** 0.5
        r = self.freqRange()

        tf = resample(corrFactor.y, H.size)
        resp = 20 * np.log10(tf[r] * H[r])
        spectrum = XY(freq[r], resp)

        H = resample(H2, corrFactor.y.size) ** 0.5
        rr = self.freqRange(corrFactor.y.size)
        resp = 20 * np.log10(corrFactor.y[rr] * H[rr])
        spectrum_resamp = XY(corrFactor.x[rr], resp)

        return spectrum, spectrum_resamp

    def targetSpectrum(self, spectrum: XY) -> Optional[XY]:
        if self._target:
            freq, resp = spectrum
            r = self.freqRange()
            target = self.target()[r]
            target += np.average(resp - target, weights=1 / freq)
            targetSpectrum = XY(freq, target)
        else:
            targetSpectrum = None
        return targetSpectrum


@lru_cache
def tone(f: float, secs: float, rate: int):
    """Generate a sine wave."""
    n = int(secs * f)
    secs = n / f
    t = np.arange(0, secs * rate) / rate
    sine = np.sin(2 * np.pi * f * t)
    return sine


@lru_cache
def geom_chirp(f0: float, f1: float, secs: float, rate: int):
    """
    Generate a geometric chirp (with an exponentially changing frequency).

    To avoid a clicking sound at the end, the last sample should be near
    zero. This is done by slightly modifying the time interval to fit an
    integer number of cycli.
    """
    n = int(secs * (f1 - f0) / np.log(f1 / f0))
    k = np.exp((f1 - f0) / n)  # =~ exp[log(f1/f0) / secs]
    secs = np.log(f1 / f0) / np.log(k)

    t = np.arange(0, secs * rate) / rate
    chirp = np.sin(2 * np.pi * f0 * (k ** t - 1) / np.log(k))
    return chirp


@lru_cache
def linear_chirp(f0: float, f1: float, secs: float, rate: int):
    """Generate a linear chirp (with a linearly changing frequency)."""
    n = int(secs * (f1 + f0) / 2)
    secs = 2 * n / (f1 + f0)
    c = (f1 - f0) / secs
    t = np.arange(0, secs * rate) / rate
    chirp = np.sin(2 * np.pi * (0.5 * c * t ** 2 + f0 * t))
    return chirp


def resample(a: np.ndarray, size: int) -> np.ndarray:
    """
    Re-sample the array ``a`` to the given new ``size`` in a way that
    preserves the overall density.
    """
    xp = np.linspace(0, 1, a.size)
    yp = np.cumsum(a)
    x = np.linspace(0, 1, size)
    y = np.interp(x, xp, yp)
    r = size / a.size * np.diff(y, prepend=0)
    return r


@njit
def smooth(freq: np.ndarray, data: np.ndarray, smoothing: float) -> np.ndarray:
    """
    Smooth the data with a smoothing strength proportional to
    the given frequency array and overall smoothing factor.
    The smoothing uses a double-pass exponential moving average (going
    backward and forward).
    """
    if not smoothing:
        return data
    weight = 1 / (1 + 2 ** (smoothing / 2 - 15) * freq)
    smoothed = np.empty_like(data)
    prev = data[-1]
    for i, w in enumerate(np.flip(weight), 1):
        smoothed[-i] = prev = (1 - w) * prev + w * data[-i]
    for i, w in enumerate(weight):
        smoothed[i] = prev = (1 - w) * prev + w * smoothed[i]
    return smoothed


@lru_cache
def window(size: int, beta: float) -> np.ndarray:
    """Kaiser tapering window."""
    return np.kaiser(size, beta)


@lru_cache
def taper(y0: float, y1: float, size: int) -> np.ndarray:
    """Create a smooth transition from y0 to y1 of given size."""
    tp = (y0 + y1 - (y1 - y0) * np.cos(np.linspace(0, np.pi, size))) / 2
    return tp


def transform_causality(x: np.ndarray, causality: float = 1) -> np.ndarray:
    """
    Homomorphic filter to create a new impulse of desired causality from
    the given impulse.

    Params:
      causality: 0 = linear-phase, 1 = minimum-phase,
        in-between values smoothly transition between the two.

    https://www.rle.mit.edu/dspg/documents/AVOHomoorphic75.pdf
    https://www.katjaas.nl/minimumphase/minimumphase.html
    """
    # Go to frequency domain, oversampling 4x to avoid aliasing.
    X = np.abs(fft(x, 4 * x.size))
    # Non-linear mapping.
    XX = np.log(np.fmax(X, 1e-9))
    # Linear filter to apply the desired amount of causal (right)
    # and anti-causal (left) parts to the complex cepstrum.
    xx = ifft(XX).real
    mid = x.size // 2
    left = slice(-1, -mid - 1, -1)
    right = slice(1, mid + 1)
    yy = np.zeros_like(xx)
    yy[0] = xx[0]
    yy[left] = (1 - causality) * xx[right]
    yy[right] = (1 + causality) * xx[right]
    YY = fft(yy)
    # Non-linear mapping back.
    Y = np.exp(YY)
    # Go back to time domain.
    y = ifft(Y).real

    # Infer the original linear-phase filter size.
    if np.allclose(x[0:mid + 1], x[-1:mid - 1:-1]):
        # x is symmetric, so it's linear-phase.
        orig_sz = x.size
    else:
        # Estimate based on location of peak.
        p = x.argmax()
        orig_sz = 2 * (x.size - p) - 1
        # src_causality = (3 - (x.size + p) / (x.size - p)) / 2
    # Roll and resize.
    y = np.roll(y, int(orig_sz * (1 - causality) / 2))
    sz = int(0.5 + orig_sz * (1 - causality / 2))
    y = y[:sz]
    return y
