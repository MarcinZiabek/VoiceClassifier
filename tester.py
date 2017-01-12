from voice import Voice
from sample import Sample

from settings import Settings

class Prediction():
	def __init__(self, voice, predictions):
		pass


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
		self.voices = [Voice(i) for i in range(1, Settings.NUMBER_OF_VOICES+1)]

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

			samples_to_predict = voice.samples[Settings.SAMPLES_TO_LEARN:(Settings.NUMBER_OF_VOICES+1)]

			features = [sample.features for sample in samples_to_predict]
			features = self.analyser.transform(features)
			predictions = self.classifier.predict_proba(features)

			predictions_result = []

			for prediction in predictions:
				p = []
				length = len(prediction)

				for i in range(0, length):
					p += [{
						"voice": i,
						"propability": prediction[i]
					}]

				predictions_result += [p]

			result_predictions += [{
				"voice": voice.id-1,
				"predictions": predictions_result
			}]

		return result_predictions
