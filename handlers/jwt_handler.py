from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from oauth2client import client, crypt
from models import User, Distributor
from app_config import config
from ndb_mixins import KeyValidatorMixin

from restler.serializers import json_response
from agar.sessions import SessionRequestHandler

TWO_WEEKS = 1209600

import os
def requires_auth(f):
    @wraps(f)
    def decorated(self, *args, **kwargs):
        token = self.request.headers.get('Authenticated')
        if token:
            string_token = token.encode('ascii', 'ignore')
            user = verify_our_token(string_token)
            if user:
                user_entity = User.get_by_email(user["email"])
                if not user_entity:
                    user_entity = User.insert_user(user["name"], user["email"])
                self.user_entity = user_entity
                return f(self, *args, **kwargs)

        return json_response(self.response, {
            "message": "Authentication is required to access this resource",
            "OAUTH_CLIENT_ID": config.OAUTH_CLIENT_ID,
            'BROWSER_API_KEY': config.PUBLIC_API_SERVER_KEY,
            'version': os.environ['CURRENT_VERSION_ID'],

        })

    return decorated


class JWTHandler(SessionRequestHandler, KeyValidatorMixin):
    def get(self):
        token = self.request.headers.get('oAuth')
        print self.request
        print "here"
        print token
        if token:
            string_token = token.encode('ascii', 'ignore')
            valid_token = verify_google_token(string_token)
            print valid_token
            if valid_token:
                user_entity = User.get_or_insert_by_email(valid_token["email"])
                if not user_entity:
                    user_entity = User.get_or_insert_by_email(valid_token["email"])
                our_token = generate_token(user_entity)

                return json_response(self.response, {"token": our_token})

        return json_response(self.response, {"message": "Authentication is required to access this resource"})

    @requires_auth
    def get_is_our_token_valid(self):
        return json_response(self.response, {"valid": True, "user": self.user_entity})


def verify_google_token(token):
    try:
        # app.config is defined in root config.py
        # OAUTH_CLIENT_ID created here:
        # https://console.cloud.google.com/apis/credentials?project=agosto-dev-danielternyak
        valid_user = client.verify_id_token(token, config.OAUTH_CLIENT_ID)
        # If multiple clients access the backend server:
        if valid_user['aud'] != config.OAUTH_CLIENT_ID:
            raise crypt.AppIdentityError("Unrecognized client.")
        if valid_user['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        valid_user = None

    return valid_user


def verify_our_token(token):
    # app.config is defined in root config.py
    s = Serializer(config.JWT_SECRET_KEY)
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired) as e:
        return None
    return data


def generate_token(user, expiration=TWO_WEEKS):
    # session_distributor = self.session.get('distributor')
    # distributors = user.distributors
    # if not session_distributor and len(distributors) == 1:
    #     session_distributor = distributors[0].name
    # 'distributor': session_distributor

    distributor_names = [distributor.name for distributor in user.distributors]
    distributors_as_admin = [each_distributor.name for each_distributor in user.distributors_as_admin]

    s = Serializer(config.JWT_SECRET_KEY, expires_in=expiration)
    token = s.dumps({
        'key': user.key.urlsafe(),
        'email': user.email,
        'is_admin': user.is_administrator,
        'is_logged_in': True,
        'distributors': [distributor.name for distributor in
                         Distributor.query().fetch()] if user.is_administrator else distributor_names,
        'distributors_as_admin': [
            distributor.name for distributor in
            Distributor.query().fetch()] if user.is_administrator else distributors_as_admin,

    }).decode('utf-8')
    return token
