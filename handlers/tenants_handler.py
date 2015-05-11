import json

from webapp2 import RequestHandler

from models import Tenant, TenantEntityGroup
from restler.serializers import json_response


__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TenantsHandler(RequestHandler):
    def get(self):
        tenants = Tenant.query(ancestor=TenantEntityGroup.singleton().key).fetch(50)
        json_response(self.response, tenants)

    def post(self):
        if self.request.body is not None:
            request_json = json.loads(self.request.body)
            tenant_entity_group = TenantEntityGroup.singleton()
            tenant = Tenant(parent=tenant_entity_group.key,
                            name=request_json['tenant']['name'])
            tenant_key = tenant.put()
            tenant_uri = self.request.app.router.build(None,
                                                       'tenant-mutator',
                                                       None,
                                                       {'tenant_id': tenant_key.urlsafe()})
            self.response.headers['Location'] = tenant_uri
            self.response.headers.pop('Content-Type', None)
            self.response.set_status(201)

    def put(self, tenant_id):
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)

    def delete(self, tenant_id):
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)

