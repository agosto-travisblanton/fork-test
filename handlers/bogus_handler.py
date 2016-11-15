from decorators import requires_auth, requires_registration_token, requires_unmanaged_registration_token
from extended_session_request_handler import ExtendedSessionRequestHandler

class BogusHandler(ExtendedSessionRequestHandler):

    @requires_auth
    def get(self):
        pass

    @requires_registration_token
    def post(self):
        pass

    @requires_unmanaged_registration_token
    def put(self):
        pass
