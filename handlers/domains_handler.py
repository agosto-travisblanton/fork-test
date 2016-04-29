import json
import logging

from google.appengine.ext import ndb
from webapp2 import RequestHandler

from decorators import requires_api_token
from models import Domain
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response
from strategy import DOMAIN_STRATEGY


__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class DomainsHandler(RequestHandler, KeyValidatorMixin):
    @requires_api_token
    def get(self, domain_key=None):
        if None == domain_key:
            distributor_key = self.request.headers.get('X-Provisioning-Distributor')
            distributor = ndb.Key(urlsafe=distributor_key)
            domain_list = Domain.query(Domain.distributor_key == distributor).fetch(100)
            result = filter(lambda x: x.active is True, domain_list)
        else:
            result = self.validate_and_get(domain_key, Domain, abort_on_not_found=True)
        json_response(self.response, result, strategy=DOMAIN_STRATEGY)

    @requires_api_token
    def post(self):
        if self.request.body is not str('') and self.request.body is not None:
            status = 201
            error_message = None
            request_json = json.loads(self.request.body)
            name = request_json.get('name')
            if name is None or name == '':
                status = 400
                error_message = 'The name parameter is invalid.'
            else:
                if Domain.already_exists(name):
                    status = 409
                    error_message = "Conflict. Domain name \"{0}\" is in use.".format(name)
            active = request_json.get('active')
            if active is None or active == '' or (str(active).lower() != 'true' and str(active).lower() != 'false'):
                status = 400
                error_message = 'The active parameter is invalid.'
            else:
                active = bool(active)
            impersonation_admin_email_address = request_json.get('impersonation_admin_email_address')
            if impersonation_admin_email_address is None or impersonation_admin_email_address == '':
                status = 400
                error_message = 'The impersonation_admin_email_address parameter is invalid.'
            distributor_urlsafe_key = self.request.headers.get('X-Provisioning-Distributor')
            if distributor_urlsafe_key is None or distributor_urlsafe_key == '':
                status = 400
                error_message = 'The distributor_key parameter is invalid.'
            if status == 201:
                domain = Domain.create(distributor_key=ndb.Key(urlsafe=distributor_urlsafe_key),
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

    @requires_api_token
    def put(self, domain_key):
        status = 204
        message = None
        domain = None
        try:
            domain = ndb.Key(urlsafe=domain_key).get()
        except Exception, e:
            logging.exception(e)
        if domain is None:
            status = 404
            message = 'Unrecognized device with key: {0}'.format(domain_key)
            return self.response.set_status(status, message)
        else:
            request_json = json.loads(self.request.body)
            domain_name = request_json.get('name')
            if Domain.already_exists(domain_name):
                error_message = "Conflict. Domain name \"{0}\" is in use.".format(domain_name)
                return self.response.set_status(409, error_message)
            else:
                domain.name = domain_name
                domain.impersonation_admin_email_address = request_json.get('impersonation_admin_email_address')
                domain.active = request_json.get('active')
                domain.put()
                self.response.headers.pop('Content-Type', None)
                self.response.set_status(status, message)

    @requires_api_token
    def delete(self, domain_key):
        key = ndb.Key(urlsafe=domain_key)
        device = key.get()
        if device:
            device.active = False
            device.put()
        self.response.set_status(204)
        self.response.headers.pop('Content-Type', None)
