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
import os
import urllib
import logging

from google.appengine.api import users
# [START import_ndb]
from google.appengine.ext import ndb
# [END import_ndb]

import jinja2
import webapp2

#JINJA_ENVIRONMENT = jinja2.Environment(
#    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
#    extensions=['jinja2.ext.autoescape'])
JINJA_ENVIRONMENT = jinja2.Environment( loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), autoescape = True)  

#template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

good_deal = "good deal the data is going in!"
no_blanks = "we can't add blanks to the database!"


DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.
    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


# [START greeting]
class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END greeting]


# [START main_page]
class MainPage(webapp2.RequestHandler):
#Well, I hope I understand this correctly.  The class detail below addresses 
#the behavior of the get post and validate functions in the guestbook form.
#the method or class here of get is going to retrieve data from the server.  Data 
#that has been previously posted.

    def get(self):

        alert = self.request.get('alert')

        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        num_greetings = 10
        greetings = greetings_query.fetch(num_greetings)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
            'alert': alert
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
        #The GET method that is passing data retrieved from database
        #(line 59) to the template (line78).  The template fills in 
        #the variables with data retrived from the database and the
        #result is rendered to the user. (this was taken almost verbatim
        #from the reviewer's notes)
        #GET requests fetch data from specified resource and POST requests
        #submit data to a specified resource
        

# [START guestbook]
class Guestbook(webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        # in this method, under the Guestbook class we are posting data
        # to the server by way of the guestbook form.
        # we are also validating/retrieving data from the database
        
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)                                 

        greeting = Greeting(parent=guestbook_key(guestbook_name))

        #It is important to validate the user.  In this exercise, it 
        #is only a very high level validation.  Truth is, anyone can sign
        #this log book.  To make it more secure you would have to confirm
        #that the user met certain criteria before even accessing the guestbook.
        #otherwise the database can be accessed, corrupted and data stolen.


        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())

        #again, a very high level validation that only validates if the
        #user has signed or left a message.  You don't want users adding
        #incorrect or corrupt data to the database.

    
        greeting.content = self.request.get('content')
        alert = self.request.get('alert')
        
        if (greeting.content == '' or greeting.content.isspace()): 
            alert = no_blanks 
        else: 
            alert = good_deal
            greeting.put()


        query_params = {'guestbook_name': guestbook_name, 'alert': alert}
        self.redirect('/?' + urllib.urlencode(query_params))
# [END guestbook]

application = webapp2.WSGIApplication([
    ('/', MainPage), # this calls the MainPage class
    ('/sign', Guestbook), #this calls the Guestbook class
    ], debug=True)
