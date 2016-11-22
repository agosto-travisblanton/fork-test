import os
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from oauth2client import client, crypt
from models import User, Distributor
from app_config import config
from restler.serializers import json_response
import httplib

HUNDRED_YEARS = 3144960000


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


def generate_token(user, expiration=HUNDRED_YEARS):
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


def requires_auth(f):
    @wraps(f)
    def decorated(self, *args, **kwargs):
        ################################################
        # DO THE ACTUAL TOKEN VALIDATION
        ################################################
        token = self.request.headers.get('JWT')

        if token and token != '':
            string_token = token.encode('ascii', 'ignore')
            user = verify_our_token(string_token)
            if user:
                self.user_entity = User.get_or_insert_by_email(user["email"])
                return f(self, *args, **kwargs)

        return json_response(self.response, {
            "message": "Authentication is required to access this resource",
            "OAUTH_CLIENT_ID": config.OAUTH_CLIENT_ID,
            'BROWSER_API_KEY': config.PUBLIC_API_SERVER_KEY,
            'version': os.environ['CURRENT_VERSION_ID']
        }, status_code=httplib.FORBIDDEN)

    return decorated
