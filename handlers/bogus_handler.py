from webapp2 import RequestHandler
from decorators import api_token_required


class BogusHandler(RequestHandler):

    @api_token_required
    def get(self):
        pass

