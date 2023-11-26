from __future__ import absolute_import, division, print_function

name = "MLEnd Datasets"
__version__ = '1.0.0.3'
__author__ = 'Jesús Requena Carrión and Nikesh Bajaj'



import sys, os

sys.path.append(os.path.dirname(__file__))

from .downloader import (download_spoken_numerals, download_london_sounds, download_hums_whistles)
from .downloader import (download_yummy_small, download_yummy, download_happiness,download_load_happiness)
from .processing import spoken_numerals_load, london_sounds_load, hums_whistles_load, yummy_small_load, yummy_load
from .processing import happiness_load
# from .downloader import ProgBar, ProgBar_JL

#__all__ = ['data','load_data','cwt','utils','io','geometry','eeg' ,'mea','stats','pylfsr', 'ml','tf_utils']
