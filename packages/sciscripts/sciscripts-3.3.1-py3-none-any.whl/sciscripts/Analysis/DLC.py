#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20210614

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('[Analysis.DLC] Loading dependencies...')
import os
try:
    import pandas as pd
    AvailPandas = True
except ModuleNotFoundError as e:
    print(f'[{ScriptName}] {e}: Module `pandas` not available. Some functions will not work.')
    AvailPandas = False


print('[Analysis.DLC] Done.')


def GetXYLh(File):
    if not AvailPandas:
        raise ModuleNotFoundError(f'[{ScriptName}] Module `pandas` not available.')

    Data = pd.read_hdf(File)
    BodyParts = Data.columns.get_level_values("bodyparts").unique().tolist()
    X, Y, Lh = Data.values.reshape((len(Data.index), -1, 3)).T
    X, Y, Lh = X.T, Y.T, Lh.T
    return(X,Y,Lh,BodyParts)


