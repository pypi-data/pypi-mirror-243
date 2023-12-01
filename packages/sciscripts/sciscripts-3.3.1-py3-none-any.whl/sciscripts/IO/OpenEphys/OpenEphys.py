#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20170708

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

ScriptName = 'IO.OpenEphys.OpenEphys'

print(f'[{ScriptName}] Loading dependencies...')
import numpy as np
from ast import literal_eval
from glob import glob

from sciscripts.Analysis import Analysis
from sciscripts.IO import IO, Bin, Hdf5, Txt
from sciscripts.IO.OpenEphys import OpenEphysFormat, SettingsXML
print(f'[{ScriptName}] Done.')


## Level 0
def ApplyChannelMap(Data, ChannelMap):
    print('Retrieving channels according to ChannelMap... ', end='')
    for R, Rec in Data.items():
        if Rec.shape[1] < len(ChannelMap) or max(ChannelMap) > Rec.shape[1]-1:
            print('')
            print('Not enough channels in data to apply channel map. Skipping...')
            continue

        Data[R] = Data[R][:,ChannelMap]

    return(Data)


def BitsToVolts(Data, ChInfo, Unit, Verbose=False):
    if Verbose: print(f'Converting to {Unit}... ', end='')
    Data = {R: Rec.astype('float32') for R, Rec in Data.items()}

    if Unit.lower() == 'uv': U = 1
    elif Unit.lower() == 'mv': U = 10**-3

    for R in Data.keys():
        for C in range(len(ChInfo)):
            Data[R][:,C] = Data[R][:,C] * ChInfo[C]['bit_volts'] * U
            if 'ADC' in ChInfo[C]['channel_name']: Data[R][:,C] *= 10**6

    return(Data)


def BitsToVoltsXML(Data, ChInfo, Unit):
    if Unit.lower() == 'uv': U = 1
    elif Unit.lower() == 'mv': U = 10**-3

    for R in Data.keys():
        for C, Ch in enumerate(sorted(ChInfo.keys(), key=lambda x: int(x))):
            # print(ChInfo[Ch]['name'])
            Data[R][:,C] = Data[R][:,C] * float(ChInfo[Ch]['gain']) * U
            if 'ADC' in ChInfo[Ch]['name']: Data[R][:,C] *= 10**6


    return(Data)


def ChooseProcs(XMLFile, Procs):
    ProcList = SettingsXML.GetRecChs(XMLFile)[1]
    ProcList = {Id: Name for Id, Name in ProcList.items() if Id in Procs}

    print(Txt.Print(ProcList))
    Procs = input('Which Procs should be kept (comma separated) ? ')
    Procs = [_ for _ in Procs.split(',')]

    return(Procs)


def EventsLoad(Folder):
    Files = sorted(glob(Folder+'/*.events'))
    if len(Files) > 1: print('Multiple sessions not supported yet.'); return(None)
    # for File in Files:
        # Session = File.split('.')[0].split('_')[-1]

    EventsDict = OpenEphysFormat.loadEvents(Folder+'/'+Files[0])
    return(EventsDict)


def GetChNoAndProcs(File):
    ChNo, Procs = SettingsXML.GetRecChs(File)
    if len(ChNo) > 1:
        Proc = [K for K,V in Procs.items() if 'FPGA'in V][0]
    else:
        Proc = list(ChNo.keys())[0]
    ChNo = len(ChNo[Proc])

    return(ChNo, Proc)


def GetResistance(ImpedanceFile):
    Impedance = SettingsXML.XML.Read(ImpedanceFile)
    Impedance = {C: Ch for C,Ch in Impedance['CHANNEL'].items()}
    Chs = sorted(Impedance.keys(), key=lambda x: int(x[2:]))

    ROhms = [
        abs(
            np.cos(float(Impedance[Ch]['phase'])) *
            float(Impedance[Ch]['magnitude'])
        )
        for C, Ch in enumerate(Chs)
    ]

    return(ROhms)


def VoltageToCurrent(Data, ImpedanceFile):
    print('Normalizing based on resistance of each channel... ', end='')
    Impedance = SettingsXML.XML.Read(ImpedanceFile)
    Impedance = {C: Ch for C,Ch in Impedance['CHANNEL'].items()}

    for R in Data.keys():
        for C, Ch in enumerate(sorted(Impedance.keys(), key=lambda x: int(x[2:]))):
            ROhms = abs(np.cos(float(Impedance[Ch]['phase'])) * float(Impedance[Ch]['magnitude']))
            Data[R][:,C] /= ROhms

    return(Data)


## Level 1
def KwikLoad(Folder, Unit='uV', ChannelMap=[], ImpedanceFile='', Experiment=None, Processor=None, Recording=None, Verbose=False):
    if not Hdf5.Avail:
        print(f'[{ScriptName}] {e}: Please install the `hdf5` library to use this module.')
        return(None)

    Kwds = sorted(glob(Folder+'/*.kwd'))
    if Unit.lower() in ['uv','mv']:
        XMLFile = sorted(glob(Folder+'/setting*.xml'))[0]
        RecChs = SettingsXML.GetRecChs(XMLFile)[0]

    if ImpedanceFile.lower() == 'auto':
        if glob(Folder+'/impedance_measurement.xml'):
            ImpedanceFile = glob(Folder+'/impedance_measurement.xml')[0]
        else:
            ImpedanceFile = ''

    Data = {}; Rate = {}
    for Kwd in Kwds:
        Exp, Proc = Kwd.split('/')[-1].split('_')[0][10:], Kwd.split('/')[-1].split('_')[1].split('.')[0]

        if Experiment:
            if Exp != Experiment: continue

        if Processor:
            if Proc != Processor: continue

        if Proc not in Data.keys(): Data[Proc], Rate[Proc] = {}, {}
        if Unit.lower() in ['uv','mv']:
            Data[Proc][Exp], Attrs = Hdf5.Load('/recordings', Kwd, Copy=True)
        else:
            Data[Proc][Exp], Attrs = Hdf5.Load('/recordings', Kwd)

        if Recording:
            Data[Proc][Exp] = {R: Rec['data'] for R, Rec in Data[Proc][Exp].items() if R == Recording}
            Rate[Proc][Exp] = [np.array(int(Rec['sample_rate'])) for R,Rec in Attrs.items()  if R == Recording]
        else:
            Data[Proc][Exp] = {R: Rec['data'] for R, Rec in Data[Proc][Exp].items()}
            Rate[Proc][Exp] = [np.array(int(Rec['sample_rate'])) for Rec in Attrs.values()]

        if len(np.unique(Rate[Proc][Exp])) == 1: Rate[Proc][Exp] = Rate[Proc][Exp][0]

        try:
            if Unit.lower() in ['uv','mv']:
                if type(RecChs[Proc]) == dict:
                    RecChs[Proc] = list(RecChs[Proc].values())
                    for c in range(len(RecChs[Proc])):
                        if 'name' in RecChs[Proc][c].keys():
                            RecChs[Proc][c]['channel_name'] = RecChs[Proc][c]['name']
                        if 'gain' in RecChs[Proc][c].keys():
                            RecChs[Proc][c]['bit_volts'] = float(RecChs[Proc][c]['gain'])

                Data[Proc][Exp] = BitsToVolts(Data[Proc][Exp], RecChs[Proc], Unit)

                if ImpedanceFile:
                    Data[Proc][Exp] = VoltageToCurrent(Data[Proc][Exp], ImpedanceFile)

        except KeyError:
            print('No gain info on file, units are in bits.')

        if ChannelMap: Data[Proc][Exp] = ApplyChannelMap(Data[Proc][Exp], ChannelMap)

    if Verbose: print('Done.')
    return(Data, Rate)


def OELoad(Folder, Unit='uV', ChannelMap=[], ImpedanceFile='', Processor=None, Recording=None, Verbose=False):
    OEs = glob(Folder+'/*continuous')

    if ImpedanceFile.lower() == 'auto':
        if glob(Folder+'/impedance_measurement.xml'):
            ImpedanceFile = glob(Folder+'/impedance_measurement.xml')[0]
        else:
            ImpedanceFile = ''

    Chs = [_.split('/')[-1] for _ in OEs]
    Procs = np.unique([_[:3] for _ in Chs])

    Data = {_: {} for _ in Procs}; Rate = {_: {} for _ in Procs}
    Chs = {Proc: [_ for _ in Chs if _[:3] == Proc] for Proc in Procs}

    for P, Proc in Chs.items():
        Type = Chs[P][0].split('_')[-1].split('.')[0][:-1]
        if Verbose: print(Type)
        Chs[P] = sorted(Proc, key=lambda x: int(x.split('_'+Type)[1].split('_')[0].split('.')[0]))

    for Proc in Data.keys():
        if Processor:
            if Proc != Processor: continue

        ACh = Chs[Proc][0].split('.')[0]
        OEData = OpenEphysFormat.loadFolder(Folder, source=Proc)
        Rate[Proc] = int(OEData[ACh]['header']['sampleRate'])

        Recs = np.unique(OEData[ACh]['recordingNumber'])
        BlockSize = int(OEData[ACh]['header']['blockLength'])
        for Rec in Recs:
            R = str(int(Rec))

            if Recording:
                if R != Recording: continue

            RecInd = np.where(OEData[ACh]['recordingNumber'].repeat(BlockSize) == Rec)
            Data[Proc][R] = [OEData[_.split('.')[0]]['data'][RecInd] for _ in Chs[Proc]]
            Data[Proc][R] = np.array(Data[Proc][R]).T

        if Unit.lower() in ['uv','mv']:
            ChsInfo = [OEData[_.split('.')[0]]['header']['bitVolts'] for _ in Chs[Proc]]
            ChsInfo = {str(Ch): {'gain': BitVolt} for Ch, BitVolt in enumerate(ChsInfo)}
            Data[Proc] = BitsToVolts(Data[Proc], ChsInfo, Unit)

            if ImpedanceFile:
                Data[Proc] = VoltageToCurrent(Data[Proc], ImpedanceFile)

        if ChannelMap: Data[Proc] = ApplyChannelMap(Data[Proc], ChannelMap)

    return(Data, Rate)


## Level 2
def GetRecs(Folder):
    FilesExt = [F[-3:] for F in glob(Folder+'/*.*')]

    if 'kwd' in FilesExt:
        if not Hdf5.Avail:
            print(f'[{ScriptName}] {e}: Please install the `hdf5` library to use this module.')
            return(None)

        Kwds = glob(Folder+'/*.kwd')

        for Kwd in Kwds:
            Proc = Kwd[-11:-8]

            Recs = {}
            Recs[Proc] = Hdf5.Load('/recordings', Kwd)[0]
            Recs[Proc] = [R for R in Recs[Proc].keys()]

    elif 'dat' in FilesExt:
        Files = glob(Folder+'/*.dat'); Files.sort()
        RecChs = SettingsXML.GetRecChs(Folder+'/settings.xml')[0]

        Recs = {Proc: [] for Proc in RecChs.keys()}

        for File in Files:
            _, Proc, Rec = File.split('/')[-1][10:-4].split('_')
            Recs[Proc].append(Rec)

    elif 'ous' in FilesExt:
        OEs = glob(Folder+'/*continuous')
        Chs = [_.split('/')[-1] for _ in OEs]
        Procs = np.unique([_[:3] for _ in Chs])
        Recs = {}

        for Proc in Procs:
            ACh = Chs[Proc][0].split('.')[0]
            OEData = OpenEphysFormat.loadFolder(Folder, source=Proc)
            R = np.unique(OEData[ACh]['recordingNumber'])
            Recs[Proc] = str(int(R))

    return(Recs)


def KwikToBin(Folders, Verbose=False):
    for Folder in Folders:
        Data = IO.DataLoader(Folder, 'bits')[0]

        for P,Proc in Data.items():
            for E,Exp in Proc.items():
                for R,Rec in Exp.items():
                    File = f'experiment{int(E)+1}_{P}_{R}.dat'
                    File = f'{Folder}_Bin/{File}'

                    if Verbose:
                        print(Rec.dtype)
                        print(P, E, R)
                        print(File)
                        print()

                    Bin.Write(Rec, File)

