class Attributs:
	def __init__(self):
		self.mydict={}
	def add_elem(self, key, value, type_value):
		self.mydict[key] = [value, type_value]

class Possessions:
	def __init__(self):
		self.mydict={}
		pass

class Evenements:
	def __init__(self):
		self.mydict={}
		pass

class Ville:
	def __init__(self):
		self.attributs = Attributs()
		self.evenements = Evenements()
		self.possessions = Possessions()
