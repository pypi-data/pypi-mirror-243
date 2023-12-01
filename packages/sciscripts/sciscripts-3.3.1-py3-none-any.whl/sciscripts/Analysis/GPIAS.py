#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20170612

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('[Analysis.GPIAS] Loading dependencies...')
import numpy as np
from copy import deepcopy as dcp
from glob import glob

from sciscripts.Analysis import Analysis as sAnalysis
from sciscripts.IO import IO
print('[Analysis.GPIAS] Done.')


## Level 0
def AmpCalc(Data, X, SliceSamples, BGNormalize=True):
    acData = dcp(Data)
    PulseStart = np.where((X >= 0))[0][0]
    PulseEnd = PulseStart + SliceSamples
    if len(acData.shape) == 1:
        acData = acData.reshape((acData.shape[0],1))

    RMSPulse = (np.mean(acData[PulseStart:PulseEnd,:]**2, axis=0))**0.5
    if BGNormalize:
        BGStart = PulseStart - SliceSamples
        BGEnd = PulseStart
        RMSBG = (np.mean(acData[BGStart:BGEnd,:]**2, axis=0))**0.5
        RMS = abs(RMSPulse-RMSBG)
    else:
        RMS = RMSPulse

    return(RMS)


# def CheckGPIASRecs(Data, SizeLimits, Plot=False):
    # ToCheck = [Rec for Rec in Data.keys()
                   # if len(Data[Rec])<min(SizeLimits)
                   # or len(Data[Rec])>max(SizeLimits)]
#
    # if ToCheck:
        # if Plot:
            # Params = {'backend': 'TkAgg'}
            # from matplotlib import rcParams; rcParams.update(Params)
            # import matplotlib.pyplot as plt
#
            # for Rec in ToCheck:
                # print('Showing Rec', Rec+', size', Data[Rec].shape[0])
                # plt.plot(Data[Rec])
                # plt.show()
#
        # return(ToCheck)
    # else:
        # print('All recs within expected size.')
        # return(None)
#
#
def ConvertIndexesToArray(Indexes):
    Array = {'Exps': [], 'Animals': [], 'Freqs': [], 'Index':[]}
    for E, Exp in Indexes.items():
        for A, Animal in Exp.items():
            for Freq, Index in Animal.items():
                Array['Exps'].append(E)
                Array['Animals'].append(A)
                Array['Freqs'].append(Freq)
                Array['Index'].append(Index)

    for K in Array.keys(): Array[K] = np.array(Array[K])
    return(Array)


def ConvertTracesToArray(Traces):
    Array = {'Exps': [], 'Animals': [], 'Freqs': [], 'Trials':[], 'Traces':[], 'Dimensions': ['Time','Channels']}
    for E, Exp in Traces.items():
        for A, Animal in Exp.items():
            for Freq, Trace in Animal.items():
                TrialOrder = sorted(Trace.keys())

                for T, Trial in enumerate(TrialOrder):
                    Array['Exps'].append(E)
                    Array['Animals'].append(A)
                    Array['Freqs'].append(Freq)
                    Array['Trials'].append(Trial)
                    Array['Traces'].append(Trace[Trial])

    if len(np.unique([str(_.shape) for _ in Array['Traces']])) == 1:
        Array['Traces'] = np.array(Array['Traces'])
        Array['Dimensions'] = ['Trials']+Array['Dimensions']

    for K in [_ for _ in Array.keys() if _ != 'Traces']: Array[K] = np.array(Array[K])
    return(Array)


def GetExpsIndexesDictSingleTrials(Exps, SliceSize, BGNormalize=True, Verbose=False):
    """
    Get index per freq per animal per exp.
    Necessary for retest overriding (the last tested is always the correct one).
    """
    Indexes_IFAE_ST = {}
    Keys = [['Gap','NoGap', 'GPIASIndex']]

    for E, Exp in Exps.items():
        if E not in Indexes_IFAE_ST: Indexes_IFAE_ST[E] = {}

        for File in sorted(Exp):
            GPIASRecST = IO.Bin.Read(f'{File}/GPIASAllTrials', Verbose=Verbose, AsMMap=False)[0]
            if 'Gap' in GPIASRecST.keys() and 'NoGap' in GPIASRecST.keys():
                fr = glob(f'{File}/GPIASAllTrials/*')[0].split('/')[-1]
                GPIASRecST = {fr: GPIASRecST}

            X = IO.Bin.Read(f'{File}/X.dat', Verbose=Verbose, AsMMap=False)[0]

            Animal = File.split('/')[-1].split('-')[1]
            if Animal not in Indexes_IFAE_ST[E]: Indexes_IFAE_ST[E][Animal] = {}

            SliceSamples = np.where((X>=0)*(X<SliceSize*1000))[0].shape[0]

            GIST = {
                F: IndexCalc(Freq, X, SliceSamples, Keys, BGNormalize)['GPIASIndex']
                for F,Freq in GPIASRecST.items()
            }

            Indexes_IFAE_ST[E][Animal] = {**Indexes_IFAE_ST[E][Animal], **{
                K: sAnalysis.GetNegEquiv(V)
                for K, V in GIST.items()
            }}

    Indexes_IFAE_ST = ConvertIndexesToArray(Indexes_IFAE_ST)
    return(Indexes_IFAE_ST)


def GetExpsIndexesDict(Exps, Verbose=False):
    """
    Get index per freq per animal per exp.
    Necessary for retest overriding (the last tested is always the correct one).
    """
    Indexes_IFAE, Traces_IFAE, X = {}, {}, []
    for E, Exp in Exps.items():
        if E not in Indexes_IFAE: Indexes_IFAE[E], Traces_IFAE[E] = {}, {}

        for File in sorted(Exp):
            GPIASRec = IO.Bin.Read(f'{File}/GPIAS', Verbose=Verbose, AsMMap=False)[0]
            if not len(X):
                X = IO.Bin.Read(f'{File}/X.dat', Verbose=Verbose, AsMMap=False)[0]

            Animal = File.split('/')[-1].split('-')[1]
            if Animal not in Indexes_IFAE[E]:
                Indexes_IFAE[E][Animal], Traces_IFAE[E][Animal] = {}, {}

            Indexes_IFAE[E][Animal] = {**Indexes_IFAE[E][Animal],
                                             **{K: sAnalysis.GetNegEquiv(V['GPIASIndex'])
                                                for K, V in GPIASRec['Index'].items()}}
            Traces_IFAE[E][Animal] = {**Traces_IFAE[E][Animal], **GPIASRec['Trace']}

    Indexes_IFAE = ConvertIndexesToArray(Indexes_IFAE)
    Traces_IFAE = ConvertTracesToArray(Traces_IFAE)

    return(Indexes_IFAE, Traces_IFAE, X)


def GetExpsIndexesDict_InDev(Exps, Verbose=False):
    """
    Get index per freq per animal per exp.
    Necessary for retest overriding (the best tested is always the correct one).
    """
    Indexes_IFAE, Traces_IFAE = {}, {}
    for E, Exp in Exps.items():
        if E not in Indexes_IFAE: Indexes_IFAE[E], Traces_IFAE[E] = {}, {}

        for File in sorted(Exp):
            GPIASRec = IO.Bin.Read(File, Verbose=Verbose)[0]
            if 'XValues' in GPIASRec:
                # Backward compatibility
                GPIASRec['X'] = GPIASRec.pop('XValues')

            GPIASRec, X = GPIASRec['GPIAS'], GPIASRec['X']
            Animal = File.split('/')[-1].split('-')[1]
            if Animal not in Indexes_IFAE[E]:
                Indexes_IFAE[E][Animal], Traces_IFAE[E][Animal] = {}, {}

            Dict = {K: sAnalysis.GetNegEquiv(V['GPIASIndex']) for K, V in GPIASRec['Index'].items()}
            for K in Dict:
                if K in Indexes_IFAE[E][Animal]:
                    if Dict[K] < Indexes_IFAE[E][Animal][K]:
                        print(Indexes_IFAE[E][Animal][K], Dict[K])
                        Indexes_IFAE[E][Animal][K] = Dict[K]
                else:
                    Indexes_IFAE[E][Animal][K] = Dict[K]

            # Indexes_IFAE[E][Animal] = {**Indexes_IFAE[E][Animal], **Dict}

            Traces_IFAE[E][Animal] = {**Traces_IFAE[E][Animal], **GPIASRec['Trace']}

    Indexes_IFAE = ConvertIndexesToArray(Indexes_IFAE)
    Traces_IFAE = ConvertTracesToArray(Traces_IFAE)

    return(Indexes_IFAE, Traces_IFAE, X)


def GetMAF(Indexes_IFAE, Animals, ExpOrder, GetAllDiff=False):
    MAF, MAFAll, MAFAllFreqs = [], [], []
    for Animal in Animals:
        ## Indexes_IFAE as array
        ThisAnimal = Indexes_IFAE['Animals'] == Animal

        Freqs = [
            Indexes_IFAE['Freqs'][ThisAnimal*(Indexes_IFAE['Exps'] == Exp)]
            for Exp in ExpOrder[:2]
        ]

        FreqsI = np.array([
            abs(Indexes_IFAE['Index'][
                ThisAnimal*(Indexes_IFAE['Exps'] == ExpOrder[0])
                *(Indexes_IFAE['Freqs'] == Freq)
            ])
            for Freq in Freqs[0]
        ]).ravel()

        Freqs[0] = np.array(Freqs[0])[FreqsI > 30].tolist()
        Freqs = sorted(
            np.intersect1d(Freqs[0], Freqs[1]),
            key=lambda x: int(x.split('-')[-1])
        )

        ExpFIDiff = [
            abs(Indexes_IFAE['Index'][
                ThisAnimal*(Indexes_IFAE['Exps'] == ExpOrder[1])
                *(Indexes_IFAE['Freqs'] == Freq)
            ])
            - abs(Indexes_IFAE['Index'][
                ThisAnimal*(Indexes_IFAE['Exps'] == ExpOrder[0])
                *(Indexes_IFAE['Freqs'] == Freq)
            ])
            for Freq in Freqs
        ]


        if not ExpFIDiff: MAF.append(None)
        else: MAF.append(Freqs[ExpFIDiff.index(min(ExpFIDiff))])

        MAFAll.append(ExpFIDiff)
        MAFAllFreqs.append(Freqs)

    if GetAllDiff: return(MAF, MAFAll, MAFAllFreqs)
    else: return(MAF)


def GetMAFIndexes(Indexes_IFAE, MAF, Animals, ExpOrder):
    Indexes = [
        np.array([
            Indexes_IFAE['Index'][
                (Indexes_IFAE['Exps'] == Exp) *
                (Indexes_IFAE['Animals'] == Animal) *
                (Indexes_IFAE['Freqs'] == MAF[A])
            ]
            if True in (
                (Indexes_IFAE['Exps'] == Exp) *
                (Indexes_IFAE['Animals'] == Animal) *
                (Indexes_IFAE['Freqs'] == MAF[A])
            ) else [np.nan]
            for A, Animal in enumerate(Animals) if MAF[A]
        ]).ravel() for E, Exp in enumerate(ExpOrder)
    ]

    return(Indexes)


def PreallocateDict(Freqs):
    Dict = {
        Key: {'-'.join([str(Freq[0]), str(Freq[1])]): {} for Freq in Freqs}
        for Key in ['Trace', 'Index', 'IndexTrace']
    }

    for Freq in Dict['Trace'].keys():
        Dict['Trace'][Freq]['NoGap'] = []; Dict['Trace'][Freq]['Gap'] = []
        Dict['IndexTrace'][Freq]['NoGap'] = []; Dict['IndexTrace'][Freq]['Gap'] = []

    return(Dict)


def OrganizeRecs(
        Dict, Data, Rate, DataInfo, TimeWindow, FilterFreq=[70, 170],
        FilterOrder=4, FilterType='bandpass', Filter='butter', Verbose=False
    ):
    FName = 'OrganizeRecs'

    orData = dcp(Data)

    Recs = sorted(orData.keys(), key=lambda i: int(i))

    if Verbose: print(f'[{FName}] Slicing and filtering Recs...')
    for R, Rec in orData.items():
        Freq = DataInfo['ExpInfo']['FreqOrder'][Recs.index(R)][0];
        Trial = DataInfo['ExpInfo']['FreqOrder'][Recs.index(R)][1];

        SFreq = ''.join([str(DataInfo['Audio']['NoiseFrequency'][Freq][0]), '-',
                         str(DataInfo['Audio']['NoiseFrequency'][Freq][1])])

        if Trial == -1: STrial = 'Pre'
        elif Trial == -2: STrial = 'Post'
        elif Trial % 2 == 0: STrial = 'NoGap'
        else: STrial = 'Gap'

        if STrial in ['Pre', 'Post']:
            if Verbose: print(f'    [{FName}][{R}] Pre- and Post- trials still to be implemented. Skipping...')
            continue

        TTLs = sAnalysis.QuantifyTTLs(
            Rec[:,DataInfo['DAqs']['TTLCh']-1], Verbose=Verbose
        )
        if len(TTLs) != 1:
            if Verbose: print(f'    [{FName}][{R}] More than one TTL detected!!')
            # TTLs = [Rec[:,DataInfo['DAqs']['TTLCh']-1].argmax()]    # Get larger TTL
            # TTLs = [TTLs[0]]                                          # Get first TTL

            # Get TTL from sound channel
            # TTLs = [sAnalysis.QuantifyTTLs(Rec[:,DataInfo['DAqs']['StimCh']-1])[0]]

            # Get TTL by convolving the TTL signal with a square wave
            ps = int(DataInfo['Audio']['SoundLoudPulseDur']*Rate/2)
            k = np.zeros(ps*4)
            k[ps:ps*2] = 1
            k[ps*2:-ps] = -1
            c = np.convolve(Rec[:,DataInfo['DAqs']['TTLCh']-1], k, 'same')
            c[:k.shape[0]] = c.mean()
            c[-k.shape[0]:] = c.mean()
            try:
                TTLs = [sAnalysis.QuantifyTTLs(c)[0]]
            except IndexError:
                TTLs = []

        # print(TTLs)

        if not len(TTLs):
            if Verbose: print(f'    [{FName}][{R}] No detected TTLs! Using recording time as TTL.')

            if 'SoundBGDur' in DataInfo['Audio'].keys():
                tb = sum([DataInfo['Audio'][_] for _ in ['SoundBGDur','SoundGapDur','SoundBGPrePulseDur']])
                t = tb + sum([DataInfo['Audio'][_] for _ in ['SoundLoudPulseDur','SoundBGAfterPulseDur']])
            else:
                tb = sum([DataInfo['Audio'][_] for _ in ['SoundBackgroundDur','SoundGapDur','SoundBackgroundPrePulseDur']])
                t = tb + sum([DataInfo['Audio'][_] for _ in ['SoundLoudPulseDur','SoundBackgroundAfterPulseDur']])

            ts = ((Rec.shape[0]/Rate)-t)/2
            TTLs = [np.where(np.linspace(ts,t,Rec.shape[0])>=tb)[0][0]]

        if len(TTLs) != 1:
            raise ValueError(f'[{FName}][{R}] There should be only one TTL!')

        if Verbose: print(f'    [{FName}][{R}] TTL sample: {TTLs[0]}; TTL time in rec: {TTLs[0]/Rate}')

        if Filter:
            if Verbose:  print(f'    [{FName}][{R}] Filtering...')
            GD = sAnalysis.FilterSignal(
                Rec[:,np.array(DataInfo['DAqs']['RecCh'])-1],
                Rate, FilterFreq, FilterOrder, Filter, FilterType
            )
        else:
            GD = Rec[:,np.array(DataInfo['DAqs']['RecCh'])-1]

        # GD = sAnalysis.Normalize_Old(GD, MeanSubtract=True, MaxDivide=False)
        for c in range(GD.shape[1]): GD[:,c] -= np.nanmean(GD[:,c])

        GDs = sAnalysis.Slice(GD, TTLs, [int(TimeWindow[0]*Rate), int(TimeWindow[1]*Rate)])
        GDs = GDs[:,0,:]
        Dict['Trace'][SFreq][STrial].append(GDs)

        GDa = sAnalysis.GetAmpEnv(GD).mean(axis=1)
        GDas = sAnalysis.Slice(GDa, TTLs, [int(TimeWindow[0]*Rate), int(TimeWindow[1]*Rate)])
        GDas = GDas[:,0]
        Dict['IndexTrace'][SFreq][STrial].append(GDas)

        # if GD.shape[1] == 3:
            # # Accelerometer data
            # GD = abs(GD).mean(axis=1)

            # # X = sAnalysis.FilterSignal(Rec[:,DataInfo['DAqs']['RecCh'][0]-1],
                                          # Rate, FilterFreq, FilterOrder, Filter, FilterType)
            # # Y = sAnalysis.FilterSignal(Rec[:,DataInfo['DAqs']['RecCh'][1]-1],
                                          # Rate, FilterFreq, FilterOrder, Filter, FilterType)
            # # Z = sAnalysis.FilterSignal(Rec[:,DataInfo['DAqs']['RecCh'][2]-1],
                                          # Rate, FilterFreq, FilterOrder, Filter, FilterType)

            # # GD = np.mean([
                # # np.abs(X-X.mean()),
                # # np.abs(Y-Y.mean()),
                # # np.abs(Z-Z.mean())],
                # # axis=0
            # # )

    return(Dict)


## Level 1
def IndexCalc(Data, X, SliceSamples, Keys, BGNormalize=True):
    Index = {}
    for Key in Keys:
        # if type(Data[Key[0]]) == list:
            # if not Data[Key[0]]:
        if not len(Data[Key[0]]):
            print('Key', Key[0], 'is empty. Skipping...')
            continue

        ResRMS = AmpCalc(Data[Key[0]], X, SliceSamples, BGNormalize)
        RefRMS = AmpCalc(Data[Key[1]], X, SliceSamples, BGNormalize)
        Index[Key[2]] = ((ResRMS/RefRMS)-1)*100

    return(Index)


def GetAllTrials(
        Data, Rate, DataInfo, TimeWindow=[-0.1, 0.15], FilterFreq=[70, 170],
        FilterOrder=3, FilterType='auto', Filter='butter', Verbose=False, **Args
    ):

    if not DataInfo:
        # Override for old .mat recordings
        if not FilterType:
            if len(FilterFreq) == 1: FilterType = 'lowpass'
            else: FilterType = 'bandpass'

        GPIASData = dcp(Data)
        for Key in ['IndexTrace', 'Trace']:
            for F,Freq in GPIASData[Key].items():
                for G,Gap in Freq.items():
                    for T,Trial in enumerate(Gap):
                        if Filter:
                            GD = sAnalysis.FilterSignal(Trial, Rate, FilterFreq, FilterOrder, Filter, FilterType)
                        else:
                            GD = Trial.copy()

                        # GD = sAnalysis.Normalize_Old(GD, MeanSubtract=True, MaxDivide=False)
                        for c in range(GD.shape[1]): GD[:,c] -= np.nanmean(GD[:,c])

                        if 'Index' in Key:
                            GD = sAnalysis.GetAmpEnv(GD)
                            GD = sAnalysis.Slice(GD, GPIASData['TTLs'], [int(TimeWindow[0]*Rate), int(TimeWindow[1]*Rate)])
                            GD = GD[:,0]
                        else:
                            GD = sAnalysis.Slice(GD, GPIASData['TTLs'], [int(TimeWindow[0]*Rate), int(TimeWindow[1]*Rate)])

                        if Verbose: print(Key, F, G, T)
                        GPIASData[Key][F][G][T] = GD.copy()

        del(GD)

    else:
        GPIASData = PreallocateDict(DataInfo['Audio']['NoiseFrequency'])
        GPIASData = OrganizeRecs(
            GPIASData, Data, Rate, DataInfo, TimeWindow,
            FilterFreq, FilterOrder, FilterType, Filter, Verbose
        )

    return(GPIASData)


## Level 2
def Analysis(
        Data, Rate, DataInfo,
        TimeWindow=[-0.15, 0.15], SliceSize=0.1,
        FilterFreq=[70, 170], FilterOrder=3, FilterType='bandpass', Filter='butter',
        BGNormalize=True, Save='', Return=True, Verbose=False):

    X = sAnalysis.GetTime(TimeWindow, Rate)*1000

    GPIASData = GetAllTrials(
        dcp(Data), Rate, DataInfo, TimeWindow, FilterFreq,
        FilterOrder, FilterType, Filter, Verbose
    )

    Keys = [['Gap', 'NoGap', 'GPIASIndex']]

    for Freq in GPIASData['IndexTrace'].keys():
        for Key in GPIASData['IndexTrace'][Freq].keys():
            # Average trials for traces
            GPIASData['Trace'][Freq][Key] = np.mean(GPIASData['Trace'][Freq][Key], axis=0)
            if GPIASData['Trace'][Freq][Key].shape == ():
                if Verbose: print('Freq', Freq, 'trial', Key, 'is empty. Skipping...')
                continue

            # for Tr in range(len(GPIASData['IndexTrace'][Freq][Key])):
                # GPIASData['IndexTrace'][Freq][Key][Tr] = sAnalysis.GetAmpEnv(
                        # GPIASData['IndexTrace'][Freq][Key][Tr]
                # )

            GPIASData['IndexTrace'][Freq][Key] = np.nanmean(GPIASData['IndexTrace'][Freq][Key], axis=0)

        # RMS
        GPIASData['Index'][Freq] = IndexCalc(
            GPIASData['IndexTrace'][Freq], X, int(SliceSize*Rate),
            Keys, BGNormalize
        )


    if len(Save):
        IO.Bin.Write({'GPIAS': GPIASData, 'X': X}, Save)

    if Return: return(GPIASData, X)
    else: return(None)

