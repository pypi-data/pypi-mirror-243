#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20170707

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

import os
import numpy as np

from sciscripts.Analysis import Analysis
from sciscripts.Analysis.Plot import Plot
plt = Plot.plt


## Level 0
def Single(ABR, X, AllCh=False, Peaks={}, StimWindow=[],
           Ax=None, AxArgs={}, File='ABRs-SingleIntensity', Ext=['svg'], Save=False, Show=True):
    Fig, Ax, ReturnAx = Plot.FigAx(Ax)

    BestCh = Analysis.GetStrongestCh(ABR)

    if AllCh:
        for Ch in range(ABR.shape[1]): Ax.plot(X, ABR[:,Ch], lw=2, label=str(Ch))
    else:
        Ax.plot(X, ABR[:,BestCh], 'k', lw=2, label=str(BestCh))

    if len(StimWindow):
        SW = (X>=StimWindow[0])*(X<=StimWindow[1])
        if True in SW:
            Y = [max(ABR[:,BestCh])*1.2]*X[SW].shape[0]
            Ax.plot(X[SW], Y, 'r', lw=2, label='Sound')

    if len(Peaks):
        Ax.plot(X[Peaks['Pos']], ABR[Peaks['Pos'],BestCh], 'r*', label='Peaks')
        Ax.plot(X[Peaks['Neg']], ABR[Peaks['Neg'],BestCh], 'r*')
        Ax.legend(loc='best')

    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def Multiple(ABRs, X, SpaceAmpF=1, StimDur=None, StimLabel='Sound', Peaks=[], PeaksColors=[], Colormap=[], LegendArgs={},
             Ax=None, AxArgs={}, File='ABRs-SingleFrequency', Ext=['svg'], Save=False, Show=True):
    Fig, Ax, ReturnAx = Plot.FigAx(Ax)

    Rev = False if '0' in ABRs else True
    Recs = sorted(ABRs.keys(), key=lambda x: int(x), reverse=Rev)

    if ABRs[Recs[0]].shape[1] > 1:
        Chs = ABRs[Recs[0]].copy()
        for M, Max in enumerate(abs(Chs).max(axis=0)): Chs[:,M] /= Max
        for Ch in range(Chs.shape[1]):
            Chs[:,Ch] = abs(np.mean(
                Chs[np.where((X>=0)*(X<1))[0],Ch]/
                Chs[np.where((X>=-1)*(X<0))[0],Ch]
            ))
        Chs = [Chs[0,:].argmax()]
        # Chs = Analysis.GetStrongestCh(ABRs[Recs[0]][np.where((X>=0)*(X<3)),:])
        # Chs = [Chs]

        ABRs = {K: V[:,Chs].reshape((V[:,Chs].shape[0], len(Chs)))
                for K,V in ABRs.items()}
    else:
        Chs = [0]

    # ABRs = {K: V/ABRs[Recs[0]][:,0].max() for K,V in ABRs.items()}
    Spaces = Plot.GetSpaces(ABRs, Recs)
    if not PeaksColors: PeaksColors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    if not Colormap:
        Colormap = plt.get_cmap('Reds')

    YTicks = np.zeros(len(Recs))
    for Ch in range(len(Chs)):
        for R,Rec in enumerate(Recs):
            Color = Colormap(255-(R*20))
            Y = ABRs[Rec][:,Ch] + Spaces[R]*SpaceAmpF
            Ax.plot(X, Y, color=Color)#, label=Rec)

            if not Ch: YTicks[-(R+1)] = Y.mean()

            if len(Peaks):
                if R >=len(Peaks): continue
                # Ax.plot(X[Peaks[R]], Y[Peaks[R]], 'k*')
                for p,P in enumerate(Peaks[R]):
                    # print(P)
                    if P == -1: continue
                    if p >= len(PeaksColors): continue
                    Ax.plot(X[P], Y[P], color=PeaksColors[p], marker='*', lw=0, zorder=-1)

            del(Y)

    Y = Ax.get_ylim()
    if StimDur:
        # Ax.plot([X[X>=0][0], X[X<=StimDur*1000][-1]], [max(Y)*1.2]*2, 'k', lw=3)
        Ax.axvspan(X[X>= 0][0], X[X <= StimDur*1000][-1], color='k', alpha=0.3, lw=0, label=StimLabel, zorder=-1)
        # FontDict = {'size':8, 'ha':'center', 'va':'bottom'}
        # Ax.text(np.mean([X[X>=0][0], X[X<=StimDur*1000][-1]]), max(Y)*1.2, 'Sound pulse', fontdict=FontDict)

    Ax.tick_params(left=False)
    Ax.spines['left'].set_visible(False)

    YLabels = np.flipud([_[:-2] if _[:-2].lower() == 'db' else _ for _ in Recs])

    AA = dict(
        xtickspacing = round((X[-1]-X[0])/5),
        yticks = YTicks,
        yticklabels = YLabels,
        xlim = [round(X[0],2), round(X[-1])],
        xlabel = 'Time [ms]',
        ylabel = 'Intensity [dB]'
    )

    AA = {**AA, **AxArgs}
    Ax.set_xlabel(AA['xlabel'])
    Ax.set_xlim(AA['xlim'])
    Ax.set_ylabel(AA['ylabel'])
    Ax.set_yticklabels(AA['yticklabels'])
    Ax.set_yticks(AA['yticks'])

    LA = {**dict(
        bbox_to_anchor=(0.4,1.2), loc='upper left', frameon=False
    ), **LegendArgs}
    Ax.legend(**LA)

    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AA, File, Ext, Save, Show)
    return(Result)


def Multiple3D(ABRs, X, UpsampleFreq=5, Azimuth=-70, Elevation=30, Colormap='inferno',
               Ax=None, AxArgs={}, File='ABRs3D-SingleFrequency', Ext=['svg'], Save=False, Show=True):
    Fig, Ax, ReturnAx = Plot.FigAx(Ax, {'subplot_kw': dict(projection='3d')})

    Intensities = sorted(ABRs.keys(), key=lambda x: int(x), reverse=True)
    ThisABRs = np.array([ABRs[_].ravel() for _ in Intensities]).T
    ABRUp, TUp, IntUp = Analysis.Upsample2d(ThisABRs, X, np.array(Intensities).astype(int), UpsampleFreq)
    ABRUp, TUp = ABRUp[::UpsampleFreq,:], TUp[::UpsampleFreq]

    AA = dict(xlabel='Time [ms]', ylabel='Intensity [dB]', zlabel='Voltage [µv]')
    AA = {**AA, **AxArgs}

    Ax = Plot.Triang3D(ABRUp, TUp, IntUp, Azimuth, Elevation, Colormap, Ax=Ax)
    Ax.set_xlabel(AA['xlabel'])
    Ax.set_ylabel(AA['ylabel'])
    Ax.set_zlabel(AA['zlabel'])

    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def MultipleSxx(ABRs, X, UpsampleFreq=5, Colormap='inferno',
               Ax=None, AxArgs={}, File='ABRsSxx-SingleFrequency', Ext=['svg'], Save=False, Show=True):
    Fig, Ax, ReturnAx = Plot.FigAx(Ax)

    Intensities = sorted(ABRs.keys(), key=lambda x: int(x), reverse=True)
    ThisABRs = np.array([ABRs[_].ravel() for _ in Intensities]).T
    ABRUp, TUp, IntUp = Analysis.Upsample2d(ThisABRs, X, np.array(Intensities).astype(int), UpsampleFreq)
    ABRUp, TUp = ABRUp[::UpsampleFreq,:], TUp[::UpsampleFreq]

    AA = dict(xlabel='Time [ms]', ylabel='Intensity [dB]', zlabel='Voltage [µv]')
    AA = {**AA, **AxArgs}

    Ax.pcolormesh(TUp, IntUp, ABRUp.T, cmap=Colormap, shading='gouraud')
    Ax.set_xlabel(AA['xlabel'])
    Ax.set_ylabel(AA['ylabel'])
    # Ax.set_zlabel(AA['zlabel'])

    Result = Plot.SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def LatencyPerFreq(Latencies, Intensities,
                   Ax=None, AxArgs={}, File='ABRs-LatencyPerFreq', Ext=['svg'], Save=False, Show=True):
    ReturnAx = True
    if not Ax:
        ReturnAx = False
        Fig, Ax = plt.subplots(figsize=(4,2))

    Colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']

    Freqs = sorted(list(Latencies.keys()), key=lambda x: [int(y) for y in x.split('-')])
    SmallFreqs = [_.split('-')[0][:-3]+'-'+_.split('-')[1][:-3] for _ in Freqs]
    Min = min([min(_) for _ in Latencies.values()])
    Min = round((Min-0.25) * 2) / 2
    Max = max([max(_) for _ in Latencies.values()])
    Max = round((Max+0.25) * 2) / 2
    if 'ylim' not in AxArgs: AxArgs['ylim'] = [Min, Max]

    for F, Freq in enumerate(Freqs):
        Ax.plot(Intensities, Latencies[Freq], Colors[F]+'.-', label=SmallFreqs[F])

    Ax.set_xlim([Intensities[0], Intensities[-1]])
    # Ax = Plot.FitLegendOutside(Ax)
    Ax.legend(loc='upper left', ncol=2, bbox_to_anchor=(0, 1.3))

    if ReturnAx:
        Plot.Set(Ax=Ax, AxArgs=AxArgs)
        return(Ax)
    else:
        Plot.Set(Ax=Ax, Fig=Fig, AxArgs=AxArgs)
        if Save:
            if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
            for E in Ext: Fig.savefig(File+'.'+E, format=E, dpi=300)#, bbox_extra_artists=(Ax.get_legend(),), bbox_inches='tight')

        if Show: plt.show()
        else: plt.close()
        return(None)


def ThresholdsPerFreq(Thresholds, Freqs,
                      Ax=None, AxArgs={}, File='ABRs-TresholdsPerFreq', Ext=['svg'], Save=False, Show=True):
    ReturnAx = True
    if not Ax:
        ReturnAx = False
        Fig, Ax = plt.subplots(figsize=(4,2))

    Pos = list(range(1,len(Freqs)+1))
    BoxPlot = Ax.boxplot(Thresholds, positions=Pos, showmeans=True)
    for K in ['boxes', 'whiskers', 'caps', 'medians', 'fliers']:
        for I in range(len(Thresholds)):
            BoxPlot[K][I].set(color='k')

    AxArgs['xticks'] = Pos
    AxArgs['xlim'] = [Pos[0]-0.5, Pos[-1]+0.5]
    AxArgs['xticklabels'] = Freqs
    AxArgs['yticks'] = [30, 40, 50, 60, 70, 80]
    AxArgs['ylim'] = [AxArgs['yticks'][0], AxArgs['yticks'][-1]]

    if ReturnAx:
        Plot.Set(Ax=Ax, AxArgs=AxArgs)
        return(Ax)
    else:
        Plot.Set(Ax=Ax, Fig=Fig, AxArgs=AxArgs)
        if Save:
            if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
            for E in Ext: Fig.savefig(File+'.'+E, format=E, dpi=300)#, bbox_extra_artists=(Ax.get_legend(),), bbox_inches='tight')

        if Show: plt.show()
        else: plt.close()
        return(None)


## Level 1
def Traces_LatencyPerFreq_AllFreqs(
        ABRs, X, Latencies, Intensities, Thresholds, Freqs, SpaceAmpF=1.5, StimDur=None, Peaks=None,
        File='ABRs-Traces_LatencyPerFreq_AllFreqs', Ext=['svg'], Save=False, Show=True
    ):

    Fig = plt.figure(figsize=(7.086614, 3.5), dpi=200)
    Axes = [plt.subplot2grid((2, 2), (0, 0), rowspan=2),
            plt.subplot2grid((2, 2), (0, 1)),
            plt.subplot2grid((2, 2), (1, 1))]

    YLabel = ['Intensity [dB]', 'Latency [ms]', 'Threshold [dB]']
    XLabel = ['Time [ms]', 'Intensity [dB]', 'Frequency [kHz]']
    AxArgs = [{'xlabel': XLabel[A], 'ylabel': YLabel[A]} for A in range(len(Axes))]

    Axes[0] = Multiple(ABRs, X, SpaceAmpF, StimDur, Peaks, Axes[0], AxArgs[0], Save=False, Show=False)
    Axes[1] = LatencyPerFreq(Latencies, Intensities, Axes[1], AxArgs[1], Save=False, Show=False)
    Axes[2] = ThresholdsPerFreq(Thresholds, Freqs, Axes[2], AxArgs[2], Save=False, Show=False)

    plt.figtext(0.0, 0.95, 'A', fontsize=14)
    plt.figtext(0.5, 0.95, 'B', fontsize=14)
    plt.figtext(0.5, 0.5, 'C', fontsize=14)

    Plot.Set(Fig=Fig)
    Fig.subplots_adjust(wspace=0.3, hspace=0.7)

    if Save:
        if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
        for E in Ext: Fig.savefig(File+'.'+E, format=E, dpi=300)#, bbox_extra_artists=(Axes[1].get_legend(),), bbox_inches='tight')

    if Show: plt.show()
    else: plt.close()
    return(None)

