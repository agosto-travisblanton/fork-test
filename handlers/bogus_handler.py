from webapp2 import RequestHandler

from decorators import api_token_required, identity_required, distributor_required


class BogusHandler1(RequestHandler):

    @api_token_required
    def get(self):
        pass


class BogusHandler2(RequestHandler):
    @identity_required
    def get(self):
        pass


class BogusHandler3(RequestHandler):
    @distributor_required
    def get(self):
        pass
