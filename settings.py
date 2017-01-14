import os

class Settings():

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

	# list of all available decomposition algorithms
	from sklearn.decomposition import PCA, FactorAnalysis, FastICA, TruncatedSVD
	AVAILABLE_DECOMPOSITION_ALGORITHMS = [
		PCA,
		FactorAnalysis, 
		FastICA, 
		TruncatedSVD
	]

	# list of all available classifier algorithms
	from sklearn.neighbors import KNeighborsClassifier
	from sklearn.naive_bayes import GaussianNB
	from sklearn.ensemble import RandomForestClassifier
	from sklearn.tree import DecisionTreeClassifier
	AVAILABLE_CLASSIFIER_ALGORITHMS = [
		KNeighborsClassifier, 
		GaussianNB,
		RandomForestClassifier, 
		DecisionTreeClassifier
	]

	DECOMPOSITION_ALGORITHM = PCA # algorithm used for simplify FFT vector into shorter vector of components
	DECOMPOSITION_COMPONENTS = 32 # length of the vector that describes each of samples

	CLASSIFIER_ALGORITHM = GaussianNB # algorithm used for classify samples as appropriate voices

	SAMPLES_TO_LEARN = 10 # number of samples to learn


	""" OTHER """

	LOG_ACTIONS_TO_CONSOLE = True # prints current actions to the console
