#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20230503

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

import os
import numpy as np

from sciscripts.Analysis.Plot import Plot
plt = Plot.plt


## Level 0
# RawBase = f'{AnalysisPath}/Test/20220614-TreadmillSound_01-Treadmill'
# MergeBase = f'{AnalysisPath}/Test/TreadmillSound_01-Merged'
# AFiles = sorted(glob(f'{RawBase}/*/*/Result'))
# SFPsList = [IO.Bin.Read(f'{_}/CNMFe/SFP', AsMMap=False)[0] for _ in AFiles]
# Dims = IO.Bin.Read(f'{MergeBase}/SFPDims.dat')[0].tolist()
# CoMActive = IO.Bin.Read(f'{MergeBase}/CoMActive.dat')[0]

def SFP(
        SFP, Dim, CoMActive=[],
        Ax=None, AxArgs={}, File='SFP', Ext=['svg'], Save=False, Show=True
    ):
    Fig, Ax, ReturnAx = Plot.FigAx(Ax)

    e = SFP.toarray().reshape(Dim+[SFP.shape[1]], order='F').max(axis=2)
    Ax.imshow(e)

    if len(CoMActive)!=0:
        Ax.plot(CoMActive[:,1], CoMActive[:,0], 'r.', markersize=2)

    Ax.axis('off')

    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)



#%% Level 1
def SFPs(
        SFPsList, Dims, CoMActive=[], MaxColNo=4,
        File='SFP', Ext=['svg'], Save=False, Show=True
    ):
    LineNo = len(Dims)//MaxColNo
    if len(Dims)%MaxColNo: LineNo += 1
    ColNo = MaxColNo if len(Dims)>=MaxColNo else len(Dims)

    Fig, Axes = plt.subplots(
        LineNo, ColNo, figsize=(6.3, 2*LineNo), squeeze=False,
        constrained_layout=True
    )

    for s,S in enumerate(SFPsList):
        l = s//MaxColNo
        c = s%MaxColNo
        Axes[l,c] = SFP(S, Dims[s], CoMActive, Axes[l,c])
        Axes[l,c].set_title(f'Rec {s}')

        if len(CoMActive)!=0:
            Axes[l,c].plot(CoMActive[:,1], CoMActive[:,0], 'r.', markersize=2)

    Result = Plot.SaveShow(False, Fig, Axes[0,0], {}, File, Ext, Save, Show)
    return(Result)


