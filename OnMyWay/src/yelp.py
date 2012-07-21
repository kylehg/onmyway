import json
import oauth2
import urllib
import urllib2
import logging

path = 'api.yelp.com/v2/search'
consumer_key = '83MKEDpPxnNnaYXUPBKmxw'
consumer_secret = '6Shbk8HTNmX6a8mmDFa7gNWm4ko'
token = 'oUjGEtvAmpA7XJWFf627_-bxYcCQqETd'
token_secret = 'GNX66S0xKzGP4BYGkYIXrT2sG8E'
url_params = {}
url_params['limit'] = 1
url_params['sort'] = 2

def yelp(self, current_location, location, keyword):
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
    url = 'http://%s?%s' % (path, encoded_params)
    logging.info('URL: %s' % (url,))
                
    # Sign the URL
    consumer = oauth2.Consumer(consumer_key, consumer_secret)
    oauth_request = oauth2.Request('GET', url, {})
    oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                          'oauth_timestamp': oauth2.generate_timestamp(),
                          'oauth_token': token,
                          'oauth_consumer_key': consumer_key})
    self.token = oauth2.Token(token, token_secret)
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
    results['latitude'] = top['location']['coordinate']['latitude']
    results['longitude'] = top['location']['coordinate']['longitude']
        
    return results
