Modules
=======

sciscripts.Analysis
-------------------
Module for calculations, signal processing and plotting. Useful for general-purpose analysis, and specially useful for analyzing experiments recorded using the `sciscripts.Exps` module.

Submodules are higher-level functions implementing the lower-level functions at `sciscripts.Analysis.Analysis`.


sciscripts.Analysis.Stats
^^^^^^^^^^^^^^^^^^^^^^^^^
Functions and wrappers for several calculations. Specifically, the `sciscripts.Analysis.Stats.Full` function takes the data, a list of factors and some more data information, and apply the most appropriate effect and post-hoc test:

.. image:: StatsSchem.svg


sciscripts.Exps
---------------
Module for preparing and running stimulation paradigms for several experiments. Depends on `sciscripts.IO` for generating signals and writing stimulus to data acquisition cards.

SciScripts can use a sound card to provide sound stimulation (d'oh!), but also to provide digital triggers (with a simple addition of a diode at the device's input). This allows for, as example, providing combined sound and laser stimulation (see `Examples/SoundAndLaserStimulation.py <https://gitlab.com/malfatti/SciScripts/-/blob/main/Examples/SoundAndLaserStimulation.py>`_). Combined with a real-time kernel and a well setup sound system, you can achieve a very precise stimulation, at high sampling rates (192kHz in our system; see `Malfatti et al., 2021, Figure 1 <https://doi.org/10.1523/ENEURO.0413-20.2020>`_):

.. image:: SLStim.jpg



sciscripts.IO
-------------
Module for generating signals, interface with input-output cards and reading/writing of several different file types.

Submodules are higher-level functions implementing the lower-level functions at `sciscripts.IO.IO`.



