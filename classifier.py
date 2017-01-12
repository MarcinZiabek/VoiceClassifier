from voice import Voice
from sample import Sample







print("Preparing voices and analysis")

predictions = Tester().perform_analysis()


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