# Changelog   

## 3.3.1

- [All] Improve and fix several functions;
- [All] Remove DATAPATH and ANALYSISPATH;
- [Analysis.Plot] Implement overview plotting of statistics calculated by `Analysis.Stats.Full`;
- [Analysis] Implement calcium imaging analysis (`Analysis.CalciumImaging`);
- [Docs] Add documentation and ReadTheDocs source.


## 3.2.1

- [Analysis.Stats] Rewrite higher-level functions to calculate effect and pairwise comparisons;
- [Analysis.Stats] Fix multiple effect tests p-correction;
- [Analysis.Stats] Deprecate AnOVa() and GetAnovaReport();
- [Analysis.Plot] Implement Circle() to plot circles based on X, Y and radius;
- [Exps.SoundMeasurements] Upgrade old code;
- [IO.Bin] Improve loading of lists;
- [CHANGELOG] Now only summary is available, commits can be found by tags.


## 3.1.1

### Summary
- Several functions under `Analysis.Stats` now are R-independent (therefore much faster);
- Several improvements to functions under `Analysis.Stats`;
- Several improvements to functions under `Analysis.Analysis`;
- Fix minor warnings and verbose output lacking consistency;
- Fix sound IO issues when running without calibration.


### Commits
```bash
27411af (HEAD -> Dev) Make `unidip` optional
ecaeca7 make pandas optional
b23ebef (origin/Dev) Account for NaNs
3b5eaa2 Update and improve formatting
9dbdf69 Implement Bartlett()
00d7788 Add effect size to TTest()
4f7bfb1 Force factors to be arrays
9aca56d Fix Paired/Unpaired test selection; Implement python Levene() and Shapiro()
58873c4 Fix LevelNames being ignored
2e61475 Fix ColorMix() override
dfaaeb5 Improve accuracy of peak detections
4664465 Try to load corrupted files even if some samples are lost
546df13 Fix typos and bad indentations
ee380f3 Add ChMap argument to Load()
4c72efa Update known probes
c3ad5bc Improve accuracy of GetPhaseRevCh() and GetComponents()
9888bdc Implement GetPhaseRevCh()
2494731 Make GetPhase() silent by default
b5dcc54 Make python Wilcoxon() and Friedman() default
16ce481 Implement PearsonRP2D()
7847f01 Implement Overview()
13684d3 Add EffectSize to _pyWilcoxon()
3ed26ea Make constrained_layout default
3896b3e Fix Upsample factors
3a2a670 Remove duplicate entry
632a9f6 Fix conflict
be7d414 Remove redundant warning
151130d Fix ReadAnalogIn
ab6648e Make SoundAmpF overridable
b516432 Make sounddevice optional
7fede52 Stop managing matplotlib parameters
754f216 Split Comodulation analysis
7eced23 Improve HartigansDip()
349b388 Implement MovingAvgWindow()
647af5a Make asdf and hdf5 optional
6c522d2 Make asdf optional
b610478 Replace struct by numpy
c015b7a Improve Arduino to read all AI and 8 DI
11053f0 Fix running without calibration
69b59b9 Fix running without calibration
aea92bb Implement automatic pairwise for more than 2 levels
00af34a Fix Normalize_Old() recursive call
7f75ab1 Improve HartigansDip() to accept FactorsGroupBy
bb3f0cc Improve PairwiseDescribe() to use FactorsGroupBy even when Factor is a string
8e572d7 Fix PairwiseDescribe() when Factor is a string
ea5b900 Fix error when there is a single `_` in folder name
126478c Implement Upsample()
aa4552e Implement KolmogorovSmirnov(); Implement PairwiseDescribe(); Make python t-test default
bd66b5d Fix arg propag for Levene(); Move try/except inside Shapiro() and Levene(); Silence R output
81cba91 Add missing fields to WaveAmp result
8dba4c5 Fix wave amp and lat calculations
f4c562d Implement HartigansDip() and fix Levene factor name
1f831a7 Fix ConvertTracesToArray()
838f604 Add effect size to GetAnovaReport() output
73cc969 Fix wrong print statement
f0d3db7 Unify Loading/Importing warnings
fea5893 Add prints, fix AnOVa() and GetAnovaReport()
3777bef Add argument to ScatterMean() for hiding the mean
e70a6e3 Add RemoveOffset argument to GetAmpEnv()
5e36614 Start implementing more R-independent tests
a4576e2 Add fix for np object arrays
10e1b1d Implemented TTest() in python
081d713 Start implementing scipy version
80d32f7 Improve output readability from GetAnOVaReport()
0811bd8 Fix wrong id being loaded
```


## 3.1.0

### Summary
- Full reorganization of `Analysis.Stats` function;
- Several improvements to `Analysis.ABRs`, `Analysis.GPIAS` and `Analysis.Plot`;
- Fix unit conversion issues;
- Several additions and improvements to `Analysis.Analysis`.

### Changes
```git
 SciScripts_Small.mplstyle              |  44 ++++
 sciscripts/Analysis/ABRs.py            | 109 ++++++----
 sciscripts/Analysis/Analysis.py        | 100 +++++++--
 sciscripts/Analysis/GPIAS.py           | 326 ++++++++++++++++-------------
 sciscripts/Analysis/Images.py          |   2 +-
 sciscripts/Analysis/Plot/ABRs.py       | 175 ++++++++--------
 sciscripts/Analysis/Plot/GPIAS.py      |   8 +-
 sciscripts/Analysis/Plot/Plot.py       | 166 ++++++++++-----
 sciscripts/Analysis/Stats.py           | 868 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------
 sciscripts/IO/Bin.py                   |  20 ++
 sciscripts/IO/IO.py                    |   3 +-
 sciscripts/IO/OpenEphys/Binary.py      |  63 +++---
 sciscripts/IO/OpenEphys/OpenEphys.py   |  41 ++--
 sciscripts/IO/OpenEphys/SettingsXML.py |  88 ++++----
 sciscripts/IO/Txt.py                   |  11 +
 sciscripts/IO/XML.py                   |  25 ++-
 16 files changed, 1404 insertions(+), 645 deletions(-)
 create mode 100644 SciScripts_Small.mplstyle
```


### Commits
effc6b2 Skip calculations that cannot be done  
367612f Fix fonts management  
7aec871 Improve Entropy() and add MovingAverage()  
4fc9be3 Allow different colors in ScatterMean()  
abdab8a Fix sub-anovas and sub-pwc names  
bc761b4 Fix default args in Multiple()  
96de829 Enable more complete output from GetMAF()  
e46f534 Change default StD to 1  
34470ac Implement MultipleSxx(); Add LegendArgs argument to Multiple()  
b1d2bd4 Fix old Normalize()  
356832f Implement ListToArrayNaNFill()  
511fb8a Return more info on WaveAmp and GetThresholds  
ab4815d Fix multiple comparisons corrections for Shapiro() and Levene()  
90eae9e Implement style with smaller fonts  
53f93e1 Fix wrong Bits-uV conversion on old recs  
91b9afe Update old functions  
c775efb Rewrite Normalize to fit an arbitrary range  
1fd6052 Implement Transpose()  
9e79aeb Process traces at OrganizeRecs() instead of anywhere else  
46ad11b Use a better XML-to-dict conversion  
33f4068 Fix bad loading when unit is `uV` or `mV`  
311f615 Decrease stim alpha and fix limits  
5729707 Change shallow to deep copies; Isolate AmpCalc from IndexCalc  
1b893f5 Allow max=0 in Normalize(); Make GetAmpEnv() silent by default  
2d4a472 Fix pAdj being ignored  
deced17 Fix Max conditional in PToStars()  
177dadf Fix Set() ignoring z args; Add generalized Triang3D() from Analysis.Plot.ABRs  
87f350f Upgrade functions; Implement Multiple3D(); Generalize Triang3D() and move it to Analysis.Plot.Plot  
5e4d1bd Implement vertical significance bars; Ignore NaNs in MeanSEM(), BoxPlots(), AllCh() and CheckData()  
358b413 Fix one-way anova; Implement PairwiseComp() and IsMatched()  
1ee52bc Ignore NaNs in Normalize()  
7cf807c Add MergeDictsAndContents()  
6f525d5 Add GetAnovaReport, GetSigEff, Friedman, Levene, and KruskalWallis; Add conditional tests according to normality and homogeneity  
ed537d7 Fix extra listing in GetSigEff()  
55b567e Complete rewrite of t-test, anova and RModelToDict()  
09f400f Fixing NaNs in ScatterMean()  
142e3be Implement recursive RModelToDict() and AnOVaR  
22db25c Fix returning levels for factors  
73eab82 Implement DictListsToArrays()  
c8450d9 Update to BitsToVolts()  
d9c2017 Add exception for unknown data type in GetSpaces()  
2bb1ef7 Remove old UniqueStr refs  
6b11590 Implement factor names  
8655ba9 Fix typo  
535256a Add NFFT and Verbose args to PSD()  
f80b56b WC: fixing Sxx  
4e4a59d Split Normalize() in 2 functions  
c2c1252 Add Start argument to GenColormap(); Fix BoxPlots() X positions  
64b7bb9 Keep F unidimensional when PSD input is 2d  
be7a522 Fix remaining RObj  


## 3.0.8

### Summary
- Make `cv2` and `rpy2` optional;  
- Fix and improve `Analysis.Stats`, specially `AnOVa()`;
- Implement read/write of scipy csc sparse matrix;  
- Improve documentation and decrease default verbosity.  

### Commits
3ff09ab Make Upsample2d accept 3d arrays, fix documentation and make functions quieter  
ba06f7e Fix for loading new open-ephys binary (finally)  
80dc7f8 Fix Spectrogram documentation  
f9492e9 Fix pairwise comparisons for one-way anova  
7f2f284 Make Slice() silent  
1481940 Add StD argument to be passed to GetPeaks()  
b908e74 Fix for when no peaks are found  
a2494be Make rpy2 optional  
2d970c1 Remove: too premature  
ed016e4 Implement Shapiro normality test  
62a28f5 Fix 1-way AnOVa and implement Kruskal Wallis and Wilcoxon tests  
5747db8 Implement parametric switch  
5265814 Make cv2 optional  
137e135 Fix zlim argument  
aee6327 Fix loading lists  
301602d Make Slice() silent by default  
dbf3689 Implement csc sparse matrix  
40f2ed2 Fix several errors in reading videos  
6ee9896 Implement functions for getting ERP components  
3f4111d Implement GetComponents()  
a3ec1e1 Remove deprecated `set_smart_bounds`  
9dd1cce Add matplotlib style  
e6eb304 Fix AllCh() scalebar position  
303d67f Implement angle calculation in EucDist()  
865896d Fix redundant entropy calculations  
cd8ac1d Fix typo leading to wrong within/between factor type  
fbe928b Add ColorMix() and ERPs-related plots  


## 3.0.7

### Summary   
- Change to a new release workflow;   
- Start implementing video under `sciscripts.IO` and `sciscripts.Analysis`;   
- Make several functions less verbose by default;   
   
### Commits   
7a8cc03 Implement GetInfo()  
c63db02 Implement GetLedBlinkStart()  
e57ff9b Add cv2 dependency  
b3dbdb5 Start implementing video analysis  
ea9b898 Fix EucDist() docstring  
c388b67 Replace XValues by X  
e4ee481 Fix reading wrong files and Fix wrong recursion of PSD()  
0c0e103 Allow GetAllTrials() to receive any arguments as input  
ef4858f Change default Verbose to False  
e7cd05a Add prints for batch cell  
5ac2fe4 Reduce IO verbosity  
171b36f Decrease verbosity when slicing recs  
827b310 Add Verbose= argument to QuantifyTTLs()  
f279b67 Fix wrong variable  
061f9c2 Fix missing whitespaces  

   
## 3.0.6   
   
### Summary   
- Improve several functions under `sciscripts.Analysis.Analysis`;   
- Improve `README.md` A LOT;   
- Remove matplotlib backend management;   
- Remove old and buggy code related to digital TTLs processing;   
- Add arduino code to allow SciScripts to control an arduino board;   
- Add docstrings, specially on `sciscripts.Analysis.Analysis`;   
- Add GPIAS analysis example.   
   
### Commits   
449e878 Update example   
1a0b28b Make better plots   
be3277f Implement GetTime()   
aa74be6 Move warnings from Exps to IO   
dbeece0 Change double hashes to single hashes   
161f176 Make paths clearer   
9396481 Add GPIAS analysis example   
7c87886 Fix saving of files   
6653053 Make arguments sane   
138acb7 Fix wrong Threshold variable   
89b2831 Remove ancient import   
19fd762 Fix error when trying to write arrays with shape `()`   
a0a1f6c Fix extra return of useless EventsDict   
cc3b5ec Move QuantifyTTLsPerRec() to QuantifyTTLs()   
f460041 Adding docstrings   
6536e8c Adding docstrings   
05c2aaf Really fix DANGER box   
9ecde5e Get rid of AnalogTTLs   
b95b8f6 Add docstrings   
13456c1 Fix DANGER box   
3e4425c Move GenTTLVector from Analysis to SigGen, Implement GetOverlap()   
96c8c96 Update SliceData() to Slice()   
567492e Load plt from Plot.Return()   
d8cf7c8 Remove backend management, Implement MeanSEM()   
309f89f Change SliceData() to Slice(), Add arguments to Normalize()   
004ce2b Add background and arduino warnings   
793c052 Add InchToPoint   
9702f99 Change default backend to `Qt5Agg`   
ec220c0 Add examples   
057a453 Fix GapIntensity type   
7a7f158 Improve documentation formatting   
e355d9c Add .ino script for setting up an arduino uno to work with SciScripts   
6389d81 Explain NoiseFrequency values   
1f68705 Implement controlling spines position through AxArgs   
   

## 3.0.5   
   
### Summary   
- Fix error when running repeated measures for AnOVa;   
- Fix wrong __init___.py files;   
- Add ABRs documentation.   
   
### Commits   
9834b7e Fix repeated measures for AnOVa   
637b609 Fix colormap in scatter plots   
03fb6cb Adding docstrings   
7a9c002 The imports were needed after all   
c4767e7 Handle ZeroDivisionError if mic is off   
5e1a6ec Fix typos   
   
   
## 3.0.4   
   
### Summary   
- Better handling of errors;   
- Fix recursive loading of hdf5 files;   
- Add warnings, documentation and examples.   
   
### Commits   
f175eef Add Examples folder   
aa74526 Handle errors, add warnings and documentation   
aa74d40 Make LaserType optional   
9010237 Fix error when NoiseFrequency is None   
abcaaf9 Make Klusta and SpyKING Circus optional   
86634ac Fix SyntaxWarning   
a3b7996 Fix missing __init__.py   
b3f0fb6 Fix excessive imports   
6dbd443 General clean-up of old, not anymore relevant, comments   
7dd9906 List optional dependencies   
28e0bfe Add warnings about how specific those modules are   
bc87bd9 Fix recursive loading of hdf5 files   
28d1775 Implement gap intensity (so now PPI is also possible)   
f7abcce Put experiment functions in their rightful place   
   
## 3.0.3   
   
### Summary   
- Fix missing package dependencies;   
- Update open-ephys file loading;   
- Fix __init__.py submodule files;   
- Last chance for xdpyinfo to cause less trouble than it solves.   
   
### Commits   
8852dd9 Fix importing submodules   
add798c Update DataLoader   
aad356c Add marker= arg to GenLegendHandle()   
c60bad5 Change plots from pdf to png   
7804ea5 Last chance for xdpyinfo   
7fd1d05 Update plots   
6355534 Add plots   
b3811e5 Update loading of open-ephys binary files   
f017c23 Adding print statements   
ea487c9 Add PearsonRP()   
de2df78 Add GenColorMap()   
4ce59f1 Remove implicit conversions in PSTHLine()   
fb38505 Implement Upsample2d()   
1018b63 Add missing __init__.py to Plot and Unit submodules   
0a2e6c7 Start implementing functions for image analysis   
b683628 Add missing AsMMap argument   
915831f Fix AnOVa() output   
0d0d8b7 Remove dpi arguments; Improve Set() and SignificanceBar()   
5c5a2f3 Add GetStrongestCh()   
84a7114 Update setup.py and CHANGELOG   
d5ae173 Specify open-ephys dependency   
   
   
## 3.0.2   
   
### Summary     
- Add `try` statements to make `xdpyinfo` and `xrandr` truly optional;     
- Add option to load binary data as array instead of mmap;     
- Improve anova and t-test output;     
- Start implementing vocalization signal processing.   
   
### Commits     
```   
f7c2589 Add automatic plot formatting   
8829b53 Adding documentation   
327a1c9 Make xdpyinfo and xrandr truly optional   
52ed7cb Add AsMMap= argument to Read()   
483644c Add Cohen's d for t-test   
48e3d73 Add lw= argument to LinePSTH()   
99dffad Fix SameScale() errors   
5b7003f Implement IsInt() and IsFloat()   
843a7e2 Update Slice arguments   
6ab908b Fix Tones playback   
f38f75a Finish implementing AnOVa   
fdb1200 Fix Axes Set and ScatterMean line colors   
0361276 Fix Analysis function vs module conflict   
1881099 Fix missing import   
1d7dca9 Comment unnecessary print   
c60add0 Update according to new matplotlib version   
9392539 Fix loading different setups   
b911c29 Fix LastCommonPath   
e7a1aba Add marker argument to Scatter3D   
0472e92 Implement .fig loading as dict   
9eed20c Fix Scatter3D return ax   
6f6a612 Add ScaleBar   
8a2669c Add Scatter3D   
872a15f Fix Mat.Read()   
089d4d8 Add recursive function to clean structs   
1fb61e5 Move back to .mat files   
5ddfe6c Fix syntax error   
00cbefa Fix read/write functions   
1d48e81 Change Spectrogram output Fxx and Txx to 1d   
296b15e Fix NFFT and implement GetFxx   
1e4003b Fix Wav loading Ch dimensions   
7caa1a7 Try to implement USVDetect   
b26dc36 Make Spectrogram work with 2dArrays   
7e7edeb Fix wrong import   
83a1b29 Implement reading of MouseProfilerTracker XML files   
3b61196 Implement lower-level returning of Tree and Root   
534d6a3 Replace .mat by .dat   
9d050ca Implement "Get coordinate by mouse click"   
dfff54e Start implementing Vocalizations analysis   
2c9e537 Implement Peaks colors   
a800e87 Removing GetDuplicates   
cd6f9f2 Trying to implement GetDuplicates   
c73d3d4 fix missing :   
d557e4a Implement WhereMultiple   
354f5fc Implement conversion from Kwik to Bin   
13b278e Implement distance and area calculations   
4a3749f Implement animation plot   
c49d8e6 Implement entropy calculations   
```   
