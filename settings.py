import os


""" PATHS AND FOLDERS """

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = CURRENT_PATH + "/database"
CACHE_PATH = CURRENT_PATH + "/cache"


""" DATABASE OF VOICES """

NUMBER_OF_VOICES = 25 # number of voices in the database
NUMBER_OF_SAMPLES = 100 # how many samples has each of voices


""" SAMPLE ANALYSIS """

CACHE_ENABLED = True # load processed data from the cache

FFT_COMPONENTS = 4096 # length of the FFT vector got from sample processing

APPLY_PREEMPHASIS = True # high-pass filter
PREEMPHASIS = 0.95 # from 0.9 to 1

APPLY_LOG_POWER = True # changes FFT energy to dB


""" LEARNING """

from sklearn.decomposition import PCA, FactorAnalysis, FastICA, TruncatedSVD
from sklearn.neighbors import KNeighborsClassifier

DECOMPOSITION_ALGORITHM = FastICA # algorithm used for simplify FFT vector into shorter vector of components
DECOMPOSITION_COMPONENTS = 32 # length of the vector that describes each of samples

CLASSIFIER_ALGORITHM = KNeighborsClassifier # algorithm used for classify samples as appropriate voices

SAMPLES_TO_LEARN = 5 # number of samples to learn


""" OTHER """

LOG_ACTIONS_TO_CONSOLE = True # prints current actions to the console
