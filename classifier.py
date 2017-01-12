from voice import Voice
from sample import Sample

from settings import VOICES_NUMBER, NUMBER_OF_SAMPLES, SAMPLES_TO_LEARN


print("Preparing voices and analysis")

voices = []

for i in range(1, VOICES_NUMBER+1):
	print(i)

	voice = Voice(i)
	voice.read_samples()

	voices += [voice]


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

	for sample in voice.samples[SAMPLES_TO_LEARN:(NUMBER_OF_SAMPLES+1)]:
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
