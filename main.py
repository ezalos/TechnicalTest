import requests
import lxml.html as LH
import pandas as pd
import urllib.request, json
import urllib.parse
from ville import Ville
import os



url_template = "http://dbpedia.org/data/"
column_name_template = "http://dbpedia.org/resource/"

class Cities:
	def __init__(self):
		self.city_list = []#all french cities of at least 30k
		self.city_common_proprety = {}#only good data but incomplete
		self.attributs_list = []#properties shared by enough city of the list to be considered as necessary
		self.city_complete_propreties = {}#has data wich we are not interested in
		self.DBpedia_data = []
		self.city_dictionnary = {}#dictionary of 'Schema Ville' of each city in city list

	def scrap_city_list_of_at_least_30k(self):
		url_cities = "https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es#Communes_de_plus_de_30_000_habitants"
		xpath_search = '//table/tbody/tr/td[2]/b/a'
		self.city_list = []
		wikipedia_page = requests.get(url_cities)
		root = LH.fromstring(wikipedia_page.content)
		table = root.xpath(xpath_search)
		for elem in table:
			self.city_list.append(elem.text)
		with open('city_list.json', 'w') as json_file:
		    json.dump(self.city_list, json_file, sort_keys=False, indent=4)
		print(self.city_list)

	def fetch_propreties_from_DBpedia(self):
		for idx, city_name in enumerate(self.city_list):
			dbpedia_city = DBpedia(city_name)
			print("Taking care of " + str(idx + 1) + "/" + str(len(self.city_list)) + "\t: " + city_name + "\n\t" + dbpedia_city.safe_url)
			if (dbpedia_city.scrapp_attributes(self.city_complete_propreties) == 0):
				print("It appears that " + city_name + " does not have data on DBpedia, it will be removed from dataset")
				self.city_list.remove(dbpedia_city.name)

	def extract_common_propreties(self):
		common_ratio = 1/3
		print("Here are the common properties to at least " + str(common_ratio * 100).split(".")[0] + "% of the cities :")
		for key, value in self.city_complete_propreties.items():
			if len(value) >= len(self.city_list) * (common_ratio):
				self.city_common_proprety[key] = value
				self.attributs_list.append(key)
				print("\t\t" + str((len(value) * 100) / len(self.city_list)).split(".")[0] + "% : "  + key)
		with open('common_atttributes.json', 'w') as json_file:
		    json.dump(self.attributs_list, json_file, sort_keys=True, indent=4)
		with open('full_data.json', 'w') as json_file:
		    json.dump(self.city_complete_propreties, json_file, sort_keys=False, indent=4)

	def fill_city_cards(self):
		for city_name in self.city_list:
			City_object = Ville()
			print("\tCity : " + city_name)
			for attribut in self.attributs_list:
				print("\t\tAttribut : " + attribut)
				attribut_package = self.city_complete_propreties[attribut]
				# print(attribut_package)
				if city_name in attribut_package.keys():
					data_package = attribut_package[city_name]
					print("\t\tdata_package : ", data_package)
					if 'value' in data_package.keys():
						value = data_package['value']
					else:
						value = None
					if 'datatype' in data_package.keys():
						datatype = data_package['datatype']
					else:
						datatype = None
				else:
					value = None
					datatype = None

				print("\t\trefined: ", value, datatype, '\n')
				# value = self.city_complete_propreties[attribut][0][city_name]['value']
				# datatype = self.city_complete_propreties[attribut][0][city_name]['datatype']
				City_object.attributs.add_elem(attribut[9:], value, datatype)
			self.city_dictionnary[city_name] = City_object


	def save_city_cards(self):
		directory = "./cities"
		if not os.path.exists(directory):
			os.makedirs(directory)
		# try:
		# 	os.mkdir(path)
		# except OSError:
		# 	print ("Creation of the directory %s failed" % path)
		# else:
		# 	print ("Successfully created the directory %s " % path)
		for City_name, City_object in self.city_dictionnary.items():
			with open(directory + '/' + City_name + '.json', 'w') as json_file:
				json.dump(City_object.attributs.mydict, json_file, sort_keys=False, indent=4)





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

	def go_through_attributes(self, my_json, city_complete_propreties):
		for key, value in my_json[self.relevant_to_page].items():
			if key.startswith(domain):
				clean_key = key[19:]
				if clean_key not in city_complete_propreties.keys():
					print("\t\tNEW Proprety key : " + clean_key + " = " + str(value[0]['value']))
					city_complete_propreties[clean_key] = {}
				city_complete_propreties[clean_key][self.name] = value[0]

	def scrapp_attributes(self, city_complete_propreties):
		with urllib.request.urlopen(self.safe_url) as url:
			my_json = json.loads(url.read().decode())
			if (len(my_json)):
				self.go_through_attributes(my_json, city_complete_propreties)
				return 1
			return 0

def main():
	Cities_30k = Cities()
	Cities_30k.scrap_city_list_of_at_least_30k()
	Cities_30k.fetch_propreties_from_DBpedia()
	Cities_30k.extract_common_propreties()
	Cities_30k.fill_city_cards()
	Cities_30k.save_city_cards()


if __name__ == "__main__":
	main()
