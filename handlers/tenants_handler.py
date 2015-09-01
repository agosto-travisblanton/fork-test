import json

from google.appengine.ext import ndb
from webapp2 import RequestHandler

from decorators import api_token_required
from models import Tenant, TenantEntityGroup, Distributor, Domain
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
        if self.request.body is not None:
            request_json = json.loads(self.request.body)
            name = request_json.get('name')
            admin_email = request_json.get('admin_email')
            tenant_code = request_json.get('tenant_code')
            content_server_url = request_json.get('content_server_url')
            chrome_device_domain = request_json.get('chrome_device_domain')
            active = request_json.get('active')

            tenant = Tenant.create(name=name,
                                   tenant_code=tenant_code,
                                   admin_email=admin_email,
                                   content_server_url=content_server_url,
                                   chrome_device_domain=chrome_device_domain,
                                   domain_key=self.get_agosto_domain_key(),
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

    @api_token_required
    def put(self, tenant_key):
        key = ndb.Key(urlsafe=tenant_key)
        tenant = key.get()
        request_json = json.loads(self.request.body)
        tenant.tenant_code = request_json.get('tenant_code')
        tenant.name = request_json.get('name')
        tenant.admin_email = request_json.get('admin_email')
        tenant.content_server_url = request_json.get('content_server_url')
        tenant.chrome_device_domain = request_json.get('chrome_device_domain')
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

    def get_agosto_domain_key(self):
        agosto_distributor = Distributor.find_by_name(self.AGOSTO_DISTRIBUTOR.lower())
        distributor_key = None
        if agosto_distributor is None:
            distributor = Distributor.create(name=self.AGOSTO_DISTRIBUTOR,
                                             active=True)
            distributor_key = distributor.put()

        domain_key = Domain.query(ndb.AND(Domain.distributor_key == distributor_key,
                                          Domain.name == self.CHROME_DEVICE_DOMAIN)).get(keys_only=True)
        if domain_key:
            return domain_key
        else:
            domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                   distributor_key=distributor_key,
                                   active=True)
            return domain.put()
