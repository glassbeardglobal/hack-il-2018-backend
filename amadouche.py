import requests
from amadeus import Flights
import json
import pprint
import csv

FILE = 'airports.dat'


def parse_airports(file):
    d = dict()
    with open(file) as f:
        reader = csv.reader(f)
        for row in reader:
            iata_code, city = row[4], row[2]
            d[iata_code] = city
    return d


AMADEUS_API_KEY = 'wwARh7fxAvIWz9vl8xgbVntCdqtIBDMM'

flights = Flights(AMADEUS_API_KEY)
resp = flights.inspiration_search(
    origin='CHI',
    departure_date="2018-03-18",
    max_price=200)

results = resp['results']
airports = [r['destination'] for r in results]
iata_cities = parse_airports(FILE)

cities = []
for a in airports:
    city = iata_cities.get(a, None)
    if city is not None:
        cities.append(city)

# pprint.pprint(cities, indent=2)
# valid_parent_categories = {'active', 'adultentertainment', 'african', 'arabian', 'artclasses', 'arts', 'artsandcrafts', 'bars', 'belgian', 'brazilian', 'breweries', 'cafes', 'cannabis_clinics', 'caribbean', 'chinese', 'diving', 'fashion', 'festivals', 'food', 'french', 'german', 'gourmet', 'hotels', 'hotelstravel', 'italian', 'japanese', 'jpsweets', 'latin', 'localflavor', 'malaysian', 'mediterranean', 'mexican', 'mideastern', 'movietheaters', 'museums', 'nightlife', 'parks', 'polish', 'portuguese', 'restaurants', 'shopping', 'social_clubs', 'spanish', 'tastingclasses', 'tours', 'transport', 'travelservices', 'turkish', 'wineries', 'zoos'}

# with open('categories.json') as jsonfile:
#     data = json.load(jsonfile)
#     # pprint.pprint(data, indent=2)

#     categories = dict()
#     for j in data:
#         alias = j['alias']
#         parents = j['parents']
#         if len(parents) == 1:
#             parent = parents[0]
#             if categories.get(parent, None) == None:
#                 categories[parent] = list()
#             if parent in valid_parent_categories:
#                 categories[parent].append(alias)

# pprint.pprint(categories, indent=2)
