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
		predictions = data["predictions"]

		for prediction in predictions:
			if prediction == voice:
				hits += 1

			all += 1
		
	return hits / all


def hits_ratio_range(sample_range):
	return [hits_ratio(n) for n in sample_range]


def save_result_to_file(filename, column_names=[], columns=[]):

	def write_line(file, columns):
		line = "\t".join([str(cell) for cell in columns]) + "\n"
		file.write(line)

	with open(str(filename), "w+") as file:
		write_line(file, column_names)

		zipped = zip(*columns)

		for column in zipped:
			write_line(file, column)


def hits_ratio_in_function_of_decomposition_components():

	sample_range = list(range(1, 51))

	components_range = [4, 8, 16, 32, 48, 64, 96, 128]
	column_names = ["N"] + [str(N) for N in components_range]
	columns = [sample_range]

	for N in components_range:
		Settings.DECOMPOSITION_COMPONENTS = N

		data = hits_ratio_range(sample_range)
		columns += [data]

	save_result_to_file("hits_ratio_in_function_of_decomposition_components.txt", column_names, columns)


def hits_ratio_in_function_of_decomposition_algorithm():

	sample_range = list(range(1, 51))

	algorithms = Settings.AVAILABLE_DECOMPOSITION_ALGORITHMS
	column_names = ["N"] + [str(algorithm.__name__) for algorithm in algorithms]
	columns = [sample_range]

	for algorithm in algorithms:
		Settings.DECOMPOSITION_ALGORITHM = algorithm

		data = hits_ratio_range(sample_range)
		columns += [data]

	save_result_to_file("hits_ratio_in_function_of_decomposition_algorithm.txt", column_names, columns)


def hits_ratio_in_function_of_classifier_algorithm():

	sample_range = list(range(1, 51))

	algorithms = Settings.AVAILABLE_CLASSIFIER_ALGORITHMS
	column_names = ["N"] + [str(algorithm.__name__) for algorithm in algorithms]
	columns = [sample_range]

	for algorithm in algorithms:
		Settings.CLASSIFIER_ALGORITHM = algorithm

		data = hits_ratio_range(sample_range)
		columns += [data]

	save_result_to_file("hits_ratio_in_function_of_classifier_algorithm.txt", column_names, columns)



hits_ratio_in_function_of_decomposition_components()
hits_ratio_in_function_of_decomposition_algorithm()
hits_ratio_in_function_of_classifier_algorithm()
