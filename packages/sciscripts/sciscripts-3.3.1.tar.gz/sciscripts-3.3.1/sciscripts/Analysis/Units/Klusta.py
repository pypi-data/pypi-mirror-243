#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20180226

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts

Function to extract spike cluster after detection and clustering with Klusta
"""

try:
    from klusta.kwik import KwikModel
    AvailKlusta = True
except ModuleNotFoundError as e:
    AvailKlusta = False


import numpy as np
import importlib.util
import types

from sciscripts.Analysis.Units import Units
from sciscripts.IO import IO


def load_source(name: str, path: str) -> types.ModuleType:
    '''
    Taken from @mscuthbert at
    https://github.com/cuthbertLab/music21/pull/1424/files

    Replacement for deprecated imp.load_source()
    Thanks to:
    https://github.com/epfl-scitas/spack for pointing out the
    important missing "spec.loader.exec_module(module)" line.
    '''
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise FileNotFoundError(f'No such file or directory: {path!r}')

    module = importlib.util.module_from_spec(spec)
    if module is None:
        raise FileNotFoundError(f'No such file or directory: {path!r}')

    spec.loader.exec_module(module)
    return module




## Level 0
def GetAllClusters(PrmFile):
    if not AvailKlusta:
        raise Exception('Klusta not available.')
        return(None)

    AnalysisFile = '/'.join(PrmFile.split('/')[:-2]) + '/Units/'+ PrmFile.split('/')[-3]
    KwikFile = PrmFile[:-3]+'kwik'
    Exp = PrmFile.split('/')[-1][:-4]

    Clusters = KwikModel(KwikFile)
    Offsets = Clusters.all_traces.offsets
    Rate = Clusters.sample_rate
    RecLengths = [int(Offsets[_]/Rate-Offsets[_-1]/Rate) for _ in range(1,len(Offsets))]

    SpkTimes = Clusters.spike_times
    SpkClusters =  Clusters.spike_clusters
    SpkRecs =  Clusters.spike_recordings
    Waveforms = Clusters.all_waveforms

    ## Get info
    Prm = load_source('', PrmFile)
    Prb = load_source('', Prm.prb_file)
    ChSpacing = Prb.channel_groups['0']['geometry']
    ChSpacing = abs(ChSpacing[0][1] - ChSpacing[1][1])

    DataInfo = Prm.DataInfo
    DataInfo['Analysis'] = {}
    DataInfo['Analysis']['Channels'] = Clusters.probe.channels
    DataInfo['Analysis']['ChNoTotal'] = Prm.traces['n_channels']
    DataInfo['Analysis']['ChSpacing'] = ChSpacing
    DataInfo['Analysis']['ClusterRecs'] = Clusters.recordings
    DataInfo['Analysis']['ClusterLabels'] = Clusters.cluster_groups
    DataInfo['Analysis']['RecLengths'] = RecLengths
    DataInfo['Analysis']['RecOffsets'] = Offsets
    DataInfo['Analysis']['Rate'] = Clusters.sample_rate
    DataInfo['Analysis']['RawData'] = Prm.DataInfo['RawData']


    for K,V in DataInfo['ExpInfo'].items():
        if 'Hz' not in V.keys():
            DataInfo['ExpInfo'][K]['Hz'] = 'Baseline'

    ## Get recs
    Recs = Units.GetRecsNested(DataInfo)
    ClusterRecs = [b for a in Recs for b in a]

    if 'Prevention/20170803-Prevention_04-UnitRec/KlustaFiles/Prevention_Exp00.prm' in PrmFile:
        ClusterRecs = Clusters.recordings
        Recs += [np.array([5])]
        DataInfo['RawData'] = DataInfo['RawData'][:-1] + [DataInfo['RawData'][3]] + [DataInfo['RawData'][-1]]
        DataInfo['ExpInfo']['05'] = DataInfo['ExpInfo']['04']

    if ClusterRecs != Clusters.recordings:
        print('Wrong number of recordings! Cannot extract TTLs!')
        DataInfo['Analysis']['RecNoMatch'] = False
    else:
        DataInfo['Analysis']['RecNoMatch'] = True

    DataInfo['Analysis']['RecsNested'] = Recs

    IO.Bin.Write(Waveforms, AnalysisFile + '_' + Exp + '_AllClusters/Waveforms.dat')
    IO.Bin.Write(SpkTimes, AnalysisFile + '_' + Exp + '_AllClusters/SpkTimes.dat')
    IO.Bin.Write(SpkClusters, AnalysisFile + '_' + Exp + '_AllClusters/SpkClusters.dat')
    IO.Bin.Write(SpkRecs, AnalysisFile + '_' + Exp + '_AllClusters/SpkRecs.dat')
    IO.Txt.Write(DataInfo, AnalysisFile + '_' + Exp + '_AllClusters/Info.dict')

    return(None)


