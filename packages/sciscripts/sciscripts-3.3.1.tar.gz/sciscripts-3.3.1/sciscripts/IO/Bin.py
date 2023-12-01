#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20170612

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

import errno
import numpy as np
import os

from glob import glob
from scipy import sparse

from sciscripts.IO import Txt
from sciscripts.Analysis.Analysis import IsInt


def PathToDict(Path, Value=None):
    Dict = {}
    Head = Path.split('/')[0]
    Tail = Path.split('/')[1:]

    if not Tail: Dict[Head] = Value
    else:
        Dict[Head] = PathToDict('/'.join(Tail), Value)

    return(Dict)


def MergeDicts(D1, D2):
    # Based on Paul Durivage's code available at
    # https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
    for K, V in D2.items():
        if K in D1 and type(D1[K]) == dict and type(D2[K]) == dict:
            MergeDicts(D1[K], D2[K])
        else:
            D1[K] = D2[K]


def MergeDictsAndContents(D1, D2):
    D1C = {**D1}

    for K, V in D2.items():
        if K in D1C and type(D1C[K]) == dict and type(D2[K]) == dict:
            D1C[K] = MergeDictsAndContents(D1C[K], D2[K])

        elif (
                K in D1C and
                type(D1C[K]) in (list, tuple, np.ndarray) and
                type(D2[K]) in (list, tuple, np.ndarray)
            ):

            try:
                D1C[K] = np.concatenate((D1C[K], D2[K]))
            except ValueError:
                D1C[K] = np.array(list(D1C[K])+list(D2[K]), dtype=object)

        elif K in D1C and type(D1C[K]) in (list, tuple, np.ndarray):
            D1C[K] = list(D1C[K])+[D2[K]]

        elif K in D1C and type(D2[K]) in (list, tuple, np.ndarray):
            D1C[K] = list(D2[K])+[D1C[K]]

        elif K in D1C:
            D1C[K] = [D1C[K], D2[K]]

        else:
            D1C[K] = D2[K]

    return(D1C)


def DictToList(Data):
    IsList = (
        (type(Data) == dict) and
        (not False in ['_' in _ for _ in Data.keys()]) and
        (len(np.unique([
            '_'.join(_.split('_')[:-1]) for _ in Data.keys()
        ])) == 1) and
        (not False in [IsInt(_.split('_')[-1]) for _ in Data.keys()])
    )
    # print('IsList:',IsList)

    if type(Data) == dict and not IsList:
        DataList = {K: DictToList(V) for K,V in Data.items()}
    elif IsList:
        Keys = sorted(Data.keys(), key=lambda x: int(x.split('_')[-1]))
        Inds = sorted([int(x.split('_')[-1]) for x in Data.keys()])
        DataList = [[] for _ in range(max(Inds)+1)]

        for i,K in zip(Inds,Keys):
            if ((type(Data[K]) == dict)
                    and (not False in ['_' in _ for _ in Data[K].keys()])
                    and (len(np.unique([
                        '_'.join(_.split('_')[:-1]) for _ in Data[K].keys()
                    ])) == 1)
                    and (not False in [IsInt(_.split('_')[-1]) for _ in Data.keys()])):
                DataList[i] = DictToList(Data[K])
            else:
                DataList[i] = Data[K]
    else:
        DataList = Data

    return(DataList)


def DictToSparse(Data, File):
    if type(Data) in (list,tuple):
        for E,El in enumerate(Data):
            Data[E] = DictToSparse(El, File+'/'+File.split('/')[-1]+'_'+str(E))

    elif type(Data) == dict \
            and sorted(Data.keys()) == ['data', 'indices', 'indptr'] \
            and len(glob(f'{File}/Info.dict.sparse_csc_matrix')):
        EInfo = Txt.Read(glob(f'{File}/Info.dict.sparse_csc_matrix')[0])
        Data = sparse.csc_matrix((Data['data'], Data['indices'], Data['indptr']), shape=EInfo['_shape'])

    return(Data)

def Read(File, ChList=[], Info={}, Verbose=False, AsMMap=True):
    """
    Read flat interleaved binary data and return it as a numpy array. Data
    will be represented as Data[Channels, Samples].

    This function needs:
    - a text file in the same path but ending in
    "-Info.dict" containing a dictionary with the data
    info. The minimal information needed is Info['Shape'] and
    Info['DType']

    OR

    - an Info dict containing Info['Shape'] and Info['DType']

    """

    if '.' not in File.split('/')[-1]:
        Data = {}
        Files = [glob(_.split('-Info.dict')[0]+'.*')[0]
                 for _ in glob(File+'/**/*-Info.dict', recursive=True)]

        Paths = ['/'.join(_.split('/')[:-1]) for _ in Files]
        if not len(Paths):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), File)

        LastCommon = os.path.commonprefix(Paths).split('/')

        while LastCommon[-1] not in Paths[0].split('/'):
            LastCommon = LastCommon[:-1]

        if len(LastCommon) == 1:
            LastCommon = LastCommon[-1]
        elif len(LastCommon[-1]) and LastCommon[-2] != LastCommon[-1].split('_')[0] :
            LastCommon = LastCommon[-1]
        else:
            LastCommon = LastCommon[-2]

        # LastCommon = LastCommon[-1]
        LastCommon += '/'
        # print('REL')

        for d,D in enumerate(Files):
            Path = '.'.join(D.split('.')[:-1])
            Path = Path.split(LastCommon)[-1]
            if Verbose: print('Loading', Path, '...')
            MergeDicts(Data, PathToDict(Path, Read(D, ChList, Info, Verbose, AsMMap)[0]))

        if len(Data.keys())==1 and list(Data.keys())[0]==File.split('/')[-1]:
            Data = Data[list(Data.keys())[0]]

        Data = DictToList(Data)
        Data = DictToSparse(Data, File)

        if Verbose: print('Done.')
        return(Data, None)

    else:
        if not Info:
            InfoFile = '.'.join(File.split('.')[:-1]) + '-Info.dict'
            Info = Txt.Read(InfoFile)

        if os.stat(File).st_size != 0:
            if AsMMap:
                Data = np.memmap(File, dtype=Info['DType'], mode='c').reshape(Info['Shape'])
            else:
                Data = np.fromfile(File, dtype=Info['DType']).reshape(Info['Shape'])

            if ChList: Data = Data[:,[Ch-1 for Ch in ChList]]
        else:
            Data = np.array([], dtype=Info['DType'])

        return(Data, Info)


def Write(Data, File, Info={}):
    """ Write numpy array to flat interleaved binary file. Data will be
        represented as ch1s1-ch2s1-ch3s1-...-chNs1-ch1s2-ch2s2...chNsN.

        Also, write a text file containing data info for data loading. """

    if type(Data) == dict or 'AsdfObject' in str(type(Data)):
        for K,V in Data.items(): Write(V, f"{File}/{K}", Info)

    elif type(Data) in [list, tuple]:
        for E,El in enumerate(Data):
            Write(El, f"{File}/{File.split('/')[-1]}_{E}", Info)

    elif type(Data) in [int, float, str]:
        Write(np.array(Data).reshape(1), File, Info)

    elif 'csc_matrix' in str(type(Data)):
        # EFile = '.'.join(File.split('.')[:-1]) if '.' in File else File
        EFile = File
        if not os.path.isdir(File):
            BN = os.path.basename(File)
            if '.' in BN: BN = '.'.join(BN.split('.')[:-1])
            EFile = f"{os.path.dirname(File)}/{BN}"

        Write(
            {
                k: np.array(v)
                for k,v in Data.__dict__.items()
                if k in ('data', 'indices', 'indptr')
            },
            EFile, Info
        )

        Txt.Write(
            {
                k: v for k,v in Data.__dict__.items()
                if k not in ('data', 'indices', 'indptr')
            },
            f'{EFile}/Info.dict.sparse_csc_matrix'
        )

    elif Data.shape == ():
        Write(np.array(Data).reshape(1), File, Info)

    else:
        if '.' not in File.split('/')[-1]: File +='.dat'
        if '/' in File: os.makedirs('/'.join(File.split('/')[:-1]), exist_ok=True)

        # Get info and generate path
        Info['Shape'] = Data.shape
        Info['DType'] = str(Data.dtype)
        Info['Flags'] = {}

        for Flag in ['C_CONTIGUOUS', 'F_CONTIGUOUS', 'OWNDATA', 'WRITEABLE',
                     'ALIGNED', 'WRITEBACKIFCOPY']:
            try:
                Info['Flags'][Flag] = Data.flags[Flag]
            except KeyError:
                pass

        InfoFile = '.'.join(File.split('.')[:-1]) + '-Info.dict'

        # Write text info file
        Txt.Write(Info, InfoFile)

        # Write interleaved data
        with open(File, 'wb') as F: Data.reshape(np.prod(Data.shape)).tofile(F)

    return(None)

