import json

from google.appengine.ext import ndb
import logging
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
            result = Domain.query(Domain.active == True)
        else:
            result = self.validate_and_get(domain_key, Domain, abort_on_not_found=True)
        json_response(self.response, result, strategy=DOMAIN_STRATEGY)

    @api_token_required
    def post(self):
        if self.request.body is not str('') and self.request.body is not None:
            status = 201
            error_message = None
            request_json = json.loads(self.request.body)
            name = request_json.get('name')
            if name is None or name == '':
                status = 400
                error_message = 'The name parameter is invalid.'
            active = request_json.get('active')
            if active is None or active == '':
                status = 400
                error_message = 'The active parameter is invalid.'
            impersonation_admin_email_address = request_json.get('impersonation_admin_email_address')
            if impersonation_admin_email_address is None or impersonation_admin_email_address == '':
                status = 400
                error_message = 'The impersonation_admin_email_address parameter is invalid.'
            distributor_urlsafe_key = request_json.get('distributor_key')
            if distributor_urlsafe_key is None or distributor_urlsafe_key == '':
                status = 400
                error_message = 'The distributor_key parameter is invalid.'
            if status == 201:
                distribution_key = ndb.Key(urlsafe=distributor_urlsafe_key)
                domain = Domain.create(distributor_key=distribution_key,
                                       name=name,
                                       impersonation_admin_email_address=impersonation_admin_email_address,
                                       active=active)
                domain_key = domain.put()
                domain_uri = self.request.app.router.build(None,
                                                           'manage-domain',
                                                           None,
                                                           {'domain_key': domain_key.urlsafe()})
                self.response.headers['Location'] = domain_uri
                self.response.headers.pop('Content-Type', None)
                self.response.set_status(201)
            else:
                self.response.set_status(status, error_message)
        else:
            logging.info("Problem creating Domain. No request body.")
            self.response.set_status(400, 'Did not receive request body.')
