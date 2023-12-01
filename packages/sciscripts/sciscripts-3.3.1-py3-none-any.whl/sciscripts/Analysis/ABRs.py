#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 2017

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts

Functions for analysis of ABR recordings.
"""

print('[Analysis.ABRs] Loading dependencies...')
import numpy as np
import os

from copy import deepcopy
from glob import glob

from sciscripts.Analysis import Analysis
from sciscripts.Analysis.Plot import Plot
from sciscripts.IO import IO

print('[Analysis.ABRs] Done.')

## Level 0
def ABRPerCh(Data, Rate, TTLs, TimeWindow=[-0.003,0.012], FilterFreq=[600,1500], FilterOrder=4, FilterCoeff='butter', Filter='bandpass'):
    """
    Extract ABR signal from each channel of Data.

    Filters according to FilterFreq, FilterOrder, FilterCoeff and Filter; slice
    around TTLs according to TimeWindow; and average the sliced trials for each
    channel in Data.

    Parameters
    ----------
    Data: array_like
        The input array, containing two dimensions ([samples, channels]).

    Rate: int
        Sampling rate of Data.

    TTLs: array_like
        Array with timestamps of each stimulus onset.

    TimeWindow: array_like, optional
        Array containing two time values (s), which are the beginning and ending of the
        window to be analyzed in relation to each timestamp mark.

    FilterFreq: array_like, optional
        Frequency (Hz) for filtering each Data channel.

    FilterOrder: int, optional
        Filter order.

    FilterCoeff: str, optional
        Filter coefficient type. Can be `'butter'` or `'fir'`.

    Filter: str, optional
        Type of filtering. Can be `'lowpass'`, `'highpass'` or `'bandpass'`.

    Returns
    -------
    ABRs: array_like
        The ABR signals for each channel in Data.
    """
    Len = abs(int((Rate*TimeWindow[0])-(Rate*TimeWindow[1])))
    ABRs = np.zeros((Len, Data.shape[1]), dtype=Data.dtype)
    ABRData = Analysis.FilterSignal(Data, Rate, FilterFreq, FilterOrder, FilterCoeff, Filter)

    if 'float' in str(type(TTLs[0])):
        if np.array(TTLs).all() == np.array(TTLs, dtype=int).all():
            TTLs = np.array(TTLs, dtype=int)

    ABRs = Analysis.Slice(
        ABRData, TTLs,
        [int(TimeWindow[0]*Rate), int(TimeWindow[1]*Rate)],
    )
    ABRs = ABRs.mean(axis=1)

    return(ABRs)


def LatencyToPeaks(ABRs, X=[], RefKey=None, Std=1, Verbose=False):
    """
    Extract peaks from `ABRs[RefKey][:,BestCh]`, where `BestCh` is the channel
    with the greatest Root-mean-square. The threshold for peaks are set as
    `ABRs[RefKey][:,BestCh].std()*Std`, see `sciscripts.Analysis.GetPeaks?` for
    more details. Then, screen each decreasing intensity for detected peaks
    that are preceded by a peak in the previous intensity. This way, only peaks
    that increases latency when decreasing stimulus intensity are kept.

    Parameters
    ----------
    ABRs: dict
        Dictionary containing one array per key, where each array is the ABR
        signal in response to a particular intensity (dict key). If `ABRs.keys()`
        are '0','1','2'... the order is mantained, otherwise it'll be sorted
        reverse (louder intensities analyzed first). Each array should have two
        dimensions ([samples, channels]), even if channels==1.

    X: array_like, optional
        Array of timestamps with shape `(ABRs[key].shape[0],)`. Can be provided
        if the data contains signal from before the stimulus. In this case,
        peaks detected with index smaller than `np.where((X>=0))[0][0]` will
        be ignored.

    RefKey: dict key, optional
        Dict key containing the data that will be used as reference to all the
        others. If `None` (default), then, if `ABRs.keys()` are '0','1','2'...
        `RefKey` will be '0'. Otherwise, it will be
        `sorted(ABRs.keys(), reverse=Rev)[0]`.

    Std: int or float, optional
        The threshold for detecting peaks is set as the standard deviation for
        the recording at `ABRs[RefKey]`, multiplied by Std.

    Returns
    -------
    AllPeaks: array
        Two-dimensional array with dimensions [keys, peaks], containing indexes
        of ABR peaks. The order of keys is as decribed above. The order of
        peaks detected in the `RefKey` is kept, so that peaks that do not
        follow the described criteria are replaced by -1.

    Examples
    --------

    .. code-block:: python

       In [10]: ABRs
       Out[10]:
       {'80': array([[ 1181, 16285],
               [37042, 16041],
               [30807,  4551],
               ...,
               [56512,  8017],
               [46125,  1472],
               [15484, 60812]]),
        '70': array([[42270,  4771],
               [29553, 42571],
               [ 1899, 41892],
               ...,
               [34616, 31499],
               [ 9830, 60458],
               [12736, 53194]]),
        '60': array([[45993, 48502],
               [23933,  3293],
               [ 2631, 61917],
               ...,
               [33227, 28280],
               [36086, 51514],
               [12659, 41927]]),
        '50': array([[16129, 37416],
               [65399,  9624],
               [40702, 13121],
               ...,
               [35727,   779],
               [45576, 17999],
               [35339, 43360]])}

       In [11]: X
       Out[11]:
       array([-5.        , -4.9824854 , -4.96497081, ..., 15.96497081,
              15.9824854 , 16.        ])

       In [12]: LatencyToPeaks(ABRs, X)
       array([[136, 178, 205, 239, 274],
              [139, 180, 207,  -1,  -1],
              [142, 181,  -1,  -1,  -1],
              [ -1,  -1,  -1,  -1,  -1],
              [ -1,  -1,  -1,  -1,  -1],
              [ -1,  -1,  -1,  -1,  -1],
              [ -1,  -1,  -1,  -1,  -1],
              [ -1,  -1,  -1,  -1,  -1],
              [ -1,  -1,  -1,  -1,  -1],
              [ -1,  -1,  -1,  -1,  -1]])

    In this example, the first and second peaks were detected until the third
    strongest intensity, which should be considered the hearing threshold.

    """
    FN = LatencyToPeaks.__name__.replace('sciscripts.','')
    Rev = False if '0' in ABRs else True
    Recs = sorted(ABRs.keys(), reverse=Rev)

    if len(Recs) == 1:
        if Verbose: print(f'[{FN}] You need at least 2 recordings in ABRs dict to compare latencies.')
        return(None)

    if not RefKey: RefKey = Recs[0]
    BestCh = Analysis.GetStrongestCh(ABRs[RefKey])

    # FixedThreshold = ABRs[RefKey][:,BestCh].std()*Std
    # Peaks = [Analysis.GetPeaks(ABRs[Rec][:,BestCh], FixedThreshold=FixedThreshold) for Rec in Recs]
    Peaks = [Analysis.GetPeaks(ABRs[Rec][:,BestCh], Std=Std) for Rec in Recs]

    Peaks = [_['Pos'] for _ in Peaks]
    if len(X): Peaks = [P[X[P] > 0] for P in Peaks]

    if not len(Peaks[0]):
        AllPeaks = np.ones((len(Recs),1), dtype=int)*-1
        return(AllPeaks)

    AllPeaks = []; ToRemove = []
    for R, Rec in enumerate(Recs):
        if R == 0: AllPeaks.append(Peaks[R].tolist()); continue
        if not len(Peaks[R]):
            ToRemove.append((R,0))
            AllPeaks.append([AllPeaks[0][-1]])
            continue

        PeakNo = min([len(Peaks[R]), len(Peaks[0])])
        RecPeaks = []
        for P in range(1,PeakNo):
            if np.where((Peaks[0][P] >= Peaks[R][P-1]) *
                        (Peaks[R][P-1] >= Peaks[0][P-1]-3))[0].size:
                RecPeaks.append(Peaks[R][P-1])
            else:
                ToRemove.append((R,P-1))
                try: RecPeaks.append(AllPeaks[0][P-1])
                except IndexError: RecPeaks.append(AllPeaks[0][-1])

        # If no peaks in previous intensity, try the one before
        LocalRef = 0
        LocalLen = 0
        while not LocalLen:
            LocalRef -= 1
            LocalLen = len(AllPeaks[LocalRef])

        if np.where((AllPeaks[LocalRef][-1] < Peaks[R]))[0].size:
            Last = Peaks[R][AllPeaks[LocalRef][-1] < Peaks[R]][0]

            if Last not in RecPeaks:
                if Verbose: print(f'[{FN}] Before:', RecPeaks)
                Ind = np.where((AllPeaks[0] <= Last))[0][0]

                IntermedNo = (Ind)-len(RecPeaks)
                if IntermedNo > 0:
                    for _ in range(IntermedNo): ToRemove.append((R,len(RecPeaks)+_))

                    Intermed = [AllPeaks[0][len(RecPeaks)+_] for _ in range(IntermedNo)]
                    RecPeaks += Intermed + [Last]

                else: RecPeaks += [Last]

        AllPeaks.append(RecPeaks)

    for R in ToRemove: AllPeaks[R[0]][R[1]] = -1

    MaxLen = max([len(_) for _ in AllPeaks])
    AllPeaks = [_ + [-1]*(MaxLen-len(_)) for _ in AllPeaks]

    AllPeaks = np.array(AllPeaks)
    for P in range(AllPeaks.shape[1]):
        Ind = np.where((AllPeaks[:,P]==max(AllPeaks[:,P])))[0][-1]+1
        AllPeaks[Ind:,P] = -1

    return(AllPeaks)


## Level 1
def GetThreshold(ABRs, X=[], Std=1, Verbose=False):
    """
    Get hearing threshold from ABR traces as the lowest intensity evoking valid
    peaks. See `sciscripts.Analysis.ABRs.LatencyToPeaks?` for more details on
    what is a valid peak.

    Parameters
    ----------
    ABRs: dict
        Dictionary containing one array per key, where each array is the ABR
        signal in response to a particular intensity (dict key). If `ABRs.keys()`
        are '0','1','2'... the order is mantained, otherwise it'll be sorted
        reverse (louder intensities analyzed first). Each array should have two
        dimensions ([samples, channels]), even if channels==1.

    X: array_like, optional
        Array of timestamps with shape `(ABRs[key].shape[0],)`. Can be provided
        if the data contains signal from before the stimulus. In this case,
        peaks detected with index smaller than `np.where((X>=0))[0][0]` will
        be ignored.

    Std: int or float, optional
        The threshold for detecting peaks is set as the standard deviation for
        the recording at highest intensity, multiplied by Std.

    Returns
    -------

    Threshold: int
        Index of the recording that evoked the smallest detectable response.

    """
    Peaks = LatencyToPeaks(ABRs, X, Std=Std, Verbose=Verbose)
    if Peaks is None or Peaks.mean() == -1:
        return(0)

    Threshold = max([np.where((Peaks[:,_] == max(Peaks[:,_])))[0][-1]
                     for _ in range(Peaks.shape[1])])
    return(Threshold)


def LatencyPerFreq(Files, Freqs, Std=1, Verbose=False):
    """
    Under dev
    """
    Latencies = {}
    for F,File in enumerate(Files):
        ABRs = IO.Bin.Read(File)[0]
        X = '/'.join(File.split('/')[:-1])+'/X.dat'
        X = IO.Bin.Read(X)[0]

        Latencies[Freqs[F]] = LatencyToPeaks(ABRs, X, Std=Std, Verbose=Verbose)

        Thrs = [np.where((Latencies[Freqs[F]][:,_] == max(Latencies[Freqs[F]][:,_])))[0][-1] for _ in range(Latencies[Freqs[F]].shape[1])]
        Ind = np.where((Thrs == max(Thrs)))[0][0]
        Latencies[Freqs[F]] = Latencies[Freqs[F]][:,Ind].astype('float32')

        Latencies[Freqs[F]][Latencies[Freqs[F]] == -1] = float('NaN')

        Latencies[Freqs[F]] /= int(round(1/(X[1] - X[0])))

    return(Latencies)


def Single(Data, Rate, ABRCh, TTLCh, TimeWindow=[-0.003,0.012], FilterFreq=[600,1500], FilterOrder=4, Filter='bandpass', Save='', Return=True, Verbose=False):
    """
    Extract ABR traces from raw data.

    Process each data channel (see `sciscripts.Analysis.ABRs.ABRPerCh?`)
    according to the input parameters.

    Parameters
    ----------
    Data: array
        Two-dimensional array ([samples, channels]) containing neural data and
        a channel containing stimulus timestamp marks.

    Rate: int
        Sampling rate in which `Data` was acquired.

    ABRCh: list
        List of channels from `Data` that contains ABR signal, *1-indexed*.

    TTLCh: list or int
        If `int`, channel from `Data` containing the stimulus timestamps,
        *1-indexed*. If `list`, list of stimulus timestamps (samples).

    TimeWindow: list, optional
        List containing the start and stop time (s) in relation to each timestamp
        mark. Values should be in milliseconds.

    FilterFreq: array_like, optional
        Frequency (Hz) for filtering each Data channel.

    FilterOrder: int, optional
        Filter order.

    Filter: str, optional
        Type of filtering. Can be `'lowpass'`, `'highpass'` or `'bandpass'`.

    Save: str, optional
        File for saving the array containing the processed ABR signals. If
        empty, no file will be saved.

    Return: bool, optional
        Toggle for disabling the return of the resulting ABR array. Useful for
        when running several datasets and writing the results to files (see
        `sciscripts.Analysis.ABRs.Multiple?`).

    Returns
    -------
    ABRs: array
        Two-dimensional array ([samples, channels]) containing the processed
        ABR signals for each channel in `Data`.

    X: array
        Array with time values based on `TimeWindow` matching `ABRs.shape[0]`.

    """
    FN = Single.__name__.replace('sciscripts.','')
    X = Analysis.GetTime(TimeWindow, Rate)*1000

    if type(TTLCh) == int:
        TTLs = Analysis.QuantifyTTLs(Data[:,TTLCh-1])
    else:
        TTLs = TTLCh

    if len(TTLs) and TTLs[0] != 'Broken':
        ABRs = ABRPerCh(Data[:,[_-1 for _ in ABRCh]], Rate, TTLs, TimeWindow, FilterFreq, FilterOrder, FilterCoeff='butter', Filter=Filter)
    else:
        if Verbose: print(f'[{FN}] No TTLs in this recording.')
        return((None,None))

    if Save:
        IO.Bin.Write(X, '/'.join(Save.split('/')[:-2])+'/X.dat')
        IO.Bin.Write(ABRs, Save)

    if Return:
        return(ABRs, X)
    else:
        del(ABRs, X)
        return(None)


## Level 2
def Multiple(Data, Rate, ABRCh, TTLCh, TimeWindow=[-0.003,0.012], FilterFreq=[600,1500], Recs=[], Intensities=[], Save='', Return=True, Verbose=False):
    """
    Extract ABR traces from recordings at different intensities.

    Process each data channel (see `sciscripts.Analysis.ABRs.ABRPerCh?`)
    from each recording (see `sciscripts.Analysis.ABRs.Single?`)  according
    to the input parameters.

    Parameters
    ----------
    Data: dict
        Dictionary containing one array per key, where each array is a two-
        dimensional array ([samples, channels]) containing neural data and
        a channel containing stimulus timestamp marks; each recorded under
        stimulation at a particular intensity (dict key). If `Recs` is not
        provided, the keys will be sorted. Each array should have two
        dimensions ([samples, channels]), even if channels==1.

    Rate: int
        Sampling rate in which `Data` was acquired.

    ABRCh: list
        List of channels from `Data` that contains ABR signal, *1-indexed*. If
        `ABRCh` is a list of lists, then each list will be used to each
        recording under `Data`, ordered as in `Recs`.

    TTLCh: list or int
        If `int`, channel from `Data` containing the stimulus timestamps,
        *1-indexed*. If `list`, list of stimulus timestamps (samples).

    TimeWindow: list, optional
        List containing the start and stop time (s) in relation to each timestamp
        mark. Values should be in milliseconds.

    FilterFreq: array_like, optional
        Frequency (Hz) for filtering each Data channel.

    Recs: list, optional
        List containing which keys in `Data` to be processed. Recordings will
        be processed in the order they are provided. If empty, keys in `Data`
        will be sorted and all recordings will be processed.

    Intensities: list, optional
        List containing the stimuli intensities used for each recording under
        `Data`. Should be provided in the same order as `Recs`. If empty, it
        will be the sorted `Data` keys as integers.

    Save: str, optional
        Path for saving the arrays containing the processed ABR signals. If
        empty, no file will be saved.

    Return: bool, optional
        Toggle for disabling the return of the resulting ABR dict. Useful for
        when running several datasets and writing the results to files..

    Returns
    -------
    ABRs: dict
        Dict containing arrays ([samples, channels]) containing the processed
        ABR signals for each channel in each key of `Data`.

    X: array
        Array with time values based on `TimeWindow`.

    """
    FN = Multiple.__name__.replace('sciscripts.','')
    if not len(Recs): Recs = sorted(Data.keys(), key=lambda x: int(x))

    ABRs = {}
    for R,Rec in enumerate(Recs):
        if Verbose: print(f'[{FN}] Processing rec {Rec}...')
        Rec_R = Rec if not len(Intensities) else Intensities[R]
        ABRCh_R = ABRCh if type(ABRCh[0]) != list else ABRCh[R]

        if Save:
            Save_R = Save+'/'+Rec if not len(Intensities) else Save+'/'+Intensities[R]
        else:
            Save_R = ''

        if type(TTLCh) == list:
            TTLCh_R = IO.Bin.Read(TTLCh[R])[0] if type(TTLCh[R]) == str else TTLCh[R]
        else:
            TTLCh_R = TTLCh

        ABRs[Rec_R] = Single(
            Data[Rec], Rate, ABRCh_R, TTLCh_R, TimeWindow, FilterFreq,
            Save=Save_R, Return=True, Verbose=Verbose
        )[0]

    X = Analysis.GetTime(TimeWindow, Rate)*1000

    if Save:
        IO.Bin.Write(X, '/'.join(Save.split('/')[:-1])+'/X.dat')

    if Verbose: print(f'[{FN}] Done.')

    if Return:
        return(ABRs, X)
    else:
        del(ABRs, X)
        return(None)


## Level 3
def GetThresholdsPerFreq(Folders, Std=1, Verbose=False):
    """
    Under dev
    """
    Thresholds = {'Thresholds': [], 'Freqs':[], 'Animals':[]}

    for Folder in Folders:
        ABR = IO.Bin.Read(Folder+'/ABRs', Verbose=Verbose)[0]
        Freqs = sorted(ABR.keys(), key=lambda i: int(i.split('-')[1]))
        Animal = Folder.split('/')[-1].split('-')[1]

        for Freq in Freqs:
            Trial = 'Trial'+str(len(ABR[Freq])-2)
            Intensities = sorted(ABR[Freq][Trial], reverse=True, key=lambda x: int(x))
            Threshold = GetThreshold(ABR[Freq][Trial], ABR[Freq]['X'], Std=Std, Verbose=Verbose)
            Thresholds['Thresholds'].append(int(Intensities[Threshold]))
            Thresholds['Freqs'].append(Freq)
            Thresholds['Animals'].append(Animal)

    Thresholds = {K: np.array(V) for K,V in Thresholds.items()}

    return(Thresholds)

def GetWaveAmpPerFreq(Folders, Std=1, Factors=[], FactorNames=[], Verbose=False):
    """
    Under dev
    """
    WaveAmps = {'Amps': [], 'Latencies':[], 'Freqs':[], 'Intensity':[], 'Animal':[], 'Folder':[]}
    WaveAmps = {**WaveAmps, **{_:[] for _ in FactorNames}}

    for F,Folder in enumerate(Folders):
        Animal = Folder.split('/')[-1].split('-')[1]
        ABR = IO.Bin.Read(Folder+'/ABRs', Verbose=Verbose)[0]
        Freqs = sorted(ABR.keys(), key=lambda i: int(i.split('-')[1]))

        for Freq in Freqs:
            Trial = 'Trial'+str(len(ABR[Freq])-2)
            Intensities = sorted(ABR[Freq][Trial], reverse=True, key=lambda x: int(x))
            X = IO.Bin.Read(Folder+'/ABRs/'+Freq+'/X.dat', Verbose=Verbose)[0]
            Peaks = LatencyToPeaks(ABR[Freq][Trial], X, Std=Std, Verbose=Verbose)
            if Peaks is None or Peaks.mean() == -1:
                for I,Int in enumerate(Intensities):
                    WaveAmps['Amps'].append(np.empty((5))*np.nan)
                    WaveAmps['Latencies'].append(np.empty((5))*np.nan)
                    WaveAmps['Freqs'].append(Freq)
                    WaveAmps['Intensity'].append(Int)
                    WaveAmps['Animal'].append(Animal)
                    WaveAmps['Folder'].append(Folder)
                    for Fa,Factor in enumerate(Factors):
                        WaveAmps[FactorNames[Fa]].append(Factor[F])
            else:
                for I,Int in enumerate(Intensities):
                    WaveAmp = Analysis.GetAmpEnv(ABR[Freq][Trial][Int])[Peaks[I,:],0]
                    WaveAmp[Peaks[I,:]==-1] = np.nan
                    WaveLat = X[Peaks[I,:]]
                    WaveLat[Peaks[I,:]==-1] = np.nan

                    WaveAmps['Amps'].append(WaveAmp)
                    WaveAmps['Latencies'].append(WaveLat)
                    WaveAmps['Freqs'].append(Freq)
                    WaveAmps['Intensity'].append(Int)
                    WaveAmps['Animal'].append(Animal)
                    WaveAmps['Folder'].append(Folder)

                    for Fa,Factor in enumerate(Factors):
                        WaveAmps[FactorNames[Fa]].append(Factor[F])

    MaxLen = max([_.shape[0] for _ in WaveAmps['Amps']])
    for WA,WaveAmp in enumerate(WaveAmps['Amps']):
        if WaveAmp.shape[0] < MaxLen:
            WaveAmps['Amps'][WA] = np.hstack((
                WaveAmp, np.empty((MaxLen-WaveAmp.shape[0]))*np.nan
            ))

            WaveAmps['Latencies'][WA] = np.hstack((
                WaveAmps['Latencies'][WA],
                np.empty((MaxLen-WaveAmp.shape[0]))*np.nan
            ))

    WaveAmps = {K: np.array(V) for K,V in WaveAmps.items()}

    return(WaveAmps)


def Session(Folders, Freqs, ABRCh, TTLCh, TimeWindow=[-0.003,0.012], FilterFreq=[600,1500], Intensities=[], Proc='', Exp='', ChannelMap=[], Save='', Return=True, Verbose=False):
    """
    Extract ABR traces from recordings at different frequencies and intensities.

    Process each data channel (see `sciscripts.Analysis.ABRs.ABRPerCh?`)
    from each recording (see `sciscripts.Analysis.ABRs.Single?`) from each
    folder (see `sciscripts.Analysis.ABRs.Multiple?`) according to the input
    parameters.

    Parameters
    ----------
    Folders: list
        List containing paths for neural recordings. Those folders must be
        loadable by `sciscripts.IO.IO.DataLoader`.

    Freqs: list
        List of stimulation frequencies (`str`) used for each folder in `Folders`.

    ABRCh: list
        List of channels from `Data` that contains ABR signal, *1-indexed*. If
        `ABRCh` is a list of lists, then each list will be used to each folder
        under `Folders`, respectively.

    TTLCh: list or int
        List of channels from `Data` containing the stimulus timestamps,
        *1-indexed*, for each folder. If `int`, then the same channel will be
        used for all folders.

    TimeWindow: list, optional
        List containing the start and stop time (s) in relation to each timestamp
        mark. Values should be in milliseconds.

    FilterFreq: array_like, optional
        Frequency (Hz) for filtering each Data channel.

    Intensities: list, optional
        List containing the stimuli intensities used for each recording under
        `Data`. Should be provided in the same order as `Recs`. If empty, it
        will be the sorted `Data` keys as integers.

    Proc: str
        If the folders contain data recorded from more than one processor,
        only data from `Proc` will be processed. If empty, all processors will
        be sorted and the first will be selected.

    ChannelMap: list, optional
        Ordering of channels. Must have the same number of channels as in the
        recorded data under `Folders`.

    Save: str, optional
        Path for saving the arrays containing the processed ABR signals. If
        empty, no file will be saved. If `'auto'`, files will be saved at
        the current directory.

    Return: bool, optional
        Toggle for disabling the return of the resulting ABR dict. Useful for
        when running several datasets and writing the results to files..

    Returns
    -------
    ABRs: dict
        | Dict
        |     containing dicts
        |         containing arrays ([samples, channels])
        |             containing the processed ABR signals
        |             for each channel
        |         for each key of `Data`
        |     for each folder in `Folders`
        | .

    X: array
        Array with time values based on `TimeWindow`.

    """
    FN = Session.__name__.replace('sciscripts.','')
    ABRs = {}
    for F, Folder in enumerate(Folders):
        if Verbose: print(f"[{FN}] {Folder}")
        Data, Rate = IO.DataLoader(Folder, Unit='uV', ChannelMap=ChannelMap, Verbose=Verbose)

        if not len(Proc):
            if len(Data.keys()) == 1: tProc = list(Data.keys())[0]
            else: ChNo, tProc = IO.OpenEphys.GetChNoAndProcs(Folder+'/settings.xml')
        else: tProc = Proc

        tExp = list(Data[tProc].keys())[0] if not len(Exp) else Exp

        Data, Rate = Data[tProc][tExp], Rate[tProc][tExp]

        TTLCh_F = TTLCh[F] if type(TTLCh) == list else TTLCh
        ABRCh_F = ABRCh[F] if type(ABRCh[0]) == list else ABRCh

        if len(Save):
            if Save.lower() == 'auto':
                Save = './' + Folder.split('/')[-3]

            XSavePath = '/'.join([Save, 'ABRs', Freqs[F]])
            if os.path.isdir(XSavePath): Trial = 'Trial'+str(len(glob(XSavePath)))
            else: Trial = 'Trial0'
            SavePath = '/'.join([XSavePath, Trial])
        else:
            SavePath = ''

        ABRs[Freqs[F]], X = Multiple(Data, Rate, ABRCh_F, TTLCh_F, TimeWindow, FilterFreq, Recs=[], Intensities=Intensities, Save=SavePath, Return=True, Verbose=Verbose)

        del(Data)

    if Return:
        return(ABRs, X)
    else:
        del(ABRs, X)
        return(None)


