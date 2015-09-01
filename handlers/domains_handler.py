import json

from google.appengine.ext import ndb
from webapp2 import RequestHandler
from decorators import api_token_required
from models import Domain
from restler.serializers import json_response
from strategy import DOMAIN_STRATEGY
from ndb_mixins import KeyValidatorMixin


__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class DomainsHandler(RequestHandler, KeyValidatorMixin):
    @api_token_required
    def get(self, domain_key=None):
        if None == domain_key:
            result = Domain.query()
            result = filter(lambda x: x.active is True, result)
        else:
            result = self.validate_and_get(domain_key, Domain, abort_on_not_found=True)
        json_response(self.response, result, strategy=DOMAIN_STRATEGY)

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
