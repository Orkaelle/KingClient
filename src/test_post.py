import random
import requests

country_name = 'Azeroth'
population = str(random.randint(289035,2098789))
landarea = str(random.randint(8675,2098902))

payload = { 'Country' : country_name, 'Population' : population, 'Land Area (Km2)' : landarea }

r = requests.post('http://127.0.0.1:5000/new', json = payload)

print(r.text)