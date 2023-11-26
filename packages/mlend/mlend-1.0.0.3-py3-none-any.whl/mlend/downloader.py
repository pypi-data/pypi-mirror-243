'''
API to download dataset.
Version : 1.0.0.0

'''

from __future__ import absolute_import, division, print_function
name = "MLEnd | data downloader"
import sys

if sys.version_info[:2] < (3, 3):
    old_print = print
    def print(*args, **kwargs):
        flush = kwargs.pop('flush', False)
        old_print(*args, **kwargs)
        if flush:
            file = kwargs.get('file', sys.stdout)
            # Why might file=None? IDK, but it works for print(i, file=None)
            file.flush() if file is not None else sys.stdout.flush()

import sys, os, six, time, collections, glob
from six.moves.urllib.error import HTTPError, URLError
from six.moves.urllib.request import urlopen, urlretrieve
import tarfile

from pathlib import Path

try:
    import queue
except ImportError:
    import Queue as queue

import spkit as sp
import pandas as pd
import numpy as np

def _download_file(origin,fpath,bar=True):
    ff = origin.split('/')[-1].split('.')[0]
    class ProgressTracker(object):
        progbar = None

    def dl_progress(count, block_size, total_size):
        #print(count, block_size, count * block_size, total_size)
        if bar:
            #sp.utils.ProgressBar(count * block_size,total_size,title=sub)
            sp.utils.ProgBar(count * block_size,total_size,L=50,title=f'{ff}')
        else:
            pass

    error_msg = 'URL fetch failure on {} : {} -- {}'
    try:
        try:
            urlretrieve(origin, fpath, dl_progress)
        except HTTPError as e:
            raise Exception(error_msg.format(origin, e.code, e.msg))
        except URLError as e:
            raise Exception(error_msg.format(origin, e.errno, e.reason))
    except (Exception, KeyboardInterrupt):
        if os.path.exists(fpath):
            os.remove(fpath)
        raise
    ProgressTracker.progbar = None

    return fpath

def download_spoken_numerals(save_to = '../MLEnd', subset = {},verbose=1,overwrite=False,pbar_style='colab'):
    """Download Spoken Numerals Dataset.

    # Arguments
        save_to: loacal path where you want to store the data
                  relative to `../MLEnd/spoken_numerals/`).
        subset: subset of data to download. {'attribute_name':list_of_values to select}
                 subset = {'Numeral':[1,2]}, will download audio files of numerals 1 and 2 only
                 subset = {'Numeral':[1,2], 'Intonation':['excited','question'], 'Speaker':[1,2,3,4,5,6]}
                 subset = {} will download entire dataset

    # Raises
        ValueError:
         - in case keys in subset are not in ['Numeral', 'Intonation', 'Speaker']
         - in case values of any keys are not valid

    # Returns

    path: path where data is saved


    """
    #DataPath = 'https://github.com/Nikeshbajaj/PhyaatDataset/raw/master/Signals/'
    repo_path = 'https://github.com/MLEndDatasets/SpokenNumerals'
    audio_files_path  = repo_path + '/raw/main/MLEndSND_audiofiles/'
    attributes_file   = repo_path + '/raw/main/MLEndSND_audio_attributes_benchmark.csv'
    speaker_demog_file = repo_path + '/raw/main/MLEndSND_speakers_demographics_benchmark.csv'


    D = pd.read_csv(attributes_file)
    S = pd.read_csv(speaker_demog_file)


    # Keys in subset should be one of ['Numeral', 'Intonation', 'Speaker']
    D_attr = list(D)
    if len(subset):
        for key in subset:
            if key not in D_attr:
                raise ValueError(f"Invalid attribute, {key}. Should be one of ['Numeral', 'Intonation', 'Speaker']")
            D_valu = set(list(D[key]))
            values = set(subset[key])

            # Values of any keys are not valid
            # Values of key
            if len(values - D_valu)>0:
                raise ValueError(f"Invalid value of attribute {key}: {values - D_valu}")

    try:
        datadir_main = os.path.join(save_to, 'spoken_numerals')
        datadir = os.path.join(datadir_main, 'MLEndSND_audiofiles')
        path    = Path(datadir)
        path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print('NOTE:: Path :  \"'+ save_to +'\" is not accessible. Creating  \"spoken_numerals\" in  "/tmp\" directory for dataset' )
        save_to = os.path.join('/tmp','MLEnd')
        datadir_main = os.path.join(save_to, 'spoken_numerals')
        datadir = os.path.join(datadir_main, 'MLEndSND_audiofiles')
        path    = Path(datadir)
        path.mkdir(parents=True, exist_ok=True)

    #print(datadir1,datadir,path)

    D.to_csv(datadir_main+'/MLEndSND_audio_attributes_benchmark.csv',index=False)
    S.to_csv(datadir_main+'/MLEndSND_speakers_demographics_benchmark.csv',index=False)

    Di = D.copy()
    Di['select'] = 0
    for key in subset:
        values = subset[key]
        for value in values:
            Di.loc[Di[key]==value,'select'] = 1

        Di = Di[Di['select']==1]
        Di['select'] = 0

    N = Di.shape[0]
    if verbose: print(f'Downloading {N} audio files from {repo_path}')

    filenames = list(Di['filename'])

    for k,filename in enumerate(filenames):
        #sp.utils.ProgBar(k,len(filenames),L=50,title=f'{filename}')
        if verbose:
            if pbar_style==None:
                sp.utils.ProgBar(k,len(filenames),style=2,L=50,color='blue',title=f'{filename}')
            elif pbar_style == 'colab':
                sp.utils.ProgBar_JL(k,len(filenames),style=2,L=50,color='blue',title=f'{filename}')
            elif pbar_style=='spkit_JL':
                sp.utils.ProgBar_JL(k,len(filenames),style=2,L=50,title=f'{filename}')

        origin = audio_files_path + filename
        fpath =  datadir +'/'+ filename
        if not(os.path.isfile(fpath)) or overwrite:
            ifpath = _download_file(origin,fpath,bar=False)

    return datadir_main

def download_london_sounds(save_to = '../MLEnd', subset = {},verbose=1,overwrite=False,pbar_style='colab'):
    """Download London Sounds Dataset.

    # Arguments
        save_to: loacal path where you want to store the data
                  relative to `../MLEnd/london_sounds/`).
        subset: subset of data to download. {'attribute_name':list_of_values to select}
                 subset = {'Area':['british_museum'], 'Spot':['forecourt','greatcourt']}, will download audio files of British museum for two spots only 'forecourt','greatcourt'
                 subset = {'Area':['british_museum']} will download all the spots of British Museum
                 subset = {'Area':['british_museum'],'In_Out':['indoor']} will download all the indoor spots of British Museum
                 subset = {} will download entire dataset

    # Raises
        ValueError:
         - in case keys in subset are not in ['Area', 'Spot', 'In_Out']
         - in case values of any keys are not valid

    # Returns

    path: path where data is saved


    """
    #DataPath = 'https://github.com/Nikeshbajaj/PhyaatDataset/raw/master/Signals/'
    repo_path = 'https://github.com/MLEndDatasets/LondonSounds/'
    audio_files_path  = repo_path + '/raw/main/MLEndLSD_audiofiles/'
    attributes_file   = repo_path + '/raw/main/MLEndLSD_audio_attributes_benchmark.csv'
    #speaker_demog_file = repo_path + '/raw/main/MLEndSND_speakers_demographics_benchmark.csv'


    D = pd.read_csv(attributes_file)
    #S = pd.read_csv(speaker_demog_file)


    # Keys in subset should be one of ['Numeral', 'Intonation', 'Speaker']
    D_attr = list(D)
    if len(subset):
        for key in subset:
            if key not in D_attr:
                raise ValueError(f"Invalid attribute, {key}. Should be one of ['Area', 'Spot', 'In_Out']")
            D_valu = set(list(D[key]))
            values = set(subset[key])

            # Values of any keys are not valid
            # Values of key
            if len(values - D_valu)>0:
                raise ValueError(f"Invalid value of attribute {key}: {values - D_valu}")

    try:
        datadir_main = os.path.join(save_to, 'london_sounds')
        datadir = os.path.join(datadir_main, 'MLEndLSD_audiofiles')
        path    = Path(datadir)
        path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print('NOTE:: Path :  \"'+ save_to +'\" is not accessible. Creating  \"london_sounds\" in  "/tmp\" directory for dataset' )
        save_to = os.path.join('/tmp','MLEnd')
        datadir_main = os.path.join(save_to, 'london_sounds')
        datadir = os.path.join(datadir_main, 'MLEndLSD_audiofiles')
        path    = Path(datadir)
        path.mkdir(parents=True, exist_ok=True)

    #print(datadir1,datadir,path)

    D.to_csv(datadir_main+'/MLEndLSD_audio_attributes_benchmark.csv',index=False)
    #S.to_csv(datadir_main+'/MLEndSND_speakers_demographics_benchmark.csv')

    Di = D.copy()
    Di['select'] = 0
    for key in subset:
        values = subset[key]
        for value in values:
            Di.loc[Di[key]==value,'select'] = 1

        Di = Di[Di['select']==1]
        Di['select'] = 0

    N = Di.shape[0]
    if verbose: print(f'Downloading {N} audio files from {repo_path}')

    filenames = list(Di['filename'])

    for k,filename in enumerate(filenames):
        #sp.utils.ProgBar(k,len(filenames),L=50,title=f'{filename}')
        if verbose:
            if pbar_style==None:
                sp.utils.ProgBar(k,len(filenames),style=2,L=50,color='green',title=f'{filename}')
            elif pbar_style == 'colab':
                sp.utils.ProgBar_JL(k,len(filenames),style=2,L=50,color='green',title=f'{filename}')
            elif pbar_style=='spkit_JL':
                sp.utils.ProgBar_JL(k,len(filenames),style=2,L=50,title=f'{filename}')

        origin = audio_files_path + filename
        fpath =  datadir +'/'+ filename
        if not(os.path.isfile(fpath)) or overwrite:
            ifpath = _download_file(origin,fpath,bar=False)

    return datadir_main

def download_hums_whistles(save_to = '../MLEnd', subset = {},verbose=1,overwrite=False,pbar_style='colab'):
    """Download Hums and Whistles Dataset.

    # Arguments
        save_to: loacal path where you want to store the data
                  relative to `../MLEnd/hums_whistles/`).
        subset: subset of data to download. {'attribute_name':list_of_values to select}
                 subset = {'Song':['Potter','Frozen']}, will download audio files of Potter and Fronzen only with both Hums and Whistles
                 subset = {'Song':['Potter','Frozen'], 'Interpretation':['Hum']} will download audio files of Potter and Fronzen with Huming only
                 subset = {'Interpretation':['Whistle']} will download all the audio files of Whistling
                 subset = {} will download entire dataset

    # Raises
        ValueError:
         - in case keys in subset are not in ['Song', 'Interpretation', 'Interpreter']
         - in case values of any keys are not valid

    # Returns

    path: path where data is saved


    """
    #DataPath = 'https://github.com/Nikeshbajaj/PhyaatDataset/raw/master/Signals/'
    repo_path = 'https://github.com/MLEndDatasets/HumsAndWhistles'
    audio_files_path  = repo_path  + '/raw/main/MLEndHWD_audiofiles/'
    attributes_file   = repo_path  + '/raw/main/MLEndHWD_audio_attributes_benchmark.csv'
    interptr_demog_file = repo_path + '/raw/main/MLEndHWD_interpreter_demographics_benchmark.csv'


    D = pd.read_csv(attributes_file)
    S = pd.read_csv(interptr_demog_file)


    # Keys in subset should be one of ['Numeral', 'Intonation', 'Speaker']
    D_attr = list(D)
    if len(subset):
        for key in subset:
            if key not in D_attr:
                raise ValueError(f"Invalid attribute, {key}. Should be one of ['Song', 'Interpretation', 'Interpreter']")
            D_valu = set(list(D[key]))
            values = set(subset[key])

            # Values of any keys are not valid
            # Values of key
            if len(values - D_valu)>0:
                raise ValueError(f"Invalid value of attribute {key}: {values - D_valu}")

    try:
        datadir_main = os.path.join(save_to, 'hums_whistles')
        datadir = os.path.join(datadir_main, 'MLEndHWD_audiofiles')
        path    = Path(datadir)
        path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print('NOTE:: Path :  \"'+ save_to +'\" is not accessible. Creating  \"hums_and_whistles\" in  "/tmp\" directory for dataset' )
        save_to = os.path.join('/tmp','MLEnd')
        datadir_main = os.path.join(save_to, 'hums_whistles')
        datadir = os.path.join(datadir_main, 'MLEndHWD_audiofiles')
        path    = Path(datadir)
        path.mkdir(parents=True, exist_ok=True)

    #print(datadir1,datadir,path)

    D.to_csv(datadir_main+'/MLEndHWD_audio_attributes_benchmark.csv',index=False)
    S.to_csv(datadir_main+'/MLEndHWD_interpreter_demographics_benchmark.csv',index=False)

    Di = D.copy()
    Di['select'] = 0
    for key in subset:
        values = subset[key]
        for value in values:
            Di.loc[Di[key]==value,'select'] = 1

        Di = Di[Di['select']==1]
        Di['select'] = 0

    N = Di.shape[0]
    if verbose: print(f'Downloading {N} audio files from {repo_path}')

    filenames = list(Di['filename'])

    for k,filename in enumerate(filenames):
        #sp.utils.ProgBar(k,len(filenames),L=50,title=f'{filename}')
        if verbose:
            if pbar_style==None:
                sp.utils.ProgBar(k,len(filenames),style=2,L=50,color='red',title=f'{filename}')
            elif pbar_style == 'colab':
                sp.utils.ProgBar_JL(k,len(filenames),style=2,L=50,color='red',title=f'{filename}')
            elif pbar_style=='spkit_JL':
                sp.utils.ProgBar_JL(k,len(filenames),style=2,L=50,title=f'{filename}')

        origin = audio_files_path + filename
        fpath =  datadir +'/'+ filename
        if not(os.path.isfile(fpath)) or overwrite:
            ifpath = _download_file(origin,fpath,bar=False)

    return datadir_main

def download_yummy_small(save_to = '../MLEnd',verbose=1,overwrite=False,pbar_style='colab'):
    """Download Yummy Small Dataset.

    # Arguments
        save_to: loacal path where you want to store the data
                  relative to `../MLEnd/yummy/`).

    # Returns

    path: path where data is saved


    """
    #DataPath = 'https://github.com/Nikeshbajaj/PhyaatDataset/raw/master/Signals/'
    repo_path = 'https://github.com/MLEndDatasets/Yummy'
    image_files_path  = repo_path + '/raw/main/MLEndYD_images_small/'
    attributes_file   = repo_path + '/raw/main/MLEndYD_image_attributes_small.csv'
    #speaker_demog_file = repo_path + '/raw/main/MLEndSND_speakers_demographics_benchmark.csv'


    D = pd.read_csv(attributes_file)
    #S = pd.read_csv(speaker_demog_file)

    try:
        datadir_main = os.path.join(save_to, 'yummy')
        datadir = os.path.join(datadir_main, 'MLEndYD_images_small')
        path    = Path(datadir)
        path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print('NOTE:: Path :  \"'+ save_to +'\" is not accessible. Creating  \"yummy\" in  "/tmp\" directory for dataset' )
        save_to = os.path.join('/tmp','MLEnd')
        datadir_main = os.path.join(save_to, 'yummy')
        datadir = os.path.join(datadir_main, 'MLEndYD_images_small')
        path    = Path(datadir)
        path.mkdir(parents=True, exist_ok=True)

    #print(datadir1,datadir,path)

    D.to_csv(datadir_main+'/MLEndYD_image_attributes_small.csv',index=False)
    #S.to_csv(datadir_main+'/MLEndSND_speakers_demographics_benchmark.csv')

    Di = D.copy()

    N = Di.shape[0]
    if verbose: print(f'Downloading {N} image files from {repo_path}')

    filenames = list(Di['filename'])

    for k,filename in enumerate(filenames):
        #sp.utils.ProgBar(k,len(filenames),L=50,title=f'{filename}')
        if verbose:
            if pbar_style==None:
                sp.utils.ProgBar(k,len(filenames),style=2,L=50,color='cyan',title=f'{filename}')
            elif pbar_style == 'colab':
                sp.utils.ProgBar_JL(k,len(filenames),style=2,L=50,color='cyan',title=f'{filename}')
            elif pbar_style=='spkit_JL':
                sp.utils.ProgBar_JL(k,len(filenames),style=2,L=50,title=f'{filename}')

        origin = image_files_path + filename
        fpath =  datadir +'/'+ filename
        if not(os.path.isfile(fpath)) or overwrite:
            ifpath = _download_file(origin,fpath,bar=False)

    return datadir_main

def download_yummy(save_to = '../MLEnd', subset = {},verbose=1,overwrite=False,pbar_style='colab',debug_mode=False):
    """Download Yummy Full Dataset.

    # Arguments
        save_to: loacal path where you want to store the data
                  relative to `../MLEnd/yummy/`).
        subset: subset of data to download. {'attribute_name':list_of_values to select}
            subset = {'Diet':['vegetarian']}, will download image files of vegetarian dishes only
            subset = {'Diet':['vegan'], 'Home_or_restaurant':['home']} will download image files of vegan dishes cooked at home
            subset = {} will download entire dataset

    # Raises
        ValueError:
         - in case keys in subset are not in the attribuate list ['Diet', 'Home_or_restaurant', 'Cuisine' ]
         - in case values of any keys are not valid

    # Returns

    path: path where data is saved


    """

    repo_path = 'https://github.com/MLEndDatasets/Yummy'
    image_files_path  = repo_path + '/raw/main/MLEndYD_images/'
    attributes_file   = repo_path + '/raw/main/MLEndYD_image_attributes_benchmark.csv'

    D = pd.read_csv(attributes_file)

    D_attr = list(D)
    if len(subset):
        for key in subset:
            if key not in D_attr:
                raise ValueError(f"Invalid attribute, {key}. Should be one of {list(D)}")
            D_valu = set(list(D[key]))
            values = set(subset[key])

            # Values of any keys are not valid
            # Values of key
            if len(values - D_valu)>0:
                raise ValueError(f"Invalid value of attribute {key}: {values - D_valu}")

    try:
        datadir_main = os.path.join(save_to, 'yummy')
        datadir = os.path.join(datadir_main, 'MLEndYD_images')
        path    = Path(datadir)
        path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print('NOTE:: Path :  \"'+ save_to +'\" is not accessible. Creating  \"yummy\" in  "/tmp\" directory for dataset' )
        save_to = os.path.join('/tmp','MLEnd')
        datadir_main = os.path.join(save_to, 'yummy')
        datadir = os.path.join(datadir_main, 'MLEndYD_images')
        path    = Path(datadir)
        path.mkdir(parents=True, exist_ok=True)

    #print(datadir1,datadir,path)

    D.to_csv(datadir_main+'/MLEndYD_image_attributes_benchmark.csv',index=False)

    Di = D.copy()
    Di['select'] = 0
    for key in subset:
        values = subset[key]
        for value in values:
            Di.loc[Di[key]==value,'select'] = 1

        Di = Di[Di['select']==1]
        Di['select'] = 0

    N = Di.shape[0]
    if verbose: print(f'Downloading {N} image files from {repo_path}')

    filenames = list(Di['filename'])

    if debug_mode: FILE_ERROR=[]

    for k,filename in enumerate(filenames):
        #sp.utils.ProgBar(k,len(filenames),L=50,title=f'{filename}')
        if verbose:
            if pbar_style==None:
                sp.utils.ProgBar(k,len(filenames),style=2,L=50,color='yellow',title=f'{filename}')
            elif pbar_style == 'colab':
                sp.utils.ProgBar_JL(k,len(filenames),style=2,L=50,color='yellow',title=f'{filename}')
            elif pbar_style=='spkit_JL':
                sp.utils.ProgBar_JL(k,len(filenames),style=2,L=50,title=f'{filename}')

        origin = image_files_path + filename
        fpath =  datadir +'/'+ filename
        if not(os.path.isfile(fpath)) or overwrite:

            if debug_mode:
                try:
                    ifpath = _download_file(origin,fpath,bar=False)
                except:
                    FILE_ERROR.append(origin)
            else:
                ifpath = _download_file(origin,fpath,bar=False)

    if debug_mode:
        return datadir_main, FILE_ERROR
    
    return datadir_main

def download_happiness(save_to = '../MLEnd',verbose=1,overwrite=False):
    """Download Happiness Dataset.

    # Arguments
        save_to: loacal path where you want to store the data
                  relative to `../MLEnd/spoken_numerals/`).

    # Returns

    path: path where data is saved


    """
    #DataPath = 'https://github.com/Nikeshbajaj/PhyaatDataset/raw/master/Signals/'
    repo_path = 'https://github.com/MLEndDatasets/Happiness'
    attributes_file   = repo_path + '/raw/main/MLEndHD_attributes.csv'


    D = pd.read_csv(attributes_file)

    try:
        datadir_main = os.path.join(save_to, 'happiness')
        #datadir = os.path.join(datadir_main, 'MLEndSND_audiofiles')
        path    = Path(datadir_main)
        path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print('NOTE:: Path :  \"'+ save_to +'\" is not accessible. Creating  \"happiness\" in  "/tmp\" directory for dataset' )
        save_to = os.path.join('/tmp','MLEnd')
        datadir_main = os.path.join(save_to, 'happiness')
        #datadir = os.path.join(datadir_main, 'MLEndSND_audiofiles')
        path    = Path(datadir_main)
        path.mkdir(parents=True, exist_ok=True)

    #print(datadir1,datadir,path)

    D.to_csv(datadir_main+'/MLEndHD_attributes.csv',index=False)

    return datadir_main

def download_load_happiness():
    """Download Happiness Dataset.

    # Arguments
        save_to: loacal path where you want to store the data
                  relative to `../MLEnd/spoken_numerals/`).

    # Returns

    pandas dataframe

    """
    #DataPath = 'https://github.com/Nikeshbajaj/PhyaatDataset/raw/master/Signals/'
    repo_path = 'https://github.com/MLEndDatasets/Happiness'
    attributes_file   = repo_path + '/raw/main/MLEndHD_attributes.csv'


    D = pd.read_csv(attributes_file)

    return D
