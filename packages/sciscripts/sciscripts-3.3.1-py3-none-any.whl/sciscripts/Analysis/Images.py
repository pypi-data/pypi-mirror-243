#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20210125

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

ScriptName = 'Analysis.Images'
print(f'[{ScriptName}] Loading dependencies...')
import inspect
import numpy as np
import matplotlib.pyplot as plt

from sciscripts.Analysis.Analysis import IsFloat, IsInt

try:
    from PIL import Image as PILImage
    from PIL.TiffTags import TAGS as PILTags
    AvailPIL = True
except ModuleNotFoundError as e:
    print(f'[{ScriptName}] {e}: Module `PIL` not available. Some functions will not work.')
    AvailPIL = False


print(f'[{ScriptName}] Done.')


def Expectation(c):
    E = np.mean(c)
    return(E)


def GetMetadata(IMG):
    FunctionName = inspect.stack()[0][3]

    if not AvailPIL:
        raise ModuleNotFoundError(
            f"[{ScriptName}.{FunctionName}] Module `PIL` not available."
        )

    with PILImage.open(IMG) as img:
        Meta = {PILTags.get(key): img.tag[key] for key in img.tag}

    Meta = {K: V for K,V in Meta.items() if len(V)}
    Meta = {K: V[0] if len(V)==1 else V for K,V in Meta.items()}

    if 'ImageDescription' in Meta.keys():
        if 'volocity' in Meta['ImageDescription'].lower():
            MD = [
                _ for _ in Meta['ImageDescription'].split('\r')
                if '=' in _
            ]
            MD = {
                K.split('=')[0]: '='.join(K.split('=')[1:])
                for K in MD
            }
            for Type,Func in zip((float,int), (IsFloat,IsInt)):
                MD = {
                    K: Type(V) if Func(V) else V
                    for K,V in MD.items()
                }

            Meta = {**Meta, **MD}

            for K in ('X','Y','Z'):
                Meta[f"PixelWidth{K}"] = 1/Meta[f"{K}CalibrationMicrons"]

    return(Meta)


def NormalizeIMGs(IMGs, Min=1, Max=99):
    IMGsNorm = []
    AllMax = max([_.max() for _ in IMGs])
    for I,IMG in enumerate(IMGs):
        IMG2 = IMG/AllMax
        IMGMin = np.percentile(IMG2.ravel(), Min)
        IMGMax = np.percentile(IMG2.ravel(), Max)

        IMG2[IMG2<IMGMin] = IMGMin
        IMG2[IMG2>IMGMax] = IMGMax
        IMG2 -= IMGMin
        IMG2 /= IMG2.max()

        IMGsNorm.append(IMG2)
        # plt.imsave(Files[I], IMG2)
        # Fig, Axes = plt.subplots(1,2,figsize=(15,10))
        # Axes[0].imshow(np.flipud(IMG))
        # Axes[1].imshow(np.flipud(IMG2))
        # plt.show()

    return(IMGsNorm)


def Normalize(Files, Min=1, Max=99):
    # IMGs = []
    # for File in Files:
        # IMG = plt.imread(File)
        # IMGs.append(IMG)

    IMGs = [plt.imread(File) for File in Files]
    IMGsNorm = NormalizeIMGs(IMGs, Min, Max)
    return(IMGsNorm)


def OptimalGain(StD):
    OG = 1/StD
    return(OG)


def Variance(c, Gain=1):
    V = Gain*Expectation(c)
    return(V)


