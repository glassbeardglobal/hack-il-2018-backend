import yelp
import requests
from amadeus import Flights

import csv
import random

''' Load dictionary into memory '''


def parse_airports(file):
    d = dict()
    with open(file) as f:
        reader = csv.reader(f)
        for row in reader:
            iata_code, city, country = row[4], row[2], row[3]
            d[iata_code] = city + ', ' + country
    return d


# Amadeus parameters
IATA2CITY_FILE = 'airports.dat'
IATA2CITY = parse_airports(IATA2CITY_FILE)
AMADEUS_API_KEY = 'wwARh7fxAvIWz9vl8xgbVntCdqtIBDMM'
NUM_EXPERIENCES = 5

# Yelp parameters
YELP_API_URL = 'https://api.yelp.com'
YELP_SEARCH_PATH = '/v3/businesses/search'
YELP_API_KEY = 'TMXm0RTcXiL8XvOn_w1zkETQMEx8FbJdWbp1_Mwd8RVjzpqvt80sIwEWvhjC8c0MmhbwKYXM-CECC5zVvl5WcTtbmmJv5Ow5h6KoBU2MQFKFgU_kZr1GlEvbg-aRWnYx'
YELP_LIMIT = 10
RATING_THRESHOLD = 4
REVIEW_THRESHOLD = 10


''' Use Amadeus API to retrieve flight plans conditioned on budget '''


def retrieve_destinations(origin, budget_query, departure_date, duration):
    # Query for flights via Amadeus
    flights = Flights(AMADEUS_API_KEY)

    # Find flights from origin
    origin_iata = flights.auto_complete(term=origin)[0]['value']

    r = flights.inspiration_search(
        origin=origin_iata,
        departure_date=departure_date,
        max_price=budget_query,
        duration=duration)

    # Cap number of experiences
    results = r['results'][:NUM_EXPERIENCES]

    # Map IATA codes from Amadeus API to human-readable places
    destinations = []
    for iata in results:
        destination = IATA2CITY.get(iata['destination'], None)
        if destination is not None:
            # Return a tuple of HRF city, dates, and price of flight
            destinations.append((destination, origin_iata, iata['destination'],  iata['departure_date'], iata['return_date'], float(iata['price'])))
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
    payload['location'] = location

    # Fit activities to remaining budget
    payload['price'] = budget2dollarsigns(budget)

    payload['limit'] = YELP_LIMIT

    # Parse category queries
    # Pick a subset of categories
    categories_sampled = categories_queries
    if len(categories_queries) > 3:
        categories_sampled = random.sample(categories_queries, 3)

    experience = {}
    guide_name = 'Not selected'
    guide_pic = 'Not selected'

    # For each category, find a good activity to form an experience
    activities = []
    for category in categories_sampled:
        # Retrieve candidate businesses and filter through
        payload['categories'] = category
        r = yelp.request(YELP_API_URL, YELP_SEARCH_PATH, YELP_API_KEY, url_params=payload)
        candidates = list(filter(lambda business:
                                 business['rating'] >= RATING_THRESHOLD and business['review_count'] >= REVIEW_THRESHOLD, r['businesses']))

        # Pick a subset of good activities to add to the experience
        if len(candidates) >= 2:
            sampled = random.sample(candidates, 2)
            for s in sampled:
                # Look at reviews for activity of interest
                reviews_url = 'https://api.yelp.com/v3/businesses/' + s['id'] + '/reviews'
                headers = {'Authorization': 'Bearer %s' % YELP_API_KEY}
                review_resp = requests.get(reviews_url, headers=headers).json()
                reviews = review_resp['reviews']

                # Find a guide for that activity
                guide = max(reviews, key=lambda x: x['rating'])

                # Store parameters into activity element
                business_name = s['name']
                business_pic = s['image_url']
                latitude = business_lat = s['coordinates']['latitude']
                longitude = business_lat = s['coordinates']['longitude']
                guide_name = guide['user']['name']
                guide_pic = guide['user']['image_url']
                guide_review = guide['text']

                activities.append({'businessName': business_name,
                                   'desc': guide_review,
                                   'pic': business_pic,
                                   'latitude': latitude,
                                   'longitude': longitude
                                   })

    # Add activities to the experience
    experience['activities'] = activities
    experience['guide'] = {'pic': guide_pic, 'name': guide_name}
    experience['name'] = 'Placeholder!!!'

    city = location.split(',')[0].strip()
    country = location.split(',')[1].strip()
    # city_pic = scrape_image(city)
    experience['place'] = {'city': city, 'country': country, 'pic': None}

    return experience


def main(origin, budget_query, categories_queries, departure_date, duration):

    # Use Amadeus to retrieve candidate cities
    try:
        destinations = retrieve_destinations(origin, budget_query, departure_date, duration)
    except:
        return []

    experiences = []
    # Use Yelp to find good activities in candidate cities
    for dst in destinations:
        leftover_budget = budget_query - dst[5]
        exp = retrieve_experience(dst[0], leftover_budget, categories_queries)

        # Add flight information to experience
        _, origin_iata, dst_iata, leave_date, return_date, price = dst
        exp['flight'] = {'to': dst_iata,
                         'from': origin_iata,
                         'price': price,
                         'departure_date': leave_date,
                         'return_date': return_date}
        experiences.append(exp)

    for exp in experiences:
        print(exp)
        print()
    return experiences


if __name__ == '__main__':
    main('New York', 3000, ['active', 'food', 'arts'], '2018-02-27', 15)
