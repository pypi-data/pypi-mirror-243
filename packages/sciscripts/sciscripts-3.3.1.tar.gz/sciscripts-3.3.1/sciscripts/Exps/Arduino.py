#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20210410

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts
"""

ScriptName = 'Exps.Arduino'
print(f'[{ScriptName}] Loading dependencies...')
import inspect, os
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from datetime import datetime
from time import sleep

from sciscripts.IO import Arduino, Txt
print(f'[{ScriptName}] Done.')


def ReadAnalogIn(Channels, Rate=100, BaudRate=Arduino.BaudRate, FramesPerBuf=128, Interp=True, AnimalName='Animal', FileName='', **Kws):
    """
    Grab serial data and continuously write to a .dat file.

    The shape will be in the filename.
    """
    FunctionName = inspect.stack()[0][3]

    ArduinoObj.write(b'I'); sleep(1) # Enable input mode
    ArduinoObj = Arduino.CreateObj(BaudRate)

    Date = datetime.now().strftime("%Y%m%d%H%M%S")
    if not len(FileName):
        FileName = '-'.join([Date, AnimalName, 'ArduinoRec'])
    InfoFile = f'{FileName}.dict'

    Kws = {**locals()}
    DataInfo = Txt.InfoWrite(**Kws)

    DataLen = 0
    try:
        print(f'[{ScriptName}.{FunctionName}] [00:00:00] Recording..')
        # ThisSec = 1; TimeStart = 0
        while True:
            Data, Time = Arduino.GetSerialData(Channels, Rate, ArduinoObj, FramesPerBuf, Interp)
            # if TimeStart == 0: TimeStart = Time[0]
            # if (Time[-1]-TimeStart)//10 >= ThisSec:
                # ThisTime = datetime.strptime(str(ThisSec*10), '%S').strftime('%H:%M:%S')
                # print(f'[{ScriptName}.{FunctionName}] [{ThisTime}] Recording..')
                # ThisSec += 1
            with open(Date+'.dat', 'ab') as File: File.write(Data.tobytes())
            with open(Date+'_Time.dat', 'ab') as File: File.write(Time.tobytes())
            DataLen += Data.shape[0]

    except KeyboardInterrupt:
        print('Done.')
        pass

    Out = f'{FileName}_{DataLen}x{len(Channels)}.dat'
    os.rename(Date+'.dat', Out)
    Out = f'{FileName}_Time_{DataLen}x1.dat'
    os.rename(Date+'_Time.dat', Out)
    print(f'Recorded to {FileName}*.dat .')


def CheckPiezoAndTTL(Channels, Rate=100, BaudRate=Arduino.BaudRate, FramesPerBuf=192, Interp=True, XLim=None, YLim=None):
    ArduinoObj.write(b'I'); sleep(1) # Enable input mode
    ArduinoObj = Arduino.CreateObj(BaudRate)

    Fig = plt.figure()
    Ax = plt.axes(xlim=XLim, ylim=YLim)

    Plots = [[], []]
    Plots[0] = Ax.plot([float('nan')]*FramesPerBuf, lw=1)[0]
    Plots[1] = Ax.plot([float('nan')]*FramesPerBuf, lw=1)[0]

    def AnimInit():
        for Plot in Plots:
            Plot.set_ydata([])
        return Plots

    def PltUp(n):
        Data, Time = Arduino.GetSerialData(Channels, Rate, ArduinoObj, FramesPerBuf, Interp)

        for Index, Plot in enumerate(Plots):
            Plot.set_ydata(Data[:,Index])
            # Plot.set_xdata(Time[:,Index])

        return tuple(Plots)

    Anim = animation.FuncAnimation(Fig, PltUp, frames=FramesPerBuf, interval=10, blit=False)


def Oscilloscope(Channel, Rate=100, BaudRate=Arduino.BaudRate, FramesPerBuf=192, Interp=True, XLim=None, YLim=None):
    ArduinoObj.write(b'I'); sleep(1) # Enable input mode
    ArduinoObj = Arduino.CreateObj(BaudRate)

    Fig = plt.figure()
    Ax = plt.axes(xlim=XLim, ylim=YLim)
    Plot = Ax.plot([float('nan')]*FramesPerBuf, lw=1)[0]

    def AnimInit():
        Data = []
        Plot.set_ydata(Data)
        return Plot,

    def PltUp(n):
        Data, Time = Arduino.GetSerialData([Channel], Rate, ArduinoObj, FramesPerBuf, Interp)
        Plot.set_ydata(Data[:,0])
        # Plot.set_xdata(Time[:,0])
        return Plot,

    Anim = animation.FuncAnimation(Fig, PltUp, frames=FramesPerBuf, interval=10, blit=False)


