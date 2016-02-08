import json
import logging

from google.appengine.ext import ndb
from webapp2 import RequestHandler

from content_manager_api import ContentManagerApi
from decorators import requires_api_token
from models import Tenant, TenantEntityGroup, Domain
from restler.serializers import json_response
from strategy import TENANT_STRATEGY
from utils.iterable_util import delimited_string_to_list

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TenantsHandler(RequestHandler):

    @requires_api_token
    def get(self, tenant_key=None):
        if None == tenant_key:
            distributor_key = self.request.headers.get('X-Provisioning-Distributor')
            distributor = ndb.Key(urlsafe=distributor_key)
            domain_keys = Domain.query(Domain.distributor_key == distributor).fetch(100, keys_only=True)
            tenant_list = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
            tenant_list = filter(lambda x: x.active is True, tenant_list)
            result = filter(lambda x: x.domain_key in domain_keys, tenant_list)
        else:
            tenant_key = ndb.Key(urlsafe=tenant_key)
            result = tenant_key.get()
        json_response(self.response, result, strategy=TENANT_STRATEGY)

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
            admin_email = request_json.get('admin_email')
            if admin_email is None or admin_email == '':
                status = 400
                error_message = 'The admin email parameter is invalid.'
            tenant_code = request_json.get('tenant_code')
            if tenant_code is None or tenant_code == '':
                status = 400
                error_message = 'The tenant code parameter is invalid.'
            content_server_url = request_json.get('content_server_url')
            if content_server_url is None or content_server_url == '':
                status = 400
                error_message = 'The content server url parameter is invalid.'
            content_manager_base_url = request_json.get('content_manager_base_url')
            if content_manager_base_url is None or content_manager_base_url == '':
                status = 400
                error_message = 'The content manager base url parameter is invalid.'
            notification_emails = delimited_string_to_list(request_json.get('notification_emails'))
            domain_key_input = request_json.get('domain_key')
            domain_key = None
            if domain_key_input is None or domain_key_input == '':
                status = 400
                error_message = 'The domain key parameter is invalid.'
            else:
                try:
                    domain_key = ndb.Key(urlsafe=domain_key_input)
                except Exception, e:
                    logging.exception(e)
                if None is domain_key:
                    status = 400
                    error_message = 'The domain did not resolve.'
            active = request_json.get('active')
            if active is None or active == '' or (str(active).lower() != 'true' and str(active).lower() != 'false'):
                status = 400
                error_message = 'The active parameter is invalid.'
            else:
                active = bool(active)
            proof_of_play_logging = request_json.get('proof_of_play_logging')
            if proof_of_play_logging is None or active == '' or (str(proof_of_play_logging).lower() != 'true' and str(proof_of_play_logging).lower() != 'false'):
                status = 400
                error_message = 'The proof_of_play_logging parameter is invalid.'
            else:
                proof_of_play_logging = bool(proof_of_play_logging)
            if status == 201:
                if Tenant.is_tenant_code_unique(tenant_code):
                    tenant = Tenant.create(name=name,
                                           tenant_code=tenant_code,
                                           admin_email=admin_email,
                                           content_server_url=content_server_url,
                                           content_manager_base_url=content_manager_base_url,
                                           domain_key=domain_key,
                                           active=active,
                                           notification_emails = notification_emails,
                                           proof_of_play_logging=proof_of_play_logging)
                    tenant_key = tenant.put()
                    content_manager_api = ContentManagerApi()
                    notify_content_manager = content_manager_api.create_tenant(tenant)
                    if not notify_content_manager:
                        logging.info('Failed to notify content manager about new tenant {0}'.format(name))
                    tenant_uri = self.request.app.router.build(None,
                                                               'manage-tenant',
                                                               None,
                                                               {'tenant_key': tenant_key.urlsafe()})
                    self.response.headers['Location'] = tenant_uri
                    self.response.headers.pop('Content-Type', None)
                    self.response.set_status(201)
                else:
                    error_message = "Conflict. Tenant code \"{0}\" is already assigned to a tenant.".format(tenant_code)
                    self.response.set_status(409, error_message)
            else:
                self.response.set_status(status, error_message)
        else:
            logging.info("Problem creating Domain. No request body.")
            self.response.set_status(400, 'Did not receive request body.')

    @requires_api_token
    def put(self, tenant_key):
        key = ndb.Key(urlsafe=tenant_key)
        tenant = key.get()
        request_json = json.loads(self.request.body)
        tenant.tenant_code = request_json.get('tenant_code')
        tenant.name = request_json.get('name')
        tenant.admin_email = request_json.get('admin_email')
        tenant.content_server_url = request_json.get('content_server_url')
        tenant.content_manager_base_url = request_json.get('content_manager_base_url')
        email_list = delimited_string_to_list(request_json.get('notification_emails'))
        tenant.notification_emails = email_list
        domain_key_input = request_json.get('domain_key')
        tenant.active = request_json.get('active')
        proof_of_play_logging = request_json.get('proof_of_play_logging')
        if str(proof_of_play_logging).lower() == 'true' or str(proof_of_play_logging).lower() == 'false':
            tenant.proof_of_play_logging = bool(proof_of_play_logging)
            if tenant.proof_of_play_logging is False:
                Tenant.turn_off_proof_of_play(tenant.tenant_code)
            elif tenant.proof_of_play_logging is True:
                Tenant.turn_on_proof_of_play(tenant.tenant_code)
        try:
            domain_key = ndb.Key(urlsafe=domain_key_input)
        except Exception, e:
            logging.exception(e)
        if domain_key:
            tenant.domain_key = domain_key
        tenant.put()
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)

    @requires_api_token
    def delete(self, tenant_key):
        key = ndb.Key(urlsafe=tenant_key)
        tenant = key.get()
        if tenant:
            tenant.active = False
            tenant.put()
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)
