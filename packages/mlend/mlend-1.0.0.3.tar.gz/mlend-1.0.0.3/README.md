# MLEnd Datasets

### Links: **[Homepage](https://MLEndDatasets.github.io)** | **[Documentation](https://mlend.readthedocs.io/)** | **[Github](https://github.com/MLEndDatasets)**  |  **[PyPi - project](https://pypi.org/project/mlend/)** |     _ **Installation:** [pip install mlend](https://pypi.org/project/mlend/)
-----

-----

## Installation

**Requirement**:  numpy, matplotlib, scipy.stats, spkit

### with pip

```
pip install mlend
```

### update with pip

```
pip install mlend --upgrade
```


## Download data :  Spoken Numerals

```
import mlend
from mlend import download_spoken_numerals, spoken_numerals_load


datadir = download_spoken_numerals(save_to = '../Data/MLEnd', subset = {},verbose=1,overwrite=False)

```

## Create Training and Testing Sets

```
TrainSet, TestSet, MAPs = spoken_numerals_load(datadir_main = datadir, train_test_split = 'Benchmark_B', verbose=1,encode_labels=True)

```

## Download data :  London Sounds


```
import mlend
from mlend import download_london_sounds, london_sounds_load


datadir = download_london_sounds(save_to = '../Data/MLEnd', subset = {},verbose=1,overwrite=False)

```


## Download data :  Hums and Whistles


```
import mlend
from mlend import download_hums_whistles, hums_whistles_load


datadir = download_hums_whistles(save_to = '../Data/MLEnd', subset = {},verbose=1,overwrite=False)

```






# Contacts:
* **Jesús Requena Carrión**
* Queen Mary University of London

* **Nikesh Bajaj**
* Queen Mary University of London
* n.bajaj[AT]qmul.ac.uk, n.bajaj[AT]imperial[dot]ac[dot]uk

______________________________________
