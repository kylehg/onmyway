import json
import oauth2
import urllib
import urllib2
import logging
from params import YelpParams

PATH = 'api.yelp.com/v2/search'

def yelp(self, current_location, location, keyword):
    
    url_params = {}
    url_params['limit'] = 1
    url_params['sort'] = 2

    if location:
        url_params['location'] = location
        logging.info(location)
    else:
        url_params['ll'] = current_location
        logging.info("ll")
    url_params['term'] = keyword
    """Returns response for API request."""
    # Unsigned URL
    encoded_params = ''
    if url_params:
        encoded_params = urllib.urlencode(url_params)
    url = 'http://%s?%s' % (PATH, encoded_params)
    logging.info('URL: %s' % (url,))
                
    # Sign the URL
    consumer = oauth2.Consumer(YelpParams.YELP_CONSUMER_KEY, YelpParams.YELP_CONSUMER_SECRET)
    oauth_request = oauth2.Request('GET', url, {})
    oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                          'oauth_timestamp': oauth2.generate_timestamp(),
                          'oauth_token': YelpParams.YELP_TOKEN,
                          'oauth_consumer_key': YelpParams.YELP_CONSUMER_KEY})
    self.token = oauth2.Token(YelpParams.YELP_TOKEN, YelpParams.YELP_TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, self.token)
    signed_url = oauth_request.to_url()
    logging.info('Signed URL: %s\n' % (signed_url,))

    # Connect
    try:
        conn = urllib2.urlopen(signed_url, None)
        try:
            response = json.loads(conn.read())
        finally:
            conn.close()
    except urllib2.HTTPError, error:
        response = json.loads(error.read())
        logging.info(response)
    results = {}
    top = response['businesses'][0]
    results['name'] = top['name']
    results['formatted_location'] = ', '.join(top['location']['address'])
    latitude = top['location']['coordinate']['latitude']
    longitude = top['location']['coordinate']['longitude']
    results['location'] = {'latitude': latitude, 'longitude':longitude}
    return results
