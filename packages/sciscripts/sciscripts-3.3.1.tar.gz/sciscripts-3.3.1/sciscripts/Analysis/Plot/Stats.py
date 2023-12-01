#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 2022-07-18

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

import os
import numpy as np
from copy import deepcopy as dcp

from sciscripts.Analysis import Analysis
from sciscripts.Analysis import Stats
from sciscripts.Analysis.Plot import Plot
from sciscripts.IO.Bin import MergeDicts

plt = Plot.plt


#%% Level 0 ====================================================================
def LevelsAsTextXPos(Levels, X):
    XPos = [[] for _ in Levels]
    XPos[-1] = X

    iLevels = np.arange(len(Levels))[::-1][1:]
    for L in iLevels:
        Step = len(Levels[L+1])
        XPos[L] = Analysis.MovingAverage(XPos[L+1], n=Step)[::Step]

    return(XPos)



def LevelsAsText(Levels, X, Ax, LevelsSpacing=1, FontDict={}):
    ylim = Ax.get_ylim()
    Step = np.ptp(ylim)*0.03
    xtp = {**dict(va='top',ha='center'), **FontDict}
    Y = min(ylim)-Step
    XPos = LevelsAsTextXPos(Levels, X)
    iLevels = np.arange(len(Levels))[::-1][1:]

    for xi,x in enumerate(XPos[-1]):
        Ax.text(x, Y, Levels[::-1][0][xi%len(Levels[::-1][0])], xtp)

    Y -= (Step*LevelsSpacing)
    LenDone, Start = [len(Levels[-1])], 0
    # for L,Level in enumerate(Levels[::-1][1:]):
    for L in iLevels:
        N = len(Levels[L])
        if N<2: continue

        # for xi,x in enumerate(Analysis.MovingAverage(X)[Start::np.prod(LenDone)]):
        for xi,x in enumerate(XPos[L]):
            Ax.text(x, Y, Levels[L][xi%N], xtp)

        Y -= (Step*LevelsSpacing)
        LenDone.append(N)
        Start = np.prod(LenDone[1:])-1

    Ax.xaxis.set_visible(False)
    Ax.spines['bottom'].set_visible(False)

    return(Ax)



#%% Level 1 ====================================================================
def Overview(
        Data, FXs, FacNames=None, FacOrder=None, LevelsOrder=None,
        LevelsNames=None, StatsResults=None, PlotType='Boxes',
        SigArgs={}, PlotArgs={}, StatsYAmpF=1, LevelsSpacing=1, LevelsFontDict={},
        Colors=None,
        Ax=None, AxArgs={}, File='Overview', Ext=['svg'], Save=False, Show=True
    ):

    # return(FXs)
    if FacNames is None: FacNames = [f'Factor{_+1}' for _ in range(FXs.shape[1])]
    if FacOrder is None: FacOrder = FacNames

    FXsOrder = [FXs[:,np.array(FacNames)==_].ravel() for _ in FacOrder]
    FacUniq = [np.unique(_) for _ in FXsOrder]
    if LevelsOrder is None: LevelsOrder = FacUniq
    if LevelsNames is None: LevelsNames = LevelsOrder

    Bars = np.unique(np.array(FXsOrder).T, axis=0)
    for LR,LevelOrder in enumerate(LevelsOrder[::-1]):
        LI = -LR-1
        Bars = np.vstack([Bars[Bars[:,LI]==L,:] for L in LevelOrder])

    X = np.arange(len(LevelsOrder[-1]))
    for L,Level in enumerate(LevelsOrder[:-1][::-1]):
        X = np.array([X+(l*(X[-1]+L+2)) for l,level in enumerate(Level)]).ravel()

    # ColorsClass = ['b','orange']
    # for B,Box in enumerate(X[::2]):
        # Ax.axvspan(Box-0.9, X[B*2+1]+0.9, facecolor=ColorsClass[B%2], alpha=0.2)


    Fig, Ax, ReturnAx = Plot.FigAx(Ax)#, dict(figsize=Plot.FigSizeA4))

    if Colors is None: Colors = ['k']*len(X)

    if PlotType == 'Scatters' and 'Paired' in PlotArgs and PlotArgs['Paired']:
        FullY = [
            Data[np.prod(
                [FXsOrder[l]==L for l,L in enumerate(Bar)],
                axis=0, dtype=bool
            )]
            for B,Bar in enumerate(Bars)
        ]

        ym = np.array([np.nanmax(_) for _ in FullY])
        PA = {**PlotArgs}
        Plot.ScatterMean(FullY, X, Colors, Colors, Colors, Ax=Ax, **PA)

    elif PlotType == 'ScattersPairedLast':
        FullY = [
            Data[np.prod(
                [FXsOrder[l]==L for l,L in enumerate(Bar)],
                axis=0, dtype=bool
            )]
            for B,Bar in enumerate(Bars)
        ]
        FullY = np.array(FullY, dtype=object)

        N = len(LevelsOrder[-1])
        SubYs = [FullY[B*N:B*N+N].tolist() for B in range(len(Bars)//N)]
        SubXs = [X[B*N:B*N+N] for B in range(len(Bars)//N)]
        SubCs = [Colors[B*N:B*N+N] for B in range(len(Bars)//N)]

        ym = np.array([np.nanmax(_) for _ in FullY])
        for sy,SY in enumerate(SubYs):
            ym[sy*N:sy*N+N] = np.nanmax(SY)

        PA = {**PlotArgs, **{'Paired':True}}

        for SX,SY,SC in zip(SubXs,SubYs,SubCs):
            Plot.ScatterMean(SY, SX, SC, SC, SC, Ax=Ax, **PA)

    else:
        ym = []
        for B,Bar in enumerate(Bars):
            i = np.prod([FXsOrder[l]==L for l,L in enumerate(Bar)], axis=0, dtype=bool)

            if PlotType == 'Boxes':
                PA = {**{'Width':0.5}, **PlotArgs}
                Plot.Boxes([Data[i]], [X[B]], [Colors[B]], [Colors[B]], Ax=Ax, **PA)
                ymax = np.nanmax(Data[i])

            elif PlotType == 'Violins':
                PA = {**{'Width':0.5}, **PlotArgs}
                Plot.Violins([Data[i]], [X[B]], [Colors[B]], [Colors[B]], Ax=Ax, **PA)
                ymax = np.nanmax(Data[i])

            elif PlotType == 'Scatters':
                PA = {**PlotArgs}
                Plot.ScatterMean([Data[i]], [X[B]], [Colors[B]], [Colors[B]], [Colors[B]], Ax=Ax, **PA)
                ymax = np.nanmax(Data[i])

            elif PlotType == 'MeanSEM':
                PA = {
                    'LineArgs': {'marker':'s','lw':1,'color':Colors[B]},
                    'PlotType': 'Markers'
                }

                MergeDicts(PA, dcp(PlotArgs))

                Plot.MeanSEM([Data[i]], [X[B]], Ax=Ax, **PA)
                ymax = np.nanmax(
                    np.nanmean(Data[i]) +
                    (np.nanstd(Data[i])/(len(Data[i])**0.5))
                )
            elif PlotType == 'Bars':
                PA = {
                    'LineArgs': {'lw':1,'color':Colors[B]},
                    'PlotType': 'Bars'
                }

                MergeDicts(PA, dcp(PlotArgs))

                Plot.MeanSEM([Data[i]], [X[B]], Ax=Ax, **PA)
                ymax = np.nanmax(
                    np.nanmean(Data[i]) +
                    (np.nanstd(Data[i])/(len(Data[i])**0.5))
                )
            else:
                return KeyError(f"{PlotType} is not a valid PlotType.")

            ym.append(ymax)

        ym = np.array(ym)


    # Stats
    ylim = Ax.get_ylim()
    Step = (np.ptp(ylim)*0.03)
    SAs = {'TicksDir':'down', 'LineTextSpacing': Step}
    SAs = {**SAs, **SigArgs}
    Step *= StatsYAmpF
    StepC = Step

    if StatsResults is not None:
        for F,Fac in enumerate(FacOrder[::-1]):
            F = -F-1
            AR = StatsResults['PWCs'][Fac]['PWCs']

            kvpk = 'p.adj' if 'p.adj' in AR else 'p'
            fnl = [_ for _ in FacOrder if _ != Fac]
            fi = [list(FacOrder).index(_) for _ in fnl]
            fk = np.array([AR[_] for _ in fnl]).T
            # fk = np.array([AR[_] if _ in AR.keys() else [] for _ in fnl]).T

            for B,Bar in enumerate(fk):
                p = AR[kvpk][B]
                if p < 0.05:
                    i = np.prod([Bars[:,fi[l]]==L for l,L in enumerate(Bar)], axis=0, dtype=bool)
                    pStart = i*(Bars[:,F]==AR['group1'][B])
                    pEnd = i*(Bars[:,F]==AR['group2'][B])
                    if True not in pStart or True not in pEnd: continue
                    # print(pStart, pEnd)

                    ps, pe = (np.where(_)[0][0] for _ in (pStart,pEnd))
                    ps, pe = sorted((ps,pe))
                    pe += 1

                    y = max(ym[ps:pe]) + StepC
                    Plot.SignificanceBar(
                        (X[pStart],X[pEnd]), [y]*2,
                        f"p = {Stats.pFormat(p)}", Ax, **SAs
                    )
                    ym[ps:pe] = y
                    # StepC += Step
                    # print(f"{Fac} Bar {B} | Step {Step} | StepC {StepC} | Y {y}")

        # # Add effect stats
        # Boxes = np.array(tuple(Stats.product(*LevelsNames)))
        # if Eff is not None:
            # pm = (Eff['Effect']=='Gen')*(Eff['Session']=='1')
            # p = Eff['p.adj'][pm][0]

            # if p<0.05:
                # p = Stats.pFormat(p)

                # py = Ax.get_ylim()[-1]
                # px = []
                # for GT in LevelsOrder[0]:
                    # l = X[Boxes[:,0]==GT]
                    # Ax.plot(l, [py]*len(l), 'k')
                    # px.append(np.mean(l))

                # Plot.SignificanceBar(px, [py*1.03]*2, p, Ax, SigArg)

    if 'ylim' in AxArgs:
        Ax.set_ylim((AxArgs['ylim'][0], Ax.get_ylim()[1]))

    Ax = LevelsAsText(LevelsNames, X, Ax, LevelsSpacing, LevelsFontDict)

    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


#%%
