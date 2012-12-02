# Lists of parameters and values used throughout the application.

class MapParams(object):
    # Application's Google Maps API key. This key identifies your application 
    # for purposes of quota management.
    API_KEY = ''

    # URL Request Addresses
    API_BASE_URL = 'http://maps.googleapis.com/maps/api'
    API_BASE_URL_SECURE = 'https://maps.googleapis.com/maps/api'

    # Latitude / Longitude Increment Amounts for Intermediate Waypoints
    WAYPOINT_INCREMENTS = 0.006
    MAX_INTERMEDIATE_WAYPOINTS = 5

class YelpParams(object):
    #Authentication for Yelp
    YELP_CONSUMER_KEY = ''
    YELP_CONSUMER_SECRET = ''
    YELP_TOKEN = ''
    YELP_TOKEN_SECRET = ''

