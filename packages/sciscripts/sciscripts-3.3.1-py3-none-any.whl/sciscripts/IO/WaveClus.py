#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20170612

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

from sciscripts.IO.IO import RunProcess
from sciscripts.IO.Mat import Read


def LoadClusters(FileList):
    Clusters = {}
    for File in FileList:
        Ch = File[-8:-4]

        ClusterFile = Read(File)
        Clusters[Ch] = {}
        Clusters[Ch]['Id'] = ClusterFile['cluster_class'][:, 0]
        Clusters[Ch]['Timestamps'] = ClusterFile['cluster_class'][:, 1]
        Clusters[Ch]['Spikes'] = ClusterFile['spikes'][:]

    return(Clusters)


def Run(Rate, Path):
    print('Clustering spikes...')

    MLab = '/home/malfatti/Software/Programs/MatLabR2015a/bin/matlab'
    CmdCd = 'cd ' + Path + '; '
    CmdCluster = 'try, par.sr=' + str(int(Rate)) + '; ' + \
                 "Get_spikes('Files.txt', 'parallel', true, 'par', par);" + \
                 "Files = dir('./*spikes.mat'); Files = {Files.name}; " + \
                 "Do_clustering(Files, 'make_plots', false); end; quit"
    RunProcess([MLab, '-nosplash', '-r', CmdCd+CmdCluster])

    print('Done clustering.')
    return(None)

