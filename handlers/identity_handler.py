from utils.auth_util import requires_auth
from ndb_mixins import KeyValidatorMixin

from restler.serializers import json_response
from agar.sessions import SessionRequestHandler


class IdentityHandler(SessionRequestHandler, KeyValidatorMixin):
    @requires_auth
    def get(self):
        return json_response(self.response, {
            "valid": True,
            "user": self.user_entity
        })
