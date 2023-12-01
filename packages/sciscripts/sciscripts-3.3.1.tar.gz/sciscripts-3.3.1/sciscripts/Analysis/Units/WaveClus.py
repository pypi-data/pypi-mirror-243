#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20170612

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

import numpy as np
import os
from glob import glob
from scipy import io

from sciscripts.IO import Bin, WaveClus


## Level 0
def SepSpksPerCluster(Clusters, Ch):
    Ids = np.unique(Clusters['Id'])
    Dict = {}
    Dict['Spks'] = {}

    print(Ch+':', str(len(Ids)), 'clusters:')
    for Id in Ids:
        IdIndex = Clusters['Id'] == Id

        SpkNo = len(Clusters['Spikes'][IdIndex,:])
        if not SpkNo: continue

        Id = "{0:02d}".format(int(Id))
        Dict['Spks'][Id] =  Clusters['Spikes'][IdIndex,:][:]

        print('    Id', Id, '-', str(SpkNo), 'spikes.')

    if len(Dict): return(Dict)
    else: return({})


## Level 1
def ClusterizeSpks(Data, Rate, ChannelMap, ClusterPath, AnalysisPath,
                   AnalysisKey, Rec='0', Override={}, Return=False):
    """ Detect and clusterize spks using WaveClus """

    os.makedirs(ClusterPath, exist_ok=True)

    Data = [Data[:, _-1] for _ in sorted(ChannelMap)]
    print('Writing files for clustering... ', end='')
    FileList = []

    try: Rec = "{0:02d}".format(int(Rec))
    except ValueError: pass

    for Ind, Ch in enumerate(Data):
        MatName = 'Rec' + Rec + '-Ch' + "{0:02d}".format(Ind+1) + '.mat'

        FileList.append(MatName)
        io.savemat(ClusterPath + '/' + MatName, {'data': Ch})

    TxtFile = open(ClusterPath + '/Files.txt', 'w')
    for File in FileList: TxtFile.write(File + '\n')
    TxtFile.close()
    print('Done.')

    WaveClus.Run(Rate, ClusterPath)

    ClusterList = glob(ClusterPath + '/times_*'); ClusterList.sort()
    ClusterList = [_ for _ in ClusterList if _.split('-')[-2].split('_')[-1] == 'Rec'+Rec]
    Clusters = {}
    Clusters[Rec] = WaveClus.LoadClusters(ClusterList, 'WaveClus')

    Bin.Write(Clusters, AnalysisPath)

    ToDelete = glob(ClusterPath + '/*')
    for File in ToDelete:
        if File not in glob(ClusterPath + '/times_*'): os.remove(File)

    if Return: return(Clusters)
    else: return(None)


def Spks(Clusters, AnalysisPath, AnalysisKey, Rec='0', Override={}):
    try: Rec = "{0:02d}".format(int(Rec))
    except ValueError: pass

    UnitsData = {Rec: {}}
    for Ch in Clusters[Rec].keys():
        UnitsData[Rec][Ch] = SepSpksPerCluster(Clusters[Rec][Ch], Ch)

    Bin.WriteUnits(UnitsData, AnalysisPath)
    return(None)

