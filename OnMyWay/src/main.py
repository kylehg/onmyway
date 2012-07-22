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
import json
import logging
import maps
import oauth2
import os
import urllib
import urllib2
import webapp2

from yelp import yelp_recommendation
from google.appengine.ext.webapp import template

TEMPLATES_DIR = 'templates'
DEBUG = True

class MainHandler(webapp2.RequestHandler):

    def get(self):
        # Render index.html
    	index_file = os.path.join(TEMPLATES_DIR, 'index.html')
        index_template = template.render(index_file, {})
        self.response.out.write(index_template)

class RPCHandler(webapp2.RequestHandler):

    def get(self):
        param_method = self.request.get('method')
        methods = {'onmyway': self.on_my_way, 'add': self.add}
        method = methods.get(param_method)
        # Look up to see if the method exists
        if method:
            response = method()
            response['status'] = 'OK'
        else:
            response = {'status': 'UNSUPPORTED_METHOD'}    
        self.response.out.write(json.dumps(response))

    def on_my_way(self):
        if DEBUG:
            recommendations = [{'id': u'starbucks-new-york-162', 'rating': 3.5, 'formatted_address': u'684 8th Ave', 'name': u'Starbucks', 'location': {'latitude': 40.7581085, 'longitude': -73.9891272}}, {'id': u'macaron-cafe-new-york-3', 'rating': 4.0, 'formatted_address': u'161 West 36 St.', 'name': u'Macaron Cafe', 'location': {'latitude': 40.7520263, 'longitude': -73.9890469}}, {'id': u'stumptown-coffee-roasters-new-york', 'rating': 4.5, 'formatted_address': u'The Ace Hotel, 20 W 29th St', 'name': u'Stumptown Coffee Roasters', 'location': {'latitude': 40.7456025, 'longitude': -73.9878759}}, {'id': u'71-irving-place-coffee-and-tea-bar-new-york', 'rating': 3.5, 'formatted_address': u'71 Irving Pl', 'name': u'71 Irving Place Coffee & Tea Bar', 'location': {'latitude': 40.736833, 'longitude': -73.987026}}, {'id': u'mud-new-york-3', 'rating': 4.0, 'formatted_address': u'307 E 9th St', 'name': u'MUD', 'location': {'latitude': 40.7290302, 'longitude': -73.986652}}]
            return {'recommendations': recommendations}

        points = []
        query = self.request.get('query')
        for prefix in ['origin', 'destination']:
            point = {}
            lat = self.request.get(prefix + '_lat')
            lng = self.request.get(prefix + '_lng')
            if lat and lng:
                point['location'] = {'lat':float(lat), 'lng':float(lng)}
            point['text'] = self.request.get(prefix + '_text')
            points.append(point)

        end_locations = []

        for point in points:
            point_location = point.get('location')
            text = point.get('text')

            # If point coordinates are not specified find them using text search
            if not point_location or text:
                logging.info('Point location not specified. Doing text search.')
                sensor = 'true'
                args = {}
                if points[0]['location']:
                    lat = points[0]['location']['lat']
                    lng = points[0]['location']['lng']
                    args['location'] = '%s,%s' % (lat, lng)
                    args['radius'] = 15000     # 15 km
                place = maps.places(query=text, sensor=sensor, **args)[0]
                logging.info('Using %s as place with address: %s',
                             place['name'], place['formatted_address'])
                point_location = place['location']

            end_locations.append(point_location)

        logging.info('Origin Point: %s', end_locations[0])
        logging.info('Destination Point: %s', end_locations[1])
        search_locations = maps.intermediate_locations(end_locations[0],
                                                       end_locations[1])
        recommendations = yelp_recommendation(query, search_locations)
        logging.info(recommendations)
        return {'recommendations': recommendations}

    def add(self):
        x = self.request.get('x')
        y = self.request.get('y')
        return {'sum': x + y}

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/find', RPCHandler)],
                              debug=True)
