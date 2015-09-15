import json
import logging

from google.appengine.ext import ndb
from webapp2 import RequestHandler
from content_manager_api import ContentManagerApi
from decorators import api_token_required
from models import Tenant, TenantEntityGroup, Domain
from restler.serializers import json_response
from strategy import TENANT_STRATEGY

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TenantsHandler(RequestHandler):
    ADMIN_ACCOUNT_TO_IMPERSONATE = 'administrator@skykit.com'
    AGOSTO_DISTRIBUTOR = 'Agosto'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'

    @api_token_required
    def get(self, tenant_key=None):
        if None == tenant_key:
            result = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
            result = filter(lambda x: x.active is True, result)
        else:
            tenant_key = ndb.Key(urlsafe=tenant_key)
            result = tenant_key.get()
        json_response(self.response, result, strategy=TENANT_STRATEGY)

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
            chrome_device_domain = request_json.get('chrome_device_domain')
            if chrome_device_domain is None or chrome_device_domain == '':
                chrome_device_domain = 'deprecated'
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
            if status == 201:
                tenant = Tenant.create(name=name,
                                       tenant_code=tenant_code,
                                       admin_email=admin_email,
                                       content_server_url=content_server_url,
                                       content_manager_base_url=content_manager_base_url,
                                       chrome_device_domain=chrome_device_domain,
                                       domain_key=domain_key,
                                       active=active)
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
                self.response.set_status(status, error_message)
        else:
            logging.info("Problem creating Domain. No request body.")
            self.response.set_status(400, 'Did not receive request body.')

    @api_token_required
    def put(self, tenant_key):
        key = ndb.Key(urlsafe=tenant_key)
        tenant = key.get()
        request_json = json.loads(self.request.body)
        tenant.tenant_code = request_json.get('tenant_code')
        tenant.name = request_json.get('name')
        tenant.admin_email = request_json.get('admin_email')
        tenant.content_server_url = request_json.get('content_server_url')
        tenant.content_manager_base_url = request_json.get('content_manager_base_url')
        tenant.chrome_device_domain = request_json.get('chrome_device_domain')
        domain_key_input = request_json.get('domain_key')
        try:
            domain_key = ndb.Key(urlsafe=domain_key_input)
        except Exception, e:
            logging.exception(e)
        if domain_key:
            tenant.domain_key = domain_key
        tenant.active = request_json.get('active')
        tenant.put()
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)

    @api_token_required
    def delete(self, tenant_key):
        key = ndb.Key(urlsafe=tenant_key)
        tenant = key.get()
        if tenant:
            tenant.active = False
            tenant.put()
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)
