domain = "http://dbpedia.org/"
url_start = domain + "data/"
url_end = ".json"
relevant_to_page = "http://dbpedia.org/resource/"

class DBpedia:
	def __init__(self, page_name):
		self.name = page_name
		self.safe_name = self.name.replace(" ", "_")
		self.safe_url = url_start + urllib.parse.quote(self.safe_name) + url_end
		self.relevant_to_page = relevant_to_page + self.safe_name

	#This function download the webpage with request
		#it then decode it as a Json and send it to go_through_attributes
	def scrapp_attributes(self, city_complete_propreties):
		with urllib.request.urlopen(self.safe_url) as url:
			my_json = json.loads(url.read().decode())
			if (len(my_json)):
				self.go_through_attributes(my_json, city_complete_propreties)
				return 1
			return 0

	#This function save in structured data if :
		#They are directly relevant to the city (Otherwise you get link to
		#other articles, most of the time linked to the history of the city)
	def go_through_attributes(self, my_json, city_complete_propreties):
		for key, value in my_json[self.relevant_to_page].items():
			if key.startswith(domain):
				clean_key = key[19:]
				if clean_key not in city_complete_propreties.keys():
					print("\t\tNEW Proprety key : " + clean_key + " = " + str(value[0]['value']))
					city_complete_propreties[clean_key] = {}
				city_complete_propreties[clean_key][self.name] = value[0]
