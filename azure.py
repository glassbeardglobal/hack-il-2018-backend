from pprint import pprint
import requests

key = '872d34c629ff4d169d55e9f0569c3770'
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"


def scrape_image(search_term):
    # search_term = "London"

    headers = {"Ocp-Apim-Subscription-Key": key}
    params = {"q": search_term, "license": "public", "imageType": "photo"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    resp = response.json()['value']
    if(len(resp) > 0):
        return resp[0]['contentUrl']
    else:
        return None
