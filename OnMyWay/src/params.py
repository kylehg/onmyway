# Lists of parameters and values used throughout the application.

class MapParams(object):
    # Application's Google Maps API key. This key identifies your application 
    # for purposes of quota management.
    API_KEY = 'AIzaSyD-byUjWuK5LEm1RCcoOvFypSp2o_GPV60'

    # URL Request Addresses
    API_BASE_URL = 'http://maps.googleapis.com/maps/api'
    API_BASE_URL_SECURE = 'https://maps.googleapis.com/maps/api'

    # Latitude / Longitude Increment Amounts for Intermediate Waypoints
    WAYPOINT_INCREMENTS = .003
    MAX_INTERMEDIATE_WAYPOINTS = 5

class YelpParamsKyle(object):
    #Authentication for Yelp
    YELP_CONSUMER_KEY = '83MKEDpPxnNnaYXUPBKmxw'
    YELP_CONSUMER_SECRET = '6Shbk8HTNmX6a8mmDFa7gNWm4ko'
    YELP_TOKEN = 'oUjGEtvAmpA7XJWFf627_-bxYcCQqETd'
    YELP_TOKEN_SECRET = 'GNX66S0xKzGP4BYGkYIXrT2sG8E'

class YelpParams(object):
    # OAuth2 Authentication Params for Yelp
    YELP_CONSUMER_KEY = 'q6EDuUKX7VHFQ4yWar_vHQ'
    YELP_CONSUMER_SECRET = 'PXUxWyX5R73PThVeNSmrgvCInkM'
    YELP_TOKEN = 'kowNVsbJEeidTefEwFUzVb6i0WnVzmnv'
    YELP_TOKEN_SECRET = 'mffJkuxDMU0v5jRVqSsPJBN3ko4'