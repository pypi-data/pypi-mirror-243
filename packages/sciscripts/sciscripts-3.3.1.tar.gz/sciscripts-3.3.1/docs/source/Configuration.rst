Configuration
=============

Triggering recordings
---------------------

For running experiments, SciScripts sends TTLs to signal start/stop of recordings through serial to an Arduino Uno. For this to work, the arduino should be programmed using the `SciScripts.ino` file. If no arduino is connected, the experiment will still run, but you will see a console warning, and recordings will have to be triggered manually on your recording system.

.. DANGER::
    If your system has an arduino connected that is NOT 
    running `SciScripts.ino`, SciScripts will NOT be    
    able to know, so it will send serial commands to the
    connected arduino and it will respond as per its    
    programming!                                        
                                                        
    I am NOT responsible for any damage or injury that  
    may happen because you ran SciScripts and your      
    arduino triggered a laser and burned your retina; or
    triggered a step motor and crashed a $600 probe, or 
    your priceless fingers.                             
                                                        
    YOU HAVE BEEN WARNED.                               
                                                        

Low latency sound system configuration
--------------------------------------

In order to achieve high sampling rates and low latency when running experiments, your operating system should be built with a real-time kernel, and all audio processing should run with real-time priority. You can follow any of the several instructions available online for setting a real-time kernel and real-time priorities for audio, or run an autio-tailored linux distribution, such as [decibel Linux](https://gentoostudio.org/).



Calibrating sound card
----------------------

For running experiments, SciScripts uses your computer's sound card as a DAQ. To achieve precise input/output, the sound card must be calibrated. Follow the instructions at the `Examples/CalibratingAudioSetup.py` script.



