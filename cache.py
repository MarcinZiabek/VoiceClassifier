import os
import pickle

from settings import CACHE_PATH, CACHE_ENABLED


class Cache():
	def __init__(self, id):
		self.id = id

	def get_path(self):
		return "{0}/{1}.json".format(CACHE_PATH, self.id)

	def exists(self):
		return os.path.exists(self.get_path())

	def get(self, func):
		if not self.exists() and (not CACHE_ENABLED):
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
