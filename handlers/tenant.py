from webapp2 import RequestHandler


__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TenantsHandler(RequestHandler):
    def get(self):
        pass

    def post(self):
        pass

    def put(self, tenant_id):
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)

    def delete(self, tenant_id):
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)

