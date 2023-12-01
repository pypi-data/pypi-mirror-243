#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 2017

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('[Analysis.Analysis] Loading dependencies...')
import numpy as np
import re
import scipy.signal as ssig
import scipy.special as ssp
from copy import deepcopy as dcp
from itertools import tee
from scipy import fftpack
print('[Analysis.Analysis] Done.')


## Level 0
def BinSizeInc(Bins, BinSize, BinSizeNew):
    """
    Increase bin size.


    Parameters
    ----------
    Bins: 2d array
        Binned data.

    BinSize: int
        Current bin size (in samples).

    BinSizeNew: int
        Intended bin size (in samples). `BinSizeNew` must be multiple of
        `BinSize`.


    Returns
    -------
    BinsNew: 2d array
        `Bins` data with bin size of `BinSizeNew`.

    """
    if BinSizeNew%BinSize:
        print('BinSizeNew must be multiple of BinSize.')
        return(None)

    if Bins.shape[0]%2:
        BinsNew = np.vstack((
            Bins,
            np.zeros((1,Bins.shape[1]))
        ))
    else:
        BinsNew = Bins.copy()

    BinsNew = BinsNew.reshape((
        int(BinsNew.shape[0]/int(BinSizeNew/BinSize)),
        int(BinSizeNew/BinSize),
        BinsNew.shape[1]
    )).sum(axis=1)

    if Bins.shape[0]%2: BinsNew = BinsNew[:-1,:]

    return(BinsNew)


def Coupling(H, HMax):
    Mi = (HMax - H)/HMax
    return(Mi)


def CumulativeMA(Base, Add, ElNo):
    """
    Cumulative moving average.

    Parameters
    ----------
    Base: array
        Array with base values to be cumulatively averaged. If empty, returns
        `Add`.

    Add:
        Array with the same size as `Base` to be added and averaged.

    ElNo: int
        How many elements were already averaged to get to `Base`.


    Returns
    -------
    Array: array
        Cumulative average of `Base` and `Add` with `Add` being the `ElNo` th
        element.


    Examples
    --------
    .. code-block:: python

        In [0]: import numpy as np

        In [1]: Base = np.zeros(10, dtype=int)
           ...: for ElNo in range(5):
           ...:     Add = np.random.uniform(-100,100,10).astype(int)
           ...:     Base = CumulativeMA(Base, Add, ElNo+1)
           ...:     Base = np.round(Base, 2)
           ...:     print(f'Iteration {ElNo+1}:'); print(Base); print()
           ...:

        Iteration 1:
        [ 70. -91.  56.  23. -63. -11. -29. -79. -86. -90.]

        Iteration 2:
        [ 44.   -8.   57.5  26.5  12.  -30.   21.  -33.  -59.5 -37.5]

        Iteration 3:
        [ 27.    -1.67  60.67  -7.    17.   -45.67  33.33 -24.   -67.33 -58.  ]

        Iteration 4:
        [  2.25  22.75  55.75  15.25  28.5  -56.    28.75 -15.5  -74.25 -54.75]

        Iteration 5:
        [  3.   15.2  61.   -5.   31.4 -51.4  13.8 -14.4 -40.2 -24.4]

    """
    if len(Base) == 0:
        Array = Add
    else:
        Array = ((Base * ElNo) + Add)/(ElNo+1)

    return(Array)


def Entropy(Signal):
    """
    Entropy as imprevisibility measurement and maximum entropy.
    """
    Hist,_ = np.histogram(Signal,np.unique(Signal).shape[0])
    Probs = Hist/np.sum(Hist)
    H = -np.sum(Probs[Probs > 0] * np.log(Probs[Probs > 0]))
    HMax = np.log(Hist.shape[0]+1)
    return(H, HMax)


def EucDist(A, B):
    """
    Function to calculate the distance and movement direction between spatial
    points.

    Parameters
    ----------
    A and B: array
        Arrays containing x (`A`) and y (`B`) coordinates. The euclidean
        distance will be sequentially calculated for all elements in `A` and
        `B`.

    Returns
    -------
    Dist: float or ndarray
        Euclidean distance between points A and B.

    Ang: float or ndarray
        Angle representing the movement direction (from -π to +π).
    """
    Dist = (np.diff(A)**2 + np.diff(B)**2)**0.5
    Ang = np.arctan2(np.diff(B), np.diff(A))
    return(Dist, Ang)


def FilterSignal(Signal, Rate, Frequency, Order=4, Coeff='butter', Type='bandpass', Verbose=False):
    """
    Filter signal according to the provided parameters.

    Parameters
    ----------
    Signal: array
        Signal to be filtered. If 2d array, each column will be processed
        separately.

    Rate: int
        Sampling rate at which `Signal` was recorded.

    Frequency: list
        List with 2 elements for `Type='bandpass'`; or 1 element for
        `Type='lowpass'` or `Type='highpass'`.

    Order: int, optional
        Filter order.

    Coeff: str, optional
        Filter coefficient type. Can be `'butter'` or `'fir'`.

    Type: str, optional
        Type of filtering. Can be `'lowpass'`, `'highpass'` or `'bandpass'`.

    Verbose: bool, optional
        Whether or not output should be printed.

    Returns
    -------
    Data: array
        The resulting filtered signal.

    """
    Data = np.zeros(Signal.shape, dtype='float32')
    if len(Signal.shape) == 2:
        for C in range(Signal.shape[1]):
            if Verbose: print('Filtering channel', C+1, '...')
            Data[:,C] = FilterSignal(Signal[:,C], Rate, Frequency, Order, Coeff, Type)

    else:
        if Coeff == 'butter':
            if Type not in ['bandpass', 'bandstop', 'lowpass', 'highpass']:
                print("Choose 'bandpass', 'bandstop', 'lowpass' or 'highpass'.")

            elif len(Frequency) not in [1, 2]:
                print('Frequency must have 2 elements for bandpass; or 1 element for \
                lowpass or highpass.')

            else:
                passband = [_/(Rate/2) for _ in Frequency]
                f2, f1 = ssig.butter(Order, passband, Type)
                Data = ssig.filtfilt(f2, f1, Signal, padtype='odd', padlen=0)

        elif Coeff == 'fir':
            Freqs = np.arange(1,(Rate/2)+1)
            DesiredFreqs = np.zeros(int(Rate/2))
            DesiredFreqs[min(Frequency):max(Frequency)] = 1

            o = Order + ((Order%2)*-1) +1
            a = ssig.firls(o, Freqs, DesiredFreqs, nyq=Rate/2)
            Data = ssig.filtfilt(a, 1.0, Signal, padtype='odd', padlen=0)

    return(Data)


def GenTTLsRising(Rate, PulseDur, PauseBefore, PauseAfter, SampleStart, PulseNo):
    """
    Generate a list of timestamp markers according to parameters.

    Parameters
    ----------
    Rate: int
        Sampling rate of the signal to be timestamped.

    PulseDur: float
        Duration (s) of each timestamp marker.

    PauseBefore: float
        Delay (s) before each timestamp marker.

    PauseAfter: float
        Delay (s) after each timestamp marker.

    SampleStart: int
        Sample at which the first timestamp should start.

    PulseNo: int
        Number of timestamp markers to be generated.


    Returns
    -------
    TTLs: array
        Array of generated timestamps (samples).

    """
    BlockDur = PauseBefore+PulseDur+PauseAfter
    TTLs = np.arange(SampleStart, SampleStart+(BlockDur*Rate*PulseNo), BlockDur*Rate, dtype='int')
    return(TTLs)


def GetAmpEnv(Signal, RemoveOffset=True, Verbose=False):
    """
    Get amplitude envelope of a signal.

    Parameters
    ----------
    Signal: array
        Signal to get the amplitude envelope. If 2d array, each column will be
        processed separately.

    Returns
    -------
    Data: Amplitude envelope of `Signal`.

    """
    if len(Signal.shape) > 1:
        Data = np.zeros(Signal.shape, 'float32')
        for C in range(Data.shape[1]):
            if Verbose: print(f'Processing ch {C+1}...')
            Data[:,C] = GetAmpEnv(Signal[:,C], RemoveOffset, Verbose)

    else:
        Mean = Signal.mean(axis=0)
        s = Signal-Mean if RemoveOffset else Signal

        # Orders faster when signal size is a power of two, so padding and truncating
        Data = ssig.hilbert(s, fftpack.next_fast_len(len(s)))[:len(s)]
        Data = abs(Data)
        if RemoveOffset: Data += Mean

    return(Data)


def GetFxx(Rate, NFFT, FreqWindow):
    """
    Based on Chronux's getfgrid @ http://chronux.org/
    Returns the frequencies associated with a given FFT-based computation.

    Parameters
    ----------
    Rate: int
        Sampling rate.

    NFFT: int
        Nuber of FFT points.

    FreqWindow: list or array
        List with the lowest and highest frequency to be calculated in Hz.


    Returns
    -------
    Fxx: array
        Frequencies to be returned in an FFT-based computation.

    """
    Fxx = np.arange(0, Rate/NFFT, Rate)
    Fxx = Fxx[:NFFT]
    Freqs = np.where((Fxx >= FreqWindow[0]) * (Fxx <= FreqWindow[-1]))[0]
    Fxx = Fxx[Freqs]

    return(Fxx)


def GetNegEquiv(Number):
    """
    Return the negative equivalent of a percentage, for calculating differences.
    The equivalent decrease of an increase of:

    - 100% is -50%;
    - 300% is -75%;
    - 400% is -80%;

    and so on. The increase can go up to infinity, but the decrease
    can only go down to -100%. In other words, this function maps values that
    range from 0 to inf into 0 to -100.

    Parameters
    ----------
    Number: int or float or array
        Number in the range 0-inf. If Number is < 0, it will be returned
        unmodified.

    Returns
    -------
    NumberNeg: int or float or array
        The representation of Number into the range 0 to -100.

    """
    if 'array' in str(type(Number)):
        NumberNeg = dcp(Number)
        N0 = NumberNeg[NumberNeg>0]
        N0 = -(100-(100/((N0+100)/100)))
        NumberNeg[NumberNeg>0] = N0
    else:
        NumberNeg = Number if Number < 0 else -(100-(100/((Number+100)/100)))
    return(NumberNeg)


def GetOverlap(a, b):
    """
    Return an array with the sorted index of `a` elements that are also
    in `b`, and an array containing the sorted index of `b` elements
    that are also in `a`.

    Stolen from Mike B-K
    @ https://www.followthesheep.com/?p=1366

    Modified to include docstring and return sorted arrays
    """

    a1 = np.argsort(a)
    b1 = np.argsort(b)

    # use searchsorted:
    sort_left_a  = a[a1].searchsorted(b[b1], side='left')
    sort_right_a = a[a1].searchsorted(b[b1], side='right')
    sort_left_b  = b[b1].searchsorted(a[a1], side='left')
    sort_right_b = b[b1].searchsorted(a[a1], side='right')

    # which values of b are also in a?
    inds_b = (sort_right_a-sort_left_a > 0).nonzero()[0]
    # which values of a are also in b?
    inds_a = (sort_right_b-sort_left_b > 0).nonzero()[0]

    a1 = np.sort(a1[inds_a])
    b1 = np.sort(b1[inds_b])

    return(a1, b1)


def GetPeaks(Signal, Std=1, FixedThreshold=None):
    """
    Detect peaks in `Signal` according to a standard deviation threshold.

    Parameters
    ----------
    Signal: array
        Signal to detect peaks. If 2d array, each column will be processed
        separately.

    Std: float, optional
        How many standard deviations far from the mean the peak must be.

    FixedThreshold: float, optional
        If set, only peaks that are `FixedThreshold` far from the mean will
        be detected.

    Returns
    -------
    Peaks: dict
        Dictionary with peaks above (`Peaks['Pos']`) and below (`Peaks['Neg']`)
        `Signal` mean.

    """
    if len(Signal.shape) == 2:
        Peaks = {'Pos':[], 'Neg':[]}
        for Ch in range(Signal.shape[1]):
            PeaksCh = GetPeaks(Signal[:,Ch], Std, FixedThreshold)
            for K in Peaks.keys(): Peaks[K].append(PeaksCh[K])

    else:
        if FixedThreshold: Threshold = FixedThreshold
        else: Threshold = Std*Signal.std()

        if Threshold:
            ThresholdPos = Signal.mean()+Threshold
            ThresholdNeg = Signal.mean()-Threshold
            Peaks = {
                'Pos': np.where((Signal[1:-1] > ThresholdPos) *
                                (Signal[:-2] < Signal[1:-1]) *
                                (Signal[1:-1] >= Signal[2:]))[0]+1,
                'Neg': np.where((Signal[1:-1] < ThresholdNeg) *
                                (Signal[:-2] > Signal[1:-1]) *
                                (Signal[1:-1] <= Signal[2:]))[0]+1
            }
        else:
            Peaks = {
                'Pos': np.where((Signal[:-2] < Signal[1:-1]) *
                                (Signal[1:-1] >= Signal[2:]))[0]+1,
                'Neg': np.where((Signal[:-2] > Signal[1:-1]) *
                                (Signal[1:-1] <= Signal[2:]))[0]+1
            }

    return(Peaks)


def GetPhase(Signal, Verbose=False):
    """
    Get signal phase.

    Parameters
    ----------
    Signal: array
        Signal to extract phase. If 2d array, each column will be processed
        separately.

    Returns
    -------
    Data:
        Signal phase vector.

    """
    if len(Signal.shape) > 1:
        Data = np.zeros(Signal.shape)
        for C in range(Data.shape[1]):
            if Verbose: print(f'Processing ch {C+1}...')
            Data[:,C] = GetPhase(Signal[:,C])

    else:
        # Orders faster when signal size is a power of two, so padding and truncating
        Data = ssig.hilbert(Signal, fftpack.next_fast_len(len(Signal)))[:len(Signal)]
        Data = np.angle(Data)

    return(Data)


def GetPowerOf2(N):
    """
    Get the exponent for the next power of 2.

    Parameters
    ----------
    N: float
        Value to get the next power of 2.

    Returns
    -------
    Next: int
        The exponent that will give the next value if `2**Next`.
    """
    Next = int(np.ceil(np.log2(N)))
    return(Next)


def GetTime(TimeWindow, Rate):
    """
    Get a time vector from a time window.

    Parameters
    ----------
    TimeWindow: list
        List with start and end time (s) of the time vector.

    Rate: int
        Sampling rate to generate the time vector.


    Returns
    -------
    Time: array
        Time vector (s) according to `TimeWindow` at `Rate`.

    """
    Time =  np.arange(
        int(TimeWindow[0]*Rate),
        int(TimeWindow[1]*Rate)
    )/Rate

    return(Time)


def IsInt(Obj):
    try: int(Obj); return(True)
    except: return(False)


def IsFloat(Obj):
    try: float(Obj); return(True)
    except: return(False)


def ListToArrayNaNFill(List):
    """
    Fill arrays in `List` with NaNs until all arrays have the same
    size, then return a 2d array.
    """
    MaxLen = max([len(_) for _ in List])
    Array = np.array([
        s if len(s)==MaxLen else np.hstack((s,[np.nan]*(MaxLen-len(s))))
        for s in List
    ])

    return(Array)



def Morlet(Freq, t, CyclesNo=5, FreqScalingFactor=1, Offset=0):
    """
    Under dev
    """
    SigmaT = CyclesNo/(2*np.pi*Freq)

    Gaussian = np.exp((-((t-Offset)/FreqScalingFactor)**2)/(2*SigmaT**2))
    CosSen = np.exp(1j * 2 * np.pi * Freq/FreqScalingFactor * (t-Offset))
    Psi = FreqScalingFactor * Gaussian * CosSen

    return(Psi)


def MovingAverage(a, n=2):
    """
    Taken from Jaime
    @ https://stackoverflow.com/a/14314054
    """
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def MovingAvgWindow(Signal, WindowSize):
    MWDiff = WindowSize - (Signal.shape[0] % WindowSize)
    PadStart = MWDiff//2
    PadEnd = (MWDiff//2)+(MWDiff%2)

    if MWDiff:
        MW = np.concatenate((
            np.empty(PadStart)*np.nan,
            Signal,
            np.empty(PadEnd)*np.nan
        ))
    else:
        MW = Signal.copy()

    MW = MW.reshape((MW.shape[0]//WindowSize,WindowSize))
    MW = np.repeat(np.nanmean(MW,axis=1),WindowSize)[PadStart:-PadEnd]
    return(MW)


def NestedClean(Obj):
    """
    Remove empty elements from nested objects.

    Parameters
    ----------
    Obj: object
        Object containing nested elements.


    Returns
    -------
    Nest: object
        The input object without empty elements.

    """
    Nest = Obj.copy()

    if 'numpy' in str(type(Nest)):
        if not Nest.size: return(None)
        else: return(Nest)
    else:
        if len(Nest) == 0: return(None)

    ToDel = []
    if type(Nest) == dict:
        for K, Key in Nest.items():
            Nest[K] = NestedClean(Key)

            if type(Nest[K]) == np.ndarray:
                if not Nest[K].size: ToDel.append(K)
            else:
                if not Nest[K]: ToDel.append(K)

        for K in ToDel: del(Nest[K])
        return(Nest)

    elif type(Nest) in [list, tuple]:
        for E, El in enumerate(Nest):
            Nest[E] = NestedClean(El)

            if type(Nest[E]) == np.ndarray:
                if not Nest[E].size: ToDel.append(E)
            else:
                if not Nest[E]: ToDel.append(E)

        for E in ToDel: del(Nest[E])
        return(Nest)

    else:
        return(Nest)


def Normalize(Data, Range=(0,1)):
    """
    Normalize data to the specified range.

    Parameters
    ----------
    Data: array
        Data to be normalized. If 2d array, each column will be processed
        separately.

    Range: iterable, optional
        Desired minimum and maximum values to fit `Data`.

    Returns
    -------
    Norm: array
        Normalized data.

    """
    Norm = Data.astype('float32')

    if len(Norm.shape) == 2:
        for Ch in range(Norm.shape[1]):
            Norm[:,Ch] = Normalize(Norm[:,Ch], Range)

    elif len(Norm.shape) == 1:
        Norm = min(Range) + (Data-np.nanmin(Data)) * (max(Range)-min(Range)) / (np.nanmax(Data)-np.nanmin(Data))

    else:
        print('Only 1 or 2 dimensions allowed.')
        return(None)

    return(Norm)


def Normalize_Old(Data, MeanSubtract=False, MaxDivide=True):
    """
    Normalize data by subtracting the mean and/or divide by the absolute
    maximum.

    Parameters
    ----------
    Data: array
        Data to be normalized. If 2d array, each column will be processed
        separately.

    MeanSubtract: bool, optional
        Toggle to subtract the mean.

    MaxDivide: bool, optional
        Toggle to divide `Data` by its absolute maximum.

    Returns
    -------
    Norm: array
        Normalized data.

    """
    Norm = Data.astype('float32')

    if len(Norm.shape) == 2:
        for Ch in range(Norm.shape[1]):
            Norm[:,Ch] = Normalize_Old(Norm[:,Ch], MeanSubtract, MaxDivide)

    elif len(Norm.shape) == 1:
        if MeanSubtract: Norm -= np.nanmean(Norm)
        if MaxDivide: Norm = Norm/np.nanmax(abs(Norm)) if np.nanmax(abs(Norm)) else Norm

    else:
        print('Only 1 or 2 dimensions allowed.')
        return(None)

    return(Norm)


def Pairwise(iterable):
    """
    Taken from https://docs.python.org/3.6/library/itertools.html#itertools-recipes
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """

    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def PolygonArea(X,Y):
    """
    Calculate the area of a polygon based on lists of x and y coordinates using
    the Shoelace formula.
    NaNs in one of the arrays lead to drop of that value in both arrays.

    Parameters
    ----------
    X and Y: lists or tuples or array_like
        Iterable containing x and y coordinates, respectively, of the
        vertices of the polygon.

    Returns
    -------
    Area: float
        Area of the polygon defined by the vertices at the provided
        coordinates.

    Modified from @Madhi at https://stackoverflow.com/a/30408825
    """
    if len(X) != len(Y):
        raise ValueError('X and Y must have the same length.')

    NaN = np.isnan(X)+np.isnan(Y)
    X,Y = X[~NaN], Y[~NaN]
    Area = 0.5 * np.abs(np.dot(X, np.roll(Y,1)) - np.dot(Y, np.roll(X,1)))
    return(Area)


def RemapChannels(Tip, Head, Connector):
    """
    Get probe channels order. It doesn't matter what logic you follow to order
    your connector channels, but you MUST follow the same logic for your probe
    head.

    If the probe tip channels are put top-down or bottom-up, the resulting
    channel map will be ordered accordingly.

    Parameters
    ----------
    Tip: list or array
        Order of channels at the electrode array tip.

    Head: list or array
        Order of channels at the electrode array head.

    Connector: list or array
        Order of channels at the connector where the array is connected.

    Examples
    --------
    Neuronexus A16 probe connected to Neuronexus A16OM16 adaptor:

        In [1]: A16OM16 = [13, 12, 14, 11, 15, 10, 16, 9, 5, 4, 6, 3, 7, 2, 8, 1]

        In [2]: A16 = {'Tip': [9, 8, 10, 7, 13, 4, 12, 5, 15, 2, 16, 1, 14, 3, 11, 6],
           ...:        'Head': [8, 7, 6, 5, 4, 3, 2, 1, 9, 10, 11, 12, 13, 14, 15, 16]}

        In [3]: RemapChannels(A16['Tip'], A16['Head'], A16OM16)
        Get channel order... Done.

        Out[3]: [5, 13, 4, 12, 7, 15, 3, 11, 8, 16, 1, 9, 2, 10, 6, 14]

    """
    print('Get channel order... ', end='')
    ChNo = len(Tip)
    ChMap = [0]*ChNo

    for Ch in range(ChNo):
        TipCh = Tip[Ch]                  # What channel should be the Ch
        HeadCh = Head.index(TipCh)       # Where Ch is in Head
        ChMap[Ch] = Connector[HeadCh]    # Channels in depth order

    print('Done.')
    return(ChMap)


def RMS(Data):
    """
    Calculate the root mean square (RMS) of a signal.

    Parameters
    ----------
    Data: array
        Data to calculate the RMS. If 2d array, each column will be processed
        separately.

    Returns
    -------
    DataRMS: float or array
        The RMS of each column in Data.

    """
    if len(Data.shape) == 2:
        DataRMS = np.empty(Data.shape[1])
        for C in range(Data.shape[1]): DataRMS[C] = RMS(Data[:,C])
    else:
        DataRMS = np.mean(Data**2)**0.5

    return(DataRMS)


def SortNatural(s, _nsre=re.compile('([0-9]+)')):
    """
    Taken from Claudiu
    @ https://stackoverflow.com/a/16090640

    Naturally sort a list of strings.
    """

    return [int(text) if text.isdigit() else text.lower()
            for text in _nsre.split(s)]


def StrRange(Start='a', End='z', Step=1):
    """
    Get an alphabetically-ordered range of strings

    Parameters
    ----------
    Start: str
        Sring range start.

    End: str
        Sring range end.

    Step: int
        Range step size.

    Returns
    -------
    Range: list
        String range from `Start` to `End` at each `Step`.

    """
    if max(len(Start), len(End)) > 1:
        print('Only 1-char length strings are accepted.')
        return(None)
    else:
        Range = list(map(chr, range(ord(Start), ord(End), Step)))
        return(Range)


def DownSample(Data, Rate, RateNew, t=[]):
    """
    Resample signal to a smaller sampling rate.

    Parameters
    ----------
    Data: array
        Signal to be resampled. If 2d array, resampling will take place in the
        1st dimension.

    Rate: int
        Sampling rate at which `Data` was recorded.

    RateNew: int
        Sampling rate to resample `Data`.

    t: array, optional
        Array with the same length as `Data`, to be equally resampled.


    Returns
    -------
    DataSub: array
        The resampled array.

    tSub: array
        The resampled auxiliar array. Returned only if `t` is provided.

    """
    DownSampleF = int(Rate/RateNew)
    if len(Data.shape) > 1:
        DataSub = Data[np.arange(0,Data.shape[0],DownSampleF), :]
    else:
        DataSub = Data[np.arange(0,Data.shape[0],DownSampleF)]

    if len(t): tSub = t[np.arange(0,t.shape[0],DownSampleF)]

    if len(t): return(DataSub, tSub)
    else: return(DataSub)


def Transpose(Data):
    """
    Transpose nested list of same length.

    Parameters
    ----------
    Data: iterable
        Nested iterables of the same length.

    Returns
    -------
    T: Transposed nested iterables.

    """
    T = list(map(list, zip(*Data)))
    return(T)


def Upsample(Data, Dim, Up, Verbose=False):
    """
    Upsample array.

    Parameters
    ----------
    Data: 1d or 2d array
        Array of shape (Dim.shape[0],) containing data values.
        If 2d, shape should be (Dim.shape[0], X), and
        upsampling will be done for every X separately.

    Dim: 1d array
        Array of shape (Data.shape[0],).

    Up: int
        How many samples to insert between each Dim sample.

    Verbose: bool, optional
        Whether or not output should be printed.


    Returns
    -------
    DataUp: array
        The upsampled array.

    DimUp: 1d array
        The upsampled array for the 1st dimension.

    """
    # Up: int
        # How many times should the dimensions be upsampled.

    # # Do not include original points, but size is Dim.shape[0]*Up, and DimUp is equally spaced
    # DimUp = np.interp(
        # np.linspace(Dim.min(), Dim.max(), len(Dim)*Up),
        # np.linspace(Dim.min(), Dim.max(), len(Dim)),
        # Dim
    # )

    # # Include original points and size is Dim.shape[0]*Up, but messes up the ending of the signal
    # DimUp = np.interp(
        # np.arange(Dim.min(), Dim.max(), 1/(len(Dim)*Up)),
        # np.arange(Dim.min(), Dim.max(), 1/len(Dim)),
        # Dim
    # )

    # # Include original points and size is Dim.shape[0]*Up, but DimUp is not equally spaced
    # DimUp = np.linspace(Dim.min(), Dim.max(), len(Dim)*Up - len(Dim) + 2)
    # DimUp = np.sort(np.append(DimUp, Dim[1:-1]))

    # Include original points and DimUp is equally spaced, but size is smaller than Dim.shape[0]*Up
    DimUp = np.linspace(Dim.min(), Dim.max(), len(Dim)+((len(Dim)-1)*Up))

    if len(Data.shape) == 2:
        DataUp = np.zeros((len(DimUp), Data.shape[1]), dtype='float')
        for C in range(Data.shape[1]):
            if Verbose: print('Upsampling channel', C+1, '...')
            DataUp[:,C] = Upsample(Data[:,C], Dim, Up, Verbose)[0]

    else:
        DataUp = np.interp(DimUp, Dim, Data)

    return(DataUp, DimUp)


def Upsample2d(Data, Dim1, Dim2, Up, Verbose=False):
    """
    Upsample a 2-dimensional array.

    Parameters
    ----------
    Data: 2d or 3d array
        Array of shape (Dim1.shape[0], Dim2.shape[0]) containing data values.
        If 3d, shape should be (Dim1.shape[0], Dim2.shape[0], X), and
        upsampling will be done for every X separately.

    Dim1: 1d array
        Array of shape (Data.shape[0],) representing the 1st dimension.

    Dim2: 1d array
        Array of shape (Data.shape[1],) representing the 2nd dimension.

    Up: int, list
        How many times should the dimensions be upsampled. If int, the value is
        applied for both dimensions. If list, the values are applied to the
        dimensions, respectively.

    Verbose: bool, optional
        Whether or not output should be printed.


    Returns
    -------
    DataUp: 2d array
        The upsampled array.

    Dim1Up: 1d array
        The upsampled array for the 1st dimension.

    Dim2Up: 1d array
        The upsampled array for the 2nd dimension.

    Examples
    --------
    To upsample a spectrogram 5x in both dimension:
        SxxUp, FUp, TUp = Analysis.Upsample2d(Sxx, F, T, 5)
    """
    DataUp, DimsUp = [], []

    if len(Data.shape) == 3:
        for C in range(Data.shape[2]):
            if Verbose: print('Upsampling channel', C+1, '...')
            d, d1, d2 = Upsample2d(Data[:,:,C], Dim1, Dim2, Up)

            if not len(DataUp):
                DimsUp = [d1, d2]
                DataUp = np.zeros((d.shape[0], d.shape[1], Data.shape[2]), dtype='float')

            DataUp[:,:,C] = d

    else:
        DimsUp = [
            np.interp(
                # np.linspace(0,1,len(Dim)*Up),
                # np.linspace(0,1,len(Dim)),
                np.arange(0,1,1/(len(Dim)*Up)),
                np.arange(0,1,1/len(Dim)),
                Dim
            )
            for Dim in [Dim1, Dim2]
        ]

        Data1Up = np.zeros((len(Dim1),len(DimsUp[1])), dtype='float32')
        for I in range(Data.shape[0]):
            Data1Up[I,:] = np.interp(
                # np.linspace(0,1,Data1Up.shape[1]),
                # np.linspace(0,1,Data.shape[1]),
                np.arange(0,1,1/Data1Up.shape[1]),
                np.arange(0,1,1/Data.shape[1]),
                Data[I,:]
            )

        DataUp = np.zeros((len(DimsUp[0]),len(DimsUp[1])), dtype='float32')
        for F in range(Data1Up.shape[1]):
            DataUp[:,F] = np.interp(
                # np.linspace(0,1,len(DimsUp[0])),
                # np.linspace(0,1,Data1Up.shape[0]),
                np.arange(0,1,1/len(DimsUp[0])),
                np.arange(0,1,1/Data1Up.shape[0]),
                Data1Up[:,F]
            )

    return(DataUp, DimsUp[0], DimsUp[1])


def VonMises(Phi, PhiMean, Kappa):
    """
    Under dev.
    """
    VM = np.exp(Kappa * (np.cos(Phi - PhiMean)))
    VM /= 2 * np.pi * ssp.iv(0, Kappa)
    return(VM)


def WhereMultiple(Test, Data):
    """
    Return indexes of elements in Test at Data.
    Values in Test must be unique.

    Parameters
    ----------
    Test: array_like
        Input array with values to be found on Data. Elements must be unique.
    Data: array_like
        The values against which to find each value of Test.


    Returns
    -------
    I: ndarray, int
        Indices of the values from Test in Data.

    Taken from Divakar @ https://stackoverflow.com/a/33678576
    """
    I = np.nonzero(Test[:,None] == Data)[1]
    return(I)


## Level 1
def CWT(
            Signal, t, Rate, Freqs, tPsi, Wavelet=Morlet,
            WaveletArgs=dict(CyclesNo=5, FreqScalingFactor=1, Offset=0)
        ):
    """
    Get the continuous wavelet transform (CWT) from `Signal`.

    Parameters
    ----------
    Signal: array
        Signal to be processed.

    t: array
        Time vector for `Signal`.

    Rate: int
        Sampling rate at which `Signal` was recorded.

    Freqs: array
        Frequencies to apply the wavelet transform.

    tPsi: array
       Time vector for the decomposition wavelet function.

    """
    Signal_Psi = np.zeros((t.shape[0], Freqs.shape[0]), dtype='complex')
    if 't' not in WaveletArgs: WaveletArgs['t'] = tPsi

    for F,Freq in enumerate(Freqs):
        WaveletArgs['Freq'] = Freq
        Psi = Wavelet(WaveletArgs)
        Signal_Psi[:,F] = np.convolve(Signal, Psi, 'same')

    return(Signal_Psi)


def GetDeltaPhase(SignalRef, SignalRes):
    """
    Get the phase difference between two signals.

    Parameters
    ----------
    SignalRef: array
        The reference signal. If 2d array, then the returned delta phase will
        be between each column of `SignalRef` vs `SignalRes`.

    SignalRes: array
        The signal to evaluate phase differences in relation to `SignalRef`.

    Returns
    -------
    DeltaPhase: array
        The phase difference between the input signals.
    """
    if len(SignalRef.shape) > 1:
        if SignalRef.shape[1] != SignalRes.shape[1]:
            print('Ref and Result dimensions have to be the same.')
            return(None)

        DeltaPhase = np.zeros(SignalRef.shape)
        for C in range(DeltaPhase.shape[1]):
            DeltaPhase[:,C] = GetDeltaPhase(SignalRef[:,C], SignalRes[:,C])

    else:
        PhaseRef = GetPhase(SignalRef)
        PhaseResult = GetPhase(SignalRes)
        DeltaPhase = np.angle(np.exp(1j * (PhaseRef - PhaseResult)))

    return(DeltaPhase)


def GetEntropyMI(Signal):
    """
    Get modulation index based on entropy.
    """
    H, HMax = Entropy(Hist)
    MI = (HMax-H)/HMax
    return(MI)


def GetInstFreq(Signal, Rate):
    """
    Get instantaneous frequency of a signal.

    Parameters
    ----------
    Signal: array
        The signal to be processed. If 2d array, each column will be processed
        separately.

    Rate: int
        Sampling rate at which `Signal` was recorded.


    Returns
    -------
    InstFreq: array
        The instantaneous frequency of `Signal`.
    """
    if len(Signal.shape) == 2:

        InstFreq = np.zeros((Signal.shape[0]-1, Signal.shape[1]))
        for C in range(Signal.shape[1]):
            InstFreq[:,C] = GetInstFreq(Signal[:,C], Rate)

    else:
        SignalPhase = GetPhase(Signal)

        # Instantaneous frequency can be achieved by
        # InstFreq = np.angle(np.exp(1j*np.diff(SignalPhase)))/(2*np.pi/Rate)
        # Or by getting the diff of the unwrapped phase
        SignalPhaseUnwrapped = np.unwrap(SignalPhase)
        InstFreq = np.diff(SignalPhaseUnwrapped)/(2*np.pi/Rate)

    return(InstFreq)


def GetNFFT(WindowSize, Pad=0):
    """
    Get a NFFT that is the next power of 2 of a window size. Auxiliar function
    for sciscripts.Analysis.PSD() and sciscripts.Analysis.Spectrogram().

    Parameters
    ----------
    WindowSize: int
        Length of each segment.

    Pad: int, optional
        If padding is used, it'll be summed to the resulting NFFT.


    Returns
    -------
    NFFT: int
        Length of the FFT to be used.
    """
    NFFT = int(2**(GetPowerOf2(WindowSize)+Pad))
    return(NFFT)


def GetPLVs(SignalRef, SignalRes, Rate, Freqs, FreqBand):
    """
    Get the phase locking value (PLV) for two signals.

    Parameters
    ----------
    SignalRef: array
        The reference signal. If 2d array, then the returned delta phase will
        be between each column of `SignalRef` vs `SignalRes`.

    SignalRes: array
        The signal to evaluate phase locking in relation to `SignalRef`.

    Rate: int
        Sampling rate at which `Signal` was recorded.

    Freqs: array
        Frequencies to process the signals.

    FreqBand: int
        Width for analysis of each frequency in `Freqs`.


    Returns
    -------
    PLVs: array
        The phase locking values for `SignalRef` vs `SignalRes`.
    """
    if len(SignalRef.shape) > 1:
        if SignalRef.shape[1] != SignalRes.shape[1]:
            print('Ref and Result dimensions have to be the same.')
            return(None)

        PLVs = np.zeros((Freqs.shape[0], SignalRef.shape[1]), dtype='float32')
        for C in range(PLVs.shape[1]):
            PLVs[:,C] = GetPLVs(SignalRef[:,C], SignalRes[:,C], Rate, Freqs, FreqBand)

    else:
        PLVs = np.zeros((Freqs.shape[0]), dtype='float32')
        for F,Freq in enumerate(Freqs):
            SignalFilteredRef = FilterSignal(SignalRef, Rate, [Freq, Freq+FreqBand])
            SignalFilteredResult = FilterSignal(SignalRes, Rate, [Freq, Freq+FreqBand])
            DP = GetDeltaPhase(SignalFilteredRef, SignalFilteredResult)
            PLVs[F] = np.abs(np.mean(np.exp(1j * DP)))

    return(PLVs)


def GetStrongestCh(Data):
    """
    Get the channel with highest magnitude (calculated as root mean square) in
    `Data`.

    Parameters
    ----------
    Data: 2d array
        Data to be processed. The dimensions should be (samples, channels).

    Returns
    -------
    BestCh: int
        The index of the channel in `Data` (column) with the highest magnitude.
    """
    BestCh = RMS(Data).argmax()
    return(BestCh)


def PSD(Signal, Rate, Scaling='density', Window='hann', WindowSize=None, NPerSeg=None, Overlap=None, NFFT=None, Verbose=False):
    """
    Get the power spectrum density (PSD) of a signal. Built around
    `scipy.signal.welch`, so see `scipy.signal.welch?` for more info.

    Parameters
    ----------
    Signal: array
        The signal to be processed. If 2d array, each column will be processed
        separately.

    Rate: int
        Sampling rate at which `Signal` was recorded.

    Scaling: { ‘density’, ‘spectrum’ }, optional
        Selects between computing the power spectral density (‘density’;
        V**2/Hz) and computing the power spectrum (‘spectrum’; V**2).

    Window: str or tuple or array_like, optional
        Desired window to use.

    WindowSize: int, optional
        The size of the window to be used. If `None`, `Signal.shape[0]` will
        be used.

    NPerSeg: int, optional
        Length of each segment. If `None`, `WindowSize//2` will be used.

    Overlap: int, optional
        Number of points to overlap between segments. If `None`,
        `WindowSize//4` will be used.

    NFFT: int, optional
        Length of the FFT used, if a zero padded FFT is desired. If
        `None`, the FFT length is calculated by Analysis.GetNFFT().

    Verbose: bool, optional
        Whether or not output should be printed.


    Returns
    -------
    F: array
        Array of sample frequencies.

    PxxSp: array
        Power spectral density or power spectrum of x.

    """
    if WindowSize is None: WindowSize = Signal.shape[0]
    if NPerSeg is None: NPerSeg = WindowSize//2
    if Overlap is None: Overlap = WindowSize//4

    F, PxxSp = [], []

    if len(Signal.shape) == 2:
        for C in range(Signal.shape[1]):
            if Verbose: print('PSD of channel', C+1, '...')
            f, pxx = PSD(Signal[:,C], Rate, Scaling, Window, WindowSize, NPerSeg, Overlap)

            if not len(F):
                PxxSp = np.zeros((len(pxx), Signal.shape[1]), dtype='float')
                F = f.copy()


            PxxSp[:,C] = pxx

    else:
        if NFFT is None: NFFT = GetNFFT(WindowSize)
        F, PxxSp = ssig.welch(Signal, Rate, window=Window, nperseg=NPerSeg,
                                noverlap=Overlap, nfft=NFFT, detrend=False)

    return(F, PxxSp)


def QuantifyTTLs(Data=[], StdNo=2.5, Edge='rise', FixedThreshold=None, Verbose=False):
    """
    Detect TTLs (rising or falling edges) in a signal.

    Parameters
    ----------
    Data: 1d array
        Data to be processed.

    StdNo: float, optional
        How many standard deviations above the mean the edge peak must be.

    Edge: { `rise`, `fall`, `both` }, optional
        What edge should be detected. Defaults to 'rise'.

    FixedThreshold: float, optional
        If set, only edges with peak higher than `FixedThreshold` will
        be detected. In this case, `StdNo` will be ignored.

    Verbose: bool, optional
        Whether or not output should be printed.


    Returns
    -------
    TTLs: array
        Array with indexes of detected edges in `Data`.

    """
    if Verbose: print('Get TTL timestamps... ', end='')
    if not FixedThreshold: Threshold = Data.mean() + StdNo*(Data.std())
    else: Threshold = FixedThreshold
    if Verbose: print('TTL threshold:', Threshold)

    Rise = (Data[:-1] < Threshold)*(Data[1:] > Threshold)
    Fall = (Data[:-1] > Threshold)*(Data[1:] < Threshold)

    if Edge.lower() == 'rise': TTLs = np.where(Rise)[0]
    elif Edge.lower() == 'fall': TTLs = np.where(Fall)[0]
    elif Edge.lower() == 'both':
        TTLs = np.where(Rise+Fall)[0]
        Type = [1 if Rise[TTL] else 0 for TTL in TTLs]
        TTLs = np.array((TTLs,Type)).T
    else:
        print('`Edge` should be `rise`, `fall` or `both`.')
        return(None)

    if Verbose: print('Done.')
    return(TTLs)


def RemapCh(Probe, Adaptor):
    """
    Get channel map according to probe and adaptor used. This is a higher level
    function which adds channelmaps for commonly used probes and connectors,
    so they can be selected by name instead of listing their channel order.
    See `sciscripts.Analysis.RemapChannels?` for more info.

    Parameters
    ----------
    Probe: str
        Probe name.

    Adaptor: str
        Adaptor name.


    Returns
    -------
    Map: list
        Channel map ordered from top to bottom.

    """
    Probes = {
        'A1x16-A16': {
            'Tip': [9, 8, 10, 7, 13, 4, 12, 5, 15, 2, 16, 1, 14, 3, 11, 6],
            'Head': [8, 7, 6, 5, 4, 3, 2, 1, 9, 10, 11, 12, 13, 14, 15, 16]
        },
        'A2x2-Tet': {
            'Tip': [2, 3, 7, 5, 1, 6, 8, 4, 12, 10, 14, 15, 13, 9, 11, 16],
            'Head': [8, 7, 6, 5, 4, 3, 2, 1, 9, 10, 11, 12, 13, 14, 15, 16]
        },
        'A1x16-CM16': {
            'Tip': [9, 8, 10, 7, 11, 6, 12, 5, 13, 4, 14, 3, 15, 2, 16, 1],
            'Head': [5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 13, 14, 15, 16]
        },
        'A4x4-CM16': {
            'Tip': [3, 2, 4, 1, 7, 6, 8, 5, 11, 10, 12, 9, 15, 14, 16, 13],
            'Head': [5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 13, 14, 15, 16]
        },
        'Ciralli': {
            'Tip': [12, 11, 10, 9, 8, 7, 6, 5, 13, 14, 15, 16, 1, 2, 3, 4],
            'Head': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        }
    }

    Adaptors = {
        # 'CustomAdaptor': [5, 6, 7, 8, 9, 10 ,11, 12, 13, 14, 15, 16, 1, 2, 3, 4],
        'RHAA16': [16, 15, 14, 13, 12, 11, 10, 9, 1, 2, 3, 4, 5, 6, 7, 8],
        'RHAOM': [12, 11, 10, 9, 8, 7, 6, 5, 13, 14, 15, 16, 1, 2, 3, 4],
        'A16OM16': [13, 12, 14, 11, 15, 10, 16, 9, 5, 4, 6, 3, 7, 2, 8, 1],
        'None16': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    }

    ProbeName = Probe.replace('_Reverse','')
    if ProbeName not in Probes or Adaptor not in Adaptors:
        print('Unknown probe and/or adaptor.')
        print('Known probes:')
        for P in Probes.keys(): print('    ' + P)
        print('Known adaptors:')
        for A in Adaptors.keys(): print('    ' + A)
        return(None)

    Tip = Probes[ProbeName]['Tip']
    if '_Reverse' in Probe: Tip = Tip[::-1]

    Map = RemapChannels(Tip, Probes[ProbeName]['Head'], Adaptors[Adaptor])
    return(Map)


def SignalIntensity(Signal, Rate, FreqBand, Ref, NoiseRMS=None, PSDArgs={}):
    """
    Get intensity of a signal in dBSPL. Calculates the PSD of the signal,
    then the RMS of the selected frequency band, and finally convert to
    dBSPL according to `Ref`.

    Parameters
    ----------
    Signal: array
        The signal to be processed.

    Rate: int
        Sampling rate at which `Signal` was recorded.

    FreqBand: list
        List with 2 values defining the frequency (Hz) range for intensity
        analysis.

    Ref: float
        Reference to normalize the intensity before converting to dBSPL
        (usually the microphone calibration, in V/Pa).

    NoiseRMS: float, optional
        If provided, it will be subtracted from the signal's RMS before
        normalizing and converting to dBSPL.

    PSDArgs: dict, optional
        Dict providing arguments that will be passed to
        `sciscripts.Analysis.PSD()`.


    Returns
    -------
    Intensity: dict
        Dict containing the signal intensity in RMS and dBSPL.

    IntensityPSD: dict
        Dict containing the results from the singal's PSD analysis.

    """
    Intensity = {}; IntensityPSD = {}

    F, PxxSp = PSD(Signal, Rate, **PSDArgs)
    Range = (F > FreqBand[0])*(F < FreqBand[1])
    BinSize = F[1] - F[0]

    PxxRMS = (sum(PxxSp[Range]) * BinSize)**0.5
    if NoiseRMS: PxxRMS = PxxRMS - NoiseRMS

    dB = 20*(np.log10((PxxRMS/Ref)/2e-5))

    IntensityPSD['F'] = F
    IntensityPSD['PxxSp'] = PxxSp
    Intensity['RMS'] = PxxRMS
    Intensity['dB'] = dB

    return(Intensity, IntensityPSD)


def Slice(Data, TTLs, SliceWindow, Verbose=False):
    """
    Slice data around timestamps (TTLs) according to a window.

    Parameters
    ----------
    Data: array
        Data to be processed. If 2d array, each column (channel) will be
        processed separately.

    TTLs: list
        List of timestamps to slice `Data`.

    SliceWindow: list
        List with start and end (in samples) of the slicing according to each
        timestamp in `TTLs`.

    Verbose: bool, optional
        Whether or not output should be printed.


    Returns
    -------
    Array: array
        Array with (at least) two dimensions, (samples, TTL), containing the
        sliced data around each TTL in TTLs. If `Data` is 2d, then `Array`
        will have 3 dimensions, (samples, TTL, Channel).

    """
    if len(Data.shape) == 2:
        NoOfSamples = abs(SliceWindow[0])+abs(SliceWindow[1])
        Array = np.zeros((NoOfSamples, len(TTLs), Data.shape[1]))

        for C in range(Data.shape[1]):
            if Verbose: print(f'Processing {C+1} of {Data.shape[1]}...')
            Array[:,:,C] = Slice(Data[:,C], TTLs, [SliceWindow[0], SliceWindow[1]])
        if Verbose: print('Done.')

    else:
        NoOfSamples = abs(SliceWindow[0])+abs(SliceWindow[1])
        Array = np.zeros((NoOfSamples, len(TTLs)))

        for T, TTL in enumerate(TTLs):
            Start = TTL+SliceWindow[0]
            End = TTL+SliceWindow[1]

            if Start < 0 or End > len(Data):
                if Verbose: print('TTL too close to the edge. Skipping...')
                continue

            Array[:,T] = Data[Start:End]

    return(Array)


def Spectrogram(Signal, Rate, Window='hann', WindowSize=None, Overlap=None, NFFT=None, Verbose=False):
    """
    Get the spectrogram of a signal. Built around
    `scipy.signal.spectrogram`, so see `scipy.signal.spectrogram?` for more info.

    Parameters
    ----------
    Signal: array
        The signal to be processed. If 2d array, each column will be processed
        separately.

    Rate: int
        Sampling rate at which `Signal` was recorded.

    Window: str or tuple or array_like, optional
        Desired window to use.

    WindowSize: int, optional
        The size of the window to be used. If `None`, `Signal.shape[0]//4` will
        be used.

    Overlap: int, optional
        Number of points to overlap between segments. If `None`,
        `WindowSize//4` will be used.

    NFFT: int, optional
        Length of the FFT to be used. If `None`, it will be automatically
        calculated based on `WindowSize` (see `sciscripts.Analysis.GetNFFT?`)

    Verbose: bool, optional
        Whether or not output should be printed.


    Returns
    -------
    F: array
        Array of sample frequencies.

    T: array
        Array of sample times.

    PxxSp: array
        Power spectral density or power spectrum of x.

    """
    if WindowSize is None: WindowSize = len(Signal)//4
    if Overlap is None: Overlap = WindowSize//2
    if NFFT is None: NFFT = GetNFFT(WindowSize)

    F, T, Sxx = [], [], []

    if len(Signal.shape) == 2:
        for C in range(Signal.shape[1]):
            if Verbose: print('Spectrogram of channel', C+1, '...')
            f, t, sxx = Spectrogram(
                Signal[:,C], Rate, Window, WindowSize, Overlap, NFFT
            )

            if not len(F):
                F = f
                T = t
                Sxx = np.zeros((sxx.shape[0], sxx.shape[1], Signal.shape[1]), dtype='float')

            Sxx[:,:,C] = sxx

    else:
        F, T, Sxx = ssig.spectrogram(
            Signal, Rate, axis=0, nperseg=WindowSize,
            noverlap=Overlap, nfft=NFFT, detrend=False, window=Window
        )

    return(F, T, Sxx)


