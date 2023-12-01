#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20210614

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts

Functions for reading and writing video files.
"""

print('[IO.Video] Loading dependencies...')
try:
    import cv2
except ModuleNotFoundError:
    raise ModuleNotFoundError('This module requires the cv2 module to be installed.')

import os
print('[IO.Video] Done.')

DefaultCodecs = {
    'avi': 'MJPG',
    'mp4': 'mp4v',
    'mkv': 'VP90',
    'webm': 'av01',
}


# Level 0

def GetFourCC(Str):
    fcc = {f'c{e+1}': el for e,el in enumerate(Str)}
    FourCC = cv2.VideoWriter_fourcc(**fcc)
    return(FourCC)


def Read(File):
    Video = cv2.VideoCapture(File)
    Info = {
        'FPS': int(Video.get(cv2.CAP_PROP_FPS)),
        'Width': int(Video.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'Height': int(Video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'FrameNo': int(Video.get(cv2.CAP_PROP_FRAME_COUNT))
    }
    return(Video, Info)


# Level 1

def GetInfo(File):
    Video, Info = Read(File)
    Video.release()
    return(Info)


def Write(Data, FPS, File, Codec='auto'):
    if len(Data.shape) not in (3,4) or 'uint8' not in str(Data.dtype).lower():
        raise TypeError('`Data` must be a 3d array (width, height, frames) or 4d array (width, height, frames, RGB) of type `uint8`.')

    if str(Codec).lower() == 'auto':
        Ext = File.split('.')[-1].lower()
        FourCC = GetFourCC(DefaultCodecs[Ext])
    else:
        FourCC = GetFourCC(Codec)

    Dimensions = Data.shape[:2]
    Color = False if len(Data.shape) == 3 else True

    Output = cv2.VideoWriter(
        filename=File,
        fourcc=FourCC,
        fps=FPS,
        frameSize=tuple(Dimensions),
        isColor=Color
    )

    if Color:
        for Fr in range(Data.shape[2]):
            F = Data[:,:,Fr,:]
            Frame = np.zeros((F.shape[1],F.shape[0],F.shape[2]),'uint8')
            for r in range(3): Frame[:,:,r] = F[:,:,r].T
            Output.write(cv2.cvtColor(Frame, cv2.COLOR_RGB2BGR))
    else:
        for Fr in range(Data.shape[2]):
            Output.write(Data[:,:,Fr].T)

    Output.release()

    return(None)


