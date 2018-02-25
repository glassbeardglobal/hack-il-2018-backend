import yelp
import requests
from amadeus import Flights
import json
import csv
import numpy as np

# Amadeus parameters
IATA2CITY_FILE = 'airports.dat'
IATA2CITY = parse_airports(IATA2CITY_FILE)
AMADEUS_API_KEY = 'wwARh7fxAvIWz9vl8xgbVntCdqtIBDMM'

# Yelp parameters
YELP_API_URL = 'https://api.yelp.com'
YELP_SEARCH_PATH = 'v3/businesses/search'
YELP_API_KEY = None


''' Load dictionary into memory '''
def parse_airports(file):
    d = dict()
    with open(file) as f:
        reader = csv.reader(f)
        for row in reader:
            iata_code, city, country = row[4], row[2]
            d[iata_code] = city + ', ' + country 
    return d


''' Use Amadeus API to retrieve flight plans conditioned on budget '''
def retrieve_destinations(origin, budget_query, departure_date):
	# Query for flights via Amadeus
	flights = Flights(AMADEUS_API_KEY)
	r = flights.inspiration_search(
	    origin=origin,
	    departure_date=departure_date,
	    max_price=budget_query)

	# Get results from query
	results = r['results']

	# Map IATA codes from Amadeus API to human-readable places
	destinations = []
	for iata in iata_codes:
	    destination = IATA2CITY.get(r['destination'], None)
	    if city is not None:
	    	# Return a tuple of HRF city, dates, and price of flight
	        dst_locs.append((destination, r['departure_date'], r['return_date'], r['price']))

    return destinations

''' Helper function that maps budgets to dollar signs '''
def budget2dollarsigns(budget):
	if budget < 10:
		return '1'
	elif 10 <= budget < 30:
		return '1,2'
	elif 30 <= budget < 60:
		return '1,2,3'
	else:
		return '1,2,3,4'


''' Use Yelp API to retrieve itineraries or experiences '''
def retrieve_experience(location, budget, categories_queries):
	# Create URL params for request
	payload = {}

	# Parse location queries
	payload['location'] = location_query

	# Parse category queries
	categories_payload = ''
	for category in categories_queries:
		categories_payload += category

	if categories_payload != '':
		payload['categories'] = categories_payload

	# Fit activities to remaining budget
	# payload['price'] = budget2dollarsigns(budget)

	r = yelp.request(host, path, api_key, url_params=payload)
	candidates = filter(lambda business: business['rating'] >= 4 and business['review_count'] >= 10, r['business'])

	for business in candidates:




def main(origin, budget_query, location_query, categories_queries)


	# Use Amadeus to retrieve candidate cities
	destinations = retrieve_destinations(origin, budget_query, departure_date)

	for dst in destinations:
		leftover_budget = budget_query - dst[3]
		retrieve_experience(destinations[0], leftover_budget, categories_queries)

	


if __name__ == '__main__':
	main()

