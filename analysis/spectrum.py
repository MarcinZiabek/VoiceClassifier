from scipy import signal

from analysis.settings import Settings


class Spectrum():
	def __init__(self, frequencies, power):
		self.frequencies = frequencies
		self.power = power

	@staticmethod
	def from_data(frequency, data):
		frequencies, power = signal.welch(data, fs=frequency, nperseg=Settings.FFT_COMPONENTS*2)
		result = Spectrum(frequencies, power)

		return result
