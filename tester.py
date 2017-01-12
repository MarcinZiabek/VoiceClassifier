import os
import math
import pickle

from bisect import bisect

import numpy as np
import matplotlib.pyplot as plt

import scipy
from scipy import signal

import soundfile


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = CURRENT_PATH + "/database"
CACHE_PATH = CURRENT_PATH + "/cache"

APPLY_PREEMPHASIS = True
PREEMPHASIS = 0.95

APPLY_MEL_FILTER = False
MEL_MAX_FREQUENCY = 3200
MEL_SCALE_N = 64

APPLY_LOG_POWER = True

CACHE_DISABLED = False


class Cache():
	def __init__(self, id):
		self.id = id

	def get_path(self):
		return "{0}/{1}.json".format(CACHE_PATH, self.id)

	def exists(self):
		return os.path.exists(self.get_path())

	def get(self, func):
		if not self.exists() or CACHE_DISABLED:
			result = func()
			self.set(result)
			return result

		data = None

		with open(self.get_path(), 'rb') as handle:
			data = pickle.load(handle)
		
		return data

	def set(self, value):
		with open(self.get_path(), 'wb') as handle:
			pickle.dump(value, handle, protocol=pickle.HIGHEST_PROTOCOL)


class Spectrum():
	def __init__(self, frequencies, power):
		self.frequencies = frequencies
		self.power = power

	@staticmethod
	def from_data(frequency, data):
		frequencies, power = signal.welch(data, fs=frequency, nperseg=8192)
		result = Spectrum(frequencies, power)

		return result


class PreemphasisFilter():

	@staticmethod
	def apply(data):
		length = len(data)

		for i in range(1, length):
			data[i] -= data[i-1] * PREEMPHASIS

		return data


class MelFilter():

	@staticmethod
	def convert_frequencies(spectrum):
		length = len(spectrum.power)

		convert = lambda x: 2595 * math.log10(1 + x/700.0)

		for i in range(0, length):
			spectrum.frequencies[i] = convert(spectrum.frequencies[i])

		return spectrum

	@staticmethod
	def get_mel_scale(spectrum):
		spectrum = MelFilter.convert_frequencies(spectrum)

		width = MEL_MAX_FREQUENCY / MEL_SCALE_N

		mel_scale = []

		for i in range(0, MEL_SCALE_N):
			min = width * MEL_SCALE_N
			max = min + width

			filter = MelFilter.create_filter(min, max)
			power, frequency = filter(spectrum)

			mel_scale += [power]

		return mel_scale

	@staticmethod
	def create_filter(min_frequency, max_frequency):

		def filter(spectrum):
			sum = 0

			min = bisect(spectrum.frequencies, min_frequency)
			max = bisect(spectrum.frequencies, max_frequency)

			half = int((min+max)/2)

			power = 0

			for k in range(min, half):
				power += spectrum.power[i] * (k - min) / (half - min)

			power += spectrum.power[half]

			for k in range(half, max):
				power += spectrum.power[i] * (max - k) / (max - min)

			return power, spectrum.frequencies[half]

		return filter


class LogPowerFilter():
	
	@staticmethod
	def apply(powers):
		length = len(powers)

		convert = lambda x: math.log2(x)

		for i in range(0, length):
			powers[i] = convert(powers[i])

		return powers

class Sample():
	def __init__(self, id):
		self.id = id

		data, frequency = self.read_file()

		if APPLY_PREEMPHASIS:
			data = PreemphasisFilter.apply(data)

		spectrum = Spectrum.from_data(frequency, data)

		self.features = spectrum.power

		if APPLY_MEL_FILTER:
			self.features = MelFilter.get_mel_scale(spectrum)

		if APPLY_LOG_POWER:
			self.features = LogPowerFilter.apply(self.features)

	def read_file(self):
		data = frequency = None

		with open(self.id, 'rb') as f:
			data, frequency = soundfile.read(f)

		return data, frequency


class Voice():

	def __init__(self, id):
		self.id = id
		self.samples = []

	def get_folder_path(self):
		    return "{0}/{1}/*.flac".format(DATA_PATH, self.id)

	def read_samples(self):
		cache = Cache(self.id)
		self.samples = cache.get(self.read_samples_helper)

	def read_samples_helper(self):
		import glob
		files = glob.glob(self.get_folder_path())

		samples = []

		for file in files:
			sample = Sample(file)
			samples += [sample]

		return samples


# ===========================================================================


print("Preparing voices and analysis")

voices = []
voice_count = 25

for i in range(1, voice_count+1):
	print(i)

	voice = Voice(i)
	voice.read_samples()

	voices += [voice]


# ===========================================================================


print("Learning")

learning_ratio = 0.1
vector_components = 32

max_samples = len(voices[0].samples)
learned_samples = int(max_samples * learning_ratio)


data = []
target = []

for voice in voices:
	print(voice.id)

	voice_features = []

	for sample in voice.samples[0:learned_samples]:
		data += [sample.features]
		target += [voice.id]


from sklearn.decomposition import PCA, FactorAnalysis, FastICA, TruncatedSVD
pca = FastICA(n_components=vector_components)
pca.fit(data)
data = pca.transform(data)


from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
knn.fit(data, target)


# ===========================================================================


print("podsumowanie")

ok_1 = 0
ok_2 = 0
ok_3 = 0
ok_4 = 0
ok_5 = 0
all = 0

for voice in voices:
	print(voice.id)

	voice_features = []

	for sample in voice.samples[learned_samples:(max_samples+1)]:
		voice_features += [sample.features]
	
	voice_features = pca.transform(voice_features)
	res = knn.predict_proba(voice_features)

	for r in res:
		res_d = []

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

print("{0} / {1}: {2} %".format(ok_1, all, ok_1*100.0/all))
print("{0} / {1}: {2} %".format(ok_2, all, ok_2*100.0/all))
print("{0} / {1}: {2} %".format(ok_3, all, ok_3*100.0/all))
print("{0} / {1}: {2} %".format(ok_4, all, ok_4*100.0/all))
print("{0} / {1}: {2} %".format(ok_5, all, ok_5*100.0/all))

