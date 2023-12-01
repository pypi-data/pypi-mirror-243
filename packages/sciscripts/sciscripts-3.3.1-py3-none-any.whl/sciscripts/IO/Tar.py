#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20170118

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts

Functions for reading and writing tar files [under development].
"""

import os, tarfile


def TarWrite(FileList, File):
    if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)
    with tarfile.open(File, 'a') as F:
        for File in FileList: F.add(File)

    return(None)

