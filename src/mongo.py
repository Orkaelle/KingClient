from flask import Flask, render_template
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import random
from datetime import datetime

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'KingClient'
app.config['MONGO_URI'] = 'mongodb+srv://ork:DataIA4321@cluster0.ie4rc.mongodb.net/KingClient?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/countries', methods=['GET'])
def get_all_countries():
  country = mongo.db.Countries
  output = []
  for c in country.find():
    output.append({'Country' : c['Country'], 'Population' : c['Population'], 'Land Area (Km2)' : c['Land Area (Km2)']})
  return jsonify({'result' : output})


@app.route('/countries/<name>', methods=['GET'])
def get_one_country(name):
  country = mongo.db.Countries
  c = country.find_one({'Country' : name})
  if c:
    output = {'Country' : c['Country'], 'Population' : c['Population'], 'Land Area (Km2)' : c['Land Area (Km2)']}
  else:
    output = "No such name"
  return jsonify({'result' : output})


@app.route('/new/<name>', methods=['GET'])
def add_country(name):
  country = mongo.db.Countries
  countryname = name
  population = random.randint(289035,2098789)
  landarea = random.randint(8675,2098902)
  density = round(population/landarea)
  lastupdate = datetime.now()
  country_id = country.insert({'Country':countryname, 'Population':population, 'Land Area (Km2)':landarea, 'Density (P/Km2)':density, 'Last Update':lastupdate})
  new_country = country.find_one({'_id': country_id })
  output = {'Country' : new_country['Country'], 'Population' : new_country['Population'], 'Land Area (Km2)' : new_country['Land Area (Km2)'], 'Density (P/Km2)' : new_country['Density (P/Km2)'], 'Last Update' : new_country['Last Update']}
  return jsonify({'result' : output})


@app.route('/density', methods=['GET'])
def get_density():
  country = mongo.db.Countries
  output = []
  slices = []
  
  for c in country.find({'Density (P/Km2)': { '$lt' : 40 }}):
    slices.append({'Country' : c['Country'], 'Density (P/Km2)' : c['Density (P/Km2)']})
  output.append({'Density < 40' : slices})
  slices = []
  
  for c in country.find({'Density (P/Km2)': { "$lt" : 100, "$gte" : 40 }}):
    slices.append({'Country' : c['Country'], 'Density (P/Km2)' : c['Density (P/Km2)']})
  output.append({'Density 40-100' : slices})
  slices = []

  for c in country.find({'Density (P/Km2)': { "$lt" : 500, "$gte" : 100 }}):
    slices.append({'Country' : c['Country'], 'Density (P/Km2)' : c['Density (P/Km2)']})
  output.append({'Density 100-500' : slices})
  slices = []

  for c in country.find({'Density (P/Km2)': { "$gte" : 500 }}):
    slices.append({'Country' : c['Country'], 'Density (P/Km2)' : c['Density (P/Km2)']})
  output.append({'Density > 500' : slices})

  return jsonify({'result' : output})



if __name__ == '__main__':
    app.run(debug=True)