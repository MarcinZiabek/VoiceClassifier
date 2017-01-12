
class PreemphasisFilter():

	@staticmethod
	def apply(preemphasis, data):
		length = len(data)

		for i in range(1, length):
			data[i] -= data[i-1] * preemphasis

		return data
