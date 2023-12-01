#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20180904

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

ScriptName = 'Analysis.SoundMeasurements'

import numpy as np
import os

try:
    from pandas import DataFrame
    AvailPandas = True
except ModuleNotFoundError as e:
    print(f'[{ScriptName}] {e}: Module `pandas` not available. Some functions will not work.')
    AvailPandas = False

from sciscripts.Analysis.Analysis import SignalIntensity
from sciscripts.IO import DAqs, IO


## Level 0
def GetMeasurements(CalibrationPath, Rate, MicSens_VPa, Noise=[]):
    print('Calculating PSD, RMS and dBSLP...')
    SoundRecPath = f"{CalibrationPath}/SoundRec"
    Freqs = os.listdir(SoundRecPath)
    Freqs = sorted(Freqs, key=lambda x: int(x.split('-')[1]))

    AmpFs = [_.split('.')[0].replace('_','.')  for _ in os.listdir(SoundRecPath+'/'+Freqs[0]) if '.dat' in _]
    AmpFs = sorted(AmpFs, reverse=True, key=lambda x: float(x))

    PSD = {}
    SoundIntensity = {K: np.zeros((len(AmpFs), len(Freqs)), dtype='float32')
                      for K in ['dB', 'RMS']}

    for F, Freq in enumerate(Freqs):
        FreqBand = [int(_) for _ in Freq.split('-')]
        SoundRec = DAqs.GetSoundRec(f"{SoundRecPath}/{Freq}", IsAll=False)

        if len(Noise):
            NoiseRMS = SignalIntensity(Noise[int(Rate*2):int(Rate*4),0], Rate, FreqBand, 1)[0]
            NoiseRMS = NoiseRMS['RMS']
        else:
            NoiseRMS = None

        for A, AmpF in enumerate(AmpFs):
            if AmpF not in SoundRec: continue

            si, psd = SignalIntensity(SoundRec[AmpF][:,0], Rate, FreqBand, MicSens_VPa, NoiseRMS)
            del(SoundRec[AmpF])
            for K in si.keys(): SoundIntensity[K][A,F] = si[K]
            for K in psd.keys():
                if K not in PSD:
                    PSD[K] = np.zeros((psd[K].shape[0], len(AmpFs), len(Freqs)),
                                      dtype='float32')
                PSD[K][:,A,F] = psd[K]

    SoundIntensity['Freqs'] = np.array(Freqs)
    SoundIntensity['AmpFs'] = np.array(AmpFs)
    SoundIntensity['Dimensions'] = np.array(['AmpF', 'Freq'])
    PSD['Freqs'] = np.array(Freqs)
    PSD['AmpFs'] = np.array(AmpFs)
    PSD['Dimensions'] = np.array(['Data', 'AmpF', 'Freq'])

    return(SoundIntensity, PSD)


def TexTableWrite(SoundIntensity, DataPath):
    if not AvailPandas:
        raise ModuleNotFoundError(f'[{ScriptName}] Module `pandas` not available.')

    TexTable =  DataFrame(
        [['Volt.'] + SoundIntensity['Freqs'].tolist()] + [
            [float(AmpF)]+[
                round(SoundIntensity['dB'][A,F], 2)
                for F,Freq in enumerate(SoundIntensity['Freqs'])
            ]
            for A,AmpF in enumerate(SoundIntensity['AmpFs'])
        ]
    )

    ssys, sset = DataPath.split('/')[-2:]

    with open(DataPath+'/'+'IntensityTable.tex', 'w') as File:
        File.write(
        r"""%% Configs =====
\documentclass[12pt,a4paper,landscape]{article}
\usepackage[left=0.5cm,right=0.5cm,top=0.5cm,bottom=0.5cm]{geometry}
\usepackage{longtable}
\title{Sound measurements}
\author{""" + f'{ssys} {sset}' + r"""}
% Document ======
\begin{document}
\maketitle
\scriptsize
"""     )
        File.write(TexTable.to_latex(longtable=True, index=False, index_names=False))
        File.write(r"""
\end{document}
"""     )

    return(None)


def Run(Rate, CalibrationPath, MicSens_dB=None, MicSens_VPa=None, **Kws):
    if MicSens_dB == None and MicSens_VPa == None:
        raise ValueError('At least one of MicSens_dB or MicSens_VPa must be provided.')

    if MicSens_VPa == None: MicSens_VPa = 10**(MicSens_dB/20)

    # Noise = IO.Bin.Read(f"{CalibrationPath}/Noise.dat")[0]
    Noise = []
    SoundIntensity, PSD = GetMeasurements(CalibrationPath, Rate, MicSens_VPa, Noise)

    ## Save analyzed data
    print('Saving analyzed data...')
    IO.Bin.Write(SoundIntensity, CalibrationPath+'/SoundIntensity')
    IO.Bin.Write(PSD, CalibrationPath+'/PSD')

    if AvailPandas: TexTableWrite(SoundIntensity, CalibrationPath)

    print('Done.')


