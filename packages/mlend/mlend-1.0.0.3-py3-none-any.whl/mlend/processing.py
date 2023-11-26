'''
Author @ Nikesh Bajaj
Date: 22 Oct 2017
Contact: n.bajaj@qmul.ac.uk

'''

from __future__ import absolute_import, division, print_function
name = "MLEnd | Processing "
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
import warnings
import spkit as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def spoken_numerals_load(datadir_main = '../MLEnd/spoken_numerals', train_test_split = 'Benchmark_A', verbose=1,encode_labels=True):


    """Read files of Spoken Numerals Dataset and create training and testing sets.


    # Arguments
        datadir_main (str): local path where 'MLEndSND_audiofiles' directory is stored
                  relative to `../MLEnd/spoken_numerals/`).
        train_test_split (str): split type for training and testing
          - 'Benchmark_A': Speaker Independent Benchmark
             Training (70%) and Testing (30%) do not have any common speaker
          - 'Benchmark_B': Speaker Dependent Benchmark
             Training (70%) and Testing (30%) both sets have same speakers
          - 'Random' or 'random': random split woth 70-30
          - float (e.g. 0.8) (>0 and <1)
            random split with given fraction for training set.
            if train_test_split = 0.8, Training set will be 80% and Testing 20%

        encode_labels: (bool), if to encode labels

    # Raises
        ValueError:
         - if train_test_split is not str ['Benchmark_A', 'Benchmark_B', 'random'] or float (<1 and >0)"

    # Returns
        TrainSet: A dictionary with keys {'X_paths', 'Y', 'Y_encoded'}
        TestSet:  A dictionary with keys {'X_paths', 'Y', 'Y_encoded'}
          - 'X_paths' is list of paths for audio files
          - 'Y' is Nx3 np.array, column 0 for Numerals, 1 for Intonation and 2 for Speaker
          - 'Y_encoded' is Nx3 np.array same as 'Y', column 0 for Numerals, 1 for Intonation and 2 for Speaker
                each column is encoded as 0, 1, 2 ..

        MAPs : A dictionary of maps, if encode_labels is true, else an empty dictionary


    """


    repo_path = 'https://github.com/MLEndDatasets/SpokenNumerals'
    attributes_file_org   = repo_path + '/raw/main/MLEndSND_audio_attributes_benchmark.csv'
    #speaker_demog_file_org = repo_path + '/raw/main/MLEndSND_speakers_demographics_benchmark.csv'


    audio_files = glob.glob(datadir_main+'/MLEndSND_audiofiles/*.wav')
    if verbose: print(f'Total {len(audio_files)} found in {datadir_main}/MLEndSND_audiofiles/')

    attributes_file = datadir_main +'/MLEndSND_audio_attributes_benchmark.csv'
    if os.path.isfile(attributes_file):
        D = pd.read_csv(attributes_file)
    else:
        D = pd.read_csv(attributes_file_org)


    aud_files_map = {file.split('/')[-1]:file for file in audio_files}
    afiles = list(aud_files_map.keys())

    Di = D.copy()
    Di['select'] = Di['filename'].apply(lambda x: True if x in afiles else False)
    Di = Di[Di['select']==True]


    X_train_filepath = []
    Y_train =[]

    X_test_filepath = []
    Y_test = []

    if isinstance(train_test_split,str):
        if train_test_split in ['Benchmark_A', 'Benchmark_B']:
            D_train = Di[Di[train_test_split]=='Train']
            D_test  = Di[Di[train_test_split]=='Test']

        elif train_test_split.lower()=='random':
            #idx = np.random.rand(Di.shape[0])<=0.7
            Nt = int(Di.shape[0]*0.7)
            idx = [True]*Nt + [False]*(Di.shape[0]-Nt)
            idx= np.array(idx)
            np.random.shuffle(idx)
            D_train = Di[idx]
            D_test  = Di[~idx]
            D_train = Di[idx]
            D_test  = Di[~idx]
    elif isinstance(train_test_split,float) and train_test_split<1 and train_test_split>0:
        #idx = np.random.rand(Di.shape[0])<=train_test_split
        Nt = int(Di.shape[0]*train_test_split)
        idx = [True]*Nt + [False]*(Di.shape[0]-Nt)
        idx= np.array(idx)
        np.random.shuffle(idx)
        D_train = Di[idx]
        D_test  = Di[~idx]
    else:
        raise ValueError(f"invalide value for train_test_split : {train_test_split},\n Should be str ['Benchmark_A', 'Benchmark_B', 'random'] or float (<1 and >0)")

    #display(D_train)
    #display(D_test)

    files_train = list(D_train['filename'])
    X_train_filepath = [aud_files_map[file] for file in files_train]
    Y_train = np.array(D_train[['Numeral','Intonation','Speaker']])

    #print(Y_train)

    files_test = list(D_test['filename'])
    X_test_filepath = [aud_files_map[file] for file in files_test]
    Y_test = np.array(D_test[['Numeral','Intonation','Speaker']])


    TrainSet = {'X_paths':X_train_filepath, 'Y':Y_train}
    TestSet  = {'X_paths':X_test_filepath, 'Y':Y_test}

    Y_train_enc =[]
    Y_test_enc =[]
    MAPs = {}

    flag1,flag2,flag3 = False,False,False

    if encode_labels:
        numeral_map ={}
        y1 = Y_train[:,0].copy().astype(int)
        y2 = Y_test[:,0].copy().astype(int)

        y_set = list(set(y1)|set(y2))
        y_set.sort()
        if len(y_set)==1: flag1=True
        for k,v in enumerate(y_set):
            numeral_map[v]=k
            y1[y1==v]=k
            y2[y2==v]=k

        Y_train_enc.append(y1)
        Y_test_enc.append(y2)


        intonation_map ={}
        y1 = Y_train[:,1].copy()
        y2 = Y_test[:,1].copy()
        y_set = list(set(y1)|set(y2))
        y_set.sort()
        if len(y_set)==1: flag2=True
        for k,v in enumerate(y_set):
            intonation_map[v]=k
            y1[y1==v]=k
            y2[y2==v]=k

        Y_train_enc.append(y1)
        Y_test_enc.append(y2)


        speaker_map ={}
        y1 = Y_train[:,2].astype(int).copy()
        y2 = Y_test[:,2].astype(int).copy()
        y_set = list(set(y1)|set(y2))
        y_set.sort()
        if len(y_set)==1: flag3=True

        for k,v in enumerate(y_set):
            speaker_map[v]=k
            y1[y1==v]=k
            y2[y2==v]=k

        Y_train_enc.append(y1)
        Y_test_enc.append(y2)

        Y_train_enc = np.vstack(Y_train_enc).T.astype(int)
        Y_test_enc = np.vstack(Y_test_enc).T.astype(int)

        MAPs = {'Numeral':numeral_map, 'Intonation':intonation_map, 'Speaker':speaker_map}

        TrainSet['Y_encoded'] = Y_train_enc
        TestSet['Y_encoded'] = Y_test_enc

        if flag1 and flag2 and flag3:
            warnings.warn('None of the attribuates have more than one unique value. Check the catogories in subset of data, while downloading.')


    return TrainSet,TestSet, MAPs

def london_sounds_load(datadir_main = '../MLEnd/london_sounds', train_test_split = 'Benchmark_A', verbose=1,encode_labels=True):


    """Read files of London Sounds Dataset and create training and testing sets.


    # Arguments
        datadir_main (str): local path where 'MLEndLSD_audiofiles' directory is stored
                  relative to `../MLEnd/london_sounds/`).
        train_test_split (str): split type for training and testing
          - 'Benchmark_A': Fixed Benchmark
             Training (70%) and Testing (30%)
          - 'Random' or 'random': random split woth 70-30
          - float (e.g. 0.8) (>0 and <1)
            random split with given fraction for training set.
            if train_test_split = 0.8, Training set will be 80% and Testing 20%

        encode_labels: (bool), if to encode labels

    # Raises
        ValueError:
         - if train_test_split is not str ['Benchmark_A', 'random'] or float (<1 and >0)"

    # Returns
        TrainSet: A dictionary with keys {'X_paths', 'Y', 'Y_encoded'}
        TestSet:  A dictionary with keys {'X_paths', 'Y', 'Y_encoded'}
          - 'X_paths' is list of paths for audio files
          - 'Y' is Nx3 np.array, column 0 for Area, 1 for Spot, and 2 for In_Out
          - 'Y_encoded' is Nx3 np.array same as 'Y', column 0 for Area, 1 for Spot and 2 for In_Out
                each column is encoded as 0, 1, 2 ..

        MAPs : A dictionary of maps, if encode_labels is true, else an empty dictionary


    """


    repo_path = 'https://github.com/MLEndDatasets/LondonSounds'
    attributes_file_org   = repo_path + '/raw/main/MLEndLSD_audio_attributes_benchmark.csv'
    #speaker_demog_file_org = repo_path + '/raw/main/MLEndSND_speakers_demographics_benchmark.csv'


    audio_files = glob.glob(datadir_main+'/MLEndLSD_audiofiles/*.wav')
    if verbose: print(f'Total {len(audio_files)} found in {datadir_main}/MLEndLSD_audiofiles/')

    attributes_file = datadir_main +'/MLEndLSD_audio_attributes_benchmark.csv'
    if os.path.isfile(attributes_file):
        D = pd.read_csv(attributes_file)
    else:
        D = pd.read_csv(attributes_file_org)


    aud_files_map = {file.split('/')[-1]:file for file in audio_files}
    afiles = list(aud_files_map.keys())

    Di = D.copy()
    Di['select'] = Di['filename'].apply(lambda x: True if x in afiles else False)
    Di = Di[Di['select']==True]


    X_train_filepath = []
    Y_train =[]

    X_test_filepath = []
    Y_test = []

    if isinstance(train_test_split,str):
        if train_test_split in ['Benchmark_A']:
            D_train = Di[Di[train_test_split]=='Train']
            D_test  = Di[Di[train_test_split]=='Test']

        elif train_test_split.lower()=='random':
            #idx = np.random.rand(Di.shape[0])<=0.7
            Nt = int(Di.shape[0]*0.7)
            idx = [True]*Nt + [False]*(Di.shape[0]-Nt)
            idx= np.array(idx)
            np.random.shuffle(idx)
            D_train = Di[idx]
            D_test  = Di[~idx]
    elif isinstance(train_test_split,float) and train_test_split<1 and train_test_split>0:
        #idx = np.random.rand(Di.shape[0])<=train_test_split
        #idx = np.random.rand(Di.shape[0])<=0.7
        Nt = int(Di.shape[0]*train_test_split)
        idx = [True]*Nt + [False]*(Di.shape[0]-Nt)
        idx= np.array(idx)
        np.random.shuffle(idx)
        D_train = Di[idx]
        D_test  = Di[~idx]
    else:
        raise ValueError(f"invalide value for train_test_split : {train_test_split},\n Should be str ['Benchmark_A', 'random'] or float (<1 and >0)")

    #display(D_train)
    #display(D_test)

    files_train = list(D_train['filename'])
    X_train_filepath = [aud_files_map[file] for file in files_train]
    Y_train = np.array(D_train[['Area','Spot','In_Out']])

    #print(Y_train)

    files_test = list(D_test['filename'])
    X_test_filepath = [aud_files_map[file] for file in files_test]
    Y_test = np.array(D_test[['Area','Spot','In_Out']])


    TrainSet = {'X_paths':X_train_filepath, 'Y':Y_train}
    TestSet  = {'X_paths':X_test_filepath, 'Y':Y_test}

    Y_train_enc =[]
    Y_test_enc =[]
    MAPs = {}

    flag1,flag2,flag3 = False,False,False

    if encode_labels:
        area_map ={}
        y1 = Y_train[:,0].copy()
        y2 = Y_test[:,0].copy()

        y_set = list(set(y1)|set(y2))
        y_set.sort()
        if len(y_set)==1: flag1=True

        for k,v in enumerate(y_set):
            area_map[v]=k
            y1[y1==v]=k
            y2[y2==v]=k

        Y_train_enc.append(y1)
        Y_test_enc.append(y2)


        spot_map ={}
        y1 = Y_train[:,1].copy()
        y2 = Y_test[:,1].copy()
        y_set = list(set(y1)|set(y2))
        y_set.sort()
        if len(y_set)==1: flag2=True

        for k,v in enumerate(y_set):
            spot_map[v]=k
            y1[y1==v]=k
            y2[y2==v]=k

        Y_train_enc.append(y1)
        Y_test_enc.append(y2)


        in_out_map ={}
        y1 = Y_train[:,2].copy()
        y2 = Y_test[:,2].copy()
        y_set = list(set(y1)|set(y2))
        y_set.sort()
        if len(y_set)==1: flag3=True

        for k,v in enumerate(y_set):
            in_out_map[v]=k
            y1[y1==v]=k
            y2[y2==v]=k

        Y_train_enc.append(y1)
        Y_test_enc.append(y2)

        Y_train_enc = np.vstack(Y_train_enc).T.astype(int)
        Y_test_enc = np.vstack(Y_test_enc).T.astype(int)

        MAPs = {'Area':area_map, 'Spot':spot_map, 'In_Out':in_out_map}

        TrainSet['Y_encoded'] = Y_train_enc
        TestSet['Y_encoded'] = Y_test_enc
        if flag1 and flag2 and flag3:
            warnings.warn('None of the attribuates have more than one unique value. Check the catogories in subset of data, while downloading.')

    return TrainSet,TestSet, MAPs

def hums_whistles_load(datadir_main = '../MLEnd/hums_whistles', train_test_split = 'Benchmark_A', verbose=1,encode_labels=True):


    """Read files of Hums and Whistles Dataset and create training and testing sets.


    # Arguments
        datadir_main (str): local path where 'MLEndHWD_audiofiles' directory is stored
                  relative to `../MLEnd/hums_whistles/`).
        train_test_split (str): split type for training and testing
          - 'Benchmark_A': Speaker Independent Benchmark
             Training (70%) and Testing (30%) do not have any common speaker
          - 'Benchmark_B': Speaker Dependent Benchmark
             Training (70%) and Testing (30%) both sets have same speakers
          - 'Random' or 'random': random split woth 70-30
          - float (e.g. 0.8) (>0 and <1)
            random split with given fraction for training set.
            if train_test_split = 0.8, Training set will be 80% and Testing 20%

        encode_labels: (bool), if to encode labels

    # Raises
        ValueError:
         - if train_test_split is not str ['Benchmark_A', 'Benchmark_B', 'random'] or float (<1 and >0)"

    # Returns
        TrainSet: A dictionary with keys {'X_paths', 'Y', 'Y_encoded'}
        TestSet:  A dictionary with keys {'X_paths', 'Y', 'Y_encoded'}
          - 'X_paths' is list of paths for audio files
          - 'Y' is Nx3 np.array, column 0 for Song, 1 for Interpretation, and 2 for Interpreter
          - 'Y_encoded' is Nx3 np.array same as 'Y', column 0 for Song, 1 for Interpretation and 2 for Interpreter
                each column is encoded as 0, 1, 2 ..

        MAPs : A dictionary of maps, if encode_labels is true, else an empty dictionary


    """


    repo_path = 'https://github.com/MLEndDatasets/HumsAndWhistles'
    attributes_file_org   = repo_path + '/raw/main/MLEndHWD_audio_attributes_benchmark.csv'
    interptr_demog_file_org = repo_path + '/raw/main/MLEndHWD_interpreter_demographics_benchmark.csv'


    audio_files = glob.glob(datadir_main+'/MLEndHWD_audiofiles/*.wav')
    if verbose: print(f'Total {len(audio_files)} found in {datadir_main}/MLEndLSD_audiofiles/')

    attributes_file = datadir_main +'/MLEndHWD_audio_attributes_benchmark.csv'
    if os.path.isfile(attributes_file):
        D = pd.read_csv(attributes_file)
    else:
        D = pd.read_csv(attributes_file_org)


    aud_files_map = {file.split('/')[-1]:file for file in audio_files}
    afiles = list(aud_files_map.keys())

    Di = D.copy()
    Di['select'] = Di['filename'].apply(lambda x: True if x in afiles else False)
    Di = Di[Di['select']==True]


    X_train_filepath = []
    Y_train =[]

    X_test_filepath = []
    Y_test = []

    if isinstance(train_test_split,str):
        if train_test_split in ['Benchmark_A','Benchmark_B']:
            D_train = Di[Di[train_test_split]=='Train']
            D_test  = Di[Di[train_test_split]=='Test']

        elif train_test_split.lower()=='random':
            #idx = np.random.rand(Di.shape[0])<=0.7
            Nt = int(Di.shape[0]*0.7)
            idx = [True]*Nt + [False]*(Di.shape[0]-Nt)
            idx= np.array(idx)
            np.random.shuffle(idx)
            D_train = Di[idx]
            D_test  = Di[~idx]
    elif isinstance(train_test_split,float) and train_test_split<1 and train_test_split>0:
        #idx = np.random.rand(Di.shape[0])<=train_test_split
        #idx = np.random.rand(Di.shape[0])<=0.7
        Nt = int(Di.shape[0]*train_test_split)
        idx = [True]*Nt + [False]*(Di.shape[0]-Nt)
        idx= np.array(idx)
        np.random.shuffle(idx)
        D_train = Di[idx]
        D_test  = Di[~idx]
    else:
        raise ValueError(f"invalide value for train_test_split : {train_test_split},\n Should be str ['Benchmark_A', 'random'] or float (<1 and >0)")

    #display(D_train)
    #display(D_test)

    files_train = list(D_train['filename'])
    X_train_filepath = [aud_files_map[file] for file in files_train]
    Y_train = np.array(D_train[['Song','Interpretation','Interpreter']])

    #print(Y_train)

    files_test = list(D_test['filename'])
    X_test_filepath = [aud_files_map[file] for file in files_test]
    Y_test = np.array(D_test[['Song','Interpretation','Interpreter']])


    TrainSet = {'X_paths':X_train_filepath, 'Y':Y_train}
    TestSet  = {'X_paths':X_test_filepath, 'Y':Y_test}

    Y_train_enc =[]
    Y_test_enc =[]
    MAPs = {}
    flag1,flag2,flag3 = False,False,False

    if encode_labels:
        song_map ={}
        y1 = Y_train[:,0].copy()
        y2 = Y_test[:,0].copy()

        y_set = list(set(y1)|set(y2))
        y_set.sort()
        if len(y_set)==1: flag1=True

        for k,v in enumerate(y_set):
            song_map[v]=k
            y1[y1==v]=k
            y2[y2==v]=k

        Y_train_enc.append(y1)
        Y_test_enc.append(y2)


        interpretation_map ={}
        y1 = Y_train[:,1].copy()
        y2 = Y_test[:,1].copy()
        y_set = list(set(y1)|set(y2))
        y_set.sort()
        if len(y_set)==1: flag2=True

        for k,v in enumerate(y_set):
            interpretation_map[v]=k
            y1[y1==v]=k
            y2[y2==v]=k

        Y_train_enc.append(y1)
        Y_test_enc.append(y2)


        interpreter_map ={}
        y1 = Y_train[:,2].astype(int).copy()
        y2 = Y_test[:,2].astype(int).copy()
        y_set = list(set(y1)|set(y2))
        y_set.sort()
        if len(y_set)==1: flag3=True

        for k,v in enumerate(y_set):
            interpreter_map[v]=k
            y1[y1==v]=k
            y2[y2==v]=k

        Y_train_enc.append(y1)
        Y_test_enc.append(y2)

        Y_train_enc = np.vstack(Y_train_enc).T.astype(int)
        Y_test_enc = np.vstack(Y_test_enc).T.astype(int)

        MAPs = {'Song':song_map, 'Interpretation':interpretation_map, 'Interpreter':interpreter_map}

        TrainSet['Y_encoded'] = Y_train_enc
        TestSet['Y_encoded'] = Y_test_enc

        if flag1 and flag2 and flag3:
            warnings.warn('None of the attribuates have more than one unique value. Check the catogories in subset of data, while downloading.')

    return TrainSet,TestSet, MAPs

def yummy_small_load(datadir_main = '../MLEnd/yummy', train_test_split = 'Benchmark_A', verbose=1,encode_labels=True):


    """Read files of Yummy Dataset and create training and testing sets.


    # Arguments
        datadir_main (str): local path where 'MLEndHWD_audiofiles' directory is stored
                  relative to `../MLEnd/hums_whistles/`).
        train_test_split (str): split type for training and testing
          - 'Benchmark_A': Speaker Independent Benchmark
             Training (70%) and Testing (30%) do not have any common speaker
          - 'Random' or 'random': random split woth 70-30
          - float (e.g. 0.8) (>0 and <1)
            random split with given fraction for training set.
            if train_test_split = 0.8, Training set will be 80% and Testing 20%

        encode_labels: (bool), if to encode labels

    # Raises
        ValueError:
         - if train_test_split is not str ['Benchmark_A', 'random'] or float (<1 and >0)"

    # Returns
        TrainSet: A dictionary with keys {'X_list', 'Y', 'Y_encoded'}
        TestSet:  A dictionary with keys {'X_list', 'Y', 'Y_encoded'}
          - 'X_paths' is list of paths for audio files
          - 'Y' is Nx1 np.array,
          - 'Y_encoded' is Nx1 np.array same as 'Y', 0=rice 1=chips

        MAPs : A dictionary of maps, if encode_labels is true, else an empty dictionary


    """


    repo_path = 'https://github.com/MLEndDatasets/Yummy'
    attributes_file_org   = repo_path + '/raw/main/MLEndYD_image_attributes_small.csv'


    img_files = glob.glob(datadir_main+'/MLEndYD_images_small/*.jpg')
    if verbose: print(f'Total {len(img_files)} found in {datadir_main}/MLEndYD_images_small/')

    attributes_file = datadir_main +'/MLEndYD_image_attributes_small.csv'
    if os.path.isfile(attributes_file):
        D = pd.read_csv(attributes_file)
    else:
        D = pd.read_csv(attributes_file_org)


    img_files_map = {file.split('/')[-1]:file for file in img_files}
    #afiles = list(img_files_map.keys())

    Di = D.copy()

    X_train_filepath = []
    Y_train =[]

    X_test_filepath = []
    Y_test = []

    if isinstance(train_test_split,str):
        if train_test_split in ['Benchmark_A']:
            D_train = Di[Di[train_test_split]=='Train']
            D_test  = Di[Di[train_test_split]=='Test']

        elif train_test_split.lower()=='random':
            #idx = np.random.rand(Di.shape[0])<=0.7
            Nt = int(Di.shape[0]*0.7)
            idx = [True]*Nt + [False]*(Di.shape[0]-Nt)
            idx= np.array(idx)
            np.random.shuffle(idx)
            D_train = Di[idx]
            D_test  = Di[~idx]
    elif isinstance(train_test_split,float) and train_test_split<1 and train_test_split>0:
        #idx = np.random.rand(Di.shape[0])<=train_test_split
        #idx = np.random.rand(Di.shape[0])<=0.7
        Nt = int(Di.shape[0]*train_test_split)
        idx = [True]*Nt + [False]*(Di.shape[0]-Nt)
        idx= np.array(idx)
        np.random.shuffle(idx)
        D_train = Di[idx]
        D_test  = Di[~idx]
    else:
        raise ValueError(f"invalide value for train_test_split : {train_test_split},\n Should be str ['Benchmark_A', 'random'] or float (<1 and >0)")

    #display(D_train)
    #display(D_test)

    files_train = list(D_train['filename'])
    X_train_filepath = [img_files_map[file] for file in files_train]
    Y_train = np.array(D_train['Rice_Chips']).copy()

    #print(Y_train)
    #display(D_train)
    #print(Y_train)

    files_test = list(D_test['filename'])
    X_test_filepath = [img_files_map[file] for file in files_test]
    Y_test = np.array(list(D_test['Rice_Chips'])).copy()


    TrainSet = {'X_paths':X_train_filepath, 'Y':Y_train}
    TestSet  = {'X_paths':X_test_filepath, 'Y':Y_test}

    Y_train_enc =[]
    Y_test_enc =[]
    MAPs = {}

    if encode_labels:
        ricechips_map ={}
        y1 = Y_train[:].copy()
        y2 = Y_test[:].copy()

        y_set = list(set(y1)|set(y2))
        y_set.sort()

        for k,v in enumerate(y_set):
            ricechips_map[v]=k
            y1[y1==v]=k
            y2[y2==v]=k

        Y_train_enc = y1
        Y_test_enc = y2

        MAPs = {'Rice_Chips':ricechips_map}

        TrainSet['Y_encoded'] = Y_train_enc.astype(int)
        TestSet['Y_encoded'] = Y_test_enc.astype(int)

    return TrainSet,TestSet, MAPs

def yummy_load(datadir_main = '../MLEnd/yummy/', train_test_split = 'Benchmark_A', verbose=1,
               attributes_as_labels = 'all',encode_labels=False):


    """Read files of Yummy Dataset and create training and testing sets.


    # Arguments
        datadir_main (str): local path where 'MLEndYD_images' directory is stored
                  relative to `../MLEnd/yummy/`).
        train_test_split (str): split type for training and testing
          - 'Benchmark_A': A predifined fixed split
             Training (70%) and Testing (30%)
          - 'Random' or 'random': random split woth 70-30
          - float (e.g. 0.8) (>0 and <1)
            random split with given fraction for training set.
            if train_test_split = 0.8, Training set will be 80% and Testing 20%

        attributes_as_labels: list of attribuetes as labels
          - attributes_as_labels = 'all' will return all the attribuetes as label
          - attributes_as_labels = ['Diet','Healthiness_rating'] will return Y_train and Y_test as Nx2 columns diet and healthiness rating as labels

        encode_labels: (bool), if to encode labels
          - Only 'Diet', 'Home_restaurent', 'Healthiness_rating' and 'Likeness' will be encoded and return as numpy array
          - regardless of selection of attribuetes for labels

    # Raises
        ValueError:
         - if train_test_split is not str ['Benchmark_A', 'random'] or float (<1 and >0)"

    # Returns
        TrainSet: A dictionary with keys {'X_list', 'Y', 'Y_encoded'}
        TestSet:  A dictionary with keys {'X_list', 'Y', 'Y_encoded'}
          - 'X_paths' is list of paths for audio files
          - 'Y' is NxC Pandas DataFrame,
          - 'Y_encoded' is Nx4 np.array encoded labels for Diet, Home_or_restaurent, Healthiness and Likeness in that order.

        MAPs : A dictionary of maps, if encode_labels is true, else an empty dictionary


    """


    repo_path = 'https://github.com/MLEndDatasets/Yummy'
    attributes_file_org   = repo_path + '/raw/main/MLEndYD_image_attributes_small.csv'


    img_files = glob.glob(datadir_main+'/MLEndYD_images/*.jpg')
    if verbose: print(f'Total {len(img_files)} found in {datadir_main}/MLEndYD_images/')

    attributes_file = datadir_main +'/MLEndYD_image_attributes_benchmark.csv'
    if os.path.isfile(attributes_file):
        D = pd.read_csv(attributes_file)
    else:
        D = pd.read_csv(attributes_file_org)


    img_files_map = {file.split('/')[-1]:file for file in img_files}
    img_filenames = list(img_files_map.keys())

    Di = D.copy()
    Di['select'] = Di['filename'].apply(lambda x: True if x in img_filenames else False)
    Di = Di[Di['select']==True]

    X_train_filepath = []
    Y_train =[]

    X_test_filepath = []
    Y_test = []

    if isinstance(train_test_split,str):
        if train_test_split in ['Benchmark_A']:
            D_train = Di[Di[train_test_split]=='Train']
            D_test  = Di[Di[train_test_split]=='Test']

        elif train_test_split.lower()=='random':
            #idx = np.random.rand(Di.shape[0])<=0.7
            Nt = int(Di.shape[0]*0.7)
            idx = [True]*Nt + [False]*(Di.shape[0]-Nt)
            idx= np.array(idx)
            np.random.shuffle(idx)
            D_train = Di[idx]
            D_test  = Di[~idx]
    elif isinstance(train_test_split,float) and train_test_split<1 and train_test_split>0:
        #idx = np.random.rand(Di.shape[0])<=train_test_split
        #idx = np.random.rand(Di.shape[0])<=0.7
        Nt = int(Di.shape[0]*train_test_split)
        idx = [True]*Nt + [False]*(Di.shape[0]-Nt)
        idx= np.array(idx)
        np.random.shuffle(idx)
        D_train = Di[idx]
        D_test  = Di[~idx]
    else:
        raise ValueError(f"invalide value for train_test_split : {train_test_split},\n Should be str ['Benchmark_A', 'random'] or float (<1 and >0)")

    #display(D_train)
    #display(D_test)

    files_train = list(D_train['filename'])
    X_train_filepath = [img_files_map[file] for file in files_train]
    if isinstance(attributes_as_labels,str) and attributes_as_labels == 'all':
        Y_train = D_train[['Diet','Cuisine','Home_or_restaurant','Healthiness_rating','Likeness','Dish_name','Ingredients','Healthiness_rating_int','Likeness_int']].copy()
    elif isinstance(attributes_as_labels,list):
        Y_train = D_train[attributes_as_labels].copy()
    else:
        raise ValueError("Invalide values in attributes_as_labels. it should be 'all' or a list of attributes: ['Diet','Cusine','Home_or_restaurant','Healthiness_rating','Likeness','Dish_name','Ingredients','Healthiness_rating_int','Likeness_int']")
    #print(Y_train)
    #display(D_train)
    #print(Y_train)

    files_test = list(D_test['filename'])
    X_test_filepath = [img_files_map[file] for file in files_test]
    #Y_test = np.array(list(D_test['Rice_Chips'])).copy()
    if isinstance(attributes_as_labels,str) and attributes_as_labels == 'all':
        Y_test = D_test[['Diet','Cuisine','Home_or_restaurant','Healthiness_rating','Likeness','Dish_name','Ingredients','Healthiness_rating_int','Likeness_int']].copy()
    elif isinstance(attributes_as_labels,list):
        Y_test = D_test[attributes_as_labels].copy()
    else:
        raise ValueError("Invalide values in attributes_as_labels. it should be 'all' or a list of attributes: ['Diet','Cusine','Home_or_restaurant','Healthiness_rating','Likeness','Dish_name','Ingredients','Healthiness_rating_int','Likeness_int']")



    TrainSet = {'X_paths':X_train_filepath, 'Y':Y_train}
    TestSet  = {'X_paths':X_test_filepath, 'Y':Y_test}

    Y_train_enc =[]
    Y_test_enc =[]
    MAPs = {}

    if encode_labels:
        # Diet
        diet_map ={}
        y1 = D_train['Diet'].to_numpy().copy()
        y2 = D_test['Diet'].to_numpy().copy()

        y_set = list(set(y1)|set(y2))
        y_set.sort()

        for k,v in enumerate(y_set):
            diet_map[v]=k
            y1[y1==v]=k
            y2[y2==v]=k

        Y_train_enc.append(y1.astype(float))
        Y_test_enc.append(y2.astype(float))

        # Home/Restaurant
        home_map ={'home':0, 'restaurant':1}

        y1 = (D_train['Home_or_restaurant']!='home').to_numpy().astype(float)
        y2 = (D_test['Home_or_restaurant']!='home').to_numpy().astype(float)

        Y_train_enc.append(y1.astype(float))
        Y_test_enc.append(y2.astype(float))

        # Healthiness_rating
        map_health = {'very_unhealthy':1,'unhealthy':2, 'neutral':3,'healthy':4,'very_healthy':5}

        y1 = D_train['Healthiness_rating_int'].to_numpy().astype(float)
        y2 = D_test['Healthiness_rating_int'].to_numpy().astype(float)

        Y_train_enc.append(y1.astype(float))
        Y_test_enc.append(y2.astype(float))


        # Likeness
        map_like = {'strongly_dislike':1, 'dislike':2,'neutral':3,'like':4, 'strongly_like':5}

        y1 = D_train['Likeness_int'].to_numpy().astype(float)
        y2 = D_test['Likeness_int'].to_numpy().astype(float)

        Y_train_enc.append(y1.astype(float))
        Y_test_enc.append(y2.astype(float))

        Y_train_enc = np.vstack(Y_train_enc).T.astype(float)
        Y_test_enc = np.vstack(Y_test_enc).T.astype(float)


        TrainSet['Y_encoded'] = Y_train_enc
        TestSet['Y_encoded'] = Y_test_enc

        MAPs = {'Diet':diet_map, 'Home_or_restaurant':home_map, 'Healthiness_rating':map_health, 'Likeness_int':map_like}


    return TrainSet,TestSet, MAPs

def happiness_load(datadir_main = '../MLEnd/happiness',train_test_split = 'Benchmark_A',verbose=1,overwrite=False):
    """Read Happiness Dataset.

    # Arguments
        save_to: loacal path where you want to store the data
                  relative to `../MLEnd/happiness/`).

    # Returns

    path: path where data is saved
    """

    D = pd.read_csv(datadir_main+'/MLEndHD_attributes.csv')

    return D