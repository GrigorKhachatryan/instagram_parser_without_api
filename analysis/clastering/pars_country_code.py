import requests
from xml.etree import ElementTree
import xmltodict
import json
from pprint import pprint

response = requests.get('https://www.artlebedev.ru/country-list/xml/')
a = response.text
tree = ElementTree.fromstring(response.content)
t = xmltodict.parse(a)
country = t['country-list']['country']
json_code = {'code':{}}
for i in country:
    json_code['code'][i['alpha2']] = i['english']
with open('country_code.json','w') as file:
    json.dump(json_code, file)

