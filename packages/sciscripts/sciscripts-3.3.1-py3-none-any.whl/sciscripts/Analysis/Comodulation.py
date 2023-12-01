#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 2017

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('[Analysis.Comodulation] Loading dependencies...')
import gc, os
import numpy as np

from sciscripts.IO import IO
from sciscripts.Analysis import Analysis, Stats
print('[Analysis.Comodulation] Done.')


def PhaseAmp(
            Data, Rate,
            PhaseFreqBand, PhaseFreqBandWidth, PhaseFreqBandStep,
            AmpFreqBand, AmpFreqBandWidth, AmpFreqBandStep,
            FilterOrder=2, Verbose=False
        ):
    """
    Calculate how strongly Phase of one frequency band modulates amplitude of
    another frequency band.

    Parameters
    ----------
    Data: array
        Data to be processed. If 2d array, each column will be processed
        separately.

    Rate: int
        Sampling rate at which `Data` was recorded.

    PhaseFreqBand: list
        List with 2 values defining the frequency (Hz) range for phase analysis.

    PhaseFreqBandWidth: int
        Frequency width (Hz) for each frequency step for phase analysis.

    PhaseFreqBandStep: int
        Frequency (Hz) step for phase analysis.

    AmpFreqBand: list
        List with 2 values defining the frequency (Hz) range for amplitude
        analysis.

    AmpFreqBandWidth: int
        Frequency width (Hz) for each frequency step for amplitude analysis.

    AmpFreqBandStep: int
        Frequency (Hz) step for amplitude analysis.

    FilterOrder: int, optional
        Filter order.


    Returns
    -------
    Comodulogram: array
        Array with the modulation index of amplitude of each frequency to phase
        of each frequency.

    AmpFreq: array
        Array of amplitude frequencies.

    PhaseFreq: array
        Array of phase frequencies.

    """
    PhaseFreq = np.arange(PhaseFreqBand[0], PhaseFreqBand[1], PhaseFreqBandStep)
    AmpFreq = np.arange(AmpFreqBand[0], AmpFreqBand[1], AmpFreqBandStep)

    if len(Data.shape) == 2:
        Comodulogram = np.empty((len(AmpFreq), len(PhaseFreq), Data.shape[1]))
        for C in range(Data.shape[1]):
            if Verbose: print(f'=== [Ch {C+1}] ===')
            Comodulogram[:,:,C] = PhaseAmp(
                Data[:,C], Rate,
                PhaseFreqBand, PhaseFreqBandWidth, PhaseFreqBandStep,
                AmpFreqBand, AmpFreqBandWidth, AmpFreqBandStep, FilterOrder
            )[0]

    else:
        Phases = np.arange(-180,161,20)
        MeanAmp = np.empty(len(Phases))
        Comodulogram = np.empty((len(AmpFreq), len(PhaseFreq)))

        Func = [Analysis.GetPhase, Analysis.GetAmpEnv]

        if Verbose: print('Getting phase and amp. env. for each frequency band...', end=' ')
        DataPhaseAmp = [
            [
                Func[A](
                    Analysis.FilterSignal(Data, Rate, [_, _+Band], FilterOrder)
                )
                for _ in AF
            ]
            for A, (AF,Band) in enumerate([
                [PhaseFreq, PhaseFreqBandWidth],
                [AmpFreq, AmpFreqBandWidth]
            ])
        ]
        if Verbose: print('Done')

        for PhF,PhaseF in enumerate(PhaseFreq):
            for AF,AmpF in enumerate(AmpFreq):
                if Verbose: print(f'    [Phase {PhaseF}-{PhaseF+PhaseFreqBandWidth}] [Amp {AmpF}-{AmpF+AmpFreqBandWidth}]')

                for P,Ph in enumerate(Phases):
                    I = (np.rad2deg(DataPhaseAmp[0][PhF])>Ph)*(np.rad2deg(DataPhaseAmp[0][PhF])<(Ph+20))
                    MeanAmp[P] = np.mean(DataPhaseAmp[1][AF][I])

                p = MeanAmp/sum(MeanAmp)
                MI = (np.log(len(p))+sum(p[p>0]*np.log(p[p>0])))/np.log(len(p))
                Comodulogram[AF,PhF] = MI

    gc.collect()
    return(Comodulogram, AmpFreq, PhaseFreq)


def AmpAmp(
            Data, Rate,
            AmpFreqBand1, AmpFreqBandWidth1, AmpFreqBandStep1,
            AmpFreqBand2, AmpFreqBandWidth2, AmpFreqBandStep2,
            FilterOrder=2, Verbose=False
        ):
    """
    Calculate how strongly amplitude of one frequency band modulates amplitude
    of another frequency band.

    Parameters
    ----------
    Data: array
        Data to be processed. If 2d array, each column will be processed
        separately.

    Rate: int
        Sampling rate at which `Data` was recorded.

    AmpFreqBand1: list
        List with 2 values defining the frequency (Hz) range for the first
        amplitude analysis.

    AmpFreqBandWidth1: int
        Frequency width (Hz) for each frequency step for the first amplitude
        analysis.

    AmpFreqBandStep1: int
        Frequency (Hz) step for the first amplitude analysis.

    AmpFreqBand2: list
        List with 2 values defining the frequency (Hz) range for the second
        amplitude analysis.

    AmpFreqBandWidth2: int
        Frequency width (Hz) for each frequency step for the second amplitude
        analysis.

    AmpFreqBandStep2: int
        Frequency (Hz) step for the second amplitude analysis.

    FilterOrder: int, optional
        Filter order.


    Returns
    -------
    Comodulogram: array
        Array with the modulation index of amplitude of each frequency to phase
        of each frequency.

    AmpFreq1: array
        Array of amplitude1 frequencies.

    AmpFreq2: array
        Array of amplitude2 frequencies.

    """
    AmpFreq1 = np.arange(AmpFreqBand1[0], AmpFreqBand1[1], AmpFreqBandStep1)
    AmpFreq2 = np.arange(AmpFreqBand2[0], AmpFreqBand2[1], AmpFreqBandStep2)

    if len(Data.shape) == 2:
        Comodulogram = np.empty((len(AmpFreq1), len(AmpFreq2), Data.shape[1]))
        for C in range(Data.shape[1]):
            if Verbose: print(f'=== [Ch {C+1}] ===')
            Comodulogram[:,:,C] = AmpAmp(
                Data[:,C], Rate,
                AmpFreqBand1, AmpFreqBandWidth1, AmpFreqBandStep1,
                AmpFreqBand2, AmpFreqBandWidth2, AmpFreqBandStep2, FilterOrder
            )[0]

    else:
        Comodulogram = np.empty((len(AmpFreq1), len(AmpFreq2)))

        if Verbose: print('Getting amp. env. for each frequency band...', end=' ')
        Amp = [
            [
                Analysis.GetAmpEnv(
                    Analysis.FilterSignal(Data, Rate, [_, _+Band], FilterOrder)
                )
                for _ in AF
            ]
            for AF,Band in [
                [AmpFreq1, AmpFreqBandWidth1],
                [AmpFreq2, AmpFreqBandWidth2]
            ]
        ]
        if Verbose: print('Done')

        for AF1,AmpF1 in enumerate(AmpFreq1):
            for AF2,AmpF2 in enumerate(AmpFreq2):
                if Verbose: print(f'    [Amp {AmpF1}-{AmpF1+AmpFreqBandWidth1}] [Amp {AmpF2}-{AmpF2+AmpFreqBandWidth2}]')
                r,p = Stats.sst.pearsonr(Amp[0][AF1], Amp[1][AF2])
                Comodulogram[AF1,AF2] = r

    gc.collect()
    return(Comodulogram, AmpFreq1, AmpFreq2)


