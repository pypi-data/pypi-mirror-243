#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@year: 20110516
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

This is a script to analyze GPIAS recordings with stimulation provided
by `sciscripts.Exps.GPIAS`.
"""

print('[GPIASAnalysis] Loading dependencies...')
import numpy as np
import os

from glob import glob
from sciscripts.Analysis import Analysis, GPIAS
from sciscripts.Analysis.Plot import GPIAS as GPIASPlot
from sciscripts.IO import IO
print('[GPIASAnalysis] Done.')


#%% GPIAS analysis
"""
The `ParametersAnalysis dict contains all parameters for running the
GPIAS analysis. For more info, see `GPIAS.Analysis?`. Similarly, the
`ParametersPlot` dict contains parameters for plotting the results.
For more info, see `GPIASPlot.Traces?`.

The variables `Folder` and `InfoFile` are the paths data and to the
auxiliary .dict file, respectively. The .dict file will contain
crucial information for analyzing the experiment, such as the order of
frequency and trials (since they are randomly presented) and the
channels containing data and TTLs.
"""

ParametersAnalysis = dict(
    TimeWindow = [-0.2, 0.2],    # Amount of time around the startle pulse
    SliceSize = 0.1,             # Quantification window for GPIAS index
    FilterFreq = [50],           # Frequency for filter
    FilterOrder = 3,             # Filter order
    FilterType = 'lowpass',      # Filter type
    Filter = 'butter',           # Filter
    BGNormalize = True,          # Toggle to subtract baseline amplitude
    Return = True,               # Toggle to disable returning results

    # Path to save the analysis. If empty, no files will be saved
    Save = f"{os.environ['ANALYSISPATH']}/Path/To/Save/Analysis/Animal1",
)

ParametersPlot = dict(
    Normalize = True,            # Toggle to normalize traces
    Type = 'Index',              # Trace type
    Ext=['svg'],                 # Extension to save plot
    Show = True                  # Toggle to show plot

    # Path to save plots. If empty, no plots will be saved
    Save = f"{os.environ['ANALYSISPATH']}/Path/To/Save/Analysis/Animal1",
)


Folder = f"{os.environ['DATAPATH']}/Path/To/Data/Animal1-GPIAS"
InfoFile = f"{os.environ['DATAPATH']}/Path/To/Data/Animal1.dict"

Data, Rate = IO.DataLoader(Folder, Unit='mV')            # Load data
Proc = list(Data.keys())[0]                              # Select 1st rec processor
DataExp = list(Data[Proc].keys())[0]                     # Select 1st experiment
Data, Rate = Data[Proc][DataExp], Rate[Proc][DataExp]
DataInfo = IO.Txt.Read(InfoFile)                         # Load experiment info

"""
If necessary, information from the .dict file can be overwritten before
running the analysis. As example, if you may want to analyze only some of
your channels, uncomment the next line and set it to the desired
channel(s).
"""
# DataInfo['DAqs']['RecCh'] = [5]


#--- Run the analysis and plot results
GPIASRec, X = GPIAS.Analysis(Data, Rate, DataInfo, **ParametersAnalysis)

ParametersPlot['SoundPulseDur'] = DataInfo['Audio']['SoundLoudPulseDur']
GPIASPlot.Traces(GPIASRec, X, **ParametersPlot)


#--- Get peak samples for each frequency, if needed
Peaks = {
    F: {
        Trial: Analysis.GetPeaks(Freq[Trial], Std=2)['Pos']
        for Trial in ['Gap', 'NoGap']
    }
    for F,Freq in GPIASRec['Trace'].items()
}


#%% Batch
"""
You may want to analyze a group of animals at once, instead of using
the above code one by one. In that case, you can use the code below.

The code below assumes your data is organized as:

    DataFolder
    └── Group1
        └── YYYYmmdd-Group1-GPIAS/
            ├── YYYY-mm-dd_HH-MM-SS_Animal1/
            ├── YYYY-mm-dd_HH-MM-SS_Animal2/
            ├── YYYY-mm-dd_HH-MM-SS_Animal3/
            ├── YYYYmmddHHMMSS-Animal1-GPIAS.dict
            ├── YYYYmmddHHMMSS-Animal2-GPIAS.dict
            └── YYYYmmddHHMMSS-Animal3-GPIAS.dict

Importantly, `DataFolder` should point to the root; and `Group` should
point to the name of the group (in this example tree it should be
`Group1`). Also, the number of folders should always match the number
of .dict files.

Results (Data and plots) will be saved to `AnalysisFolder`, with the
same structure as for the provided data.
"""

ParametersAnalysis = dict(
    TimeWindow = [-0.2, 0.2],    # Amount of time around the startle pulse
    SliceSize = 0.1,             # Quantification window for GPIAS index
    FilterFreq = [50],           # Frequency for filter
    FilterOrder = 3,             # Filter order
    FilterType = 'lowpass',      # Filter type
    Filter = 'butter',           # Filter
    BGNormalize = True,          # Toggle to subtract baseline amplitude
    Return = True,               # Toggle to disable returning results
)

ParametersPlot = dict(
    Normalize = True,            # Toggle to normalize traces
    Type = 'Index',              # Trace type
    Ext=['svg'],                 # Extension to save plot
    Show = False                 # Toggle to show plot
)

DataFolder = f"{os.environ['DATAPATH']}"
AnalysisFolder = f"{os.environ['ANALYSISPATH']}"
Group = 'Group1'

Exps = sorted(glob(f'{DataFolder}/{Group}/*-GPIAS'))
GPIASIndexes = {}

print(f'[GPIAS batch] Running analysis for group {Group}...')
for E,Exp in enumerate(Exps):
    #-- Get all subfolders
    Folders = sorted(glob(Exp + '/' + Exp.split('/')[-1][:4] + '-*'))
    Files = sorted(glob(Exp + '/' + Exp.split('/')[-1][:4] + '*dict'))

    for F, Folder in enumerate(Folders):
        print(f'    Processing folder {F+1} of {len(Folders)}...')

        Data, Rate = IO.DataLoader(Folder, Unit='mV')
        Proc = list(Data.keys())[0]
        DataExp = list(Data[Proc].keys())[0]
        Data, Rate = Data[Proc][DataExp], Rate[Proc][DataExp]

        RecFolder = Folder.split('/')[-1]
        SavePath = Exp.replace(DataFolder, AnalysisFolder)
        SavePath += f"/{Files[F][:-5].split('/')[-1]}-{Group}"
        DataInfo = IO.Txt.Read(Files[F])

        Animal = DataInfo['Animal']['AnimalName']
        if Animal not in GPIASIndexes: GPIASIndexes[Animal] = {}

        GPIASRec, X = GPIAS.Analysis(
            Data, Rate, DataInfo, Save=SavePath, **ParametersAnalysis
        )

        ParametersPlot['SoundPulseDur'] = DataInfo['Audio']['SoundLoudPulseDur']
        GPIASPlot.Traces(GPIASRec, X, Save=SavePath+'/Traces', **ParametersPlot)

        GPIASIndexes[Animal].update({F: Freq['GPIASIndex']
                                     for F, Freq in GPIASRec['Index'].items()})

        del(GPIASRec, X)

print('[GPIAS batch] Done.')


