import math


class LogPowerFilter():
	@staticmethod
	def apply(powers):
		length = len(powers)

		convert = lambda x: math.log2(x)

		for i in range(0, length):
			powers[i] = convert(powers[i])

		return powers


class PreemphasisFilter():
	@staticmethod
	def apply(preemphasis, data):
		length = len(data)

		for i in range(1, length):
			data[i] -= data[i-1] * preemphasis

		return data
