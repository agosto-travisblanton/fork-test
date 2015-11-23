from webapp2 import RequestHandler

from decorators import requires_api_token, requires_registration_token, requires_unmanaged_registration_token


class BogusHandler(RequestHandler):

    @requires_api_token
    def get(self):
        pass

    @requires_registration_token
    def post(self):
        pass

    @requires_unmanaged_registration_token
    def put(self):
        pass
