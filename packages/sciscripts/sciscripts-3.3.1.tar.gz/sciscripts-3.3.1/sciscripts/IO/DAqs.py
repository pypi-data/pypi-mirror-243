#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20170904

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

import os
from sciscripts.IO import IO



## Level 0
def NoCalibrationMsg(CalibrationPath):
    Msg = f'No such file or directory: {CalibrationPath}'+r'''
Calibration files were not found. You have to calibrate your setup before using it, or manually
provide the voltage amplification factor that will be applied to the speaker
using the SoundAmpF variable.

For more details, read the sciscripts.Exps.SoundMeasurements documentation:
    sciscripts.Exps import SoundMeasurements
    print(SoundMeasurements.__doc__)
'''
    return(Msg)


# Level 1
def CalibrationLoad(Dataset):
    try:
        Data = IO.Bin.Read(Dataset)[0]
    except FileNotFoundError as e:
        raise FileNotFoundError(NoCalibrationMsg(Dataset))

    return(Data)


def CalibrationOverrideWarning():
    Msg = f'=========================== WARNING =============================\n'
    Msg += 'You provided specific voltages to drive the speaker. That means\n'
    Msg += 'that the sound intensities were NOT calibrated by SciScripts. Thus,\n'
    Msg += 'the stimulus will neither be normalized according to the sound card\n'
    Msg += 'amplification nor corrected for the sound card filter settings.\n'
    Msg += '\n'
    Msg += 'It is HIGHLY UNLIKELY that the intensities requested at the\n'
    Msg += '`Intensities` variable will be the real intensity played.\n'
    Msg += '\n'
    Msg += 'You should calibrate your setup first, or ensure that the correct\n'
    Msg += 'intensities are being played externally.\n'
    Msg += '=================================================================\n'
    return(Msg)


def Normalize(Data, AmpFFile, Mode=''):
    try:
        AmpF = IO.Txt.Read(AmpFFile)
    except FileNotFoundError as e:
        raise FileNotFoundError(NoCalibrationMsg(AmpFFile))

    if Mode.lower() == 'in': Data *= AmpF['InAmpF']
    elif Mode.lower() == 'out': Data *= AmpF['OutAmpF']
    else: print('"Mode" should be "in" or "out"'); return(None)

    return(Data)


# Level 2
def GetSoundRec(Path, IsAll=True):
    SoundRec = IO.Bin.Read(Path)[0]

    if IsAll:
        SoundRec = {
            F: {A.replace('_', '.'): AmpF for A, AmpF in Freq.items()}
            for F, Freq in SoundRec.items()
        }
    else:
        SoundRec = {
            A.replace('_', '.'): AmpF for A, AmpF in SoundRec.items()
        }

    return(SoundRec)


# Level 3
def dBToAmpF(Intensities, CalibrationPath):
    print('Converting dB to AmpF...')
    SoundIntensity = IO.Bin.Read(f"{CalibrationPath}/SoundIntensity")[0]
    SoundIntensity['dB'] = SoundIntensity['dB'][:-1,:]
    SoundIntensity['AmpFs'] = SoundIntensity['AmpFs'][:-1]


    SoundAmpF = {
        Freq: [
            float(min(SoundIntensity['AmpFs'],
                      key=lambda i:
                          abs(SoundIntensity['dB'][SoundIntensity['AmpFs'].tolist().index(i),F]-dB)
            ))
            for dB in Intensities
        ]
        for F,Freq in enumerate(SoundIntensity['Freqs'])
    }

    return(SoundAmpF)

