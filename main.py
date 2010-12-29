import datetime
import logging
import os
import random
from django.utils import simplejson
from google.appengine.api import channel
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.deferred import deferred
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app


def create_channel():
  return channel.create_channel("test_channel")

def send(message):
    channel.send_message("test_channel", simplejson.dumps(message))

class SendMessage(webapp.RequestHandler):

    def get(self):
        send(self.request.get('msg','default test message'))
        
class Index(webapp.RequestHandler):

    def get(self):
        channel_id = create_channel()
        context = {'channel_id': channel_id,}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, context))

application = webapp.WSGIApplication([('/', Index),
                                      ('/send', SendMessage)
                                     ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
