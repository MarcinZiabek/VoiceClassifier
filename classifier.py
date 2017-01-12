from voice import Voice
from sample import Sample

from settings import NUMBER_OF_VOICES, NUMBER_OF_SAMPLES, SAMPLES_TO_LEARN
from settings import DECOMPOSITION_ALGORITHM, DECOMPOSITION_COMPONENTS, CLASSIFIER_ALGORITHM
from settings import LOG_ACTIONS_TO_CONSOLE

class Tester():

	def __init__(self):
		self.voices = []
		self.analyser = DECOMPOSITION_ALGORITHM(n_components=DECOMPOSITION_COMPONENTS)
		self.classifier = CLASSIFIER_ALGORITHM()

		self.load_voices()
		self.load_samples()
		self.learn()

	def log_action(self, text):
		if LOG_ACTIONS_TO_CONSOLE:
			print(str(text))
	
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

		data = []
		target = []

		for voice in self.voices:
			self.log_action(voice.id)

			samples_to_learn = voice.samples[0:SAMPLES_TO_LEARN]
			voice_features = []

			for sample in samples_to_learn:
				data += [sample.features]
				target += [voice.id]

	def get_predictions(self, analysis_function):
		self.log_action("getting predictions")

		for voice in voices:
			self.log_action(voice.id)

			voice_features = []

			for sample in voice.samples[SAMPLES_TO_LEARN:(NUMBER_OF_VOICES+1)]:
				voice_features += [sample.features]
	
			voice_features = pca.transform(voice_features)
			res = knn.predict_proba(voice_features)

			for r in res:
				res_d = []




print("Preparing voices and analysis")

voices = Tester().voices


	

	


# ===========================================================================


print("Learning")

data = []
target = []

for voice in voices:
	print(voice.id)

	voice_features = []

	for sample in voice.samples[0:SAMPLES_TO_LEARN]:
		data += [sample.features]
		target += [voice.id]


pca = DECOMPOSITION_ALGORITHM(n_components=DECOMPOSITION_COMPONENTS)
pca.fit(data)
data = pca.transform(data)


knn = CLASSIFIER_ALGORITHM()
knn.fit(data, target)


# ===========================================================================


print("podsumowanie")

ok_1 = 0
ok_2 = 0
ok_3 = 0
ok_4 = 0
ok_5 = 0
probability = 0
selected = 0
all = 0

for voice in voices:
	print(voice.id)

	voice_features = []

	for sample in voice.samples[SAMPLES_TO_LEARN:(NUMBER_OF_VOICES+1)]:
		voice_features += [sample.features]
	
	voice_features = pca.transform(voice_features)
	res = knn.predict_proba(voice_features)

	for r in res:
		res_d = []

		probability += r[voice.id-1]
		selected += len([s for s in r if s!=0])

		for i in range(0, len(r)):
			res_d += [{
				"index": i+1,
				"value": r[i]
			}]

		v = sorted(res_d, key=lambda x: x["value"], reverse=True)

		if v[0]["index"] == voice.id:
			ok_1 += 1

		if v[1]["index"] == voice.id:
			ok_2 += 1

		if v[2]["index"] == voice.id:
			ok_3 += 1

		if v[3]["index"] == voice.id:
			ok_4 += 1

		if v[4]["index"] == voice.id:
			ok_5 += 1
		
		all += 1

print("probability: {0} %".format(probability*100.0/all))
print("selected: {0}".format(selected/all))
print("{0} / {1}: {2} %".format(ok_1, all, ok_1*100.0/all))
print("{0} / {1}: {2} %".format(ok_2, all, ok_2*100.0/all))
print("{0} / {1}: {2} %".format(ok_3, all, ok_3*100.0/all))
print("{0} / {1}: {2} %".format(ok_4, all, ok_4*100.0/all))
print("{0} / {1}: {2} %".format(ok_5, all, ok_5*100.0/all))
