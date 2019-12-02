import requests
import lxml.html as LH
import pandas as pd
import urllib.request, json
import urllib.parse
from DBpedia import DBpedia
from ville import Ville
import os

city_list_url = "https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es#Communes_de_plus_de_30_000_habitants"

class Cities:
	def __init__(self):
		self.city_list = []#all french cities of at least 30k
		self.attributs_list = []#properties shared by enough city of the list to be considered as necessary
		self.city_complete_propreties = {}#has data wich we are not interested in
		self.city_dictionnary = {}#dictionary of 'Schema Ville' of each city in city list

	#This function will scrap the list of French cities of at least 30k habitant
		#It uses a link from wikipedia citing them all in a table
		#I'm able to extract them by using an xpath search
	def scrap_city_list_of_at_least_30k(self):
		url_cities = city_list_url
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

	#This function allow me te treat each of the city in my list
		#Each city has her link found in DBpedia
		#Then get her relevant data put in dbpedia_city
		#If cant be found, city is removed (3 cases in total)
	def fetch_propreties_from_DBpedia(self):
		for idx, city_name in enumerate(self.city_list):
			dbpedia_city = DBpedia(city_name)
			print("Taking care of " + str(idx + 1) + "/" + str(len(self.city_list)) + "\t: " + city_name + "\n\t" + dbpedia_city.safe_url)
			if (dbpedia_city.scrapp_attributes(self.city_complete_propreties) == 0):
				print("It appears that " + city_name + " does not have data on DBpedia, it will be removed from dataset")
				self.city_list.remove(dbpedia_city.name)

	#This function looks through all propreties scrapped from dbpedia:
		#as a lot of them are irrelevant (Meteo, overspecific details,...)
		#and therefore only select attributes shared by at least common_ratio of cities
	def extract_common_propreties(self):
		common_ratio = 1/3
		print("Here are the common properties to at least " + str(common_ratio * 100).split(".")[0] + "% of the cities :")
		for key, value in self.city_complete_propreties.items():
			if len(value) >= len(self.city_list) * (common_ratio):
				self.attributs_list.append(key)
				print("\t\t" + str((len(value) * 100) / len(self.city_list)).split(".")[0] + "% : "  + key)
		with open('common_atttributes.json', 'w') as json_file:
		    json.dump(self.attributs_list, json_file, sort_keys=True, indent=4)
		with open('full_data.json', 'w') as json_file:
		    json.dump(self.city_complete_propreties, json_file, sort_keys=False, indent=4)

	#Scrapped data is stored in structured Classes and Dictionnaries
	def fill_city_cards(self):
		for city_name in self.city_list:
			City_object = Ville()
			print("\tCity : " + city_name)
			for attribut in self.attributs_list:
				print("\t\tAttribut : " + attribut)
				attribut_package = self.city_complete_propreties[attribut]
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
				City_object.attributs.add_elem(attribut[9:], value, datatype)
			self.city_dictionnary[city_name] = City_object


	#Scrapped data is stored in individual files in the folder cities
	def save_city_cards(self):
		directory = "./cities"
		if not os.path.exists(directory):
			os.makedirs(directory)
		for City_name, City_object in self.city_dictionnary.items():
			with open(directory + '/' + City_name + '.json', 'w') as json_file:
				json.dump(City_object.attributs.mydict, json_file, sort_keys=False, indent=4)





def main():
	Cities_30k = Cities()
	Cities_30k.scrap_city_list_of_at_least_30k()
	Cities_30k.fetch_propreties_from_DBpedia()
	Cities_30k.extract_common_propreties()
	Cities_30k.fill_city_cards()
	Cities_30k.save_city_cards()


if __name__ == "__main__":
	main()
