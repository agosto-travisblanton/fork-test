import json
import logging
import requests
from models import User
from oauth2client.crypt import AppIdentityError
from oauth2client import client
from app_config import config
from stormpath.resources import Provider
from stormpath.error import Error as StormpathError


def get_auth_application():
    return config.STORMPATH_CLIENT.applications.search(config.STORMPATH_AUTH_APP)[0]


def get_google_directory():
    return config.STORMPATH_CLIENT.directories.items(Provider.GOOGLE)[0]


def google_login(id_token, access_token, code):
    user = None
    if id_token is not None:
        # Check that the ID Token is valid.
        try:
            # Client library can verify the ID token.
            client.verify_id_token(id_token, config.CLIENT_ID)  # returns jwt. jwt["sub"] = gplus id
        except AppIdentityError:
            logging.error('Invalid ID Token.')

    if access_token is not None:
        # Check that the Access Token is valid.
        url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'.format(access_token)
        result = json.loads(requests.get(url).text)

        if result.get('error') is not None:
            # This is not a valid token.
            logging.error('Invalid Access Token.')
        elif result['issued_to'] != config.CLIENT_ID:
            # This is not meant for this app. It is VERY important to check
            # the client ID in order to prevent man-in-the-middle attacks.
            logging.error('Access Token not meant for this app.')
        else:
            stormpath_app = get_auth_application()
            try:
                account = stormpath_app.get_provider_account(provider=Provider.GOOGLE, code=code)
                if account:
                    user = User.update_or_create_with_api_account(account)

            except StormpathError as e:
                logging.exception(e)

    return user


def cloud_login(email, password):
    user = None
    stormpath_app = get_auth_application()

    try:
        resp = stormpath_app.authenticate_account(email, password)
        if resp and resp.account:
            user = User.update_or_create_with_api_account(resp.account)

    except StormpathError as e:
        logging.exception(e)

    return user

