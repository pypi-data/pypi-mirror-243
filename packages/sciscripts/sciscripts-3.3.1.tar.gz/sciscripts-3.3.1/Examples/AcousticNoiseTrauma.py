#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20171004
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

#%% Acoustic trauma
from sciscripts.Exps import AcousticNoiseTrauma

## === Experiment parameters === ##

Parameters = dict(
    AnimalName      = 'Mouse',
    StimType        = ['Sound'],

    Intensities     = [90],
    NoiseFrequency  = [[9000, 11000]],
    SoundPulseDur   = 60,                 # in MINUTES!

    ## === Hardware === ##
    System  = 'Jack-IntelOut-Marantz-IntelIn',
    Setup   = 'ANT',
)

AcousticNoiseTrauma.Run(**Parameters)
