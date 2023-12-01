Dependencies
============


Software
--------

#. Mandatory
    1.1. OS:
        - Linux
    1.2. Python:
        - matplotlib
        - numpy
        - scipy
#. Optional
    2.1. OS:
        - xdpyinfo [needed for adjusting default figure size and dpi]
        - xrandr [needed for adjusting default figure size and dpi]
    2.2. Python:
        - asdf [needed for reading/writing ASDF files]
        - cv2 [needed for video analysis]
        - h5py [needed for reading/writing hdf5 files]
        - klusta [needed for spike clustering analysis]
        - opencv-python [needed for video analysis and IO]
        - pandas [needed for statistics]
        - pyserial [needed for Arduino control]
        - pytables [needed for statistics]
        - rpy2 [needed for statistics]
        - sounddevice [needed for sound stimulation]
        - spyking-circus [needed for spike clustering analysis]
        - statsmodels [needed for statistics]
        - unidip [needed for statistics]


Hardware
--------

#. Analysis:
    - [None]
#. Exps:
    - Sound card
    - Arduino Uno [optional, needed for syncing devices and timestamps]
    - Data Acquisition card [optional, needed for recordings, tested with Open-ephys DAQ]
#. IO:
    - Sound card [for sciscripts.IO.SoundCard]
    - Arduino Uno [for sciscripts.IO.Arduino]



