import requests
import lxml.html as LH
import pandas as pd
import urllib.request, json
import urllib.parse
from ville import Ville

url_cities = "https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es#Communes_de_plus_de_30_000_habitants"
xpath_search = '//table/tbody/tr/td[2]/b/a'
city_list = []
url_start = "http://dbpedia.org/data/"
url_end = ".json"


url_template = "http://dbpedia.org/data/"
column_name_template = "http://dbpedia.org/resource/"
relevant_to_city = "http://dbpedia.org/resource/"

r = requests.get(url_cities)
root = LH.fromstring(r.content)
table = root.xpath(xpath_search)
for elem in table:
	city_list.append(elem.text)

print(city_list)

complete_city_data = {}
city_common_proprety = {}
city_common_ontology = {}
# data = {}
villes=[]

# city_list = city_list[76:78]

# for city_name in city_list:
for idx, city_name in enumerate(city_list):
	city_name = city_name.replace(" ", "_")
	safe_url = url_start + urllib.parse.quote(city_name) + url_end
	print("Taking care of " + str(idx + 1) + "/" + str(len(city_list)) + "\t: " + city_name + "\n\t" + safe_url)
	with urllib.request.urlopen(safe_url) as url:
		tmp = json.loads(url.read().decode())
		if len(tmp):
			complete_city_data[city_name] = tmp[column_name_template + city_name]
			for key, value in complete_city_data[city_name].items():
				if key.startswith("http://dbpedia.org/"):
					clean_key = key[19:]
					if clean_key.startswith("property/"):
						if clean_key[9:] in city_common_proprety.keys():
							city_common_proprety[clean_key[9:]] += 1
						else:
							print("\t\tNEW Proprety key : " + clean_key[9:])
							city_common_proprety[clean_key[9:]] = 1
					elif clean_key.startswith("ontology/"):
						if clean_key[9:] in city_common_ontology.keys():
							city_common_ontology[clean_key[9:]] += 1
						else:
							print("\t\tNEW Ontology key : " + clean_key[9:])
							city_common_ontology[clean_key[9:]] = 1
					else:
						print("\tStart with unknown key : " + clean_key)
		else:
			print("It appears that " + city_name + " does not have data on DBpedia, it will be removed from dataset")
			city_list.remove(city_name.replace("_", " "))

common_ratio = 2/3

print("Here are the common properties to at least " + str(common_ratio * 100).split(".")[0] + " cities :")

good_propreties = {}
for key, value in city_common_proprety.items():
	if value >= len(city_list) * (common_ratio):
		good_propreties[key] = 1
		print("\t\t" + str((value * 100) / len(city_list)).split(".")[0] + "%\t: "  + key)

good_ontologies = {}

print("Here are the common ontologies to at least " + str(common_ratio * 100).split(".")[0] + " cities :")

for key, value in city_common_ontology.items():
	if value >= len(city_list) * (common_ratio):
		good_ontologies[key] = 1
		print("\t\t" + str((value * 100) / len(city_list)).split(".")[0] + "%\t: "  + key)

# ville = Ville()
# print(ville)
# ville.attributs.add_elem("Superficie", 1033882)
# ville.attributs.add_elem("Population", 100000000)
# print(ville.attributs.mydict)
