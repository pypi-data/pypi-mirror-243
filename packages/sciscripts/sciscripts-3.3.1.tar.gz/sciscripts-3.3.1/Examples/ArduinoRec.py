#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20220523
@license: GNU GPLv3 <https://gitlab.com/malfatti/LabScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/LabScripts

Record arduino analog channels to file, essentially using an arduino uno as a
DAq. Make sure there is only one arduino connected, and that it is running the
`SciScriptsUno.ino` code.
"""



#%% Arduino recording ==========================================================
import matplotlib.pyplot as plt
import numpy as np

from glob import glob
from sciscripts.Exps import Arduino
from sciscripts.Analysis import Analysis



#%% Experiment parameters ======================================================
Parameters = dict(
    AnimalName = 'Test',

    Channels   = [7,9],
    Rate       = 100,
    Setup      = 'Treadmill',
)



#%% Run ========================================================================
print('Recording from Arduino; press Ctrl+C to stop.')
Arduino.ReadAnalogIn(**Parameters)



#%% Check rec ==================================================================
"""
There should be three files for each recording with the following name format:

1. {YYYYmmddHHMMSS}-{AnimalName}-ArduinoRec_{Samples}x{Channels}.dat
    - Contains the recorded data.

2. {YYYYmmddHHMMSS}-{AnimalName}-ArduinoRec_Time_{Samples}x1.dat
    - Contains the timestamp for each sample

3. {YYYYmmddHHMMSS}-{AnimalName}-ArduinoRec.dict
    - Contains all rec info, including all `Parameters`.
"""

# Get the files for the last recording
Files = sorted(glob('*-Test-ArduinoRec_*'))[-2:]

for File in Files:
    Shape = [int(_) for _ in File.split('.')[0].split('_')[-1].split('x')]
    Array = np.fromfile(File, dtype=float).reshape(Shape)

    if 'Time' in File: Time = Array
    else: Data = Array

Time = Time[:,0]

# Check if requested and recorded sampling rates match
RecRate = int((1/np.diff(Time)).mean())
RateMatch = Parameters['Rate'] == RecRate


# Analysis and plotting example: Filter, normalize and detect positive peaks
# on the last channel
DataFilt = abs(
    Analysis.FilterSignal(
        Data[:,-1], Parameters['Rate'], [1,5], 2
    )
)

DataNorm = Analysis.Normalize(DataFilt)

Peaks = Analysis.GetPeaks(DataNorm)['Pos']

Fig, Axes = plt.subplots(3,1)
Axes[0].plot(Time, DataNorm)
Axes[0].plot(Time[Peaks], DataNorm[Peaks], 'x')
Axes[1].plot(Time, Data[:,0])
Axes[2].plot(Dist/(d/1000))
plt.show()



