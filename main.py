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


class BaseHandler(webapp.RequestHandler):

    def get(self):
        pass
        
    def post(self): # POST and GET use same handler, making testing easier
        return self.get()


class SendMessage(BaseHandler):

    def get(self):
        # TODO:
        # when the client posts a message to return to browser via channel API,
        # also, save to datastore (pass to background task for best performance)
        json_str = self.request.get('json','{"foo":30,"foo2":40,"foo3":50}')
        json_obj = simplejson.loads(json_str) # now we have a dictionary!
        send(str(json_obj.keys()))
    
        
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
