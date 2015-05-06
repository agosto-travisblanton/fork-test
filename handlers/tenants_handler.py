import json
from webapp2 import RequestHandler, uri_for
from models import Tenant


__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TenantsHandler(RequestHandler):
    def get(self):
        pass

    def post(self):
        if self.request.body is not None:
            request_json = json.loads(self.request.body)
            tenant = Tenant(name=request_json['tenant']['name'])
            tenant_key = tenant.put()
            tenant_uri = self.request.app.router.build(None,
                                                       'tenants-mutator',
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

