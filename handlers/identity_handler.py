from extended_session_request_handler import ExtendedSessionRequestHandler
from app_config import config
from utils.auth_util import verify_our_token
from models import User
from restler.serializers import json_response
import os

class IdentityHandler(ExtendedSessionRequestHandler):
    def get(self):
        token = self.request.headers.get('JWT')

        if token and token != '':
            string_token = token.encode('ascii', 'ignore')
            user = verify_our_token(string_token)
            if user:
                user_entity = User.get_by_email(user["email"])
                if not user_entity:
                    user_entity = User.get_or_insert_by_email(user["email"])
                self.user_entity = user_entity

                return json_response(self.response, {
                    "valid": True,
                    "user": self.user_entity
                })

        return json_response(self.response, {
            "message": "YOU ARE NOT AUTHENTICATED",
            "OAUTH_CLIENT_ID": config.OAUTH_CLIENT_ID,
            'BROWSER_API_KEY': config.PUBLIC_API_SERVER_KEY,
            'version': os.environ['CURRENT_VERSION_ID'],
        })

