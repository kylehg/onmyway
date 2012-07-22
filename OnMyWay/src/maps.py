# Maps module for accessing information from Google Maps

import logging
import json
import urllib

from params import MapParams


def geocode(address, sensor, **geo_args):
    """Given an address find geographic coordinates.

    Args:
        address: the address of the place
        sensor: True/False wether the application has user GPS info

    Returns:
        A dictionary with the following structure:
        {'formatted_address': The formatted address of the place,
         'location': {'lat': latitude coordinate, 
                      'lng': longitude coordinate}
        }
    """
    geo_args.update({
        'address': address,
        'sensor': sensor  
    })
    args = urllib.urlencode(geo_args)
    url = MapParams.API_BASE_URL + '/geocode/json?' + args
    result = json.load(urllib.urlopen(url))
    if result['status'] == 'OK':
        place = result['results'][0]
        logging.info(place)
        output = {'formatted_address': place['formatted_address'],
                  'location': place['geometry']['location']}
        return output
    else:
        logging.error('Geocode API Returned Status: %s', result['status'])


def places(query, sensor, **geo_args):
    """Given a text query return a list of places.

    Args:
        address: the address of the place
        sensor: True/False wether the application has user GPS info
        location(optional): The latitude/longitude around which to retrieve
                            Place information. This must be specified as
                            latitude,longitude.

    Returns:
        A dictionary with the following structure:
        {'name': The name of the place
         'formatted_address': The formatted address of the place,
         'location': {'lat': latitude coordinate, 
                      'lng': longitude coordinate}
        }
    """
    geo_args.update({
        'query': query,
        'sensor': sensor,
        'key': MapParams.API_KEY
    })
    params = urllib.urlencode(geo_args)
    url = MapParams.API_BASE_URL_SECURE + '/place/textsearch/json?' + params
    logging.info('Making request to Google: %s', url)
    result = json.load(urllib.urlopen(url))
    if result['status'] == 'OK':
        output = []
        for place in result['results']:
            output.append({'name': place['name'], 
                           'formatted_address': place['formatted_address'],
                           'location': place['geometry']['location']})
        return output
    else:
        logging.error('Places API Returned Status: %s', result['status'])


def intermediate_locations(start_location, end_location):
    """Given a start and end location, returns a list of intermediate locations.

    Args:
        start_location: A location dictionary with 'lat' and 'lng' keys.
        end_location: A location dictionary with 'lat' and 'lng' keys.

    Returns:
        intermediate_locations: A list of locations in between start and end.
    """
    start_lat = start_location['lat']
    start_lng = start_location['lng']
    end_lat = end_location['lat']
    end_lng = end_location['lng']

    dist_lat = abs(end_lat - start_lat)
    dist_lng = abs(end_lng - start_lng)
    dist_max = max(dist_lat, dist_lng)

    num_points_between = int(dist_max / MapParams.WAYPOINT_INCREMENTS)
    num_steps = min(num_points_between, MapParams.MAX_INTERMEDIATE_WAYPOINTS)

    intermediate_locations = []

    for i in range(num_steps):
        lat = start_lat + (end_lat - start_lat) / num_steps * i
        lng = start_lng + (end_lng - start_lng) / num_steps * i
        location = {'lat': lat, 'lng': lng}
        intermediate_locations.append(location)

    return intermediate_locations

if __name__ == '__main__':
    start_location = {"lat": 40.74189000000001, "lng": -74.00468000000001}
    end_location = {"lat": 40.77415000000001, "lng": -73.96914000000001}
    # start_location = {"lat": 0.0, "lng": -400.0}
    # end_location = {"lat": 20.0, "lng": 25.0}
    points = intermediate_locations(start_location, end_location)
    for point in points:
        print point

