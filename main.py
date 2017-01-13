from voice import Voice
from sample import Sample

from tester import Tester
from settings import Settings


def percentage_of_correct_hits_in_function_of_learning_samples():

	def check_percentage(number_of_learning_samples):
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

	return [(n, check_percentage(n)) for n in range(1, 76)]


data = percentage_of_correct_hits_in_function_of_learning_samples()

print("====================================")

for n, h in data:
	print(n, h)


"""	

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

	all += 1

print("probability: {0} %".format(probability*100.0/all))
print("selected: {0}".format(selected/all))
print("{0} / {1}: {2} %".format(ok_1, all, ok_1*100.0/all))

"""