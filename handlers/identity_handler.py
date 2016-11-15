from utils.auth_util import requires_auth
from extended_session_request_handler import ExtendedSessionRequestHandler
from app_config import config
from utils.auth_util import verify_google_token, verify_our_token
from models import User
from restler.serializers import json_response
import os
import httplib

class IdentityHandler(ExtendedSessionRequestHandler):
    def get(self):
        token = self.request.headers.get('JWT')

        if token and token != '':
            string_token = token.encode('ascii', 'ignore')
            user = verify_our_token(string_token)
            if user:
                user_entity = User.get_by_email(user["email"])
                if not user_entity:
                    user_entity = User.insert_user(user["name"], user["email"])
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

