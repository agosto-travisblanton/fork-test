import json
from google.appengine.ext import ndb

from webapp2 import RequestHandler

from models import Tenant, TenantEntityGroup
from restler.serializers import json_response
from strategy import TENANT_STRATEGY


__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TenantsHandler(RequestHandler):
    def get(self, tenant_key=None):
        if tenant_key == None:
            result = Tenant.query(ancestor=TenantEntityGroup.singleton().key).fetch(50)
        else:
            tenant_key = ndb.Key(urlsafe=tenant_key)
            result = tenant_key.get()
        json_response(self.response, result, strategy=TENANT_STRATEGY)

    def post(self):
        if self.request.body is not None:
            request_json = json.loads(self.request.body)
            name = request_json['name']
            admin_email = request_json['admin_email']
            content_server_url = request_json['content_server_url']
            chrome_device_domain = request_json['chrome_device_domain']
            if chrome_device_domain is not None:
                chrome_device_domain = request_json['chrome_device_domain']
            tenant = Tenant.create(name, admin_email, content_server_url, chrome_device_domain)
            tenant_key = tenant.put()
            tenant_uri = self.request.app.router.build(None,
                                                       'manage-tenant',
                                                       None,
                                                       {'tenant_key': tenant_key.urlsafe()})
            self.response.headers['Location'] = tenant_uri
            self.response.headers.pop('Content-Type', None)
            self.response.set_status(201)

    def put(self, tenant_key):
        key = ndb.Key(urlsafe=tenant_key)
        tenant = key.get()
        request_json = json.loads(self.request.body)
        tenant.name = request_json.get('name')
        tenant.put()
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)

    def delete(self, tenant_key):
        key = ndb.Key(urlsafe=tenant_key)
        tenant = key.get()
        if tenant:
            tenant.key.delete()
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)
