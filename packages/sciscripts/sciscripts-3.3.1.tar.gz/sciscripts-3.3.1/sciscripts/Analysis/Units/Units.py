#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20170612

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('[Analysis.Units.Units] Loading dependencies...')

import os
import numpy as np
from glob import glob

from sciscripts.Analysis import Analysis
from sciscripts.IO import IO

print('[Analysis.Units.Units] Done.')


## Level 0
def FiringRate(SpkTimes, RecLen, Offset=0):
    Spks = SpkTimes-Offset

    FR = np.array([
        len(Spks[(Spks >= Sec) * (Spks < Sec+1)])
        for Sec in range(RecLen)
    ], dtype=int)

    return(FR)


def GetProbeChPos(ChPerShank, SpaceZ, SpaceX=0, SpaceY=0, OffsetX=[0], OffsetY=[0], OffsetZ=[0]):
    ShNo = len(ChPerShank)
    Pos = []

    for Shank in range(ShNo):
        ChNo = ChPerShank[Shank]
        ChPos = np.zeros((ChNo, 3))

        for Ch in range(ChNo):
            x = (SpaceX * Shank) + OffsetX[Shank]
            y = (SpaceY * Shank) + OffsetY[Shank]
            z = (Ch * SpaceZ[Shank]) + OffsetZ[Shank]
            ChPos[Ch,:] = x, y, z

        Pos.append(ChPos)

    Pos = np.vstack(Pos)
    return(Pos)


def GetBestCh(Spks):
    # ChAmp = (Spks.mean(axis=0)**2).mean(axis=0)**0.5    # RMS - account for broadness
    ChAmp = abs(Spks.mean(axis=0)).max(axis=0)            # Max abs ampl
    BestCh = ChAmp.argmax()
    return(BestCh)



def ISI(SpkTimes, ISISize, Rate):
    ISIY = np.histogram(np.diff(SpkTimes), bins=np.arange(0, ISISize, 1/Rate))[0]
    return(ISIY)


def PSTH(Spks, TTLs, PSTHX, Offset=0, Output='all'):
    """ Output: 'all', 'mean', 'binnorm'"""

    PSTHY = np.zeros((len(PSTHX)-1, len(TTLs)), dtype='int32')
    for T, TTL in enumerate(TTLs):
        Firing = (Spks - Offset - TTL)
        Firing = Firing[(Firing >= PSTHX[0]) * (Firing < PSTHX[-1])]

        PSTHY[:,T] = np.histogram(Firing, PSTHX)[0]; del(Firing)

    BinSize = PSTHX[1] - PSTHX[0]
    if Output.lower() == 'all': return(PSTHY)
    elif Output.lower() == 'mean': return(PSTHY.mean(axis=1))
    elif Output.lower() == 'binnorm': return(PSTHY.sum(axis=1)/(len(TTLs)*BinSize))
    else: print('Output should be "all", "mean" or "norm".'); return(None)


def Raster(Spks, TTLs, Rate, RasterX, Offset=0):
    RasterY = np.zeros((len(RasterX)-1, len(TTLs)), dtype='float32')

    for T, TTL in enumerate(TTLs):
        Firing = ((Spks-Offset)*1000/Rate) - (TTL*1000/Rate)
        Firing = Firing[(Firing >= RasterX[0]) * (Firing < RasterX[-1])]

        RasterY[:,T] = np.histogram(Firing, RasterX)[0]; del(Firing)

    RasterY[RasterY == 0] = np.nan

    return(RasterY)


def SpkResp(PSTHY, PSTHX):
    """
        This function returns the difference between the RMS of the mean of
        values after zero (PSTHX>0) and before zero (PSTHX<0). The returned
        value is a 'baseline-corrected' event count.
    """
    # BLRMS = np.zeros(PSTHY.shape)
    # BLRMS[:,:] = PSTHY[:,:]
    # BLRMS = BLRMS.sum(axis=1)

    # BL = PSTHY[PSTHX[:-1]<0,:].sum()
    # BLRMS[BLRMS>BL] = BL

    # SpkResp = ((sum(PSTHY.sum(axis=1)[PSTHX[:-1]>0]) * 2)**0.5) - \
    #           ((sum(BLRMS[PSTHX[:-1]>0]) * 2)**0.5)

    RespRMS = PSTHY.mean(axis=1)[PSTHX[:-1]>0]
    # RespRMS = PSTHY.mean(axis=1)[PSTHX[:-1]>-10]
    RespRMS = ((RespRMS**2).mean())**0.5

    BLRMS = PSTHY.mean(axis=1)[PSTHX[:-1]<0]
    # BLRMS = PSTHY.mean(axis=1)[PSTHX[:-1]<-30]
    BLRMS = ((BLRMS**2).mean())**0.5

    SpkRespRMS = RespRMS - BLRMS
    return(SpkRespRMS)


## Level 1
def SpkRespPVal(PSTHY, PSTHX, N=None):
    """
        Implemented as described in Parras et al., 2017.

        This function generates a sample of N histograms with the same size
        of PSTH containing random values in a poisson distribution, with lambda
        equal to the PSTH baseline firing rate (mean of values when PSTHX<0).
        Then, it corrects the spike count after stimulus using the mean of
        values before stimulus for both the original and simulated PSTHYograms.
        Finally, it calculates the p-value as p = (g+1)/(N+1), where g is
        the number of simulated PSTHYograms with spike count >= than the
        original spike count. Therefore, the returned p-value represents the
        probability of the cell firing NOT be affected by stimulation.
    """
    if not N: N = PSTHY.shape[1]
    BL = PSTHY.mean(axis=1)[PSTHX[:-1]<0].mean()
    SimPSTH = [np.random.poisson(BL, (PSTHY.shape[0],1)) for _ in range(N)]
    SimPSTH = [SpkResp(_, PSTHX) for _ in SimPSTH]
    SpikeCount = SpkResp(PSTHY, PSTHX)

    # abs() is used because cells can also stop firing in response to stimulation :)
    g = len([_ for _ in SimPSTH if abs(_) >= abs(SpikeCount)])
    p = (g+1)/(N+1)

    return(p)


## Level 2
def GetCellsResponse(PSTHX, PSTHY, AnalysisFile='CellsResponse', Save=False, Return=True):
    CellsResponse = {}
    for K in ['SpkResp', 'SpkCount']:
        CellsResponse[K] = np.zeros(len(PSTH), dtype=np.float32)

    for U in range(len(PSTHY)):
        UPSTHY = PSTHY[U]
        if 'str' in str(type(UPSTHY)):
            UPSTHY = IO.Bin.Read(UPSTHY)[0]

        TrialNo = UPSTHY.shape[1]
        if UPSTHY.sum() < TrialNo*0.03:
            # if too few spikes in PSTHY
            CellsResponse['SpkResp'][U] = 1
            CellsResponse['SpkCount'][U] = 0
        else:
            CellsResponse['SpkResp'][U] = SpkRespPVal(UPSTHY, PSTHX[U], N=TrialNo)
            CellsResponse['SpkCount'][U] = SpkResp(UPSTHY, PSTHX[U])

    if Save: IO.Bin.Write(CellsResponse, AnalysisFile)

    if Return:
        return(CellsResponse)
    else:
        del(CellsResponse)
        return(None)


