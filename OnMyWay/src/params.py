# Lists of parameters and values used throughout the application.

class MapParams(object):
    # Application's Google Maps API key. This key identifies your application 
    # for purposes of quota management.
    API_KEY = 'AIzaSyAIyNInDkYpSNjc5DJh9ViNqyXD1AusiI8'

    # URL Request Addresses
    API_BASE_URL = 'http://maps.googleapis.com/maps/api'
    API_BASE_URL_SECURE = 'https://maps.googleapis.com/maps/api'

    # Latitude / Longitude Increment Amounts for Intermediate Waypoints
    WAYPOINT_INCREMENTS = 0.006
    MAX_INTERMEDIATE_WAYPOINTS = 5

class YelpParams(object):
    #Authentication for Yelp
    YELP_CONSUMER_KEY = '83MKEDpPxnNnaYXUPBKmxw'
    YELP_CONSUMER_SECRET = '6Shbk8HTNmX6a8mmDFa7gNWm4ko'
    YELP_TOKEN = 'oUjGEtvAmpA7XJWFf627_-bxYcCQqETd'
    YELP_TOKEN_SECRET = 'GNX66S0xKzGP4BYGkYIXrT2sG8E'

class YelpParamsWaseem(object):
    # OAuth2 Authentication Params for Yelp
    YELP_CONSUMER_KEY = 'yDbF4bpNdDWW2clY7VnXHw'
    YELP_CONSUMER_SECRET = 'L4jLP4q3kUrcwCJzfHKffAWGi0I'
    YELP_TOKEN = 'SS4UfObtS8d8E6BYsDHNlsc0ZjGsNjWt'
    YELP_TOKEN_SECRET = '-U1arPRU3EpSCPAuETyU3MxC_zA'

class YelpParamsDina(object):
    # OAuth2 Authentication Params for Yelp
    YELP_CONSUMER_KEY = 'xP3Xi0nxQT3_haz3lATTdw'
    YELP_CONSUMER_SECRET = 'Jt2TA5x9FrYC1cvJtpOjNK5IrNE'
    YELP_TOKEN = '6fIyzoZejx7Jdwob5aJ3QGdh2X8y3Ol5'
    YELP_TOKEN_SECRET = 'No0jktoh-lXztoID9mTof3BllOA'