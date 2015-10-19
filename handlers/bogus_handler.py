from webapp2 import RequestHandler

from decorators import api_token_required, identity_required, distributor_required


class BogusHandler(RequestHandler):

    @api_token_required
    def get(self):
        pass
