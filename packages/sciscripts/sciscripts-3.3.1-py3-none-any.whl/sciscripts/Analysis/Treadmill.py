#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20170612

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

import numpy as np
from scipy.interpolate import interp1d
from sciscripts.Analysis import Analysis

# def GetSxx(Data, Rate, SensorCh, PeakDist, Theta=[7, 10], Delta=[2, 4]):
def GetSxx(Data, Rate, SensorCh, PeakDist, FilterBands=[[2,4],[4,12],[12,30],[30,60]], FilterOrders=[2,2,2,2]):
    SensorData = Data[:,SensorCh-1]*-1
    Peaks = Analysis.QuantifyTTLs(SensorData)

    V = np.zeros(len(SensorData))
    for P in range(1, len(Peaks)):
        Samples = Peaks[P] - Peaks[P-1]; Time = Samples/Rate
        Speed = PeakDist/Time; V[Peaks[P-1]:Peaks[P]] = [Speed]*Samples

    VInd, VPeaks = Analysis.GetPeaks(V, Rate*3)
    f = interp1d(VInd, VPeaks, fill_value=0.0, bounds_error=False)
    V = f(np.arange(len(V))); V[V!=V] = 0.0

    F, T, Sxx = Analysis.Spectrogram(Data, Rate, WindowSize=Rate*2)

    BandMaxs = [
        Sxx[(F>=min(Band))*(F<max(Band)),:,:].max(axis=0)
        for Band in FilterBands
    ]

    SxxMaxs = np.zeros(Sxx.shape[1:])
    for Band in BandMaxs:
        SxxMaxs = np.array((BandMaxs, SxxMaxs)).max(axis=0)

    VMeans = [np.mean(V[int(T[t]*Rate):int(T[t+1]*Rate)])
              for t in range(len(T)-1)] + [0.0]
    VMeansSorted = sorted(VMeans)
    VInds = [VMeansSorted.index(v) for v in VMeans]

    Treadmill = {}
    for C in range(Data.shape[1]-1):
        Ch = "{0:02d}".format(C+1); Treadmill[Ch] = {}
        print('Processing Ch', Ch, '...')

        SxxPerV = Sxx[:,VInds]

        Start = np.where(T>Peaks[0]/Rate)[0][0]
        End = np.where(T<Peaks[-1]/Rate)[0][-1]
        TDIndex = max(ThetaMaxs[Start:End])/max(DeltaMaxs[Start:End])
        # SxxSR = 1/(T[1]-T[0]); SxxLowPass = SxxSR*5/100
        # SxxMeans = Analysis.FilterSignal(SxxMeans, SxxSR,
        #                                       [SxxLowPass], 1, 'butter',
        #                                         'lowpass')

        Treadmill[Ch] = {
            'F': F, 'T': T, 'Sxx': Sxx, 'SxxMaxs': SxxMaxs,
            'SxxPerV': SxxPerV, 'TDIndex': TDIndex, 'VMeans': VMeans,
            'VMeansSorted': VMeansSorted, 'VInds':VInds
        }

    print('Done.')
    return(Treadmill)

