import numpy

from analysis import Settings, Tester


""" HELPERS """

def analyse(property, learning_samples=25, components=32, voices=25):
	Settings.NUMBER_OF_VOICES = voices
	Settings.SAMPLES_TO_LEARN = learning_samples
	Settings.DECOMPOSITION_COMPONENTS = components

	predictions = Tester().perform_analysis()
	return predictions[property]


def save_result_to_file(filename, column_names=[], columns=[]):

	def write_line(file, columns):
		line = "\t".join([str(cell) for cell in columns]) + "\n"
		file.write(line)

	file_path = "{0}/{1}".format(Settings.ANALYSIS_PATH, filename)

	with open(file_path, "w+") as file:
		write_line(file, column_names)

		zipped = zip(*columns)

		for column in zipped:
			write_line(file, column)


""" FINDING THE BEST PAIRS (DECOMPOSITION, CLASSIFIER) OF ALGORITHMS """

def test_algorithms(property, number_of_learning_samples):
	decompositors = Settings.AVAILABLE_DECOMPOSITION_ALGORITHMS
	classifiers = Settings.AVAILABLE_CLASSIFIER_ALGORITHMS

	N = number_of_learning_samples

	column_names = ["N = " + str(N)] + [str(algorithm.__name__) for algorithm in classifiers]
	columns = [[str(algorithm.__name__) for algorithm in decompositors]]

	for classifier in classifiers:
		Settings.CLASSIFIER_ALGORITHM = classifier
		column = []

		for decompositor in decompositors:
			Settings.DECOMPOSITION_ALGORITHM = decompositor

			column += [analyse(property, learning_samples=N)]

		columns += [column]

	filename = "{0}_different_algorithms_N_{1}_{2}.txt".format(analysis_function.__name__, N, property)
	save_result_to_file(filename, column_names, columns)


def test_algorithms_range():
	for N in [1, 5, 10, 15, 25, 50]:
		test_algorithms(hits_ratio, N)


""" NUMBER OF LEARNING SAMPLES """

from sklearn.decomposition import PCA, FactorAnalysis, FastICA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

def test_learning_samples(algorithm_pair, property):
	column_names = ["N"] + ["{0}_{1}".format(pair[0].__name__, pair[1].__name__) for pair in algorithm_pair]
	columns = [list(range(1, 65))]

	for pair in algorithm_pair:
		Settings.DECOMPOSITION_ALGORITHM = pair[0]
		Settings.CLASSIFIER_ALGORITHM = pair[1]

		columns += [[analyse(property, learning_samples=N) for N in range(1, 65)]]

	filename = "algorithms_number_of_learning_samples_{0}.txt".format(property)
	save_result_to_file(filename, column_names, columns)

algorithm_pairs = [
	(FastICA, GaussianNB),
	(FactorAnalysis, GaussianNB),
	(PCA, GaussianNB),
	(FastICA, KNeighborsClassifier),
	(FactorAnalysis, KNeighborsClassifier),
]


""" NUMBER OF COMPONENTS """

def test_components(algorithm_pair, property):
	column_names = ["C"] + ["{0}_{1}".format(pair[0].__name__, pair[1].__name__) for pair in algorithm_pair]
	columns = [list(range(1, 65))]

	for pair in algorithm_pair:
		Settings.DECOMPOSITION_ALGORITHM = pair[0]
		Settings.CLASSIFIER_ALGORITHM = pair[1]

		columns += [[analyse(property, components=N) for N in range(1, 65)]]

	filename = "algorithms_{0}_number_of_components.txt".format(property)
	save_result_to_file(filename, column_names, columns)


""" NUMBER OF VOICES """

def test_voices(algorithm_pair, property):
	column_names = ["V"] + ["{0}_{1}".format(pair[0].__name__, pair[1].__name__) for pair in algorithm_pair]
	columns = [list(range(1, 65))]

	for pair in algorithm_pair:
		Settings.DECOMPOSITION_ALGORITHM = pair[0]
		Settings.CLASSIFIER_ALGORITHM = pair[1]

		columns += [[analyse(property, voices=N) for N in range(1, 26)]]

	filename = "algorithms_{0}_number_of_voices.txt".format(property)
	save_result_to_file(filename, column_names, columns)


""" ANALYSIS """

#test_algorithms_range()
#test_learning_samples(algorithm_pairs, hits_ratio)
#test_components(algorithm_pairs, "correct_prediction")
#test_voices(algorithm_pairs, "correct_prediction")