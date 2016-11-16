from utils.auth_util import verify_google_token, generate_token
from models import User
from ndb_mixins import KeyValidatorMixin

from restler.serializers import json_response
from agar.sessions import SessionRequestHandler

TWO_WEEKS = 1209600



class LoginHandler(SessionRequestHandler, KeyValidatorMixin):
    def get(self):
        token = self.request.headers.get('oAuth')
        if token:
            string_token = token.encode('ascii', 'ignore')
            valid_token = verify_google_token(string_token)
            if valid_token:
                user_entity = User.get_or_insert_by_email(valid_token["email"])
                if not user_entity:
                    user_entity = User.get_or_insert_by_email(valid_token["email"])
                our_token = generate_token(user_entity)

                return json_response(self.response, {
                    "token": our_token,
                })

        return json_response(self.response, {
            "message": "Authentication is required to access this resource"
        }, status_code=403)
