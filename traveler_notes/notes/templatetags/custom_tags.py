from django.template import Library
import requests
from traveler_notes.settings import MAP_REST_API_KEY
register = Library()


@register.simple_tag
def get_address(lat, lng):

    url = f'https://apis.mapmyindia.com/advancedmaps/v1/{MAP_REST_API_KEY}/rev_geocode'
    params = {
        'lat': lat,
        'lng': lng,
        'region': 'IND'
    }
    response = requests.get(url, params=params)
    json = response.json()
    print(json)
    if json.get('results'):
        return json['results'][0]
    return json
