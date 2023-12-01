#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20170612

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

ScriptName = 'Analysis.Plot.Plot'
print(f'[{ScriptName}] Loading dependencies...')
import inspect, os
import numpy as np
from copy import deepcopy as dcp
from itertools import accumulate#, combinations
from subprocess import check_output

from matplotlib import pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap, to_rgba
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Patch, Rectangle
from matplotlib.tri import Triangulation
# from matplotlib.animation import FuncAnimation as Animation
# from matplotlib.gridspec import GridSpec
# from matplotlib.gridspec import GridSpecFromSubplotSpec
# from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# from mpl_toolkits.mplot3d.axes3d import Axes3D

from sciscripts.Analysis.Analysis import EucDist, Pairwise, StrRange
from sciscripts.IO.Bin import MergeDicts
print(f'[{ScriptName}] Done.')



#%% Level 0
def BarAutolabel(Bars, Ax, Color='k', Position='bottom'):
    """
    Modified from http://matplotlib.org/examples/api/barchart_demo.html
    Attach a text label above each bar displaying its height.
    """

    for Bar in Bars:
        Height = Bar.get_height()
        Ax.text(Bar.get_x() + Bar.get_width()/2.,
                Height,# * Space,
                str(Height),
                color=Color,
                ha='center',
                va=Position)

    return(Ax)


def ClickCallback(Event):
    """ Taken and modified from Joe Kington's code.
        Source at https://stackoverflow.com/a/27566966 """

    FN = inspect.stack()[0][3]

    global X, Y
    # X, Y = None, None
    while X == Y == None:
        print(f'[{ScriptName}.{FN}] Click on the speaker position.')
        if Event.inaxes is not None:
            print(Event.xdata, Event.ydata)
            X, Y = Event.inaxes.transData.inverted().transform((Event.x, Event.y))
        else:
            print(f'[{ScriptName}.{FN}] Clicked coordinate is ouside axes limits')

    plt.close()
    return(None)


def ColorMix(ColorA, ColorB):
    if max(ColorA)==0: Mix = np.array(ColorB)/2
    elif max(ColorB)==0: Mix = np.array(ColorA)/2
    else: Mix = np.array(ColorA)+np.array(ColorB)

    if max(Mix) > 1: Mix /= max(Mix)
    if max(Mix) == 1: Mix *= 0.85
    return(Mix)


def FitLegendOutside(Ax, Width=0.8, Loc='center left', Frame=False):
    # Shrink axis and fit legend outside plot
    # Taken from IanS at https://stackoverflow.com/a/4701285
    Box = Ax.get_position()
    Ax.set_position([Box.x0, Box.y0, Box.width * Width, Box.height])
    Ax.legend(loc=Loc, bbox_to_anchor=(1, 0.5), frameon=Frame)

    return(Ax)


def GetScreenInfo():
    FN = inspect.stack()[0][3]

    Screen = {}
    try:
        Screen['DPI'] = check_output(['xdpyinfo'])
        Screen['DPI'] = str(Screen['DPI']).split('screen #')[1:]
        Screen['DPI'] = [_.split('resolution')[1].split('\\n')[0].split('x')[0].split(' ')[-1] for _ in Screen['DPI']]
        Screen['DPI'] = [int(_) for _ in Screen['DPI']]
    except:
        print(f'[{ScriptName}.{FN}] xdpyinfo not available. Assuming a 96 dpi screen.')
        Screen['DPI'] = [96]

    try:
        Size = check_output(['xrandr'])
        Size = [l for l in str(Size).split('\\n') if ' connected' in l]
        Screen['Size_mm'] = [[int(_[:-2]) for _ in f.split(' ') if 'mm' in _] for f in Size ]
        Screen['Size_px'] = [_.split('+')[0].split('x') for f in Size for _ in f.split(' ') if 'x' in _ and '+' in _]
        Screen['Size_px'] = [[int(_) for _ in s] for s in Screen['Size_px']]
    except:
        print(f'[{ScriptName}.{FN}] xrandr not available. Assuming a 15.6" full HD screen.')
        Screen['Size_mm'] = [[344, 193]]
        Screen['Size_px'] = [[1920, 1080]]

    if len(np.unique([
        len(Screen['DPI']),
        len(Screen['Size_mm']),
        len(Screen['Size_px'])
    ])) > 1:
        # In case only one of xdpyinfo or xrandr are available, and the system
        # has more than one screen, use only info about the first screen.
        Screen['DPI'] = [Screen['DPI'][0]]
        Screen['Size_mm'] = [Screen['Size_mm'][0]]
        Screen['Size_px'] = [Screen['Size_px'][0]]

    ScreenNo = len(Screen['DPI'])
    Screen['Size_in'] = [[_*0.03937008 for _ in s] for s in Screen['Size_mm']]
    Screen['RealDPI'] = [round(Screen['Size_px'][_][0]/Screen['Size_in'][_][0]) for _ in range(ScreenNo)]

    return(Screen)


def GetSpaces(Data, KeyList=None):
    """
        Calculate offsets for plotting all channels in the same plot without overlap.

        Parameters:
            Data: array_like or dict
                If array_like, Data must be a 2D array, with dimensions (samples, channels).
                If dict, Data must be shaped as {Channel: Samples}.

            KeyList: list or None, optional
                List of keys if Data is a dict. If None, Data keys should be int or int() convertable, and KeyList will be  a list of the sorted keys.
                Ignored if Data is array_like.

        Returns:
            Spaces: list
                The offset for each channel to be plot without overlap.
    """
    if type(Data) in [list, np.ndarray, np.memmap]:
        Spaces = [min(Data[:,P[0]])-max(Data[:,P[1]]) for P in Pairwise(range(Data.shape[1]))]

    elif type(Data) == dict:
        if not KeyList: KeyList = sorted(Data.keys(), key=lambda x: int(x))
        Spaces = [min(Data[P[0]])-max(Data[P[1]]) for P in Pairwise(KeyList)]

    else:
        raise TypeError(f'Not sure what to do with data of type {type(Data)}')

    Spaces = [0]+list(accumulate(Spaces))

    return(Spaces)


def GetTicks(Ax, Lim):
    # Override automatic tick formatter
    Step = round((Ax.get_yticks()[1]-Ax.get_yticks()[0])-0.5)
    print(Lim); print(Step)
    Ticks = np.arange(min(Lim), max(Lim)+Step, Step)

    return(Ticks)


def InchToPoint(Size_in): return(Size_in*72)


def InchToRealSize(Size_in, ScreenDPI=96, RealDPI=142):
    Size = Size_in*RealDPI/ScreenDPI
    return(Size)


def LegendVertical(Ax, Rotation=90, XPad=0, YPad=0, **LegendArgs):
    if Rotation not in (90,270):
        raise NotImplementedError('Rotation must be 90 or 270.')

    # Extra spacing between labels is needed to fit the rotated labels;
    # and since the frame will not adjust to the rotated labels, it is
    # disabled by default
    DefaultLoc = 'center left' if Rotation==90 else 'center right'
    ArgsDefaults = dict(loc=DefaultLoc, labelspacing=4, frameon=False)
    Args = {**ArgsDefaults, **LegendArgs}

    Handles, Labels = Ax.get_legend_handles_labels()
    if Rotation==90:
        # Reverse entries
        Handles, Labels = (reversed(_) for _ in (Handles, Labels))
    AxLeg = Ax.legend(Handles, Labels, **Args)

    LegTexts = AxLeg.get_texts()
    LegHandles = AxLeg.legend_handles

    for L,Leg in enumerate(LegHandles):
        if type(Leg) == Rectangle:
            BBounds = np.ravel(Leg.get_bbox())
            BBounds[2:] = BBounds[2:][::-1]
            Leg.set_bounds(BBounds)

            LegPos = (
                # Ideally,
                #    `(BBounds[0]+(BBounds[2]/2)) - AxLeg.handletextpad`
                # should be at the horizontal center of the legend patch,
                # but for some reason it is not. Therefore the user will
                # need to specify some padding.
                (BBounds[0]+(BBounds[2]/2)) - AxLeg.handletextpad + XPad,

                # Similarly, `(BBounds[1]+BBounds[3])` should be at the vertical
                # top of the legend patch, but it is not.
                (BBounds[1]+BBounds[3])+YPad
            )

        elif type(Leg) == Line2D:
            LegXY = Leg.get_xydata()[:,::-1]
            Leg.set_data(*(LegXY[:,_] for _ in (0,1)))

            LegPos = (
                LegXY[0,0] - AxLeg.handletextpad + XPad,
                max(LegXY[:,1]) + YPad
            )

        elif type(Leg) == PathCollection:
            LegPos = (
                Leg.get_offsets()[0][0] + XPad,
                Leg.get_offsets()[0][1] + YPad,
            )
        else:
            raise NotImplementedError('Legends should contain Rectangle, Line2D or PathCollection.')

        PText = LegTexts[L]
        PText.set_verticalalignment('bottom')
        PText.set_rotation(Rotation)
        PText.set_x(LegPos[0])
        PText.set_y(LegPos[1])

    return(None)


def SameScale(Axes, Axis):
    if Axis.lower() == 'x':
        Lim = [f(Ax.get_xlim()) for f in (min,max) for Ax in Axes]
        Lim = [f(Lim) for f in (min,max)]
        for Ax in Axes:
            Ax.set_xlim(Lim)
            Ax.spines['bottom'].set_bounds(Lim[0], Lim[1])

    elif Axis.lower() == 'y':
        Lim = [f(Ax.get_ylim()) for f in (min,max) for Ax in Axes]
        Lim = [f(Lim) for f in (min,max)]
        for Ax in Axes:
            Ax.set_ylim(Lim)
            Ax.spines['left'].set_bounds(Lim[0], Lim[1])

    return(None)


def Set(
        Ax=None, AxArgs={}, SetSpines=True,
        Fig=None, FigTitle=None, Tight=True
    ):
    if Ax:
        ## General
        for ax in ['bottom', 'left']:
            if ax+'pos' not in AxArgs: AxArgs[ax+'pos'] = 2
            Ax.spines[ax].set_position(('outward', AxArgs[ax+'pos']))

        # Ax.spines['bottom'].set_position(('outward', 2))
        # Ax.spines['left'].set_position(('outward', 2))

        Ax.spines['right'].set_visible(False)
        Ax.spines['top'].set_visible(False)
        Ax.tick_params(top=False, right=False)
        Ax.patch.set_visible(False)

        if 'title' in AxArgs: Ax.set_title(AxArgs['title'])


        ## X
        if 'xlabel' in AxArgs: Ax.set_xlabel(AxArgs['xlabel'])
        if 'xlim' in AxArgs: Ax.set_xlim(AxArgs['xlim'])
        if 'xticks' in AxArgs: Ax.set_xticks(AxArgs['xticks'])
        if 'xticklabels' in AxArgs: Ax.set_xticklabels(AxArgs['xticklabels'])

        if 'xtickspacing' in AxArgs:
            import matplotlib.ticker as ticker
            Ax.xaxis.set_major_locator(ticker.MultipleLocator(AxArgs['xtickspacing']))

        if 'xbounds' in AxArgs:
            Ax.spines['bottom'].set_bounds(AxArgs['xbounds'])
        else:
            if SetSpines:
                if len(Ax.get_xticks()) and len(Ax.get_xlim()):
                    Lim, Ticks = Ax.get_xlim(), Ax.get_xticks()
                    Bounds = [Ticks[Ticks >= Lim[0]][0],
                              Ticks[Ticks <= Lim[1]][-1]]
                    Ax.spines['bottom'].set_bounds(Bounds)


        ## Y
        if 'ylabel' in AxArgs: Ax.set_ylabel(AxArgs['ylabel'])
        if 'ylim' in AxArgs: Ax.set_ylim(AxArgs['ylim'])
        if 'yticks' in AxArgs: Ax.set_yticks(AxArgs['yticks'])
        if 'yticklabels' in AxArgs: Ax.set_yticklabels(AxArgs['yticklabels'])

        if 'ytickspacing' in AxArgs:
            import matplotlib.ticker as ticker
            Ax.yaxis.set_major_locator(ticker.MultipleLocator(AxArgs['ytickspacing']))

        if 'ybounds' in AxArgs:
            Ax.spines['left'].set_bounds(AxArgs['ybounds'])
        else:
            if SetSpines:
                if len(Ax.get_yticks()) and len(Ax.get_ylim()):
                    Lim, Ticks = Ax.get_ylim(), Ax.get_yticks()
                    Bounds = [Ticks[Ticks >= Lim[0]][0],
                              Ticks[Ticks <= Lim[1]][-1]]
                    Ax.spines['left'].set_bounds(Bounds)


        ## Z
        if 'zlim' in AxArgs: Ax.set_zlim(AxArgs['zlim'])
        if 'zlabel' in AxArgs: Ax.set_zlabel(AxArgs['zlabel'])
        if 'zticks' in AxArgs: Ax.set_zticks(AxArgs['zticks'])
        if 'zticklabels' in AxArgs: Ax.set_zticklabels(AxArgs['zticklabels'])


    if Fig:
        if FigTitle: Fig.suptitle(FigTitle)

        if Tight:
            Fig.tight_layout()
            if FigTitle: Fig.subplots_adjust(top=0.85)

        Fig.patch.set_visible(False)

    return(None)


def SignificanceBar(
        X, Y, Text, Ax, TextArgs={}, LineArgs={},
        TicksDir='down', LineTextSpacing=None
    ):

    if TicksDir == 'down':
        from matplotlib.markers import TICKDOWN as Tick
        # AmpF = LineTextSpacing if LineTextSpacing is not None else 1.02
    elif TicksDir == 'up':
        from matplotlib.markers import TICKUP as Tick
        # AmpF = LineTextSpacing if LineTextSpacing is not None else 0.98
    elif TicksDir == 'left':
        from matplotlib.markers import TICKLEFT as Tick
        # AmpF = LineTextSpacing if LineTextSpacing is not None else 1.02
    elif TicksDir == 'right':
        from matplotlib.markers import TICKRIGHT as Tick
        # AmpF = LineTextSpacing if LineTextSpacing is not None else 0.98
    elif TicksDir == None:
        Tick = None
        # AmpF = LineTextSpacing if LineTextSpacing is not None else 1.02
    else:
        raise TypeError('TicksDir should be "up", "down", "left", "right" or None.')

    if LineTextSpacing is None:
        if TicksDir in ('up', 'down', None):
            Step = np.ptp(Ax.get_ylim())*0.03
        else:
            Step = np.ptp(Ax.get_xlim())*0.03
    else:
        Step = LineTextSpacing

    if TicksDir in ('up','right'): Step *= -1

    TextArgsLoc = {'ha': 'center', 'va': 'center'}
    LineArgsLoc = {'color': 'k'}
    TextArgsLoc = {**TextArgsLoc, **TextArgs}
    LineArgsLoc = {**LineArgsLoc, **LineArgs}

    # Yy = max(Y)*AmpF
    Yy = max(Y)+Step
    Xx = max(X)+Step
    if TicksDir in ['up', 'down', None]:
        Ax.plot(X, Y, marker=Tick, **LineArgsLoc)
        Ax.text(sum(X)/2, Yy, Text, **TextArgsLoc)
    else:
        Ax.plot(X, Y, marker=Tick, **LineArgsLoc)
        Ax.text(Xx, sum(Y)/2, Text, **TextArgsLoc)

    return(None)


def SubLabelsPos(Axes, XOffsets=None, YOffsets=None):
    Pos = np.array([_.get_position().corners() for _ in Axes.ravel()]).T
    Pos = [Pos[:,1,_] for _ in range(Pos.shape[2])]

    if XOffsets is None:
        XOffsets = [0 for _ in Axes.ravel()]
    if YOffsets is None:
        YOffsets = [0 for _ in Axes.ravel()]

    X = [Pos[_][0]+XOffsets[_] for _ in range(len(Pos))]
    Y = [Pos[_][1]+YOffsets[_] for _ in range(len(Pos))]
    Pos = np.array(list(zip(X,Y)))

    return(Pos)


def SubLabels(Fig, Positions, Letters=[], FontArgs={'size':12, 'va': 'top'}, Color=''):
    if not len(Letters):
        Letters = StrRange('A','Z')*len(Positions)

    for P,Pos in enumerate(Positions):
        if Color:
            Fig.text(Pos[0], Pos[1], Letters[P], fontdict=FontArgs, color=Color)
        else:
            Fig.text(Pos[0], Pos[1], Letters[P], fontdict=FontArgs)
    return(None)


def TextBox(Fig, AxGroups, Texts=[], Directions=[], RectArgs=[]):
    if len(Texts)==0: Texts = [f'AxGroup {_+1}' for _ in range(len(AxGroups))]
    if len(Directions)==0: Directions = ['Horizontal' for _ in AxGroups]
    if len(RectArgs)==0: RectArgs = [{} for _ in AxGroups]

    AxRects = []
    for Gr,Axes in enumerate(AxGroups):
        GrDir = Directions[Gr]
        Axes = np.array(Axes)

        Pos = np.array([_.get_position().corners() for _ in Axes.ravel()]).T

        if 'hor' in GrDir.lower():
            RA = dict(
                XOffset=0,
                YOffset=-0.05,
                XSizeFac=1,
                YSizeFac=1,
                XText=0.5,
                YText=0.4,
                RectAxArgs={},
                RectArgs=dict(facecolor='w', edgecolor='k', clip_on=False, linewidth=1),
                TextArgs=dict(ha='center', va='center')
            )

            MergeDicts(RA, dcp(RectArgs[Gr]))

            Pos = [
                [
                    Pos[0,1,_], Pos[1,1,_],
                    (Pos[0,2,_]-Pos[0,1,_]),
                    0.025
                    # (Pos[1,1,_]-Pos[1,0,_])
                ]
                for _ in range(Pos.shape[2])
            ]

        elif 'ver' in GrDir.lower():
            RA = dict(
                XOffset=0.095,
                YOffset=0,
                XSizeFac=1,
                YSizeFac=1,
                XText=0.6,
                YText=0.5,
                RectAxArgs={},
                RectArgs=dict(facecolor='w', edgecolor='k', clip_on=False, linewidth=1),
                TextArgs=dict(ha='center', va='center', rotation=90)
            )

            MergeDicts(RA, dcp(RectArgs[Gr]))

            Pos = np.sort(Pos, axis=2)

            Pos = [
                [
                    Pos[0,0,_], Pos[1,0,_],
                    # (Pos[0,2,_]-Pos[0,1,_]),
                    0.025,
                    (Pos[1,1,_]-Pos[1,0,_])
                ]
                for _ in range(Pos.shape[2])
            ]

        PosRec = [
            Pos[0][0]-RA['XOffset'], Pos[0][1]-RA['YOffset'],
            ((Pos[-1][0]+Pos[-1][2])-Pos[0][0])*RA['XSizeFac'],
            ((Pos[-1][1]+Pos[-1][3])-Pos[0][1])*RA['YSizeFac']
        ]

        AxRect = Fig.add_axes(PosRec, **RA['RectAxArgs'])
        AxRect.add_patch(plt.Rectangle((0,0),1,1, **RA['RectArgs']))
        AxRect.text(RA['XText'], RA['YText'], Texts[Gr], **RA['TextArgs'])
        AxRect.axis('off')

        AxRects.append(AxRect)

    return(AxRects)


#%% Level 1
Screen = GetScreenInfo()
FigSizeA4 = [8.27, 11.69]
FigSize = [InchToRealSize(FigSizeA4[0]-1.97), InchToRealSize((FigSizeA4[1]-1.97)*0.3)]


def ApplyColorMapToCycle(Lines, CMap=None, Interval=[0,0.8]):
    '''
    Apply colormap colors as color cycle on a list of lines.

    Parameters
    ----------
    Lines: list
        List of `matplotlib.lines.Line2D` objects.

    CMap: str or matplotlib.colors.ListedColormap
        Colormap to be applied to color cycle.

    Interval: list
        List with start and end colormap values. Useful for when the extremes
        of the colormap are the same as the figure background. Defaults to
        `[0,0.8]`, since the colormap value of `1` gives white color for most
        colormaps.
    '''

    if not CMap: CMap = plt.get_cmap()
    else: CMap = plt.get_cmap(CMap)

    for L,Line in enumerate(Lines):
        Line.set_color(CMap(np.linspace(Interval[0],Interval[1],len(Lines)))[L])

    return(None)


def CheckData(Data, Rate, SpaceAmpF=0.3, TimeWindow=0.2, SkipTime=10, ChLabels=[]):
    """
        Plot an animated visualization of Data.

        Parameters:
            Data: array_like
                Input 2D array, with dimensions (samples, channels).
            Rate: int
                Data's sampling rate.
            SpaceAmpF: float, optional
                Amplification factor for spacing between channels. Defaults to 0.3.
            TimeWindow: float, optional
                Amount of Data to show  at once, in seconds. Defaults to 0.2.
            SkipTime: int, optional
                Amount of samples to advance per step. Defaults to 10.
            ChLabels: list, optional
                Label of channels. If empty, channel number will be used. Defaults to [].
    """
    FN = inspect.stack()[0][3]

    for C in range(Data.shape[1]): Data[:,C] /= Data[:,C].max()
    Data[:,-1] *= 0.6

    Spaces = GetSpaces(Data, SpaceAmpF)
    if not ChLabels:
        ChLabels = list(range(1, Data.shape[1]+1))

    SkipTime = int(Rate*SkipTime/1000)

    try:
        Fig, Ax = plt.subplots(figsize=(7,6))
        for S in range(0,Data.shape[0]-int(TimeWindow*Rate),SkipTime):
            t = np.arange(S, (TimeWindow*Rate)+S, 1)/Rate

            YTicks = []
            for Ch in range(Data.shape[1]):
                Y = Data[S:int(TimeWindow*Rate)+S,Ch] - Spaces[Ch]
                YTicks.append(np.nanmean(Y))
                Ax.plot(t, Y, 'k')

            XBar = [t[t.shape[0]//2], t[t.shape[0]//2+int(TimeWindow*0.2*Rate)]]
            Ax.plot(XBar, [-Spaces[-1]*1.05]*2, 'k', lw=2)

            Ax.set_yticks(YTicks)
            Ax.set_yticklabels(ChLabels)
            Ax.set_xlabel('Time [s]')
            Ax.set_ylabel('Depth [µm]')

            plt.pause(0.001)
            Ax.clear()
        plt.show()

    except KeyboardInterrupt:
        print(f'[{ScriptName}.{FN}] Stopping animation...')
        plt.close('all')
        return(None)


def ClickXY(Frame):
    X, Y = None, None
    Fig, Ax = plt.subplots()
    Ax.imshow(Frame, vmin=0, vmax=(2**24)-1)
    Ax.tick_params(bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
    Fig.tight_layout(pad=0)
    Fig.canvas.callbacks.connect('button_press_event', ClickCallback)
    plt.show()


def FigAx(Ax, SubPlotsArgs={}):
    ReturnAx = True
    spa = dict(constrained_layout=True)
    spa = {**spa, **SubPlotsArgs}
    if not Ax:
        ReturnAx = False
        Fig, Ax = plt.subplots(**spa)
    else:
        Fig = Ax.get_figure()

    return(Fig, Ax, ReturnAx)


def GenColorMap(RGB, Start=0):
    """
    Generate colormap based on the provided RGB color.

    Parameters
    ----------
    RGB: list
        List of three values (red, green, blue) representing the desired RGB
        color. The values should be in the range 0-1 or 0-255.

    Returns
    -------
    CMap: colormap
        A colormap based on the provided RGB color.
    """
    CMap = np.ones((256, 4))
    for RGBInd,RGBVal in enumerate(RGB):
        CMap[:, RGBInd] = np.linspace(Start, RGBVal, 256)
    CMap = ListedColormap(CMap)

    return(CMap)


def GenLegendHandle(ltype='line', **Args):
    if ltype == 'line':
        Handler = Line2D([0], [0], **Args)
    elif ltype == 'rect':
        Handler = Patch(**Args)
    else:
        raise Exception('`ltype` should be `line` or `rect`.')

    return(Handler)


def SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show, Verbose=False):
    FN = inspect.stack()[0][3]

    if ReturnAx:
        # Set(Ax=Ax, AxArgs=AxArgs, SetSpines=False)
        return(Ax)
    else:
        Set(Ax=Ax, AxArgs=AxArgs)
        if Save:
            if '/' in File:
                os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
            for E in Ext:
                Fig.savefig(File+'.'+E)

                if Verbose:
                    print(f"[{ScriptName}.{FN}] Written to {File}.{E}")

        if Show: plt.show()
        else: plt.close()
        return(None)


def ScaleBar(
        Fig, Ax,
        ScalarMappableArgs={'cmap': 'inferno', 'vmin':0, 'vmax':1},
        ColorbarArgs={}
    ):
    SM = plt.cm.ScalarMappable(
        cmap=ScalarMappableArgs['cmap'],
        norm=plt.Normalize(
            vmin=ScalarMappableArgs['vmin'],
            vmax=ScalarMappableArgs['vmax']
        )
    )
    SM._A = []

    Fig.colorbar(SM, ax=Ax, **ColorbarArgs)

    return(None)



#%% Level 3
def AllCh(Data, X=[], Colors=[], Labels=[], Leg=[], SpaceAmpF=1, ScaleBar=0, lw=2,
          Ax=None, AxArgs={}, File='AllCh', Ext=['svg'], Save=False, Show=True, SubPlotsArgs={}):
    if type(Data) == list: Data = np.array(Data).T
    if len(Data.shape) == 1: Data = Data.reshape((Data.shape[0],1))

    DataLen, ChNo = Data.shape
    if not len(X): X = np.arange(DataLen)
    if not len(Colors): Colors = ['k'] * ChNo
    Spaces = GetSpaces(Data) if ChNo > 1 else [0]

    Fig, Ax, ReturnAx = FigAx(Ax, SubPlotsArgs)

    YTicks = np.zeros(ChNo)
    Lines = [0] * ChNo
    for Ch in range(ChNo):
        Y = Data[:,Ch] + Spaces[Ch]*SpaceAmpF
        if ScaleBar:
            sbX = X[0]-(X[1]-X[0])*int(X.shape[0]*0.03)
            if Ch == 0: Ax.plot([sbX]*2, [np.nanmean(Y), -ScaleBar], 'k', lw=lw)

        Lines[Ch] = Ax.plot(X, Y, lw=lw)
        YTicks[Ch] = np.nanmean(Y)

        Lines[Ch][0].set_color(Colors[Ch])
        if Leg: Lines[Ch][0].set_label(Leg[Ch]); Ax.legend(loc='best')

    # AxArgs['yticks'] = YTicks
    # AxArgs['yticklabels'] = Labels if len(Labels) else 1+np.arange(ChNo)
    Ax.set_yticks(YTicks)
    Ax.set_yticklabels(Labels if len(Labels) else 1+np.arange(ChNo))
    Ax.tick_params(left=False)
    Ax.spines['left'].set_visible(False)
    Ax.spines['left'].set_position(('axes', 0))

    Result = SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def Violins(Data, X=[], EdgeColors=[], FaceColors=[], FaceAlpha=[], LinesAmpF=1, Width=0.5, Means=True, PlotArgs={},
             Ax=None, AxArgs={}, File='Violins', Ext=['svg'], Save=False, Show=True):

    BPData = [[_ for _ in d if not np.isnan(_)] for d in Data]

    if not len(X): X = list(range(len(BPData)))
    if not len(EdgeColors): EdgeColors = ['k']*len(BPData)
    if not len(FaceColors): FaceColors = ['k']*len(BPData)
    if not len(FaceAlpha): FaceAlpha = [0.2]*len(BPData)

    PA = {**{'showmeans':False}, **PlotArgs}

    Fig, Ax, ReturnAx = FigAx(Ax)
    AxP = Ax.violinplot(BPData, positions=X, widths=Width, **PA)

    for I in range(len(AxP['bodies'])):
        AxP['bodies'][I].set_edgecolor(EdgeColors[I])
        AxP['bodies'][I].set_facecolor(FaceColors[I])
        AxP['bodies'][I].set_alpha(FaceAlpha[I])

    for iK in ('cmaxes','cmins','cbars'):
        AxP[iK].set_edgecolor(EdgeColors[I])
        AxP[iK].set_facecolor(FaceColors[I])
        AxP[iK].set_alpha(FaceAlpha[I])

    if 'medians' in AxP.keys():
        for I in range(len(AxP['medians'])):
            AxP['medians'][I].set(color=EdgeColors[I])

    if Means:
        # in matplotlib 2.2.4 the 'showmeans' feature somehow prevents
        # inkscape from opening the resulting figure if exported to svg
        # so means have to be manually plotted
        Means = [np.mean(_) for _ in BPData]
        for B,Box in enumerate(Means):
            Ax.plot(X[B], Box, color=EdgeColors[B], marker='^')

    AxArgs = {**{'xticks': X}, **AxArgs}

    Result = SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def Boxes(Data, X=[], EdgeColors=[], FaceColors=[], FaceAlpha=[], LinesAmpF=1, Width=None, Means=True, PlotArgs={},
             Ax=None, AxArgs={}, File='Boxplots', Ext=['svg'], Save=False, Show=True):

    BPData = [[_ for _ in d if not np.isnan(_)] for d in Data]

    if not len(X): X = list(range(len(BPData)))
    if not len(EdgeColors): EdgeColors = ['k']*len(BPData)
    if not len(FaceColors): FaceColors = ['k']*len(BPData)
    if not len(FaceAlpha): FaceAlpha = [0.2]*len(BPData)

    PA = {**{'patch_artist':True, 'showmeans':False}, **PlotArgs}

    Fig, Ax, ReturnAx = FigAx(Ax)
    AxP = Ax.boxplot(BPData, positions=X, widths=Width, **PA)

    for I in range(len(AxP['fliers'])):
        AxP['fliers'][I].set_markeredgecolor(EdgeColors[I])
        AxP['fliers'][I].set_marker('.')

    for I in range(len(AxP['boxes'])):
        AxP['boxes'][I].set(edgecolor=EdgeColors[I], facecolor=to_rgba(FaceColors[I], FaceAlpha[I]))

    for I in range(len(AxP['medians'])):
        AxP['medians'][I].set(color=EdgeColors[I])

    for K in ['whiskers', 'caps']:
        for I in range(len(AxP[K])):
            AxP[K][I].set(color=EdgeColors[I//2])

    if Means:
        # in matplotlib 2.2.4 the 'showmeans' feature somehow prevents
        # inkscape from opening the resulting figure if exported to svg
        # so means have to be manually plotted
        Means = [np.mean(_) for _ in BPData]
        for B,Box in enumerate(Means):
            Ax.plot(X[B], Box, color=EdgeColors[B], marker='^')

    AxArgs = {**{'xticks': X}, **AxArgs}

    Result = SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def Circles(
        X, Y, Radius, CirclesArgs={},
        Ax=None, AxArgs={}, File='Circles', Ext=['svg'], Save=False, Show=True
    ):
    """
    Make a scatter of circles plot of X vs Y, where X and Y are sequence
    like objects of the same lengths. The size of circles are in data scale.

    Parameters
    ----------
    X,Y : scalar or array_like, shape (n, )
        Input data
    Radius : scalar or array_like, shape (n, )
        Radius of circle in data unit.
    CirclesArgs : `~matplotlib.collections.Collection` properties
        Eg. alpha, edgecolor(ec), facecolor(fc), linewidth(lw), linestyle(ls),
        norm, cmap, transform, etc.

    Returns
    -------
    paths : `~matplotlib.collections.PathCollection`

    Examples
    --------
    a = np.arange(11)
    Circles(a, a, a*0.2, alpha=0.5, edgecolor='none')
    plt.colorbar()

    :License: [BSD 3-Clause License](http://opensource.org/licenses/BSD-3-Clause)

    :ModifiedFrom: @Syrtis-Major

    :Source: https://stackoverflow.com/a/24567352
    """

    Fig, Ax, ReturnAx = FigAx(Ax)

    if 'fc' in CirclesArgs.keys(): CirclesArgs['facecolor'] = CirclesArgs.pop('fc')
    if 'ec' in CirclesArgs.keys(): CirclesArgs['edgecolor'] = CirclesArgs.pop('ec')
    if 'ls' in CirclesArgs.keys(): CirclesArgs['linestyle'] = CirclesArgs.pop('ls')
    if 'lw' in CirclesArgs.keys(): CirclesArgs['linewidth'] = CirclesArgs.pop('lw')

    patches = [Circle((x, y), r) for x, y, r in np.broadcast(X, Y, Radius)]
    collection = PatchCollection(patches, **CirclesArgs)

    Ax.add_collection(collection)
    Ax.autoscale_view()

    if not Ax:
        Ax.set_xlim([X[0]-(XSpread*2), X[-1]+(XSpread*2)])
        Ax.set_xticks(X)

    Result = SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def Comodulogram(Cmdlgrm, AmpFreq, PhaseFreq, CMap='inferno',
                 Ax=None, AxArgs={}, File='Comodulogram', Ext=['pdf'], Save=False, Show=True):

    if len(Cmdlgrm.shape) == 3:
        for C in range(Cmdlgrm.shape[2]):
            Comodulogram(Cmdlgrm[:,:,C], AmpFreq, PhaseFreq, CMap, Ax, AxArgs,
                         File=File+'_'+str(C), Ext=Ext, Save=Save, Show=Show)

        return(None)

    Fig, Ax, ReturnAx = FigAx(Ax)

    Ax.pcolormesh(PhaseFreq, AmpFreq, Cmdlgrm)
    SM = plt.cm.ScalarMappable(cmap=CMap, norm=plt.Normalize(vmin=0, vmax=1))
    SM._A = []
    Fig.colorbar(SM, ax=Ax, label='Modulation Index')
    Ax.set_xlabel('Phase Frequency [Hz]')
    Ax.set_ylabel('Amplitude Frequency [Hz]')

    Result = SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def MeanSEM(Data, X=[], LineArgs={}, FillArgs={}, PlotType='Lines',
            Ax=None, AxArgs={}, File='MeanSEM', Ext=['pdf'], Save=False, Show=True):
    AArg = AxArgs.copy()
    Fig, Ax, ReturnAx = FigAx(Ax)

    LineArgsDef = dict(color='k', lw=2, label='Mean')
    FillArgsDef = dict(color='k', lw=0, alpha=0.3, label='SEM')
    LA = {**LineArgsDef, **LineArgs}

    if type(Data) == np.ndarray:
        Mean = np.nanmean(Data, axis=1)
        SEM = np.nanstd(Data, axis=1) / (Data.shape[1]**0.5)
    else:
        Mean = np.array([np.nanmean(_) for _ in Data])
        SEM = np.array([np.nanstd(_)/(len(_)**0.5) for _ in Data])

    if not len(X): X = np.arange(len(Mean))

    # if FillArgs is not None:
    if PlotType=='Lines':
        FA = {**FillArgsDef, **FillArgs}
        Ax.fill_between(X, Mean+SEM, Mean-SEM, **FA)
    elif PlotType=='Markers':
        Ax.errorbar(X, Mean, SEM, **LA)
    elif PlotType=='Bars':
        BarsLA = {**{'linestyle':''},**LA}
        Ax.errorbar(X, Mean, SEM, **BarsLA)
    else:
        return KeyError(f"{PlotType} is not a valid PlotType.")

    if PlotType in ('Lines','Markers'):
        Ax.plot(X, Mean, **LA)
    elif PlotType=='Bars':
        BarsLA = {**{'alpha':0.6},**LA}
        Ax.bar(X, Mean, **BarsLA)

    Result = SaveShow(ReturnAx, Fig, Ax, AArg, File, Ext, Save, Show)
    return(Result)


def Scatter3D(
        Data, ScatterArgs={}, Elevation=30, Azimuth=-130,
        ScaleBarArgs={},
        Ax=None, AxArgs={}, File='Scatter3D', Ext=['pdf'], Save=False, Show=True
    ):
    Fig, Ax, ReturnAx = FigAx(Ax, {'subplot_kw': {'projection': '3d'}})

    ScatterDefaults = dict(c=Data[:,0], cmap='inferno', edgecolors='face', alpha=1, marker='.')
    ScatterArgs = {**ScatterDefaults, **ScatterArgs}

    Ax.scatter(Data[:,0], Data[:,1], Data[:,2], **ScatterArgs)
    Ax.view_init(Elevation, Azimuth)

    if ScaleBarArgs:
        if 'label' in ScaleBarArgs: ColorbarArgs={'label': ScaleBarArgs['label']}

        ScalarMappableArgs = {'cmap': ScatterArgs['cmap'], 'vmin':0, 'vmax':1}
        for K in ['vmin', 'vmax']:
            if K in ScaleBarArgs: ScalarMappableArgs[K] = ScaleBarArgs[K]

        ScaleBar(ScaleBarArgs['Fig'], Ax, ScalarMappableArgs, ColorbarArgs)

    Result = SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def ScatterMean(
        Data, X=[],
        ColorsAvg=[], ColorsMarkers=[], ColorsLines=[], Alpha=0.4,
        XSpread=0.1, YSpread=0, LogY=False, Mean=['MeanSEM'],
        Markers=[], Line='--', CMap=None, Paired=False, PlotArgs={}, ErrorArgs={}, MeanArgs={},
        Ax=None, AxArgs={}, File='ScatterMean', Ext=['svg'], Save=False, Show=True
    ):

    FN = inspect.stack()[0][3]

    if not len(X): X = list(range(len(Data)))

    Boxes = [[np.random.uniform(V-YSpread, V+YSpread, 1)[0] if ~np.isnan(V) else V for V in L] for L in Data]
    XPoss = [np.random.uniform(Pos-XSpread, Pos+XSpread, len(Boxes[P])) for P,Pos in enumerate(X)]
    Errors = [[0, np.nanstd(Box)/len(Box)**0.5, 0] for Box in Boxes]
    Colors = [ColorsMarkers, ColorsLines, ColorsAvg]
    PlotArgs = {**dict(linestyle=''), **PlotArgs}
    ErrorArgs = {**dict(zorder=np.inf, lw=3, elinewidth=1, capsize=5), **ErrorArgs}
    MeanArgs = {**dict(alpha=Alpha*0.75), **MeanArgs}

    ApplyColor = False if 'color' in MeanArgs else True

    pCMap = plt.get_cmap(CMap)

    for C,ColorItem in enumerate(Colors):
        if not len(ColorItem):
            Colors[C] = ['k']*max(len(Data), len(X))

    if not len(Markers):
        Markers = ['.']*len(Boxes)

    Fig, Ax, ReturnAx = FigAx(Ax)
    for P,Pos in enumerate(X):
        Box, XPos, Error = Boxes[P], XPoss[P], Errors[P]

        if LogY:
            pMarkers = Ax.semilogy(
                XPos, Box, color=Colors[1][P], markeredgecolor=Colors[0][P],
                markerfacecolor=Colors[0][P], marker=Markers[P], alpha=Alpha, **PlotArgs
            )
        else:
            pMarkers = Ax.plot(
                XPos, Box, color=Colors[1][P], markeredgecolor=Colors[0][P],
                markerfacecolor=Colors[0][P], marker=Markers[P], alpha=Alpha, **PlotArgs
            )

        if CMap:
            pColors = pCMap(np.linspace(0,0.8,len(Box)))
            for cl, CL in enumerate(pColors):
                Ax.plot(
                    pMarkers[0].get_xdata()[cl], pMarkers[0].get_ydata()[cl],
                    color=CL, marker=pMarkers[0].get_marker(),
                    linestyle=pMarkers[0].get_linestyle()
                )

        if 'BarSEM' in Mean:
            if ApplyColor: MeanArgs['color'] = Colors[0][P]
            Ax.bar(Pos, np.nanmean(Box), yerr=Error[1], **MeanArgs)

        if 'MeanSEM' in Mean:
            Ax.errorbar([Pos-XSpread, Pos, Pos+XSpread], [np.nanmean(Box)]*3, Error, color=Colors[2][P], **ErrorArgs)

    if Paired:
        if len(np.unique([len(_) for _ in Data])) != 1:
            print(f'[{ScriptName}.{FN}] All boxes must have the same length.')
            return(None)

        for L in range(len(Boxes[0])):
            if LogY: Ax.semilogy(
                [_[L] for _ in XPoss],
                [_[L] for _ in Boxes],
                color=Colors[1][P], linestyle=Line, alpha=Alpha
            )
            else: Ax.plot(
                [_[L] for _ in XPoss],
                [_[L] for _ in Boxes],
                color=Colors[1][P], linestyle=Line, alpha=Alpha
            )

    # if CMap:
        # CMapLines = [_ for _ in Ax.get_lines() if len(_.get_xdata()) == 2]
        # ApplyColorMapToCycle(CMapLines, CMap=CMap)

    if not Ax:
        Ax.set_xlim([X[0]-(XSpread*2), X[-1]+(XSpread*2)])
        Ax.set_xticks(X)

    Result = SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def Spectrogram(T, F, Sxx, Colormap='inferno', Line={},
                Ax=None, AxArgs={}, File='Spectrogram', Ext=['svg'], Save=False, Show=True):

    FN = inspect.stack()[0][3]

    Fig, Ax, ReturnAx = FigAx(Ax)

    Ax.pcolormesh(T, F, Sxx, cmap=Colormap)
    if 'xlim' not in AxArgs: AxArgs['xlim'] = [round(T[0]), round(T[-1])]
    if 'ylim' not in AxArgs: AxArgs['ylim'] = [0, max(F)]
    if 'xlabel' not in AxArgs: AxArgs['xlabel'] = 'Time [s]'
    if 'ylabel' not in AxArgs: AxArgs['ylabel'] = 'Frequency [Hz]'

    Set(Ax=Ax, AxArgs=AxArgs, SetSpines=False)

    if Line:
        if 'Y' not in Line:
            print(f"[{ScriptName}.{FN}] Line['Y'] should contain plottable 1D data.")
            return(None)
        if 'X' not in Line: Line['X'] = np.arange(len(Line['Y']))
        if 'ylim' not in Line: Line['ylim'] = [min(Line['Y']), max(Line['Y'])]

        LineAx = Ax.twinx()
        LineAx.plot(Line['X'], Line['Y'], Line['Color'])
        Set(Ax=LineAx, AxArgs={k:v for k,v in Line if k not in ['X', 'Y']}, SetSpines=False)

    Result = SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)


def Triang3D(Data, X, Y, Azimuth=-70, Elevation=30, Colormap='inferno',
             Ax=None, AxArgs={}, File='Data3D', Ext=['svg'], Save=False, Show=True):
    Fig, Ax, ReturnAx = FigAx(Ax, {'subplot_kw': dict(projection='3d')})

    x = np.tile(X,2)

    for LineIndex in range(len(Y)-1):
        Y0, Y1 = Y[LineIndex], Y[LineIndex+1]
        Data0, Data1 = Data[:,LineIndex], Data[:,LineIndex+1]
        func = float if '.' in str(Y0) or '.' in str(Y1) else int

        y = [func(Y0)]*len(Data0) + [func(Y1)]*len(Data1)
        z = np.concatenate([Data0, Data1])
        T = Triangulation(x, y)

        Ax.plot_trisurf(
            x, y, z, triangles=T.triangles,
            cmap=Colormap, edgecolor='none',
            antialiased=False, shade=False
        )

    Ax.grid(False)
    Ax.view_init(Elevation, Azimuth)

    Result = SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show)
    return(Result)



#%% Level 4

def Polygon(
        Coords, Areas=None, ScatterArgs={}, FillArgs={},
        Ax=None, AxArgs={}, File='Polygon', Ext=['svg'], Save=False, Show=True
    ):

    Fig, Ax, ReturnAx = FigAx(Ax)

    if Areas is not None:
        SAs = dict(edgecolor='k', facecolor='k', alpha=0.4)
        SAs = {**SAs, **ScatterArgs}

        r = (Areas/np.pi)**0.5
        Ax = Circles(
            Coords[1,:], Coords[0,:], r,
            SAs, Ax=Ax
        )
    else:
        SAs = dict(edgecolor='k', facecolor='k', alpha=0.4, marker='.')
        SAs = {**SAs, **ScatterArgs}

        Ax.scatter(Coords[1,:], Coords[0,:], **SAs)

    NaNs = np.isnan(Coords).prod(axis=0).astype(bool)
    GSXY = Coords[:,~NaNs].T
    GSC = GSXY.mean(axis=0)

    DistToC = np.zeros((GSXY.shape[0]*2,2))
    DistToC[::2,:] = GSXY
    DistToC[1::2,:] = GSC
    DistToC = EucDist(DistToC[:,0], DistToC[:,1])[0][::2]

    Vert = np.array(sorted(
        GSXY.tolist(),
        key=lambda x: np.arctan2(x[1]-GSC[1], x[0]-GSC[0])
    ))

    FAs = dict(color='k', alpha=0.2)
    FAs = {**FAs, **FillArgs}

    Ax.fill(Vert[:,1], Vert[:,0], **FAs)

    Result = SaveShow(ReturnAx, Fig, Ax, AxArgs, File, Ext, Save, Show, Verbose=True)
    return(Result)



