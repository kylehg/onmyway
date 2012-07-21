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
import os
import webapp2

from google.appengine.ext.webapp import template

TEMPLATES_DIR = 'templates'

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	index_file = os.path.join(TEMPLATES_DIR, 'index.html')
        index_template = template.render(index_file, {})
        self.response.out.write(index_template)

app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)