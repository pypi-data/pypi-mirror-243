#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20220922

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

import numpy as np
import os

from sciscripts.IO import Txt

# Level 0
def Read(File):
    with open(File, 'r') as F: Dict = json.load(F)
    # Dict = Txt.DictListsToArrays(Dict)
    return(Dict)


# Level 1
def Write(Var, File):
    eVar = Txt.DictArraysToLists(Var)
    if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
    with open(File, 'w') as F: json.dump(eVar, F, indent=4)
    return(None)


