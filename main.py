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
		voice = data["voice"]
		hits += data["correct_prediction"]
		all += data["samples"]

	return hits / all


def analyse_for_size(N, function):

	def result():
		return function(N)

	return result

def analyse_range(sample_range, function):
	return [function(n) for n in sample_range]


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

#hits_ratio_range = analyse_range(hits_ratio)
#hits_ratio_range = analyse_for_size(1, hits_ratio)



#hits_ratio_in_function_of_decomposition_components(hits_ratio_range)
#hits_ratio_in_function_of_decomposition_algorithm(hits_ratio_range)
#hits_ratio_in_function_of_classifier_algorithm(hits_ratio_range)
