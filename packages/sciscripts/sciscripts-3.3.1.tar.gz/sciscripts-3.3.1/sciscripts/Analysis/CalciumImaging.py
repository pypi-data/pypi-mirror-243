#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20230314

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts

Functions to analyze calcium imaging videos. Requires CaImAn for motion
correction, source extraction, components evaluation and multisession
registering.
"""


ScriptName = 'Analysis.CalciumImaging'

print(f'[{ScriptName}] Loading dependencies...')
import scipy.io as sio
import numpy as np
import gc, inspect, json, os, psutil, re, time, shutil

from copy import deepcopy as dcp
from datetime import datetime, timedelta
from multiprocessing import Array as mpArray, Lock as mpLock
from glob import glob
from scipy import sparse

try:
    import caiman as cm
    from caiman.base.rois import register_multisession
    from caiman.source_extraction import cnmf
    from caiman.utils import visualization
    from caiman.utils.visualization import inspect_correlation_pnr
    from caiman.motion_correction import MotionCorrect
    from caiman.source_extraction.cnmf import params
    AvailCaImAn = True
except ModuleNotFoundError as e:
    AvailCaImAn = False

from sciscripts.Analysis.Analysis import PolygonArea, GetPeaks
from sciscripts.IO import IO
from sciscripts.Analysis import Videos

AvailMsg = '[{sm}.{fn}] Module `{module}` not available.'

ParamsVidDef = dict(
    CopyVideos=False,
    FPSDefault_v3=30,
    FPSDefault_v4=20,
    Downsampling=3,
    DownsampleCodec=827737670,         # FourCC codec
    MotionCorr=True
)

ParamsMCDef = dict(
    border_nan = 'copy',               # replicate values along the boundaries
    decay_time = 0.4,                  # length of a typical transient in seconds
    gSig_filt = (3, 3),                # size of high pass spatial filtering, used in 1p data
    isnonrigid = False,                # flag for non-rigid motion correction
    max_deviation_rigid = 3,           # maximum deviation allowed for patch with respect to rigid shifts
    max_shifts = (5, 5),               # maximum allowed rigid shift
    niter_rig = 1,
    num_splits_to_process_rig = None,  # intervals at which patches are laid out for motion correction
    only_init_patch = True,
    overlaps = (24, 24),               # overlap between patches (size of patch strides+overlaps)
    pw_rigid = False,                  # flag for performing piecewise-rigid motion correction (otherwise just rigid)
    strides = (48, 48),                # start a new patch for pw-rigid motion correction every x pixels
    use_cuda = True,                   # Set to True in order to use GPU
    memory_fact = 0.8,                 # Memory to allocate. 1 ~ 16Gb; 0.8 ~ 12Gb.

    splits_rig = 20,                   # for parallelization split the movies in num_splits chuncks across time
                                       # if none all the splits are processed and the movie is saved
)

ParamsSEDDef = dict(
    Ain = None,                           # possibility to seed with predetermined binary masks
    K = None,                             # upper bound on number of components per patch, in general None
    center_psf = True,                    # leave as is for 1 photon
    del_duplicates = True,                # whether to remove duplicates from initialization
    frames_window = 250,                  # number of frames for computing running quantile
    gSig = (3, 3),                        # gaussian width of a 2D gaussian kernel, which approximates a neuron
    gSiz = (15, 15),                      # average diameter of a neuron, in general 4*gSig+1
    merge_thr = .65,                      # merging threshold, max correlation allowed
    method_deconvolution = 'oasis',       # 'oasis' or 'cvxpy'
    method_init = 'corr_pnr',             # use 'corr_pnr' for 1 photon
    min_corr = .8,                        # min peak value from correlation image
    min_pnr = 8,                          # min peak to noise ration from PNR image
    normalize_init = False,
    only_init = True,                     # set it to True to run CNMF-E
    p = 1,                                # order of the autoregressive system
    quantile_min = 8,                     # quantile used to estimate the baseline
    rf = 40,                              # half-size of the patches in pixels. e.g., if rf=40, patches are 80x80
    ring_size_factor = 1.4,               # radius of ring is gSiz*ring_size_factor
    ssub_B = 2,                           # additional downsampling factor in space for background
    update_background_components = True,  # sometimes setting to False improve the results
    use_cuda = True,                      # Set to True in order to use GPU

    low_rank_background = None,  # None leaves background of each patch intact,
                                 # True performs global low-rank approximation if nb>0

    stride = 20,       # amount of overlap between the patches in pixels
                       # (keep it at least large as gSiz, i.e 4 times the neuron size gSig)

    tsub = 1,        # downsampling factor in time for initialization,
                     # increase if you have memory problems

    ssub = 1,        # downsampling factor in space for initialization,
                     # increase if you have memory problems
                     # you can pass them here as boolean vectors

    nb = 1,          # number of background components (rank) if positive,
                     # else exact ring model with following settings
                     #     nb= 0: Return background as b and W
                     #     nb=-1: Return full rank background B
                     #     nb<-1: Don't return background

    nb_patch = 0,    # number of background components (rank) per patch if nb>0,
                     # else it is set automatically
)

ParamsCEDef = dict(
    min_SNR = 3,        # adaptive way to set threshold on the transient size
    use_cnn = False,
    rval_thr = 0.85,    # threshold on space consistency
)

print(f'[{ScriptName}] Done.')



#%% Level 0 ============================================================
def AcceptedAssigned(Assignments, Accepted):
    AsAc = np.array([[n in Acc for n in Assignments[:,S]] for S,Acc in enumerate(Accepted)]).T
    AsAc = AsAc.sum(axis=1)>0#=len(ASessions)#-1
    Assignments = Assignments[AsAc,:]

    return(Assignments)


def GetFilesList(FolderData, FolderAnalysis, Info):
    if "miniscopes" in Info.keys():
        FileRoot = '/'.join(FolderData.split('/')[:-1])
        filesList = sorted(glob(f"{FileRoot}/{Info['miniscopes'][0].replace(' ','_')}/*"))
        auxFileList = sorted(glob(f"{FileRoot}/*.*"))
        auxFileList = [
            _ for _ in auxFileList
            if _.endswith('.csv') or _.endswith('.json')
        ]

        auxSubFiles = sorted(glob(f"{FileRoot}/*/*json"))
        auxSubFiles += sorted(glob(f"{FileRoot}/*/*csv"))
    else:
        filesList = sorted(glob(f"{FolderData}/*"))
        auxFileList = []
        auxSubFiles = []

    msFileList = []
    for i in filesList[:]:
        if i.endswith('.avi'): msFileList.append(i)
        if i.endswith('.dat'): auxFileList.append(i)

    msfl = []
    for v in msFileList:
        try:
            _ = int(re.sub('[msCam.avi]','', v.split('/')[-1]))
            msfl.append(v)
        except ValueError:
            continue
    msFileList = msfl

    msFileList = sorted(
        msFileList,
        key=lambda x: int(re.sub('[msCam.avi]','', x.split('/')[-1]))
    )

    DataToAnalysisBase = f"{FileRoot}/{Info['miniscopes'][0].replace(' ','_')}" if "miniscopes" in Info.keys() else FolderData

    msLocalFileList = [
        fname.replace(DataToAnalysisBase, FolderAnalysis)
        for fname in msFileList
    ]

    auxLocalSubFiles = [
        f"{FolderAnalysis}/{_.split('/')[-2]}_{_.split('/')[-1]}"
        for _ in auxSubFiles
    ]

    auxLocalFileList = [
        fname.replace(FileRoot, FolderAnalysis)
            if "miniscopes" in Info.keys()
            else fname.replace(FolderData, FolderAnalysis)
        for fname in auxFileList
    ]

    auxFileList += auxSubFiles
    auxLocalFileList += auxLocalSubFiles

    return(msFileList, auxFileList, auxSubFiles, msLocalFileList, auxLocalFileList)


def GetSigCoActivity(Data, ShuffleRounds=1000, Alpha=0.05, Parallel=None):
    """
    Get significant co-activity threshold for a group of neurons.

    Parameters
    ----------
    Data: 2d array
        Input array with Samples x Neurons dimensions
    ShuffleRounds: int
        Number of shuffles.
    Alpha: float
        Significance level.
    Parallel: int or None
        Number of simultaneous processes to run. If `None` all but one
        core will be used.

    Returns
    -------
    SigCoAct: float
        Threshold for significant co-activation.
    ShuffleCoAct: 2d array
        Array of Shuffles x Samples.

    Inspired by findSignificantCoactivity(), by Moelter (2018), at
    https://github.com/GoodhillLab/neural-assembly-detection/
    """
    FN = inspect.stack()[0][3]

    SampleNo = Data.shape[0]
    lock = [mpLock() for _ in range(SampleNo)]
    d = [
        mpArray('f', np.zeros(ShuffleRounds), lock=lock[_])
        for _ in range(SampleNo)
    ]

    def RRun(N,DataRun,d):
        rng = np.random.default_rng()
        ShuffleSum = np.sum(rng.permutation(DataRun, axis=0), axis=1)
        # print(N,ShuffleSum)

        for S in range(len(d)): d[S][N] = ShuffleSum[S]

    print(f'[{ScriptName}.{FN}] Getting significant co-activity...')
    IO.MultiProcess(RRun, [(_,Data,d) for _ in range(ShuffleRounds)], Parallel)

    print(f'[{ScriptName}.{FN}] Getting activity threshold...')
    ShuffleCoAct = np.array(d).T
    SigCoAct = np.percentile(ShuffleCoAct, (1 - Alpha) * 100)

    gc.collect()
    print(f'[{ScriptName}.{FN}] Done.')

    return(SigCoAct, ShuffleCoAct)


def GetCoMsArea(SFP, Dims):
    """
    SFP: sparse matrix
        Spatial footprints of recording.

    Dims: tuple,list,array
        Real dimensions of the SFP.
    """
    Dims = tuple(Dims)

    CoMs, Coords = (
        [_[K] for _ in visualization.get_contours(SFP, Dims)]
        for K in ('CoM','coordinates')
    )

    Areas = np.array([PolygonArea(_[:,0], _[:,1]) for _ in Coords])
    CoMs = np.array(CoMs)

    return(CoMs, Areas)


def PrintLog(Msg):
    print(Msg)
    return([Msg])


def StepMark(File, Content=[]):
    with open(File, 'w') as F: F.writelines(Content)
    return(None)


def Write(Data, OutFile):
    Log = []
    if '.' not in OutFile.split('/')[-1]:
        os.makedirs(OutFile, exist_ok=True)
        IO.Bin.Write(Data, OutFile)

    elif OutFile[-4:] == '.dat': IO.Bin.Write(Data, OutFile)
    elif OutFile[-4:] == '.mat': sio.savemat(OutFile, Data)

    else:
        msg = '''
Supported `Outfile`:
    - Folder (no extension (`Data` have to be `dict`), will have .dat files inside);
    - .mat file (`Data` have to be `dict`);
    - .dat file (`Data` have to be `array_like`).
'''
        raise TypeError(msg)

    return(None)


#%% Level 1 ============================================================
def CNMFeRun(
        images, bord_px, sed_dict, ce_dict, cnmf_opts, FolderAnalysis,
        OutFile, OutputExt, Parallel=None, Return=True
    ):
    """
    Perform a projection of correlated pixels, run CNMFe and evaluate components.

    The components are evaluated in three ways:
    1. the shape of each component must be correlated with the data;
    2. a minimum peak SNR is required over the length of a transient;
    3. each shape passes a CNN based classifier, if enabled.

    Parameters
    ----------
    Parallel: int or None
        Amount of processes for CNMF cluster. If None, the number of processes
        will be `(RAMAvailGB-0.5)//3`, since each process uses approximately
        3GB.

    Return: bool
        Whether to return the resulting CNMFe dict.

    Returns
    -------
    CNM: dict
        All CNMFe calculations. Only returned if `Return` is `True`.
    """
    FN = inspect.stack()[0][3]
    if not AvailCaImAn:
        raise ModuleNotFoundError(
            AvailMsg.format(sm=ScriptName, fn=FN, module='caiman')
        )

    Log = []

    CC = dcp(Parallel)
    if CC is None:
        CC = (psutil.virtual_memory().available-0.5)/(1024**3)
        CC = CC/3

    CC = int(CC)

    global dview
    if dview is not None: cm.stop_server(dview=dview)
    c, dview, n_processes = cm.cluster.setup_cluster(
        backend='local', n_processes=CC, single_thread=False
    )

    sed_dict['border_pix'] = bord_px
    cnmf_opts.change_params(params_dict=sed_dict)
    start = time.time()

    # Perform CNMF
    CorrProj, PNR = cm.summary_images.correlation_pnr(
        images[::5], gSig=sed_dict['gSig'][0], swap_dim=False
    )

    cnm = cnmf.CNMF(n_processes=n_processes, dview=dview, Ain=sed_dict['Ain'], params=cnmf_opts)
    cnm.fit(images)
    gc.collect()

    cnm.params.set('quality', ce_dict)
    cnm.estimates.evaluate_components(images, cnm.params, dview=dview)
    cnm.estimates.detrend_df_f(quantileMin=sed_dict['quantile_min'], frames_window=sed_dict['frames_window'])
    gc.collect()

    dff = cnm.estimates.F_dff.T if cnm.estimates.F_dff is not None else None
    SFP = cnm.estimates.A
    Dim = CorrProj.shape

    CoMs, Areas = GetCoMsArea(SFP, Dim)

    CNM = {
        'Accepted': cnm.estimates.idx_components,
        'Areas': Areas,
        'CompBaseline': cnm.estimates.bl,
        'CompSNR': cnm.estimates.SNR_comp,
        'CompTimeConst': cnm.estimates.g,
        'CoMs': CoMs,
        'CorrProj': CorrProj,
        'CorrSpace': cnm.estimates.r_values,
        'DeconvTraces': cnm.estimates.S.T,
        'PNR': PNR,
        'RawTraces': cnm.estimates.C.conj().T,
        'RawTraces_dF_F': dff,
        'Rejected': cnm.estimates.idx_components_bad,
        'SFP': SFP,
        'SFPDims': np.array(images.shape[1:]+(cnm.estimates.A.shape[1],)),
    }

    for k in ('Accepted', 'CompBaseline', 'CompTimeConst', 'Rejected'):
        if CNM[k] is not None:
            CNM[k] = np.array(CNM[k])

    CNM = {**CNM, **{
        k: np.array(v)
        for k,v in cnm.estimates.__dict__.items()
        if k not in (
            'idx_components', 'idx_components_bad', 'bl', 'g',
            'r_values', 'SNR_comp', 'S', 'C', 'F_dff', 'A',
            'optional_outputs'
        )
        and v is not None
    }}

    CNM['optional_outputs'] = {
        k: np.array(v)
        for k,v in cnm.estimates.optional_outputs.items()
        if np.array(v).dtype != 'O' and np.array(v).size
    }

    kOOs = ['neurons_sn_tot', 'idx_tot', 'bl_tot']
    g_tot = [np.array(_.tolist()) for _ in cnm.estimates.optional_outputs['g_tot']]
    if max([_.size for _ in g_tot]): kOOs.append('g_tot')

    for kOO in kOOs:
        CNM['optional_outputs'][kOO] = [
            np.array(_.tolist())
            for _ in cnm.estimates.optional_outputs[kOO]
        ]

    CNM = {k:v if v is not None else np.array([]) for k,v in CNM.items()}

    for ext in OutputExt:
        if ext == 'dat': Write(CNM, OutFile)
        elif ext == 'mat': Write(CNM, f'{OutFile}.mat')
        elif ext == 'hdf5': cnm.save(f'{OutFile}.hdf5')
        else:
            raise TypeError(
                f'[{ScriptName}.{FN}] Only "dat", "hdf5" and/or "mat" are supported in `OutputExt`.'
            )

    end = time.time()
    Dur = str(timedelta(seconds=end-start))
    Log += PrintLog(f'[{ScriptName}.{FN}] Time for CNMFe: {Dur}')
    Log += PrintLog(f'[{ScriptName}.{FN}] Number of total components: {CNM["RawTraces"].shape[1]}')
    Log += PrintLog(f'[{ScriptName}.{FN}] Number of accepted components: {CNM["Accepted"].shape[0]}')

    StepMark(f'{FolderAnalysis}/.CNMFeRun', Log)
    gc.collect()

    if Return: return(CNM)
    else: return(None)


def CopyFiles(
        msFileList, auxFileList, auxSubFiles, msLocalFileList,
        auxLocalFileList, FolderAnalysis, CopyVideos=False
    ):
    FN = inspect.stack()[0][3]

    Log = []
    Log += PrintLog(f'[{ScriptName}.{FN}] Copying files...')
    if CopyVideos:
        FLists = [[msFileList, msLocalFileList], [auxFileList, auxLocalFileList]]
    else:
        FLists = [[auxFileList, auxLocalFileList]]

    for FList in FLists:
        for FileIn,FileOut in zip(*FList):
            Log += PrintLog(f'[{ScriptName}.{FN}]    {FileIn}')
            os.makedirs(os.path.dirname(FileOut), exist_ok=True)
            shutil.copyfile(FileIn, FileOut)

    Log += PrintLog(f'[{ScriptName}.{FN}] Done!')


    Log += PrintLog(f'[{ScriptName}.{FN}] Miniscope files in folder:')
    for _ in msFileList: Log += PrintLog(_)
    Log += PrintLog(f'[{ScriptName}.{FN}] '+'='*50)
    Log += PrintLog(f'[{ScriptName}.{FN}] Auxiliary files in data folder:')
    for _ in auxFileList: Log += PrintLog(_)
    Log += PrintLog(f'[{ScriptName}.{FN}] '+'='*50)
    Log += PrintLog(f'[{ScriptName}.{FN}] Auxiliary files in data subfolders:')
    for _ in auxSubFiles: Log += PrintLog(_)
    Log += PrintLog(f'[{ScriptName}.{FN}] '+'='*50)
    Log += PrintLog(f'[{ScriptName}.{FN}] Miniscope files in Local folder:')
    if CopyVideos:
        for _ in msLocalFileList: Log += PrintLog(_)
        Log += PrintLog(f'[{ScriptName}.{FN}] '+'='*50)
    Log += PrintLog(f'[{ScriptName}.{FN}] Auxiliary files in Local folder:')
    for _ in auxLocalFileList: Log += PrintLog(_)

    if len(msFileList) == 0: Log += PrintLog(f'[{ScriptName}.{FN}] No miniscope avi files found')

    StepMark(f'{FolderAnalysis}/.CopyFiles', Log)
    return(None)


def Downsample(FileListIn, FileListOut, Downsampling, Path, Codec=827737670):
    FN = inspect.stack()[0][3]

    Log = []
    ListOut = []
    if Downsampling > 1:
        Log += PrintLog(f'[{ScriptName}.{FN}] Downsampling videos...')
        for V,Video in enumerate(FileListOut):
            Log += PrintLog(f'[{ScriptName}.{FN}]    Video {V+1} of {len(FileListIn)}...')
            if FileListIn[V]==Video:
                # Not touching the original data
                vp = os.path.dirname(Video)
                vf = os.path.basename(Video)
                ve = vf.split('.')[-1]
                vs = f"Downsampled{Downsampling}x.{ve}"
                vf = f"{'.'.join(vf.split('.')[:-1])}_{vs}"
                Video = f"{vp}/{vf}"

            Videos.Downsample(FileListIn[V], Video, Downsampling, Codec)
            ListOut.append(Video)

        Log += PrintLog(f'[{ScriptName}.{FN}] Done.')

    gc.collect()

    StepMark(f'{Path}/.Downsample', Log)
    return(ListOut)


def GetFPS(Time, FPSVideos, FileList, FPSDefault_v3=30, FPSDefault_v4=20, Log=[]):
    FN = inspect.stack()[0][3]

    FPSVideo = int(round(np.mean(FPSVideos)))
    FPSReal = int(round(1/np.diff(Time[1:-1]).mean())) if len(Time) else None

    if FPSReal:
        if FPSReal != FPSVideo:
            Log += PrintLog(f"[{ScriptName}.{FN}]    Video FPS is wrong! Video: {FPSVideo} Real: {FPSReal}")
        FPS = FPSReal
    else:
        if True in ['timestamp.dat' in _ for _ in FileList]:
            Log += PrintLog(f"[{ScriptName}.{FN}]    No timestamps available! Assuming FPS = {FPSDefault_v3}.")
            FPS = FPSDefault_v3
        else:
            Log += PrintLog(f"[{ScriptName}.{FN}]    No timestamps available! Assuming FPS = {FPSDefault_v4}.")
            FPS = FPSDefault_v4

    return(FPS, FPSReal, FPSVideo)


def GetInfo(FolderData):
    """
    Extract the date/time of the experiment and save as a timestamp variable

    The date/time values are extracted from:

        the .json file in the data folder (if recorded by miniscope v4);
        the automatic DAQ folder organization (if recorded by miniscope v3, might not work if you renamed your folders).
    """
    FN = inspect.stack()[0][3]

    Log = []
    InfoFile = [
        _ for _ in sorted(glob(f"{FolderData}/*"))
        if 'metaData.json' in _ or 'settings_and_notes.dat' in _
    ]

    Info = {}

    if len(InfoFile):
        InfoFile = InfoFile[0]

        if InfoFile[-5:] == '.json':
            # Miniscope v4
            FileRoot = '/'.join(FolderData.split('/')[:-1])
            with open(f'{FileRoot}/metaData.json', 'r') as F: Info = json.load(F)

            for Folder in sorted(glob(f"{FileRoot}/*/*.json")):
                FolderName = Folder.split('/')[-2]
                with open(InfoFile, 'r') as F: Info[FolderName] = json.load(F)

            year, month, day, hour, minute, seconds = [
                Info["recordingStartTime"][_] for _ in
                ['year', 'month', 'day', 'hour', 'minute', 'second']
            ]
            Info['experiment_timestamp'] = datetime.timestamp(datetime(year,month,day,hour,minute,seconds))
            Log += PrintLog(f'[{ScriptName}.{FN}] [Miniscope v4] Info loaded.')

        else:
            try:
                splitname = str.split(FolderData, '/')

                dateStrPart = splitname[-3]
                timeStrPart = splitname[-2]

                date_result = str.split(dateStrPart, '_')
                month = int(date_result[0])
                day = int(date_result[1])
                year = int(date_result[2])

                timeStrPart = re.sub('[HSM]','', timeStrPart)
                time_result = str.split(timeStrPart,'_')

                hour = int(time_result[0])
                minute = int(time_result[1])
                seconds = int(time_result[2])

                Info['experiment_timestamp'] = datetime.timestamp(datetime(year,month,day,hour,minute,seconds))

                Info["recordingStartTime"]: {
                    "day": day,
                    "hour": hour,
                    "minute": minute,
                    "month": month,
                    "second": seconds,
                    "year": year
                }

                Log += PrintLog(f'[{ScriptName}.{FN}] [Miniscope v3] Info loaded.')

            except:
                Log += PrintLog(f'[{ScriptName}.{FN}] [Miniscope v3] Could not retrieve date information')

    return(Info)


def GetSigPeaks(Data, STDThr=2, ShuffleRounds=1000, Alpha=0.05, Parallel=None):
    """
    Get peaks of populational activity for a set of neurons.

    Parameters
    ----------
    Data: 2d array
        Input array with Samples x Neurons dimensions.
    STDThr: float
        How many sd above the mean the activity should be to be considered active.
    ShuffleRounds: int
        Number of shuffles.
    Alpha: float
        Significance level.
    Parallel: int or None
        Number of simultaneous processes to run. If `None` all but one
        core will be used.


    Returns
    -------
    Sig: 2d array
        Raster array of Samples x Neurons.
    SigCoActThr: float
        Threshold for significant co-activation.
    SigCoActPeaks: 1d array
        Array of Samples representing populational activity where `0` is
        inactive and `1` is active.

    Inspired by findSignificantDF_FCoactivity(), by Moelter (2018), at
    https://github.com/GoodhillLab/neural-assembly-detection/
    """
    FN = inspect.stack()[0][3]

    SampleNo, NeuronNo = Data.shape
    Mean, STD = Data.mean(axis=0), Data.std(axis=0)
    Thr = Mean+(STDThr*STD)
    Sig = (Data > np.tile(Thr, (SampleNo,1))).astype(int)

    SigCoActThr = GetSigCoActivity(Sig, ShuffleRounds, Alpha, Parallel)[0]
    SigCoActNorm = np.sum(Sig, axis=1)/max(np.sum(Sig, axis=1))
    SigCoActNormThr = SigCoActThr/max(np.sum(Sig, axis=1))

    print(f'[{ScriptName}.{FN}] Getting activity peaks...')
    SigCoActPeaks = GetPeaks(
        SigCoActNorm, FixedThreshold=SigCoActNormThr-SigCoActNorm.mean()
    )['Pos']
    print(f'[{ScriptName}.{FN}] Done.')

    return(Sig, SigCoActThr, SigCoActPeaks)


def MatchRecs(SFPs, CorrProjs, MinSessionsValid='All'):
    """
    Match neuron identities between recordings from the same animal.


    Parameters
    ----------
    SFPs: list
        List containing spatial footprints of recordings to be matched.

    CorrProjs: list
        List containing correlation projections from  recordings to be
        matched.

    MinSessionsValid: int or 'All'
        The number of sessions a neuron has to be detected and assigned
        to be accepted.
    """
    FN = inspect.stack()[0][3]

    Valid = np.array([_.shape[1] for _ in SFPs]).astype(bool)
    SFPs = [el for i,el in enumerate(SFPs) if Valid[i]]
    CorrProjs = [el for i,el in enumerate(CorrProjs) if Valid[i]]
    Dims = [_.shape for _ in CorrProjs]

    if len(SFPs) > 1:
        print(f'[{ScriptName}.{FN}] Aligning components...')
        SFPUnion, Assignments, Matchings = register_multisession(A=SFPs, dims=Dims[0], templates=CorrProjs)

        print(f'[{ScriptName}.{FN}] Selecting components active in selected sessions...')
        NoSessions = len(SFPs) if MinSessionsValid=='All' else MinSessionsValid

        AssignmentsActive = np.array(
            Assignments[
                np.sum(~np.isnan(Assignments), axis=1)>=NoSessions
            ], dtype=int
        )
        SFPActive = SFPs[0][:, AssignmentsActive[:, 0]]
    else:
        Assignments = np.array([])
        AssignmentsActive = np.array([])
        Matchings = np.array([])
        SFPUnion = SFPs[0]
        SFPActive = SFPs[0]

    CoMActive, Area = GetCoMsArea(SFPActive, Dims[0])

    # # Visual checking the SFPs
    # # import matplotlib.pyplot as plt
    # ColNo = 4
    # Fig,Axes = plt.subplots(len(Dims)//ColNo, ColNo)
    # for s,S in enumerate(SFPs):
         # e = S.toarray().reshape(Dims[s]+(S.shape[1],), order='F').max(axis=2)
         # Ax = Axes[s//ColNo,s%ColNo]
         # Ax.imshow(e)
         # Ax.set_title(f'Rec {s+1}')
         # Ax.axis('off')
         # # Ax.plot(CoMActive[:,1], CoMActive[:,0], 'r.')
    # plt.show()

    Matched = {
        'SFPUnion': sparse.csc_matrix(SFPUnion),
        'Assignments': Assignments,
        'Matchings': [np.array(_) for _ in Matchings],
        'AssignmentsActive': AssignmentsActive,
        'SFPActive': SFPActive,
        'SFPDims': np.array(Dims),
        'CellArea': Area,
        'CoMActive': CoMActive
    }

    print(f'[{ScriptName}.{FN}] Assignments: {AssignmentsActive.shape}/{Assignments.shape} active.')
    print(f'[{ScriptName}.{FN}] Done.'); print()

    return(Matched)


def MotionCorrection(fnames, ParamsMC, cnmf_opts, FolderAnalysis, OutFile, OutputExt, Parallel=None):
    FN = inspect.stack()[0][3]
    if not AvailCaImAn:
        raise ModuleNotFoundError(
            AvailMsg.format(sm=ScriptName, fn=FN, module='caiman')
        )

    Log = []

    if Parallel is not None and Parallel > os.cpu_count():
        Ans = IO.WarningOverParallel()
        if Ans.lower() not in ['y', 'yes']:
            return(None)


    CC = dcp(Parallel)
    if CC is None:
        CC = (psutil.virtual_memory().available-0.5)/(1024**3)
        CC = CC/0.5
        if CC > os.cpu_count()-1: CC = os.cpu_count()-1

    CC = int(CC)

    global dview
    if dview is not None: cm.stop_server(dview=dview)
    c, dview, n_processes = cm.cluster.setup_cluster(
        backend='local', n_processes=CC, single_thread=False
    )

    start = time.time()

    # do motion correction rigid
    mc = MotionCorrect(fnames, dview=dview, **cnmf_opts.get_group('motion'))
    mc.motion_correct(save_movie=True)
    fname_mc = mc.fname_tot_els if ParamsMC['pw_rigid'] else mc.fname_tot_rig

    if ParamsMC['pw_rigid']:
        bord_px = np.ceil(np.maximum(np.max(np.abs(mc.x_shifts_els)),
                                    np.max(np.abs(mc.y_shifts_els)))).astype(int)
    else:
        bord_px = np.ceil(np.max(np.abs(mc.shifts_rig))).astype(int)

    bord_px = 0 if ParamsMC['border_nan'] == 'copy' else bord_px

    Log += PrintLog(f'[{ScriptName}.{FN}] Motion correction has been done! Mapping to memory...')
    fname_new = cm.save_memmap(
        fname_mc, base_name='memmap_', order='C', border_to_0=bord_px
    )

    MCShifts = {
        'Shifts': np.array(mc.shifts_rig),
        'MCTemplate': np.array(mc.total_template_rig)
    }

    for ext in OutputExt:
        if ext == 'dat': Write(MCShifts, OutFile)
        elif ext == 'mat': Write(MCShifts, f'{OutFile}.mat')
        else:
            raise TypeError(
                f'[{ScriptName}.{FN}] Only "dat" and/or "mat" are supported in `OutputExt`.'
            )

    gc.collect()
    end = time.time()
    Dur = str(timedelta(seconds=end-start))

    Log += PrintLog(f'[{ScriptName}.{FN}] Motion corrected video has been mapped to memory')
    Log += PrintLog(f'[{ScriptName}.{FN}] Time for motion correction: {Dur}')
    StepMark(f'{FolderAnalysis}/.MotionCorrection', Log)
    StepMark(f'{FolderAnalysis}/.MotionCorrection.dict', [f"('{fname_new}', {bord_px})"])
    return(fname_new, bord_px, np.array(mc.shifts_rig))


def TimestampsMatch(FileList, FrameNo, OutFile, OutputExt, FolderAnalysis, Return=True):
    FN = inspect.stack()[0][3]

    Log = []
    cameraMatched = False
    mstime = []

    if True in ['timestamp.dat' in _ for _ in FileList]:
        # Miniscope v3
        timestampFile = [_ for _ in FileList if 'timestamp.dat' in _][0]
        with open(timestampFile) as f: Lines = f.readlines()

        camNum = []; i=0
        while not len(camNum):
            try:
                camNum, frameNum, sysClock, buffer = np.loadtxt(
                    Lines[:len(Lines)-i], dtype='float',
                    comments='#', skiprows=1, unpack = True
                )
            except ValueError:
                i += 1

        for j in range(int(max(camNum))+1):
            if sum(camNum==j) != 0:
                camFrameList, = np.where(camNum == j)
                camLastFrame = camFrameList[-1]
                LastFrame = frameNum[camLastFrame]

            if (sum(camNum==j) >= FrameNo) and (LastFrame >= FrameNo):
                mstime_idx = np.where(camNum == j)
                mstime = sysClock[mstime_idx][:FrameNo]
                mstime[0] = 0
                cameraMatched = True
            elif len(camNum):
                Log += PrintLog(f'[{ScriptName}.{FN}] The timestamps file contains less values than the amount of frames.')
                Log += PrintLog(f'[{ScriptName}.{FN}] The time for remaining frames will be calculated according to the average frame rate.')
                Diff = FrameNo-sum(camNum==j)
                mstime_idx = np.where(camNum == j)
                mstime = np.zeros(FrameNo)
                mstime[:sum(camNum==j)] = sysClock[mstime_idx]
                df = np.diff(mstime[1:sum(camNum==j)-1]).mean()
                mstime[sum(camNum==j):] = np.linspace(mstime[sum(camNum==j)-1]+int(df), int(FrameNo*df), Diff, dtype=int)
                mstime[0] = 0
                cameraMatched = True


    elif True in [
            'miniscope' in _.lower() and 'timestamps.csv' in _.lower()
            for _ in FileList
        ]:
        # Miniscope v4
        timestampFile = [_
            for _ in FileList
            if 'miniscope' in _.lower() and 'timestamps.csv' in _.lower()
        ][0]

        mstime = np.genfromtxt(
            timestampFile, dtype=float, delimiter=',', skip_header=1
        )
        mstime[0,:] = 0
        mstime = mstime[:,1]
        cameraMatched = True

    if cameraMatched is not True:
        Log += PrintLog(f'[{ScriptName}.{FN}] Problem matching up timestamps.')
    else:
        Log += PrintLog(f'[{ScriptName}.{FN}] Successfully registered timestamps.')

    if len(mstime):
        mstime /= 1000

        for ext in OutputExt:
            if ext == 'dat': Write(mstime, f'{OutFile}.dat')
            elif ext == 'mat': Write({'Time': mstime}, f'{OutFile}.mat')
            else:
                raise TypeError(
                    f'[{ScriptName}.{FN}] Only "dat" and/or "mat" are supported in `OutputExt`.'
                )

    else: Log += PrintLog(f'[{ScriptName}.{FN}] Timestamps information missing from data!')

    StepMark(f'{FolderAnalysis}/.TimestampsMatch', Log)

    if Return: return(mstime)
    else: return(None)



#%% Level 2 ============================================================
def Full(
        FolderData, FolderAnalysis=None, OutputExt=['dat'], Parallel=None,
        ParamsVid={}, ParamsMC={}, ParamsSED={}, ParamsCE={}
    ):
    """
    Get timestamps, motion-correct, extract sources and evaluate components.

    Parameters
    ----------
    FolderData: str
        Path to folder containing calcium imaging videos.
    FolderAnalysis: str or None
        Path to folder to write analysis results. If `None`, write to `FolderData`.
    OutputExt: iterable
        Iterable containing extensions to write the analysis output.
    ParamsVid: dict
        Parameters for video manupulation. Default parameters from
        `CalciumImaging.ParamsVidDef` are used, and overwritten by `ParamsVid`.
    ParamsMC: dict
        Parameters for motion correction. Default parameters from
        `CalciumImaging.ParamsMCDef` are used, and overwritten by `ParamsMC`.
    ParamsSED: dict
        Parameters for source extraction and deconvolution. Default parameters from
        `CalciumImaging.ParamsSEDDef` are used, and overwritten by `ParamsSED`.
    ParamsCE: dict
        Parameters for component evaluation. Default parameters from
        `CalciumImaging.ParamsCEDef` are used, and overwritten by `ParamsCE`.
    """
    FN = inspect.stack()[0][3]
    if not AvailCaImAn:
        raise ModuleNotFoundError(
            AvailMsg.format(sm=ScriptName, fn=FN, module='caiman')
        )

    Log = []

    try:
        global dview
        dview.terminate()
    except:
        dview = None

    if FolderAnalysis is None: FolderAnalysis = FolderData

    pVid = {**ParamsVidDef, **ParamsVid}
    pMC = {**ParamsMCDef, **ParamsMC}
    pSED = {**ParamsSEDDef, **ParamsSED}
    pCE = {**ParamsCEDef, **ParamsCE}

    OutFile = f'{FolderAnalysis}/Result'
    os.makedirs(FolderAnalysis, exist_ok=True)

    Log += PrintLog(f"[{ScriptName}.{FN}]     Directory: {FolderAnalysis}")
    if '.AllDone' in os.listdir(FolderAnalysis) or '.ToSkip' in os.listdir(FolderAnalysis):
        Log += PrintLog(f'[{ScriptName}.{FN}]     Analysis already done!')
        return(None)

    AnalysisTime = datetime.now().strftime("%Y-%m-%d %H:%M")
    AnalysisStart = time.time()

    Log += PrintLog(f'[{ScriptName}.{FN}]     Analysis started on ' + AnalysisTime)

    print(''); print(f'[{ScriptName}.{FN}]     Preparing files...')
    Info = GetInfo(FolderData)
    msFileList, auxFileList, auxSubFiles, msLocalFileList, auxLocalFileList =  GetFilesList(FolderData, FolderAnalysis, Info)
    Info['Videos'] = {'Info': [Videos.Video.GetInfo(_) for _ in msFileList]}
    FPSVideos = np.array([_['FPS'] for _ in Info['Videos']['Info']])
    FrameNos = np.array([_['FrameNo'] for _ in Info['Videos']['Info']])
    FrameNo = sum(FrameNos)

    Broken = np.where((FrameNos==0))[0]

    if len(Broken):
        print(f'[{ScriptName}.{FN}]     The following files are broken and were excluded from analysis:')
        for _ in Broken:
            print(f"[{ScriptName}.{FN}]         {msFileList[_].replace(FolderData+'/','')}")

        msFileList, msLocalFileList, FPSVideos, FrameNos = [
            [El for E,El in enumerate(List) if E not in Broken]
            for List in (msFileList, msLocalFileList, FPSVideos, FrameNos)
        ]

    print(''); print(f'[{ScriptName}.{FN}]     TimestampsMatch...')
    if '.TimestampsMatch' not in os.listdir(FolderAnalysis):
        Time = TimestampsMatch(auxFileList, FrameNo, f'{OutFile}/Time', OutputExt, FolderAnalysis, Return=True)
    else:
        try:
            if 'dat' in OutputExt: Time = IO.Bin.Read(f'{OutFile}/Time.dat', AsMMap=False)[0]
            elif 'mat' in OutputExt: Time = sio.loadmat(f'{OutFile}/Time.mat')['Time']
        except FileNotFoundError:
            Log += PrintLog(f'[{ScriptName}.{FN}]    Timestamps not available, cannot calculate real FPS!')
            Time = None

    print(f'[{ScriptName}.{FN}]     Done.'); print('')

    FPS, FPSReal, FPSVideo = GetFPS(Time, FPSVideos, auxLocalFileList, pVid['FPSDefault_v3'], pVid['FPSDefault_v4'], Log)

    if '.CopyFiles' not in os.listdir(FolderAnalysis):
        CopyFiles(
            msFileList, auxFileList, auxSubFiles,
            msLocalFileList, auxLocalFileList, FolderAnalysis, pVid['CopyVideos']
        )

    if '.Downsample' not in os.listdir(FolderAnalysis):
        msLocalFileList = Downsample(
            msFileList, msLocalFileList, pVid['Downsampling'],
            FolderAnalysis, pVid['DownsampleCodec']
        )

    pMC['fr'] = FPS

    print(''); print(f'[{ScriptName}.{FN}]     Motion correction...')
    pCNMF = params.CNMFParams(params_dict=pMC)
    if pVid['MotionCorr']:
        if '.MotionCorrection' not in os.listdir(FolderAnalysis):
            fname_new, bord_px, Shifts = MotionCorrection(msLocalFileList, pMC, pCNMF, FolderAnalysis, f'{OutFile}/Shifts', OutputExt)
        else:
            with open(f'{FolderAnalysis}/.MotionCorrection.dict', 'r') as F:
                fname_new, bord_px = IO.Bin.Txt.literal_eval(F.readlines()[0])

    else:
        fname_new = cm.save_memmap(msLocalFileList, base_name='memmap_',
                                order='C', border_to_0=0, dview=dview)
        bord_px = 0
    print(f'[{ScriptName}.{FN}]     Done.'); print('')

    Yr, dims, T = cm.load_memmap(fname_new)
    images = Yr.T.reshape((T,) + dims, order='F')

    print(''); print(f'[{ScriptName}.{FN}]     CNMFe...')
    if '.CNMFeRun' not in os.listdir(FolderAnalysis):
        CNMFeRun(
            images, bord_px, pSED, pCE, pCNMF, FolderAnalysis,
            f'{OutFile}/CNMFe', OutputExt, Parallel, False
        )
    print(f'[{ScriptName}.{FN}]     Done.'); print('')


    AnalysisEnd = time.time()
    AnalysisDur = AnalysisEnd - AnalysisStart
    EndTime = str(timedelta(seconds=AnalysisDur))
    # SS = round(AnalysisDur%60,3)
    # MM = AnalysisDur//60
    # HH = int(MM//60)
    # MM = int(MM%60)
    # EndTime = f'{HH}h{MM}m{SS}s'

    Info['CaImAn'] = {
        'AnalysisDuration': AnalysisDur,
        'AnalysisStart': AnalysisTime,
        'DataPath': FolderData,
        'FileNo': len(msFileList),
        'FPSs': dict(FPS=FPS, FPSReal=FPSReal, FPSVideo=FPSVideo),
        'ParametersEvaluation': pCE.copy(),
        'ParametersMotionCorrection': pMC.copy(),
        'ParametersSourceExtraction': pSED.copy(),
        'ParametersVideo': pVid.copy(),
    }
    IO.Bin.Txt.Write(Info, f'{OutFile}/CaImAn.dict')

    Log += PrintLog(f'[{ScriptName}.{FN}] Done analyzing. This took a total of {EndTime}')
    StepMark(f'{FolderAnalysis}/.AllDone', Log); print('')

    return(None)


def _LoadSFPsCorrProjs(
        A, Animal, FN, Files, Info, OutputExt,
    ):
    Files = np.array(Files)
    Info = {K: np.array(V) for K,V in Info.items()}

    RN = f"{A+1}|{len(np.unique(Info['Animals']))}"
    Pf = f'[{ScriptName}.{FN} ({RN})]'

    AInd = Info['Animals'] == Animal
    ASessions = Info['Sessions'][AInd]
    ATrials = Info['Trials'][AInd]
    AFiles = Files[AInd]
    AGroup = Info['Groups'][AInd][0]

    print(f'{Pf} Loading spatial footprints...')
    if 'dat' in OutputExt:
        SFPs = [IO.Bin.Read(f'{_}/CNMFe/SFP', AsMMap=False)[0] for _ in AFiles]
        CorrProjs = [
            IO.Bin.Read(f'{_}/CNMFe/CorrProj.dat', AsMMap=False)[0]
                if len(glob(f'{_}/CNMFe/CorrProj.dat'))
                else IO.Bin.Read(f'{_}/CorrProj.dat')[0]
            for _ in AFiles
        ]
    elif 'mat' in OutputExt:
        SFPs = [sio.loadmat(f'{_}/CNMFe.mat')['SFP'] for _ in AFiles]
        CorrProjs = [sio.loadmat(f'{_}/CNMFe.mat')['CorrProj'] for _ in AFiles]

    AInfo = dict(Sessions=ASessions, Trials=ATrials, MSFiles=AFiles)

    return(SFPs, CorrProjs, AInfo)


def _MatchRecsFull_Core(
        A, Animal, FN, Files, Info, FolderAnalysis, OutputExt,
        MinSessionsValid
    ):

    SFPs, CorrProjs, AInfo = _LoadSFPsCorrProjs(
        A, Animal, FN, Files, Info, OutputExt
    )

    Matched = MatchRecs(SFPs, CorrProjs, MinSessionsValid)
    Matched = {**Matched, **AInfo}

    AOut = f'{FolderAnalysis}/{Animal}-Matched'
    print(f'{Pf}     Writing to {AOut}...')

    AOutF = [f'{AOut}.{_}' if _ != 'dat' else AOut for _ in OutputExt]
    if 'dat' in OutputExt:
        for K in ('Matchings','SFPActive','SFPUnion'):
            try: shutil.rmtree(f"{AOut}/{K}")
            except FileNotFoundError: pass

    for ao in AOutF: Write(Matched, ao)

    print(f'{Pf} Done.'); print()


def MatchRecsFull(
        Files, Info, FolderAnalysis=None, OutputExt=['dat'],
        MinSessionsValid='All', Parallel=None
    ):
    """
    Match neuron identities between recordings from the same animal
    among a set of recording including multiple animals.


    Parameters
    ----------
    Files: iterable
        List, tuple or array containing paths to analysis results.

    Info: dict
        Dictionary containing the keys `Animals`, `Sessions`,`Groups`
        and `Trials`. The value of those keys should be arrays of the
        same length as `Files`, such that the animal for `Files[0]` is
        `Info['Animals'][0]`; the session is `Info['Sessions'][0]`, and
        so on.

    FolderAnalysis: str or None
        Path to save results. if `None`, the common path among all files
        is chosen. If there is no common path, results will be written
        to the current working directory.

    OutputExt: iterable
        Iterable containing extensions to write the analysis output.

    MinSessionsValid: int or 'All'
        The number of sessions a neuron has to be detected and assigned
        to be accepted.

    Parallel: int or None
        Number of simultaneous processes to run. If `None` all but one
        core will be used.
    """
    FN = inspect.stack()[0][3]

    if FolderAnalysis is None:
        FolderAnalysis = os.path.commonpath(list(Files))
        if len(FolderAnalysis) == 0:
            FolderAnalysis = '.'

    IO.MultiProcess(
        _MatchRecsFull_Core,
        [
            _+(FN,Files,Info,FolderAnalysis,OutputExt,MinSessionsValid)
            for _ in enumerate(np.unique(Info['Animals']))
        ],
        Parallel, ASync=True
    )

    return(None)



#%% EOF ================================================================
