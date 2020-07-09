import hashlib
import json

class cell(object):
	def __init__ (self, site = None, N = None, E = None, W = None, S = None, info =None):
		self.site = site
		self.N = self.hash(N)
		self.E = self.hash(E)
		self.W = self.hash(W)
		self.S = self.hash(S)
		self.info = info

	@staticmethod
	def hash(cell):
		CellString = json.dumps(str(cell), sort_keys=True).encode()
		return hashlib.sha256(CellString).hexdigest()