import glob

from analysis.cache import Cache
from analysis.sample import Sample

from analysis.settings import Settings


class Voice():

	def __init__(self, id):
		self.id = id
		self.samples = []

	def get_folder_path(self):
		    return "{0}/{1}/*.flac".format(Settings.DATA_PATH, self.id)

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
