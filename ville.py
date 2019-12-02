#Imposed structure
class Attributs:
	def __init__(self):
		self.mydict={}
	def add_elem(self, key, value, datatype):
		self.mydict[key] = [value, datatype]

class Possessions:
	def __init__(self):
		pass

class Evenements:
	def __init__(self):
		pass

class Ville:
	def __init__(self):
		self.attributs = Attributs()
		self.evenements = Evenements()
		self.possessions = Possessions()
