@app.route('/new/<name>', methods=['GET'])
def add_country(name):
  country = mongo.db.Countries
  countryname = name
  population = random.randint(289035,2098789)
  landarea = random.randint(8675,2098902)
  density = round(population/landarea)
  print(countryname, population, landarea)
  country_id = country.insert({'Country':countryname, 'Population':population, 'Land Area (Km2)':landarea, 'Density (P/Km2)':density}, {'$currentDate':{'Last Update': 'true'}})
  new_country = country.find_one({'_id': country_id })
  output = {'Country' : new_country['Country'], 'Population' : new_country['Population'], 'Land Area (Km2)' : new_country['Land Area (Km2)'], 'Density (P/Km2)' : new_country['Density (P/Km2)']}
  return jsonify({'result' : output})
