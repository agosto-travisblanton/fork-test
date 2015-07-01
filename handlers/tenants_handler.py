import json

from google.appengine.ext import ndb

from webapp2 import RequestHandler

#from content_manager_api import ContentManagerApi
from models import Tenant, TenantEntityGroup
from restler.serializers import json_response
from strategy import TENANT_STRATEGY

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TenantsHandler(RequestHandler):
    ADMIN_ACCOUNT_TO_IMPERSONATE = 'administrator@skykit.com'

    def get(self, tenant_key=None):
        if None == tenant_key:
            result = Tenant.query(ancestor=TenantEntityGroup.singleton().key).fetch(100)
            result = filter(lambda x: x.active is True, result)
        else:
            tenant_key = ndb.Key(urlsafe=tenant_key)
            result = tenant_key.get()
        json_response(self.response, result, strategy=TENANT_STRATEGY)

    def post(self):
        if self.request.body is not None:
            request_json = json.loads(self.request.body)
            name = request_json.get('name')
            admin_email = request_json.get('admin_email')
            tenant_code = request_json.get('tenant_code')
            # content_manager_api = ContentManagerApi()
            content_manager_tenant_key = 'some key' #content_manager_api.create_tenant(name, admin_email)
            if content_manager_tenant_key:
                content_server_url = request_json.get('content_server_url')
                chrome_device_domain = request_json.get('chrome_device_domain')
                content_server_api_key = request_json.get('content_server_api_key')
                active = request_json.get('active')
                tenant = Tenant.create(name=name,
                                       tenant_code=tenant_code,
                                       admin_email=admin_email,
                                       content_server_url=content_server_url,
                                       content_server_api_key=content_server_api_key,
                                       chrome_device_domain=chrome_device_domain,
                                       active=active)
                tenant_key = tenant.put()
                tenant_uri = self.request.app.router.build(None,
                                                           'manage-tenant',
                                                           None,
                                                           {'tenant_key': tenant_key.urlsafe()})
                self.response.headers['Location'] = tenant_uri
                self.response.headers.pop('Content-Type', None)
                self.response.set_status(201)
            else:
                self.response.set_status(422, 'Unable to obtain content server key')

    def put(self, tenant_key):
        key = ndb.Key(urlsafe=tenant_key)
        tenant = key.get()
        request_json = json.loads(self.request.body)
        tenant.tenant_code = request_json.get('tenant_code')
        tenant.name = request_json.get('name')
        tenant.admin_email = request_json.get('admin_email')
        tenant.content_server_url = request_json.get('content_server_url')
        tenant.content_server_api_key = request_json.get('content_server_api_key')
        tenant.chrome_device_domain = request_json.get('chrome_device_domain')
        tenant.active = request_json.get('active')
        tenant.put()
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)

    def delete(self, tenant_key):
        key = ndb.Key(urlsafe=tenant_key)
        tenant = key.get()
        if tenant:
            tenant.active = False
            tenant.put()
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)
