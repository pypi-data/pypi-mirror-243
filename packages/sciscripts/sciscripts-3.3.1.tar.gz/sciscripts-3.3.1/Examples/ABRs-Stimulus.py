#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@year: 20210516
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

Example script for running Auditory Brainstem Responses test (ABRs), which is
an electrophysiological measurement of hearing.

For more info about the parameters and functions, see the
`Examples/SoundAndLaserStimulation.py` script. This is a copy of that script
with parameters adjusted for ABRs.

This script does NOT handle data recording, only stimulus. SciScripts will
provide:
    - Sound stimulus through the sound card output 1;
    - Sound timestamp markers through the sound card output 2;
    - Recording toggle TTLs through arduino serial communication;
    - An InfoFile with all stimulus information.

Based on this, you are expected to setup a recording apparatus for the
experiment, for example:
    - Computer with a sound card having at least 2 outputs;
    - Sound amplifier and Loudspeaker;
    - Arduino Uno running `SciScriptsUno.ino`;
    - Open-ephys DAQ with:
        - a RecordControl module listening to TTL Ch 4 as edge;
        - a Record module set to record only channel 1 and ADCs 1 and 2;
    - Intan RHD headstage with an A16-OM16 adaptor;
    - 2 Silver wire electrodes.

    1. The Arduino and Open-ephys connects to the computer;
    2. The sound card output 1 connects to a splitter;
        2.1. One side of the splitter connects to the sound amplifier;
        2.2. The other side connects to the Open-ephys analog input 1;
    3. The loudspeaker connects to the sound amplifier;
    4. The sound card output 2 connects to Open-ephys analog input 2;
    5. The 8 digital pins set at `SciScriptsUno.ino` connects to the 8 Open-ephys digital inputs;
    6. The Intan headstage with the adaptor connects to the Open-ephys;
    7. The silver electrodes connects to the A16-OM16 channel 1 and reference;
    8. A ground wire connects to the A16-OM16 ground.
"""

print('[SoundAndLaserStimulation] Loading dependencies...')
from sciscripts.Exps import SoundAndLaserStimulation
print('[SoundAndLaserStimulation] Done.')


#%% Prepare ABR stimulation
Parameters = dict(
    # === General === #
    AnimalName    = 'Test_01',                              # Animal name
    CageName      = 'A1',                                   # Animal label in its cage
    StimType      = ['Sound'],                              # Type of stimulation


    # === Sound === #
    SoundType                   = 'Noise',                  # Type of sound stimulus ('Noise' or 'Tone')
    Intensities                 = list(range(80,40,-5)),    # Stimulus intensities in dB
    SoundPulseNo                = 21**2,                    # Number of sound pulses
    SoundPauseBeforePulseDur    = 0.004,                    # Duration of pause before each pulse
    SoundPulseDur               = 0.003,                    # Duration of each pulse
    SoundPauseAfterPulseDur     = 0.093,                    # Duration of pause after each pulse
    PauseBetweenIntensities     = 10,                       # Duration of pause between each intensity
    NoiseFrequency              = [                         # Stimulus frequency ranges in Hz
        [8000, 10000],
        [9000, 11000],
        [10000, 12000],
        [12000, 14000],
        [14000, 16000]
    ],


    # === Hardware === #
    System    = 'Jack-IntelOut-Marantz-IntelIn',            # System name as given during calibration
    Setup     = 'UnitRec',                                  # Setup name as given during calibration


    # === Extra === #
    RecCh     = [1],
    StimCh    = 2,
    TTLCh     = 3,
)

Stimulation, InfoFile = SoundAndLaserStimulation.Prepare(**Parameters)


#%% Run
SoundAndLaserStimulation.Play(Stimulation, InfoFile, ['Sound'], DV='Out')


#%% Check out the played stimulus
import numpy as np
from sciscripts.Analysis.Plot import Plot

Rate = Stimulation['Stim'].samplerate
Time = np.arange(Stimulation['Sound'].shape[0])/Rate
Ax = {'xlabel': 'Time [s]', 'ylabel': 'Channel #'}
Colors = ['b', 'k']

# This will plot the TTL and sound channels at the first intensity
Ax['title'] = 'Sound'
Plot.AllCh(Stimulation['Sound'][:,:,0,0], Time, Colors, AxArgs=Ax)


