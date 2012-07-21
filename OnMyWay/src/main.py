#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import json
import oauth2
import urllib
import urllib2
import logging
from google.appengine.ext.webapp import template

TEMPLATES_DIR = 'templates'

SCOPE = 'https://www.googleapis.com/auth/userinfo.email'
HOST = 'api.yelp.com'
PATH = '/v2/search'
CONSUMER_KEY = 'eHr2SL2LJYafgwfwP22NoQ'
CONSUMER_SECRET = 'yKepW4_EPYfeE7dU4viGI1u2LDw'
TOKEN = '8JkZ4i4f0pdoBaSOnQ5ruKxXRQGXHnve'
TOKEN_SECRET = 'aGQBDoS33Cm6VipOeCLVRVM31s4'
url_params = {}
url_params['location'] = 'sf'
url_params['term'] = 'bar'

class MainHandler(webapp2.RequestHandler):

    def get(self):
    	index_file = os.path.join(TEMPLATES_DIR, 'index.html')
        index_template = template.render(index_file, {})
        self.response.out.write(index_template)
#        answer = self.yelp(HOST, PATH, url_params, CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET)
#        self.response.out.write(answer)
        
    def yelp(self, host, path, url_params, consumer_key, consumer_secret, token, token_secret):
        """Returns response for API request."""
        # Unsigned URL
        encoded_params = ''
        if url_params:
            encoded_params = urllib.urlencode(url_params)
        url = 'http://%s%s?%s' % (host, path, encoded_params)
        logging.info('URL: %s' % (url,))
                
        # Sign the URL
        consumer = oauth2.Consumer(consumer_key, consumer_secret)
        oauth_request = oauth2.Request('GET', url, {})
        oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                              'oauth_timestamp': oauth2.generate_timestamp(),
                              'oauth_token': token,
                              'oauth_consumer_key': consumer_key})

        token = oauth2.Token(token, token_secret)
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
        return response

app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)
