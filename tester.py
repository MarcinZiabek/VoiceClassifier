from voice import Voice
from sample import Sample

from settings import {
	NUMBER_OF_VOICES, NUMBER_OF_SAMPLES, SAMPLES_TO_LEARN
	}
	
from settings import DECOMPOSITION_ALGORITHM, DECOMPOSITION_COMPONENTS, CLASSIFIER_ALGORITHM
from settings import LOG_ACTIONS_TO_CONSOLE


class Tester():

	def __init__(self):
		self.voices = []
		self.analyser = DECOMPOSITION_ALGORITHM(n_components=DECOMPOSITION_COMPONENTS)
		self.classifier = CLASSIFIER_ALGORITHM()

	def log_action(self, text):
		if LOG_ACTIONS_TO_CONSOLE:
			print(str(text))

	def perform_analysis(self):
		self.load_voices()
		self.load_samples()
		self.learn()
		return self.get_predictions()
	
	def load_voices(self):
		self.log_action("loading {0} voices".format(NUMBER_OF_VOICES))

		for i in range(1, NUMBER_OF_VOICES+1):
			voice = Voice(i)
			self.voices += [voice]

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
			samples_to_learn = voice.samples[0:SAMPLES_TO_LEARN]
			voice_features = []

			for sample in samples_to_learn:
				features += [sample.features]
				target += [voice.id]

		self.analyser.fit(features)
		features = self.analyser.transform(features)

		self.classifier.fit(features, target)

	def get_predictions(self):
		self.log_action("getting predictions")
		result_predictions = []

		for voice in self.voices:
			self.log_action(voice.id)

			samples_to_predict = voice.samples[SAMPLES_TO_LEARN:(NUMBER_OF_VOICES+1)]

			features = []

			for sample in samples_to_predict:
				features += [sample.features]
	
			features = self.analyser.transform(features)
			predictions = self.classifier.predict_proba(features)

			result_predictions += [{
				"index": voice.id-1,
				"predictions": predictions
			}]

		return result_predictions

