import json

from google.appengine.ext import ndb
from webapp2 import RequestHandler
from decorators import api_token_required
from models import Domain
from restler.serializers import json_response
from strategy import DOMAIN_STRATEGY

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class DomainsHandler(RequestHandler):
    @api_token_required
    def get(self, domain_urlsafe_key):
        device = self.validate_and_get(domain_urlsafe_key, Domain, abort_on_not_found=True)
        json_response(self.response, device, strategy=DOMAIN_STRATEGY)

    @api_token_required
    def post(self):
        if self.request.body is not None:
            request_json = json.loads(self.request.body)
            name = request_json.get('name')
            active = request_json.get('active')
            distributor_urlsafe_key = request_json.get('distributor_key')
            distribution_key = ndb.Key(urlsafe=distributor_urlsafe_key)
            domain = Domain.create(distributor_key=distribution_key,
                                   name=name,
                                   active=active)
            domain_key = domain.put()
            domain_uri = self.request.app.router.build(None,
                                                       'manage-domain',
                                                       None,
                                                       {'domain_key': domain_key.urlsafe()})
            self.response.headers['Location'] = domain_uri
            self.response.headers.pop('Content-Type', None)
            self.response.set_status(201)

    # @api_token_required
    # def put(self, domain_key):
    #     key = ndb.Key(urlsafe=domain_key)
    #     domain = key.get()
    #     request_json = json.loads(self.request.body)
    #     domain.name = request_json.get('name')
    #     domain.active = request_json.get('active')
    #     domain.put()
    #     self.response.headers.pop('Content-Type', None)
    #     self.response.set_status(204)
    #
    # @api_token_required
    # def delete(self, domain_key):
    #     key = ndb.Key(urlsafe=domain_key)
    #     domain = key.get()
    #     if domain:
    #         domain.active = False
    #         domain.put()
    #     self.response.headers.pop('Content-Type', None)
    #     self.response.set_status(204)
