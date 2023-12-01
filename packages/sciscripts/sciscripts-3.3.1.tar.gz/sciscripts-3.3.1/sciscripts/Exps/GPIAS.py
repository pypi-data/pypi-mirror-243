#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20171123

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""
ScriptName = 'Exps.GPIAS'

print(f'[{ScriptName}] Loading dependencies...')
from time import sleep

from sciscripts.IO import SoundCard

if SoundCard.Avail:
    import numpy as np
    import random
    from datetime import datetime

    from sciscripts.IO import Arduino, DAqs, SigGen, Txt


    # Level 0
    def GPIASSound(Rate, SoundBGDur, SoundGapDur, SoundBGPrePulseDur,
              SoundLoudPulseDur, SoundBGAfterPulseDur,
              SoundBetweenStimDur, SoundBGAmpF, SoundPulseAmpF,
              NoiseFrequency, TTLAmpF=1, Map=[2,1], GapAmpF={}, **Kws):

        if not len(GapAmpF):
                GapAmpF = {K: [0.0 for _ in V] for K,V in SoundBGAmpF.items()}

        Sound = {}
        print('Creating SoundBG...')
        Sound['BG'] = SigGen.SoundStim(Rate, SoundBGDur, SoundBGAmpF, NoiseFrequency,
                                TTLAmpF, TTLs=False, Map=Map)

        print('Creating SoundGap...')
        Sound['NoGap'] = SigGen.SoundStim(Rate, SoundGapDur, SoundBGAmpF,
                                          NoiseFrequency, TTLAmpF,
                                          TTLs=False, Map=Map)
        Sound['Gap'] = SigGen.SoundStim(Rate, SoundGapDur, GapAmpF,
                                          NoiseFrequency, TTLAmpF,
                                          TTLs=False, Map=Map)
        # Sound['Gap'] = np.zeros(Sound['NoGap'].shape, dtype=Sound['NoGap'].dtype)
        # for F in range(Sound['Gap'].shape[3]):
        #     for A in range(Sound['Gap'].shape[2]):
        #         Sound['Gap'][:,:,A,F] = np.ascontiguousarray(Sound['Gap'][:,:,A,F])

        print('Creating SoundBGPrePulse...')
        Sound['BGPrePulse'] = SigGen.SoundStim(Rate, SoundBGPrePulseDur, SoundBGAmpF,
                                        NoiseFrequency, TTLAmpF,
                                        TTLs=False, Map=Map)

        print('Creating SoundLoudPulse...')
        Sound['LoudPulse'] = SigGen.SoundStim(Rate, SoundLoudPulseDur, SoundPulseAmpF,
                                       NoiseFrequency, TTLAmpF, Map=Map)

        print('Creating SoundBGAfterPulse...')
        Sound['BGAfterPulse'] = SigGen.SoundStim(Rate, SoundBGAfterPulseDur, SoundBGAmpF,
                                          NoiseFrequency, TTLAmpF,
                                          TTLs=False, Map=Map)

        print('Creating SoundBetweenStim...')
        Sound['BetweenStim'] = SigGen.SoundStim(Rate, max(SoundBetweenStimDur),
                                         SoundBGAmpF, NoiseFrequency,
                                         TTLAmpF,  TTLs=False, Map=Map)

        return(Sound)


    def PlayTrial(Sound, Stim, ArduinoObj, RealFreq, RealTrial, SBSSamples):
        Sound['BetweenStim'] = np.ascontiguousarray(Sound['BetweenStim'][:SBSSamples,:,0,RealFreq])
        for K in Sound:
            if K != 'BetweenStim':
                Sound[K] = np.ascontiguousarray(Sound[K][:,:,0,RealFreq])

        Stim.write(Sound['BetweenStim'])

        if ArduinoObj:
            ArduinoObj.write(b'd')

        Stim.write(Sound['BG'])
        Stim.write(Sound[RealTrial])
        Stim.write(Sound['BGPrePulse'])
        Stim.write(Sound['LoudPulse'])
        Stim.write(Sound['BGAfterPulse'])

        if ArduinoObj: ArduinoObj.write(b'w')


    # Level 1
    def Play(Sound, Stim, ArduinoObj, NoiseFrequency, SoundBetweenStimDur, NoOfTrials, SoundBGAmpF, SoundPulseAmpF, Rate, DataInfo, Normalize=True, PrePost=0, **kwargs):
        if 'ExpInfo' not in DataInfo: DataInfo['ExpInfo'] = {}
        for K in Sound.keys():
            if Normalize:
                AmpFFile = f"{DataInfo['Audio']['CalibrationFile']}/AmpF.txt"
                Sound[K] = DAqs.Normalize(Sound[K], AmpFFile, 'Out')

        print('Pseudo-randomizing frequencies...')
        TrialsStr = ['NoGap', 'Gap']
        Freqs = [In for In, El in enumerate(NoiseFrequency)]*NoOfTrials
        np.random.shuffle(Freqs)

        FreqSlot = [[0] for _ in range(len(Freqs)*2)]
        for FE in range(len(Freqs)):
            FreqSlot[FE*2] = (Freqs[0:FE+1].count(Freqs[FE])-1)*2
            FreqSlot[FE*2+1] = (Freqs[0:FE+1].count(Freqs[FE])-1)*2+1

        FreqOrder = [[0]]
        Rec = -1

        if ArduinoObj:
            ArduinoObj.write(b'O'); sleep(1) # Enable output mode

        print("Running...")
        Stim.start()
        # Play the Pre-trials
        for Pre in range(PrePost):
            Rec += 1
            RealFreq = -1
            FreqOrder[len(FreqOrder)-1] = [-1, -1]
            FreqOrder.append([0])
            SBSDur = random.randrange(SoundBetweenStimDur[0], SoundBetweenStimDur[1])

            print('Playing ', DataInfo['Audio']['Freqs'][RealFreq], ' Pre-trial', 'Rec', Rec)
            PlayTrial(Sound.copy(), Stim, ArduinoObj, RealFreq, 'NoGap', SBSDur*Rate)

        # Play the test trials
        for Hz in range(len(Freqs)):
            Trials = [0, 1]
            random.shuffle(Trials)
            print(str(Hz+1), 'of', str(len(Freqs)))

            for Trial in Trials:
                Rec += 1
                RealFreq = Freqs[Hz]
                RealTrial = FreqSlot[Hz*2+Trial]
                FreqOrder[len(FreqOrder)-1] = [Freqs[Hz], RealTrial]
                FreqOrder.append([0])
                SBSDur = random.randrange(SoundBetweenStimDur[0], SoundBetweenStimDur[1])

                print('Playing ', DataInfo['Audio']['Freqs'][RealFreq], ' trial ', TrialsStr[Trial], 'Rec', Rec)
                PlayTrial(Sound.copy(), Stim, ArduinoObj, RealFreq, TrialsStr[Trial], SBSDur*Rate)

        # Play the Post-trials
        for Post in range(PrePost):
            Rec += 1
            RealFreq = -1
            FreqOrder[len(FreqOrder)-1] = [-1, -2]
            FreqOrder.append([0])
            SBSDur = random.randrange(SoundBetweenStimDur[0], SoundBetweenStimDur[1])

            print('Playing ', DataInfo['Audio']['Freqs'][RealFreq], ' Post-trial', 'Rec', Rec)
            PlayTrial(Sound.copy(), Stim, ArduinoObj, RealFreq, 'NoGap', SBSDur*Rate)

        Stim.stop()
        FreqOrder.remove([0])

        DataInfo['ExpInfo']['FreqOrder'] = FreqOrder
        DataInfo['ExpInfo']['FreqSlot'] = FreqSlot
        DataInfo['ExpInfo']['Freqs'] = Freqs

        Txt.Write(DataInfo, DataInfo['InfoFile'])


    # Level 2
    def Run(AnimalName, StimType, BGIntensity, PulseIntensity,
            NoiseFrequency, SoundBGDur, SoundGapDur,
            SoundBGPrePulseDur, SoundLoudPulseDur,
            SoundBGAfterPulseDur, SoundBetweenStimDur, NoOfTrials,
            CalibrationPath, StimCh, TTLCh, RecCh,
            Rate=192000, BlockSize=384, Channels=2, BaudRate=Arduino.BaudRate, TTLAmpF = 1,
            PrePost=0, GapIntensity=[0], SoundBGAmpF={}, SoundPulseAmpF={}, GapAmpF={}, **Kws):

        Normalize = False
        if not len(SoundBGAmpF):
            SoundBGAmpF = DAqs.dBToAmpF(BGIntensity, CalibrationPath)
            Normalize = True
        if not len(SoundPulseAmpF):
            SoundPulseAmpF = DAqs.dBToAmpF(PulseIntensity, CalibrationPath)
            Normalize = True
        if not len(GapAmpF):
            GapAmpF = DAqs.dBToAmpF(GapIntensity, CalibrationPath)
            Normalize = True

        Date = datetime.now().strftime("%Y%m%d%H%M%S")
        InfoFile = '-'.join([Date, AnimalName, 'GPIAS.dict'])
        Kws = {**locals()}
        DataInfo = Txt.InfoWrite(**Kws)

        Map = [2,1] if 'GPIAS' in CalibrationFile else [1,2]
        Sound = GPIASSound(Map=Map, **DataInfo['Audio'])
        Stim = SoundCard.AudioSet(Rate, BlockSize, Channels, ReturnStream='Out')
        ArduinoObj = Arduino.CreateObj(BaudRate)
        if not ArduinoObj: print(Arduino.NotFoundWarning())

        try:
            Play(Sound, Stim, ArduinoObj, DataInfo=DataInfo, Normalize=Normalize, **DataInfo['Audio'])
        except KeyboardInterrupt:
                print(''); print('=====')
                print('Sorry for the wait.')
                if ArduinoObj:
                    print('Rebooting Arduino...')
                    Arduino.Reset(ArduinoObj)
                print('Bye!')
                print('====='); print('')

        print('Finished', AnimalName, 'GPIAS.')

    Avail = True

else:
    print(SoundCard.Msg)
    def GPIASSound(**kws): print(SoundCard.Msg)
    def PlayTrial(**kws): print(SoundCard.Msg)
    def Play(**kws): print(SoundCard.Msg)
    def Run(**kws): print(SoundCard.Msg)
    Avail = False



