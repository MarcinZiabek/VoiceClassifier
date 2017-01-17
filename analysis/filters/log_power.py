import math


class LogPowerFilter():
	
	@staticmethod
	def apply(powers):
		length = len(powers)

		convert = lambda x: math.log2(x)

		for i in range(0, length):
			powers[i] = convert(powers[i])

		return powers
