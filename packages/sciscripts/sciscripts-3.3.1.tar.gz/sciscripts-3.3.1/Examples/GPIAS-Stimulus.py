#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20210516
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

Example script for running Gap Prepulse Inhibition of Acoustic Startle test
(GPIAS; Turner et al., 2006). This test is used as an objective measurement
of tinnitus-like behaviour in rodents.

This script does NOT handle data recording, only stimulus. SciScripts will
provide:
    - Sound stimulus through the sound card output 2;
    - Sound timestamp markers through the sound card output 1;
    - Recording toggle TTLs through arduino serial communication;
    - An InfoFile with all stimulus information.

Based on this, you are expected to setup a recording apparatus for the
experiment, for example:
    - Computer with a sound card having at least 2 outputs;
    - Sound amplifier and Loudspeaker;
    - Arduino Uno running `SciScriptsUno.ino`;
    - Open-ephys DAQ with:
        - a RecordControl module listening to TTL Ch 4 as edge;
        - a Record module set to record only ADCs 1, 2 and 8;
    - Vibration sensor (piezo, accelerometer, etc).

    1. The Arduino and Open-ephys connects to the computer;
    2. The sound card output 1 connects to Open-ephys analog input 1;
    3. The sound card output 2 connects to a splitter;
        3.1. One side of the splitter connects to the sound amplifier;
        3.2. The other side connects to the Open-ephys analog input 2;
    4. The loudspeaker connects to the sound amplifier;
    5. The 8 digital pins set at `SciScriptsUno.ino` connects to the 8 Open-ephys digital inputs;
    6. The vibration sensor output connects to the Open-ephys analog input 8.
"""

print('[GPIASRec] Loading dependencies...')
from sciscripts.Exps import GPIAS
print('[GPIASRec] Done.')


#%% GPIAS
"""
The Parameters dictionary will contain all the parameters for running the
experiment. All parameters are required, except the ones under `Extra`.

Besides the required parameters, you can use this dictionary to record any
information you want about the experiment, since any variable you add to it
will be recorded to the InfoFile. As example, here the parameters RecCh,
StimCh and TTLCh are included to make it easier later in the analysis to
know what recorded channels contains sensor data (RecCh), the played stimulus
(StimCh) or the stimulation timestamps (TTLCh). The InfoFile will be written
to $DATAPATH/ under the format `%Y%m%d%H%M%S-AnimalName-GPIAS.dict`, for example
`~/Data/20210125151000-Test_01-GPIAS.dict`.

Since each trial is composed by 1 startle stimulus and 1 gap-startle stimulus,
the number of stimuli played will be 2*NoOfTrials for each frequency tested.

All durations (parameters ending with Dur) are in seconds; and
all intensities (parameters ending with Intensity) are in dB.
"""

Parameters = dict(
    # === General === #
    AnimalName  = 'Test_01',    # Animal name
    CageName = 'B2',            # Animal label in its cage
    StimType    = ['Sound'],    # Type of stimulation
    NoOfTrials  = 9,            # Number of trials per frequency tested


    # === Sound === #
    GapIntensity            = [0],         # Gap intensity
    BGIntensity             = [60],        # Background noise intensity
    PulseIntensity          = [105],       # Startle pulse intensity
    SoundBGDur              = 2.3,         # Duration of noise before gap
    SoundGapDur             = 0.04,        # Duration of gap
    SoundBGPrePulseDur      = 0.1,         # Duration of noise between gap and startle pulse
    SoundLoudPulseDur       = 0.05,        # Duration of startle pulse
    SoundBGAfterPulseDur    = 0.51,        # Duration of noise after startle pulse
    SoundBetweenStimDur     = [10, 20],    # Duration range of noise between trials
    NoiseFrequency          = [            # Stimulus frequency ranges in Hz
        [8000, 10000],
        [9000, 11000],
        [10000, 12000],
        [12000, 14000],
        [14000, 16000],
        [8000, 18000]
    ],


    # === Hardware  === #
    System          = 'Jack-IntelOut-Marantz-IntelIn',    # System name as given during calibration
    Setup           = 'GPIAS',                            # Setup name as given during calibration


    # === Extra === #
    StimCh          = 2,
    TTLCh           = 1,
    RecCh           = [3,4,5],
)

GPIAS.Run(**Parameters)
