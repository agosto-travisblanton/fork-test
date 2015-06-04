"""
The configuration file used by :py:mod:`agar.config` implementations and other libraries using the
`google.appengine.api.lib_config`_ configuration library. Configuration overrides go in this file.
"""
from env_setup import setup;

setup()
import os
from agar.env import on_development_server, on_server, on_production_server, on_integration_server

##############################################################################
# APPLICATION SETTINGS
##############################################################################

def _APP_ROOT():
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


app_APP_ROOT = _APP_ROOT()


def _APP_NAME():
    if on_development_server or on_integration_server or not on_server:
        return 'skykit-display-device-int'
    if on_production_server:
        return 'skykit-display-device'
    return None


app_APP_NAME = _APP_NAME()


def _SECRET_KEY_FILE():
    return '{}/privatekeys/{}.pem'.format(app_APP_ROOT, app_APP_NAME)


app_SECRET_KEY_FILE = _SECRET_KEY_FILE()


def _PRIVATE_KEY():
    with open(app_SECRET_KEY_FILE) as f:
        private_key = f.read()
    return private_key


app_PRIVATE_KEY = _PRIVATE_KEY()


def _SERVICE_ACCOUNT_EMAIL():
    if on_development_server or on_integration_server or not on_server:
        return '390010375778-87capuus77kispm64q27iah4kl0rorv4@developer.gserviceaccount.com'
    if on_production_server:
        return ''
    return None


app_SERVICE_ACCOUNT_EMAIL = _SERVICE_ACCOUNT_EMAIL()


def _CLIENT_ID():
    if on_development_server or not on_server:
        return '390010375778-87capuus77kispm64q27iah4kl0rorv4.apps.googleusercontent.com'
    if on_integration_server:
        return '390010375778-87capuus77kispm64q27iah4kl0rorv4.apps.googleusercontent.com'
    if on_production_server:
        return ''
    return None


app_CLIENT_ID = _CLIENT_ID()

# def _CLIENT_SECRET():
#     if on_development_server or not on_server:
#         return '5uw_Cj78Iygf3rfnJKZ_SVVO'
#     if on_integration_server:
#         return 'h-PGaqnkAfRhjVTtbxcgSLD5'
#     if on_production_server:
#         return 'NWCFk0IyE8QPqD2CDwloKvjH'
#     return None
# app_CLIENT_SECRET = _CLIENT_SECRET()

def _PUBLIC_API_SERVER_KEY():
    if on_development_server or not on_server:
        return 'AIzaSyAzS-hwl5dV-Wn4g5opG_34gGYplgJT1Fc'
    if on_integration_server:
        return 'AIzaSyAzS-hwl5dV-Wn4g5opG_34gGYplgJT1Fc'
    if on_production_server:
        return ''
    return None


app_PUBLIC_API_SERVER_KEY = _PUBLIC_API_SERVER_KEY()


def _API_TOKEN():
    return '6C346588BD4C6D722A1165B43C51C'

app_API_TOKEN = _API_TOKEN()
