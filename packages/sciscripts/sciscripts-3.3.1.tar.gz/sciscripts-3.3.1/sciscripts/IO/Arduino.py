# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 2015

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts

This is a script to define functions allowing Arduino/Python integration.
"""

print('[IO.Arduino] Loading dependencies...')
import numpy as np, time

from scipy.interpolate import interp1d
from serial import Serial
from serial.tools.list_ports import comports
from threading import Thread
print('[IO.Arduino] Done.')

BaudRate = 115200 # To match SciScripts.ino

## Level 0
def CreateObj(BaudRate):
    Port = comports()
    if Port: Arduino = Serial(Port[-1][0], BaudRate)
    else: Arduino = None

    return(Arduino)


def GetFullLine(SerialObj):
    SerialObj.flushInput()
    Char = SerialObj.read().decode()
    while Char != '\n':
        SerialObj.flushInput()
        Char = SerialObj.read().decode()

    Line = Char
    while len(Line)<5 or Line[-1] !='\n':
        Line += SerialObj.read().decode()

    return(Line)


SerialInput_LastLine = ''
SerialInput_Started = False


def ReadSerialInput(SerialObj):
    global SerialInput_LastLine
    global SerialInput_Started
    SerialInput_Started = True

    buffer_string = ''
    while True:
        new = ''
        while new == '':
            try:
                new = SerialObj.read(SerialObj.inWaiting()).decode()
            except:
                new = ''

        buffer_string = buffer_string + new
        if '\n' in buffer_string:
            lines = buffer_string.split('\n')
            SerialInput_LastLine = lines[-2]
            buffer_string = lines[-1]


def GetSerialData(Channels, Rate, ArduinoObj, FramesPerBuf=128, Interp=True):
    Data = np.zeros((FramesPerBuf, len(Channels)), dtype=int)
    Time = np.zeros(FramesPerBuf, dtype=int)

    global SerialInput_Started
    if not SerialInput_Started:
        Thread(target=ReadSerialInput, args=(ArduinoObj,)).start()

    LastTime = 0
    for F in range(FramesPerBuf):
        Start = time.perf_counter()

        Line = []
        while len(Line) != 16:
            if time.perf_counter()-Start > 10:
                print('Cannot read a line for 10s. Giving up.')
                return(Data[:F,:], Time[:F])

            # Line = GetFullLine(ArduinoObj)
            # Line = Line.split('\n')[1].split('\r')[0].split('\t')

            Line = SerialInput_LastLine
            Line = Line.split('\r')[0].split(',')
            Line = [_ for _ in Line if len(_)]

            if len(Line):
                if int(Line[0]) in Time or int(Line[0]) < Time.max():
                    Line = []

        Data[F,:] = np.array(Line[1:-1]).astype(int)[Channels]
        Time[F] = int(Line[0])

        if not Interp:
            End = time.perf_counter() - Start
            if End < 1/Rate: time.sleep((1/Rate)-End)

    if Interp:
        TimeI = np.arange(Time[0], Time[-1], 1000/Rate)
        DataI = np.zeros((TimeI.shape[0], Data.shape[1]), dtype=float)
        for Ch in range(Data.shape[1]):
            f = interp1d(Time, Data[:,Ch], bounds_error=False)
            DataI[:,Ch] = f(TimeI)

        Data = DataI
        Time = TimeI

    return(Data, Time)


def NotFoundWarning():
    Msg = f'=============== WARNING =================\n'
    Msg += 'No Arduino detected!!!\n'
    Msg += 'NO DIGITAL TTLs WILL BE DELIVERED!!!\n'
    Msg += 'YOU HAVE BEEN WARNED!!!\n'
    Msg += '\n'
    Msg += 'Analog TTLs will still work.\n'
    Msg += '=========================================\n'
    return(Msg)



def Reset(Obj):
    Obj.setDTR(False)
    Obj.flushInput()
    Obj.setDTR(True)
    return(None)


