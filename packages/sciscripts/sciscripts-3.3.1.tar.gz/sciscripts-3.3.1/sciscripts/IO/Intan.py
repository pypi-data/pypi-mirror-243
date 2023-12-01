#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T Malfatti

:Date: 20101102

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts

"""

import json, os, sys
import numpy as np
from glob import glob

from sciscripts.Analysis.Analysis import GetPeaks
from sciscripts.IO import Txt


## Level 0
def ReadData(filename, verbose = False, describe_only = False):
    """
    :Author: Max Hodak

    Fixed, modified to increase speed using numpy, Alex Chubykin, 06 June 2012

    .. warning::
        This is a modified copy ###

        The original script was once avaliable for download at
        http://intantech.com/downloads.html

        Modified by T. Malfatti to:
        - Work in python3;
        - Improve performance by replacing struct by numpy

    Examples
    --------
    .. code-block:: python

       from sciscripts.IO.Intan import ReadData
       mydata = ReadData("spikes_101029_011129.int")
       print(mydata)

       Out:
       {
         "duration": 60,                             # seconds
         "channel_count": 17,                        # number of amps
         "analog": [((-0.2594, -0.1502, ...), ...],  # voltage data
         "aux": [((0, 1, 1, 1, 0, 0, ...), ...],     # aux data
       }

    `len(mydata['analog'])` is approximately `mydata['duration']*25000` and
    `len(mydata['analog'][i]) = mydata['channel_count'] for i < mydata['duration']*25000`
    (ish, unless the fpga dropped frames).  ReadData always returns a dict
    for extensability reasons.  For example, other lines may be added later.

    """
    with open(filename, mode='rb') as f:
        data = f.read()
        if verbose: print('data length',len(data))

        header = data[0:3]
        version, major_version, minor_version = np.frombuffer(header, np.uint8)

        if version != 128:
            raise Exception("Improper data file format.")
        if (major_version != 1 or minor_version != 1):
            print("Datafile may not be compatible with this script.")

        sr = 25000            # Fixed on Intan RHA
        header_size = 67
        num_amps = sum([np.frombuffer(data[i+2:i+3], np.uint8)[0] for i in range(1,64)])
        t_count = int((len(data) - header_size) / (1+4*num_amps))
        t_max = t_count/sr
        BLOCK_SIZE = 4*num_amps+1

        description = {"duration": t_max, "channel_count": num_amps}

        if verbose:
            print('Data file contains %0.2f seconds of data from %d amplifier channel(s)' % (t_max, num_amps))

        if describe_only: return(description)

        data = data[header_size:] # Throw away the header.
        aux = np.frombuffer(data[BLOCK_SIZE-1::BLOCK_SIZE], np.int8)
        data = bytearray(data)
        del data[BLOCK_SIZE-1::BLOCK_SIZE]

        try:
            analog = np.frombuffer(data, np.float32).reshape((t_count, num_amps))
        except ValueError:
            analog = np.frombuffer(data[:-(len(data)%4)], np.float32)
            analog = analog[:-(analog.shape[0]%num_amps)]
            analog = analog.reshape((analog.shape[0]//num_amps, num_amps))
            minlen = min((_.shape[0] for _ in (analog,aux)))
            analog, aux = analog[:minlen,:], aux[:minlen]

    description.update({'analog': analog, 'aux': aux})
    return(description)


## Level 1
def Load(File, ChannelMap=[], Verbose=False):
    Data = ReadData(File, verbose=Verbose)

    try: len(Data['aux'][0])
    except TypeError: Data['aux'] = Data['aux'].reshape((Data['aux'].shape[0], 1))

    Data = np.hstack((Data['analog'], Data['aux']))

    if ChannelMap:
        ChannelMap = [_-1 for _ in ChannelMap]
        Data[:, (range(len(ChannelMap)))] = Data[:, ChannelMap]

    Rate = 25000

    return(Data, Rate)


## Level 2
def FolderLoad(Folder, ChannelMap=[], Verbose=False):
    Rate = 25000
    Data = {str(F): Load(File, ChannelMap, Verbose)[0]
            for F,File in enumerate(sorted(glob(Folder+'/*int')))}

    return(Data, Rate)


def ToOpenEphysBinary(Files, SavePath, Verbose=False):
    BitVolts = 0.19499999284744263

    Info = {
        'GUI version': '0.0.0',
        'continuous': [ {
                'folder_name': 'Intan_RHA-100.0/',
                'sample_rate': 25000,
                'source_processor_name': 'Intan RHA',
                'source_processor_id': 100,
                'source_processor_sub_idx': 0,
                'recorded_processor': 'Intan RHA',
                'recorded_processor_id': 100,
            }],
        'events': [ {
                'folder_name': 'Intan_RHA-100.0/TTL_1/',
                'channel_name': 'Intan RHA source TTL events input',
                'description': 'TTL Events coming from the hardware source processor "Intan RHA"',
                'identifier': 'sourceevent',
                'sample_rate': 25000,
                'type': 'int16',
                'num_channels': 5,
                'source_processor': 'Intan RHA'
            }],
        'spikes': []
    }

    InfoChannels = {
        'description': 'Headstage data channel',
        'identifier': 'genericdata.continuous',
        'history': 'Intan RHA',
        'bit_volts': BitVolts,
        'units': 'uV',
    }

    Offset = 0

    for E,Exp in enumerate(Files):
        for R,Rec in enumerate(Exp):
            ERData = Load(Rec, Verbose=Verbose)[0]

            ERData, Evs = ERData[:,:-1], ERData[:,-1]
            ERData = (ERData/BitVolts).round().astype('int16')
            Timestamps = np.arange(ERData.shape[0], dtype='int64')

            if max(Evs)>0:
                p = GetPeaks(Evs, Std=0)
                p, n = p['Pos'], p['Neg']
                pCh = Evs[p]-Evs[p-1]
                nCh = Evs[n-1]-Evs[n]

                Events, Chs = np.hstack((p,n)), np.hstack((pCh,nCh))
                Type = np.array(([1]*p.shape[0])+([0]*n.shape[0]))
                s = np.argsort(Events)
                Events, Chs, Type = Events[s], Chs[s], Type[s]
                States = np.array([
                    Ch if Type[c] else -Ch for c,Ch in enumerate(Chs)
                ]).astype(int)
            else:
                Events, Chs, States = (np.array([]) for _ in range(3))

            Timestamps += Offset

            EK, RK = f'experiment{E+1}', f'recording{R+1}'
            os.makedirs(f'{SavePath}/{EK}/{RK}/continuous/Intan_RHA-100.0', exist_ok=True)
            os.makedirs(f'{SavePath}/{EK}/{RK}/events/Intan_RHA-100.0/TTL_1', exist_ok=True)

            File = f'{SavePath}/settings.xml'
            with open(File, 'w') as F: pass

            Info['continuous'][0]['num_channels'] = ERData.shape[1]
            Info['continuous'][0]['channels'] = [
                {**InfoChannels, **{
                    'channel_name': f'CH{Ch+1}',
                    'source_processor_index': Ch,
                    'recorded_processor_index': Ch
                }}
                for Ch in range(ERData.shape[1])
            ]

            File = f'{SavePath}/{EK}/{RK}/structure.oebin'
            with open(File, 'w') as F: json.dump(Info, F, indent=2)

            File = f'{SavePath}/{EK}/{RK}/continuous/Intan_RHA-100.0/continuous.dat'
            with open(File, 'wb') as F:
                ERData.reshape(np.prod(ERData.shape)).tofile(F)

            File = f'{SavePath}/{EK}/{RK}/continuous/Intan_RHA-100.0/timestamps.npy'
            np.save(File, Timestamps, allow_pickle=False)

            for EvData,EvFile in (
                    (States, 'channel_states'),
                    (Chs, 'channels'),
                    (Events,'timestamps')
                ):
                File = f'{SavePath}/{EK}/{RK}/events/Intan_RHA-100.0/TTL_1/{EvFile}.npy'
                np.save(File, EvData, allow_pickle=False)

            Offset += Timestamps.shape[0]

    return(None)



if __name__ == '__main__':
    a=ReadData(sys.argv[1], verbose = True, describe_only = False) # a is a dictionary with the data, a["analog"] returns the 2xD np array with the recordings
    print(a)


