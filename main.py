import numpy

from voice import Voice
from sample import Sample

from tester import Tester
from settings import Settings


def hits_ratio(number_of_learning_samples):
	Settings.SAMPLES_TO_LEARN = number_of_learning_samples

	predictions = Tester().perform_analysis()

	hits = 0
	all = 0

	for data in predictions:
		hits += data["correct_prediction"]
		all += data["samples"]

	return hits / all

def propability(number_of_learning_samples):
	Settings.SAMPLES_TO_LEARN = number_of_learning_samples

	predictions = Tester().perform_analysis()
	return numpy.average([data["propability"] for data in predictions])

def non_zero(number_of_learning_samples):
	Settings.SAMPLES_TO_LEARN = number_of_learning_samples

	predictions = Tester().perform_analysis()
	return numpy.average([data["non_zero_predictions"] for data in predictions])

""" HELPERS """

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

def check_algorithms(analysis_function, number_of_learning_samples):
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

			column += [analysis_function(N)]

		columns += [column]

	filename = "{0}_different_algorithms_N_{1}.txt".format(analysis_function.__name__, N)
	save_result_to_file(filename, column_names, columns)

def check_algorithms_range():
	for N in [1, 5, 10, 15, 25, 50]:
		check_algorithms(hits_ratio, N)


""" ANALYSING ALGORITHMS IN FUNCTION OF NUMBER OF LEARNING SAMPLES """

from sklearn.decomposition import PCA, FactorAnalysis, FastICA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

def check_algorithm_pairs(algorithm_pair, analysis_function):
	column_names = ["N"] + ["{0}_{1}".format(pair[0].__name__, pair[1].__name__) for pair in algorithm_pair]
	columns = [list(range(1, 65))]

	for pair in algorithm_pair:
		Settings.DECOMPOSITION_ALGORITHM = pair[0]
		Settings.CLASSIFIER_ALGORITHM = pair[1]

		columns += [[analysis_function(N) for N in range(1, 65)]]

	filename = "algorithms_number_of_learning_samples.txt"
	save_result_to_file(filename, column_names, columns)

algorithm_pairs = [
	(FastICA, GaussianNB),
	(FactorAnalysis, GaussianNB),
	(PCA, GaussianNB),
	(FastICA, KNeighborsClassifier),
	(FactorAnalysis, KNeighborsClassifier),
]

""" HIT RATIO VS PROPABILITY """

def check_algorithm_propability(algorithm_pair, analysis_function):
	column_names = ["N"] + ["{0}_{1}".format(pair[0].__name__, pair[1].__name__) for pair in algorithm_pair]
	columns = [list(range(1, 65))]

	for pair in algorithm_pair:
		Settings.DECOMPOSITION_ALGORITHM = pair[0]
		Settings.CLASSIFIER_ALGORITHM = pair[1]

		columns += [[analysis_function(N) for N in range(1, 65)]]

	filename = "algorithms_propability_number_of_learning_samples.txt"
	save_result_to_file(filename, column_names, columns)

def check_algorithm_nonzero(algorithm_pair, analysis_function):
	column_names = ["N"] + ["{0}_{1}".format(pair[0].__name__, pair[1].__name__) for pair in algorithm_pair]
	columns = [list(range(1, 65))]

	for pair in algorithm_pair:
		Settings.DECOMPOSITION_ALGORITHM = pair[0]
		Settings.CLASSIFIER_ALGORITHM = pair[1]

		columns += [[analysis_function(N) for N in range(1, 65)]]

	filename = "algorithms_nonzero_number_of_learning_samples.txt"
	save_result_to_file(filename, column_names, columns)

""" ANALYSIS """

#check_algorithms_range()
#check_algorithm_pairs(algorithm_pairs, hits_ratio)
#check_algorithm_propability(algorithm_pairs, propability)
check_algorithm_nonzero(algorithm_pairs, non_zero)
