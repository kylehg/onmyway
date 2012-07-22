import json
import oauth2
import urllib
import urllib2
import logging
from params import YelpParams

PATH = 'api.yelp.com/v2/search'

def yelp_recommendation(keyword, stops):
    locations = []
    for stop in stops:
        coord = str(stop['lat']) + ", " + str(stop['lng'])
        answer = find_stop(coord, keyword)
        if not answer['id'] in [location['id'] for location in locations]:
            locations.append(answer)
    return locations

def find_stop(ll, keyword):
    
    url_params = {}
    url_params['limit'] = 4
    url_params['sort'] = 1

    url_params['ll'] = ll
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
    token = oauth2.Token(YelpParams.YELP_TOKEN, YelpParams.YELP_TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
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
    top = sorted(response['businesses'], key=lambda k: k['rating'], reverse=True)[0]
    results = {}
    results['name'] = top['name']
    results['formatted_address'] = ', '.join(top['location']['address'])
    latitude = top['location']['coordinate']['latitude']
    longitude = top['location']['coordinate']['longitude']
    results['location'] = {'latitude': latitude, 'longitude':longitude}
    results['rating'] = top['rating']
    results['id'] = top['id']
    return results
