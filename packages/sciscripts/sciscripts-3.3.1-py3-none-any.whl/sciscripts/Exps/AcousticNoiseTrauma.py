#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti

:Date: 20171123

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""
ScriptName = 'Exps.AcousticNoiseTrauma'

print(f'[{ScriptName}] Loading dependencies...')
from sciscripts.IO import SoundCard
from time import sleep

if SoundCard.Avail:
    from datetime import datetime

    from sciscripts.IO import Arduino, DAqs, SigGen, Txt


    ## Level 0
    def Play(Sound, Stim, Intensities, SoundPulseNo, DataInfo, Trigger=False, ArduinoObj=None):
        try:
            AmpFFile = f"{DataInfo['Audio']['CalibrationFile']}/AmpF.txt"
            Sound = DAqs.Normalize(Sound, AmpFFile, 'Out')
        except Exception as e:
            # print(CalibrationOverrideWarning())
            pass

        if 'ExpInfo' not in DataInfo: DataInfo['ExpInfo'] = {}

        if Trigger:
            if ArduinoObj:
                ArduinoObj.write(b'O'); sleep(1) # Enable output mode
                ArduinoObj.write(b'T')                # Enable custom trigger
            else:
                print('There is no Arduino board connected.')
                print('Cannot run stimulation with Trigger.')
                return(None)

        try:
            Stim.start()
            print('Playing', DataInfo['Audio']['Freqs'][0], 'at', str(Intensities[0]), 'dB')
            for Pulse in range(SoundPulseNo): Stim.write(Sound[:,:,0,0])
            Stim.stop()
        except KeyboardInterrupt:
            print(''); print('=====')
            print('Sorry for the wait.')
            print('The sound was played for',
                  str(((Pulse+1)*DataInfo['Audio']['SoundPulseDur'])//60)+"'"+\
                  str(((Pulse+1)*DataInfo['Audio']['SoundPulseDur'])%60)+'"')
            print('====='); print('')

        if Trigger: Arduino.Reset(ArduinoObj)

        DataInfo['Audio']['SoundPulseNo'] = 1
        DataInfo['Audio']['SoundPulseDur'] = ((Pulse+1)*DataInfo['Audio']['SoundPulseDur'])/60
        DataInfo['ExpInfo']['0'] = {'DVCoord': None,
                                    'StimType': DataInfo['Animal']['StimType'],
                                    'Hz': DataInfo['Audio']['Freqs'][0]}

        Txt.Write(DataInfo, DataInfo['InfoFile'])
        print('Done.')
        return(None)


    ## Level 1
    def Run(AnimalName, StimType, Intensities, NoiseFrequency, SoundPulseDur, CalibrationPath, Rate=192000, BlockSize=384, Channels=2, Trigger=False, BaudRate=Arduino.BaudRate, **kws):
        SoundPulseNo = round((SoundPulseDur*60)/20)
        SoundPulseDur = 20

        if 'SoundAmpF' in kws.keys():
            SoundAmpF = kws['SoundAmpF']
            print(DAqs.CalibrationOverrideWarning())
        else:
            SoundAmpF = DAqs.dBToAmpF(Intensities, CalibrationPath)

        Date = datetime.now().strftime("%Y%m%d%H%M%S")
        InfoFile = '-'.join([Date, AnimalName, 'AcousticNoiseTrauma.dict'])
        Kws = {**kws, **locals()}
        if 'kws' in Kws.keys(): del(Kws['kws'])
        DataInfo = Txt.InfoWrite(**Kws)

        if Trigger:
            ArduinoObj = Arduino.CreateObj(BaudRate)
            if not ArduinoObj:
                print('There is no Arduino board connected.')
                print('Cannot run stimulation with Trigger.')
                return(None)
        else:
            ArduinoObj = None

        Stim = SoundCard.AudioSet(ReturnStream='Out', **DataInfo['Audio'])
        Map = [2,1] if 'GPIAS' in CalibrationPath else [1,2]
        Sound = SigGen.SoundStim(Rate, SoundPulseDur, SoundAmpF, NoiseFrequency,
                                 0, TTLs=False, Map=Map)

        Play(Sound, Stim, Intensities, SoundPulseNo, DataInfo, Trigger=Trigger, ArduinoObj=ArduinoObj)
        return(None)

    Avail = True

else:
    print(SoundCard.Msg)
    def Play(**kws): print(SoundCard.Msg)
    def Run(**kws): print(SoundCard.Msg)
    Avail = False


