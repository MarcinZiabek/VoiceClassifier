import numpy

from analysis.voice import Voice
from analysis.sample import Sample

from analysis.settings import Settings


class Tester():

	def __init__(self):
		self.voices = []
		self.analyser = Settings.DECOMPOSITION_ALGORITHM(n_components=Settings.DECOMPOSITION_COMPONENTS)
		self.classifier = Settings.CLASSIFIER_ALGORITHM()

	def log_action(self, text):
		if Settings.LOG_ACTIONS_TO_CONSOLE:
			print(str(text))

	def perform_analysis(self):
		self.load_voices()
		self.load_samples()
		self.learn()

		return self.get_predictions()
	
	def load_voices(self):
		self.log_action("loading {0} voices".format(Settings.NUMBER_OF_VOICES))
		self.voices = [Voice(i) for i in range(0, Settings.NUMBER_OF_VOICES)]

	def load_samples(self):
		self.log_action("loading samples")

		for voice in self.voices:
			self.log_action("{0}".format(voice.id))
			voice.read_samples()

	def learn(self):
		self.log_action("learning")

		features = []
		target = []

		for voice in self.voices:
			samples_to_learn = voice.samples[0:Settings.SAMPLES_TO_LEARN]

			features += [sample.features for sample in samples_to_learn]
			target += [voice.id] * len(samples_to_learn)

		self.analyser.fit(features)
		features = self.analyser.transform(features)

		self.classifier.fit(features, target)

	def get_predictions(self):
		self.log_action("getting predictions")
		result_predictions = []

		for voice in self.voices:
			self.log_action(voice.id)

			samples_to_predict = voice.samples[Settings.SAMPLES_TO_LEARN:(Settings.NUMBER_OF_SAMPLES+1)]

			features = [sample.features for sample in samples_to_predict]
			features = self.analyser.transform(features)

			predictions = self.classifier.predict(features)
			probabilities = self.classifier.predict_proba(features)

			result_predictions += [self.analyse_voice_predictions(voice.id, predictions, probabilities)]

		return self.analyse_predictions(result_predictions)

	def analyse_voice_predictions(self, voice_id, predictions, probabilities):
		correct_prediction = numpy.average([1 if p == voice_id else 0 for p in predictions])
		probability = numpy.average([p[voice_id] for p in probabilities])
		non_zero_probabilities = numpy.average([len([p for p in probability if p > 10**-3]) for probability in probabilities])

		return {
			"voice": voice_id,
			"correct_prediction": correct_prediction,
			"probability": probability,
			"non_zero_predictions": non_zero_probabilities
		}

	def analyse_predictions(self, predictions):
		properties = ["correct_prediction", "probability", "non_zero_predictions"]
		result = {}

		for property in properties:
			data = [p[property] for p in predictions]

			result[property] = numpy.average(data)
			result[property+"_std"] = numpy.std(data)

		return result
