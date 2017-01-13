import os
import pickle

from settings import Settings


class Cache():
	def __init__(self, id):
		self.id = id

	def get_path(self):
		return "{0}/{1}.json".format(Settings.CACHE_PATH, self.id)

	def exists(self):
		return os.path.exists(self.get_path())

	def get(self, func):
		if not self.exists() or (not Settings.CACHE_ENABLED):
			result = func()
			self.set(result)
			return result

		data = None

		with open(self.get_path(), 'rb') as handle:
			data = pickle.load(handle)
		
		return data

	def set(self, value):
		with open(self.get_path(), 'wb') as handle:
			pickle.dump(value, handle, protocol=pickle.HIGHEST_PROTOCOL)
