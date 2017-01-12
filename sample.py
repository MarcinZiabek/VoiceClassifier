import soundfile

from spectrum import Spectrum
from filters import PreemphasisFilter, LogPowerFilter

from settings import APPLY_PREEMPHASIS, PREEMPHASIS, APPLY_LOG_POWER


class Sample():
	def __init__(self, id):
		self.id = id

		data, frequency = self.read_file()

		if APPLY_PREEMPHASIS:
			data = PreemphasisFilter.apply(PREEMPHASIS, data)

		spectrum = Spectrum.from_data(frequency, data)

		self.features = spectrum.power

		if APPLY_LOG_POWER:
			self.features = LogPowerFilter.apply(self.features)

	def read_file(self):
		data = frequency = None

		with open(self.id, 'rb') as f:
			data, frequency = soundfile.read(f)

		return data, frequency
