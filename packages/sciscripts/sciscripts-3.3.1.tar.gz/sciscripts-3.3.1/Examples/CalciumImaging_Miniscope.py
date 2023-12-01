#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@year: 20230503
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

This is a script to analyze miniscope V3 and V4 videos.
"""

print('[CalciumImaging] Loading dependencies...')
import os
from glob import glob
from sciscripts.Analysis import CalciumImaging
from sciscripts.Analysis.Plot import CalciumImaging as CIPlot
from sciscripts.Analysis.Plot import Plot

plt = Plot.plt # This is exactly the same as `import matplotlib.pyplot as plt`
print('[CalciumImaging] Done.')


#%% Analysis
"""
This will recursively find all folders under `DataPath` containing a
`0.avi` file, get timestamps, motion-correct, extract sources and evaluate
components. Analysis result will be saved at `AnalysisPath` following the same
folder tree as `DataPath`.

In this example, the analysis will be ran with all parameters set at their
defaults. To check these parameters, uncomment the `print` lines after thisc
docstring. All video, motion correction, source extraction and component
evaluation parameters can be edited by providing the respective dicts to the
`CalciumImaging.Full` function (see `CalciumImaging.Full?`). You can add only
the modified parameters, the function will keep the ones you did not change at
their default values.
"""

# print(
#     {K:V for K,V in CalciumImaging.__dict__.items() if 'Params' in K}
# )

DataPath = '/Path/To/Folder/With/Miniscope/Recs'
AnalysisPath = '/Path/To/Save/Analysis'

Exps = sorted(glob(f"{DataPath}/**/0.avi"))
Exps = [os.path.dirname(_) for _ in Exps]

for E,Exp in enumerate(Exps):
    CalciumImaging.Full(Exp, Exp.replace(DataPath, AnalysisPath))


#%% Multiple sessions
"""
In case multiple sessions were recorded from the same animal, neurons can
have their identity assigned through sessions. You can add data from different
animals and groups, as long as the animal names are not the same when they
belong to different groups (it will NOT work if, for example `Group1` and
`Group2` both have an animal named `Animal_01`).

By default, a neuron has to be detected and assigned on every session to be
accepted. To change this behavior, pass the number of sessions neurons have
to be detected to be accepted through the argument `MinSessionsValid`. For
example, suppose you have recorded 4 sessions (as in this example) but it is
enough for your analysis if the neuron is detected on at least 2 of the 4
sessions. To accept neurons that are detected on at least 2 sessions:
    CalciumImaging.MergeRecs(ExpsRes, Info, AnalysisPath, MinSessionsValid=2)

For this example, the output will be written to
f"{AnalysisPath}/Group1/Animal1-Merged".
"""
# Get the results folder for experiments ran with the previous cell
ExpsRes = [
    f"{AnalysisPath}/Group1/20220614-Animal1-Treat1_Trial1/Videos/Result",
    f"{AnalysisPath}/Group1/20220614-Animal1-Treat1_Trial2/Videos/Result",
    f"{AnalysisPath}/Group1/20220614-Animal1-Treat2_Trial1/Videos/Result",
    f"{AnalysisPath}/Group1/20220614-Animal1-Treat3_Trial1/Videos/Result",
]

# Create a dict with info about each of the files
Info = {}
Info['Groups'] = ['Group1']*4
Info['Animals'] = ['Animal1']*4
Info['Sessions'] = [1,1,2,3]
Info['Trials'] = [1,2,1,1]

CalciumImaging.MergeRecs(ExpsRes, Info, AnalysisPath)



#%% Plot traces
"""
Show the full recording for the first `NeuronMax` accepted neurons for each
recording on `ExpsRes`. This cell assumes that analysis results were saved as
flat binary files (`.dat`, default).
"""
NeuronMax = 20

for Exp in ExpsRes:
    Time = IO.Bin.Read(f'{Exp}/Time.dat')[0]
    RawTraces_dF_F = IO.Bin.Read(f'{Exp}/CNMFe/RawTraces_dF_F.dat')[0]
    Accepted = IO.Bin.Read(f'{Exp}/CNMFe/Accepted.dat')[0]
    RawTraces_dF_F = RawTraces_dF_F[:,Accepted]

    Args = dict(xlabel='Time [s]', ylabel='Neuron [#]')
    Plot.AllCh(RawTraces_dF_F[:,:NeuronMax], Time, AxArgs=Args)



#%% Plot traces of the same neuron on different sessions
"""
Show the full recording for the first accepted neuron at each
recording on `ExpsRes` that was successfully merged through multiple sessions.
This cell assumes that analysis results were saved as flat binary files
(`.dat`, default).
"""
# MergeBase = f'{AnalysisPath}/Group1/Animal1-Merged'

Assignments = IO.Bin.Read(f"{MergeBase}/AssignmentsActive.dat")[0]
ASessions = IO.Bin.Read(f"{MergeBase}/Sessions.dat")[0]
ATrials = IO.Bin.Read(f"{MergeBase}/Trials.dat")[0]

Accepted = [
    IO.Bin.Read(f'{Exp}/CNMFe/Accepted.dat')[0]
    for Exp in ExpsRes
]

RawFiles = [
    f'{Exp}/CNMFe/RawTraces_dF_F.dat'
    for Exp in ExpsRes
]

TimeFiles = [
    f'{Exp}/Time.dat'
    for Exp in ExpsRes
]

Assignments = CalciumImaging.AcceptedAssigned(Assignments, Accepted)

if not Assignments.size:
    print(f"No accepted neurons assigned for this animal!")
else:
    Fig, Axes = plt.subplots(len(ASessions), 1, constrained_layout=True)
    for S,Session in enumerate(ASessions):
        Time = IO.Bin.Read(TimeFiles[S])[0]
        RawTraces_dF_F = IO.Bin.Read(RawFiles[S])[0]
        RawTraces_dF_F = RawTraces_dF_F[:,Assignments[0,S]]

        Axes[S].plot(Time, RawTraces_dF_F)
        Axes[S].set_title(f'Session {Session}, trial {ATrials[S]}')
        Axes[S].set_ylabel('Amp. [$\Delta$F/F]')

    Axes[-1].set_xlabel('Time [s]')
    for Ax in Axes: Plot.Set(Ax=Ax)
    plt.show()



#%% Plot spatial footprints and active neurons
"""
Show SFPs for all sessions of an animal. This cell assumes that every rec on
`ExpsRes` are from the same animal (`Animal1` in this example); and that
analysis results were saved as flat binary files (`.dat`, default).
"""
MergeBase = f'{AnalysisPath}/Group1/Animal1-Merged'

SFPsList = [IO.Bin.Read(f'{_}/CNMFe/SFP', AsMMap=False)[0] for _ in ExpsRes]
Dims = IO.Bin.Read(f'{MergeBase}/SFPDims.dat')[0].tolist()
CoMActive = IO.Bin.Read(f'{MergeBase}/CoMActive.dat')[0]

CIPlot.SFPs(SFPs, Dims, CoMActive)


