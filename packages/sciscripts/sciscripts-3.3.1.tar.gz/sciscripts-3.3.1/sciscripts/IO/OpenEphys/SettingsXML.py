#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20170704

Loads info from the settings.xml file.

Examples:
    File = '/Path/To/Experiment/settings.xml

    # To get all info the xml file can provide:
    AllInfo = SettingsXML.XML.Read(File)

    # AllInfo will be a dictionary following the same structure of the XML file.

    # To get the sampling rate used in recording:
    Rate = SettingsXML.GetSamplingRate(File)

    # To get info only about channels recorded:
    RecChs = SettingsXML.GetRecChs(File)[0]

    # To get also the processor names:
    RecChs, PluginNames = SettingsXML.GetRecChs(File)

    # RecChs will be a dictionary:
    #
    # RecChs
    #     ProcessorNodeId
    #         ChIndex
    #             'name'
    #             'number'
    #             'gain'
    #         'PluginName'

"""

from sciscripts.IO import XML


def FindRecProcs(Ch, Proc, RecChs):
    ChNo = Ch['number']
    ChI = [_['number'] for _ in Proc['CHANNEL']].index(ChNo)
    Rec = Proc['CHANNEL'][ChI]['SELECTIONSTATE'][0]['record']

    if Rec == '1':
        if Proc['NodeId'] not in RecChs: RecChs[Proc['NodeId']] = {}
        RecChs[Proc['NodeId']][ChNo] = Ch

    return(RecChs)


def GetSamplingRate(File):
    Info = XML.Read(File)['SETTINGS']
    Error = 'Cannot parse sample rate. Check your settings.xml file at SIGNALCHAIN>PROCESSOR>Sources/Rhythm FPGA.'

    try:
        for SignalChain in Info['SIGNALCHAIN']:
            Names = [_['name'] for _ in SignalChain['PROCESSOR']]

            if 'Sources/Rhythm FPGA' in Names:
                FPGA = Names.index('Sources/Rhythm FPGA')
                FPGA = SignalChain['PROCESSOR'][FPGA]['EDITOR'][0]

                if 'SampleRateString' in FPGA.keys():
                    Rate = FPGA['SampleRateString']
                    Rate = float(Rate.split(' ')[0])*1000
                elif FPGA['SampleRate'] == '17':
                    Rate = 30000
                elif FPGA['SampleRate'] == '16':
                    Rate = 25000
                else:
                    Rate = None
            else:
                Rate = None

        if not Rate:
            print(Error); return(None)
        else:
            return(Rate)

    except Exception as Ex:
        print(Ex); print(Error); return(None)


def GetRecChs(File):
    Info = XML.Read(File)['SETTINGS']
    RecChs = {}; ProcNames = {}

    for SignalChain in Info['SIGNALCHAIN']:
        Names = [_['name'] for _ in SignalChain['PROCESSOR']]

        for P, Proc in enumerate(SignalChain['PROCESSOR']):
            if 'isSource' in Proc.keys():
                if Proc['isSource'] == '1': SourceProc = Names[P]
            else:
                if Proc['name'].split('/')[0] == 'Sources': SourceProc = Names[P]

            if 'CHANNEL_INFO' in Proc.keys() and len(Proc['CHANNEL_INFO'][0]):
                for Ch in Proc['CHANNEL_INFO'][0]['CHANNEL']:
                    RecChs = FindRecProcs(Ch, Proc, RecChs)

            elif 'CHANNEL' in Proc:
                for Ch in Proc['CHANNEL']:
                    RecChs = FindRecProcs(Ch, Proc, RecChs)

            else: continue

            if 'pluginName' in Proc:
                ProcNames[Proc['NodeId']] = Proc['pluginName']
            else:
                ProcNames[Proc['NodeId']] = Proc['name']

        SPI = Names.index(SourceProc)
        if SignalChain['PROCESSOR'][SPI]['CHANNEL_INFO'][0]:
            SourceProc = SignalChain['PROCESSOR'][SPI]['CHANNEL_INFO'][0]['CHANNEL']
        else:
            SourceProc = SignalChain['PROCESSOR'][SPI]['CHANNEL']

        for P, Proc in RecChs.items():
            for C, Ch in Proc.items():
                if 'gain' not in Ch:
                    if type(SourceProc) == dict:
                        RecChs[P][C].update([c for c in SourceProc.values() if c['number'] == C][0])
                    else:
                        RecChs[P][C].update([c for c in SourceProc if c['number'] == C][0])

    return(RecChs, ProcNames)

