#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20210614

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts

Functions for analyzing and manipulating video files.

Under heavy development, highly unstable.
"""

print('[Analysis.Videos] Loading dependencies...')
try:
    import cv2
except ModuleNotFoundError:
    raise ModuleNotFoundError('This module requires the cv2 module to be installed.')

import numpy as np
import os
from sciscripts.Analysis.Analysis import GetPeaks
from sciscripts.IO import Video
print('[Analysis.Videos] Done.')


# Level 0
def FrameScale(frame, downsampling=3):
    """
    Taken and modified from Justin Mitchel
    @ https://www.codingforentrepreneurs.com/blog/open-cv-python-change-video-resolution-or-scale
    """
    width = int(frame.shape[1]/downsampling)
    height = int(frame.shape[0]/downsampling)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


def GetLedBlinkStart(File, Channel='r', Dur=10, StD=1, Verbose=False):
    LedVideo, dvInfo = Video.Read(File)
    ChInd = {'r':2, 'g':1, 'b':0}

    # print('Get time offset...', end='')
    # Start = perf_counter()
    Ch = np.zeros(int(dvInfo['FPS']*Dur), dtype=float)
    for F in range(int(dvInfo['FPS']*Dur)):
        f, Frame = LedVideo.read()
        if not f: break
        Ch[F] = Frame[:,:,ChInd[Channel]].mean()

    # End = perf_counter()-Start
    # print(f'Done in {End}s.')
    LedPeaks = GetPeaks(abs(np.diff(Ch)), StD)['Pos']
    LedStart = LedPeaks[0]/dvInfo['FPS'] if len(LedPeaks) else 0
    # print('Done.')

    LedVideo.release()
    return(LedStart)


def Read(File):
    V, VInfo = Video.Read(File)
    Vid = np.array([V.read()[1] for _ in range(VInfo['FrameNo'])])
    V.release()
    return(Vid)


def RGB2BW(FileInput, FileOutput, Codec='same'):
    RGBVideo, Info = Video.Read(FileInput)

    if str(Codec).lower() == 'same':
        FourCC = int(RGBVideo.get(cv2.CAP_PROP_FOURCC))
    elif str(Codec).lower() == 'auto':
        Ext = FileOutput.split('.')[-1]
        FourCC = Video.GetFourCC(Video.DefaultCodecs[Ext])
    else:
        FourCC = Video.GetFourCC(Codec)

    Dimensions = [int(Info[_]) for _ in ['Width','Height']]

    Output = cv2.VideoWriter(
        filename=FileOutput,
        fourcc=FourCC,
        fps=Info['FPS'],
        frameSize=tuple(Dimensions)
    )

    for F in range(Info['FrameNo']):
        _, Frame = RGBVideo.read()
        Frame = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
        Output.write(Frame)

    RGBVideo.release()
    Output.release()

    return(None)


# Level 1
def Downsample(FileInput, FileOutput, Downsampling, Codec='same'):
    InVideo, Info = Video.Read(FileInput)

    if str(Codec).lower() == 'same':
        FourCC = int(InVideo.get(cv2.CAP_PROP_FOURCC))
    elif str(Codec).lower() == 'auto':
        Ext = FileOutput.split('.')[-1]
        FourCC = Video.GetFourCC(Video.DefaultCodecs[Ext])
    elif type(Codec) == int:
        FourCC = Codec
    else:
        FourCC = Video.GetFourCC(Codec)

    Dimensions = [int(Info[_]/Downsampling) for _ in ['Width','Height']]

    Output = cv2.VideoWriter(
        filename=FileOutput,
        fourcc=FourCC,
        fps=Info['FPS'],
        frameSize=tuple(Dimensions)
    )

    for F in range(Info['FrameNo']):
        _, Frame = InVideo.read()
        Frame = FrameScale(Frame, Downsampling)
        Output.write(Frame)

    InVideo.release()
    Output.release()

    return(None)


