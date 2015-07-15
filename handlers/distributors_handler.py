import json

from google.appengine.ext import ndb

from webapp2 import RequestHandler

from decorators import api_token_required
from models import Distributor
from restler.serializers import json_response

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class DistributorsHandler(RequestHandler):
    @api_token_required
    def get(self, distributor_key=None):
        if None == distributor_key:
            result = Distributor.query().fetch(100)
            result = filter(lambda x: x.active is True, result)
        else:
            distributor_key = ndb.Key(urlsafe=distributor_key)
            result = distributor_key.get()
        json_response(self.response, result)

    @api_token_required
    def post(self):
        if self.request.body is not None:
            request_json = json.loads(self.request.body)
            name = request_json.get('name')
            active = True #request_json.get('active')
            distributor = Distributor.create(name=name,
                                            active=active)
            distributor_key = distributor.put()
            distributor_uri = self.request.app.router.build(None,
                                                       'manage-distributor',
                                                       None,
                                                       {'distributor_key': distributor_key.urlsafe()})
            self.response.headers['Location'] = distributor_uri
            self.response.headers.pop('Content-Type', None)
            self.response.set_status(201)
