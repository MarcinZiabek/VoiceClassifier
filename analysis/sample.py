import soundfile

from analysis.spectrum import Spectrum
from analysis.filters import PreemphasisFilter, LogPowerFilter

from analysis.settings import Settings


class Sample():
	def __init__(self, id):
		self.id = id

		data, frequency = self.read_file()

		if Settings.APPLY_PREEMPHASIS:
			data = PreemphasisFilter.apply(Settings.PREEMPHASIS, data)

		spectrum = Spectrum.from_data(frequency, data)

		self.features = spectrum.power

		if Settings.APPLY_LOG_POWER:
			self.features = LogPowerFilter.apply(self.features)

	def read_file(self):
		data = frequency = None

		with open(self.id, 'rb') as f:
			data, frequency = soundfile.read(f)

		return data, frequency
