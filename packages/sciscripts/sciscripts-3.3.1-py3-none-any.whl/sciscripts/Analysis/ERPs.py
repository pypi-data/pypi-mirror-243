#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>, B. Ciralli <barbara.ciralli@gmail.com>

:Date: 20190428

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts

Analysis of evoked response potentials (ERPs) during the paired-click
behavioural paradigm.
"""

import numpy as np
import os
from glob import glob

from sciscripts.Analysis import Analysis, Stats
from sciscripts.IO import IO


# Level -1
def GetTTLs(Signal, Folder):
    """
    This function is super specific for a very customized experimental setup.
    You'll probably have to get your TTLs timestamps using other functions (see
    `sciscripts.Analysis.QuantifyTTLs?`).
    """
    if 'SLFull' in Folder or 'SLFast' in Folder:
        L = Analysis.QuantifyTTLs(Signal, 0.6)
        S = Analysis.QuantifyTTLs(Signal, 0.15)
        TTLs = [s for s in S if True not in [l in L for l in np.arange(s-1, s+2)]]
        Bad = np.where((np.diff(TTLs) < 15000))[0]
        if len(Bad): del(TTLs[Bad[-1]])
    else:
        TTLs = Analysis.QuantifyTTLs(Signal, 4)
        if len(TTLs) == 101:
            Diff = np.diff(TTLs)[::2]
            Wrong = np.where(~((12000<Diff)*(Diff<18000)))[0][0]*2
            TTLs = np.concatenate((TTLs[:Wrong], TTLs[Wrong+1:]))

    return(TTLs)


def Load(Folder, ChannelMap=[], ImpedanceFile='', InfoFile=''):
    """
    This function is super specific for a very customized experimental setup.
    You'll probably have to load your data using other functions (see
    `sciscripts.IO.DataLoader?`).
    """
    if 'Control_03' in Folder:
        ExtraCh = [33] if 'Treadmill' in Folder else [33,34]
        if len(ChannelMap):
            ChMap = ChannelMap
        else:
            ChMap = [9, 13, 15, 18, 20, 6, 4, 5, 32, 1, 31, 29, 28, 27, 25, 26] + ExtraCh
    elif 'int' in [_.split('.')[-1] for _ in glob(Folder+'/*')]:
        if len(ChannelMap):
            ChMap = ChannelMap
        else:
            ChMap = Analysis.RemapCh('A1x16-CM16', 'RHAOM') + [17]
    else:
        if InfoFile:
            Info = IO.Txt.Read(InfoFile)
            ExtraCh = [Info['DAqs']['StimCh'], Info['DAqs']['TTLCh']]
        else:
            ExtraCh = [17] if 'Treadmill' in Folder else [17,18]

        if len(ChannelMap):
            ChMap = ChannelMap
        else:
            ChMap = Analysis.RemapCh('Ciralli', 'None16') + ExtraCh

    Data, Rate = IO.DataLoader(Folder, ChannelMap=ChMap, ImpedanceFile=ImpedanceFile)
    if 'int' in [_.split('.')[-1] for _ in glob(Folder+'/*')]:
        D = np.vstack([Data[_] for _ in sorted(Data.keys(), key=lambda x: int(x))])
        Data = {'100': {'0': {'0': D}}}
        Rate = {'100': {'0': Rate}}

    Key = list(Data.keys())[0]
    Rec = sorted(Data[Key]['0'].keys(), key=lambda x: [int(i) for i in x])[0]
    Data, Rate = Data[Key]['0'][Rec], Rate[Key]['0']

    return(Data, Rate)


# Level 0

def GetComponents(Signal, X, PWindows, Verbose=False):
    if len(Signal.shape) == 2:
        P20, N40, P80, Doublets = [], [], [], []
        for C in range(Signal.shape[1]):
            if Verbose: print('Processing channel', C+1, '...')
            c1, c2, c3, d = GetComponents(Signal[:,C], PWindows, Verbose)
            P20.append(c1); N40.append(c2); P80.append(c3); Doublets.append(d)
    else:
        # Detect all peaks
        PAllPN = Analysis.GetPeaks(Signal, Std=0)
        PAll = sorted(np.concatenate((PAllPN['Pos'], PAllPN['Neg'])))
        P = [[_ for _ in PAll if _ in np.arange(W[0], W[1], dtype=int)] for W in PWindows]
        PDiff = [np.diff(Signal[_]) for _ in P]
        PDiffSorted = [sorted(_) for _ in PDiff]

        # Detect N40 and P80 by negative-positive change
        PDiffN40 = [np.where((PDiff[_] == PDiffSorted[_][-1]))[0][0] for _ in range(2)]
        PDiffN40[1] += len(P[0])
        P = [b for a in P for b in a]
        PDiff = np.diff(Signal[P])
        PDiffSorted = sorted(PDiff)

        PDiffN40 = sorted(PDiffN40)
        N40, P80 = [sorted([P[PDiffN40[0]+_], P[PDiffN40[1]+_]]) for _ in range(2)]

        # Detect P20 by positive-negative change happening before N40
        PDiffP20 = [10000, 10000]
        for Peak in range(2):
            Index = -1
            while PDiffP20[Peak] > PDiffN40[Peak] and Index < len(PDiffSorted)-1:
                Index += 1
                p20 = np.where((PDiff == PDiffSorted[Index]))[0][0]
                if PWindows[Peak][0] <= P[p20] <= PWindows[Peak][1]:
                    PDiffP20[Peak] = p20

        if 10000 in PDiffP20: raise Exception("    Oh no! Bad P20Diff!")

        P20 = sorted([P[PDiffP20[0]], P[PDiffP20[1]]])
        P20 = [v if Signal[P[PDiffP20[i]+1]] < v else P[PDiffP20[i]+1] for i,v in enumerate(P20)]

        # Detect doublets and correct N40 to get the first doublet peak
        N40 = [P[P.index(P20[i])+1] if v != P20[i] else v for i,v in enumerate(N40)]
        DoubletsLen = [P.index(P80[_])-P.index(N40[_]) for _ in range(2)]
        Doublets = [_>1 for _ in DoubletsLen]

        # Correct N40 to the most negative peak within P20-P80 range
        N40LimL = [
            P20[_] if P20[_] != N40[_] else PWindows[_][0]
            for _ in range(2)
        ]
        N40LimU = P80
        # N40LimU = [
            # np.where((X>=(X[PWindows[_][0]]+0.06)))[0][0]
            # for _ in range(2)
        # ]
        N40 = [
            np.where((Signal == Signal[
                np.arange(N40LimL[_], N40LimU[_], dtype=int)
            ].min()))[0][-1]
            for _ in range(2)
        ]

        # Correct missing P20 to the peak preceding N40
        for p,peak in enumerate(P20):
            if peak != peak or peak == N40[p]:
                # pi = PAll.index(N40[p])-1-((DoubletsLen[p]-1)*2)
                # P20[p] = PAll[pi] if PAll[pi] in np.arange(*PWindows[p]) else P20[p]
                pi = PAllPN['Pos'][np.where((PAllPN['Pos']<N40[p]))[0][-1]]
                P20[p] = pi if pi in np.arange(*PWindows[p]) else P20[p]


        # Correct P80 for the most positive point from N40-max(PWindow)
        # for p,peak in enumerate(N40):
            # P80[p] = Signal[peak:int(PWindows[p][-1])].argmax()+peak

    P20, N40, P80, Doublets = (np.array(_).T for _ in (P20, N40, P80, Doublets))
    return(P20, N40, P80, Doublets)


def GetPhaseRevCh(ERP, X, BrokenCh=[], Window=[], Debug=False):
    SampleNo, ChNo = ERP.shape
    BrokenChZP = [_-1 for _ in BrokenCh]

    if not len(Window): Window = [0,0.1]
    Sl = (X>=Window[0])*(X<=Window[1])

    ERPc = ERP.copy()
    ERPc[:,BrokenChZP] = 0
    ChGood = [_ for _ in range(ChNo) if _ not in BrokenChZP]
    if len(ChGood) == 1:
        return(ChGood[0]+1)

    Phase = Analysis.GetPhase(ERPc)
    PhaseRes = Phase[Sl,:].mean(axis=0)

    PairLabels = list(Analysis.Pairwise(ChGood))
    DeltaPhase = np.array([
        Analysis.GetDeltaPhase(ERPc[:,Pair[0]], ERPc[:,Pair[1]])
        for Pair in PairLabels
    ]).T

    DeltaPhaseRes = DeltaPhase[Sl,:].mean(axis=0)
    Pair = abs(DeltaPhaseRes).argmax()
    Chs = np.array(PairLabels[Pair])

    ChNeg = abs(ERPc[:,Chs].min(axis=0)) > ERPc[:,Chs].max(axis=0)
    if len(np.unique(ChNeg)) == 2:
        ChosenCh = Chs[ChNeg][0]+1
    else:
        ChosenCh = Chs[PhaseRes[Chs].argmin()]+1

    if Debug: return(PhaseRes, Chs, Pair, ChosenCh)
    else: return(ChosenCh)


def PairedERP(Data, Rate, TTLs, FilterFreq, FilterOrder, FilterType, ERPWindow,
              File='PairedERP', Save=False):
    ChNo = Data.shape[1]
    TrialNo = len(TTLs)//2

    DataERPs = Analysis.FilterSignal(Data, Rate, FilterFreq, FilterOrder, Type=FilterType)
    ERPs = Analysis.Slice(
        DataERPs, TTLs[::2],
        [int(ERPWindow[0]*Rate), int(ERPWindow[1]*Rate)]
    )

    X = Analysis.GetTime(ERPWindow, Rate)

    if Save:
        if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
        IO.Bin.Write(ERPs, File+'.dat')
        IO.Bin.Write(X, File+'_X.dat')

    return(ERPs, X)


# Level 1
def GetSensoryGatingSet(Data, ERPsX, Rate, BLDur, PWindows):
    Zeros = [np.where((ERPsX >= 0))[0][0], np.where((ERPsX >= 0.5))[0][0]]
    BLStart = Zeros[0]-int(Rate*BLDur)
    BLStart = BLStart if BLStart > 0 else 0
    BL = Data[BLStart:Zeros[0],:].mean(axis=0)

    P20, N40, P80, _ = GetComponents(Data, PWindows)

    Set = np.array([
        [
            [
                Data[comp[click,_],_]-BL[_]
                for _ in range(comp.shape[1])
            ]
            for click in [0,1]
        ]
        for comp in [P20, N40, P80]
    ])

    return(Set)


