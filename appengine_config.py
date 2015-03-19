"""
The configuration file used by :py:mod:`agar.config` implementations and other libraries using the
`google.appengine.api.lib_config`_ configuration library. Configuration overrides go in this file.
"""
from env_setup import setup
setup()

import re
import os
import json

from agar.env import on_development_server, on_integration_server, on_server, appid
from goodyear_env import on_stage_server, on_production_server

##############################################################################
# AGAR SETTINGS
##############################################################################

# Root level WSGI application modules that 'agar.url.uri_for()' will search
agar_url_APPLICATIONS = ['main']

##############################################################################
# APPSTATS SETTINGS
##############################################################################

appstats_SHELL_OK = on_development_server or on_integration_server

##############################################################################
# GOODYEAR BACK OFFICE SETTINGS
##############################################################################

def _MAILGUN_APIKEY():
    return "key-7g5zunub4weun65nb9aop2kcsgher-l0"
app_MAILGUN_APIKEY = _MAILGUN_APIKEY()


def _MAILGUN_MESSAGES_URL():
    return "https://api.mailgun.net/v2/skykit.com/messages"
app_MAILGUN_MESSAGES_URL = _MAILGUN_MESSAGES_URL()


def _MAILGUN_STATS_URL():
    return "https://api.mailgun.net/v2/skykit.com/stats"
app_MAILGUN_STATS_URL = _MAILGUN_STATS_URL()


def _STORMPATH_APIKEY_ID():
    if on_development_server or not on_server:
        return '1WHC80QIP2X8AGZEUZZ0UAQ2R'
    elif on_integration_server:
        return '1WHC80QIP2X8AGZEUZZ0UAQ2R'
    elif on_stage_server:
        return '3IE3EU7FQ2Z2CVL0TUJSLCF98'
    elif on_production_server:
        return '2N1XDW0UNIA5CNH1YXHMY1ATK'
    return None
app_STORMPATH_APIKEY_ID = _STORMPATH_APIKEY_ID()


def _STORMPATH_APIKEY_SECRET():
    if on_development_server or not on_server:
        return 'QHcw92sQ8x8JNwsDkkxQ7hPN5S/BeZLj4iJiNLZm5RQ'
    elif on_integration_server:
        return 'QHcw92sQ8x8JNwsDkkxQ7hPN5S/BeZLj4iJiNLZm5RQ'
    elif on_stage_server:
        return 'EC/3HBpXTuxCkmSihVtUV15YPzlx37KtW4K406tMvLg'
    elif on_production_server:
        return 'DPC5+qhGGTG0zGZj/omFNqcw2VeV0YeN3xxW8ihrAZs'
    return None
app_STORMPATH_APIKEY_SECRET = _STORMPATH_APIKEY_SECRET()


def _STORMPATH_AUTH_APP():
    if on_development_server or not on_server:
        return 'goodyear-smart-tire-int'
    elif on_integration_server:
        return 'goodyear-smart-tire-int'
    elif on_stage_server:
        return 'goodyear-smart-tire-stage'
    elif on_production_server:
        return 'proactiveservices'
    return None
app_STORMPATH_AUTH_APP = _STORMPATH_AUTH_APP()


def _BOOTSTRAP_SPREADSHEET_KEY():
    if on_production_server or on_stage_server:
        return '17clcJsGrvnUOu5KHxwRMTHO6vUpu-nn3XgPQTGiR8dk'
    else:
        return '1gEOD2dMtQqYjP5NGQeSkUaF7vM9u2tOdaW_BRW2598o'
app_BOOTSTRAP_SPREADSHEET_KEY = _BOOTSTRAP_SPREADSHEET_KEY()


def _BOOTSTRAP_SPREADSHEET_USER():
    return 'devadmin@demo.agosto.com'
app_BOOTSTRAP_SPREADSHEET_USER = _BOOTSTRAP_SPREADSHEET_USER()


def _BOOTSTRAP_SPREADSHEET_PASSWORD():
    return 'ag0st01234'
app_BOOTSTRAP_SPREADSHEET_PASSWORD = _BOOTSTRAP_SPREADSHEET_PASSWORD()


def _BUCKET_NAME():
    if not on_server:
        return 'testbed-test'
    else:
        from google.appengine.api.app_identity import get_default_gcs_bucket_name

        return get_default_gcs_bucket_name()
app_BUCKET_NAME = _BUCKET_NAME()


def _IMAGE_DOMAIN():
    if on_development_server:
        return "https://localhost:8080"
    else:
        return "https://{}.appspot.com".format(appid)
app_IMAGE_DOMAIN = _IMAGE_DOMAIN()


def _MAPS_API_KEY():
    if not on_server or on_integration_server or on_development_server:
        return 'AIzaSyDi8UdS0E3ypetlHaQY3_jMJTpQHhrwv8A'
    elif on_stage_server:
        return 'AIzaSyD0HxUp2XSm3IBrXcR_XIqyOaIcVQAy6IE'
    elif on_production_server or on_server:
        return 'AIzaSyATR1HEXi2c-NQKiC2l5sSqUV_3B0cPkBE'
app_MAPS_API_KEY = _MAPS_API_KEY()

"""
EMAIL TESTING: The easiest way to test emails is with the following command:

    TEST_EMAIL=1 python manage.py test -p test_email.py

The email address to send test emails will be auto-detected by parsing the output of "hg config ui.username".

Alternatively, the email address can be explicitly specified using the following:

    TEST_EMAIL_ADDRESS="karl.kroening@agosto.com" python manage.py test -p test_email.py

Finally, if you're against setting environment variables (for whatever reason) the settings for EMAIL_SUPPORT and
TEST_EMAIL_ADDRESS can just be hardcoded below.
"""


def _EMAIL_SUPPORT():
    if on_server:
        return True
    elif 'TEST_EMAIL' in os.environ:
        return bool(int(os.environ['TEST_EMAIL']))
    elif 'TEST_EMAIL_ADDRESS' in os.environ:
        return True
    else:
        return False  # Change for testing if desired.
app_EMAIL_SUPPORT = _EMAIL_SUPPORT()


def _TEST_EMAIL_ADDRESS():
    if on_development_server or not on_server:  # tests are 'not on_server' when run in PyCharm
        email = 'test@localhost'  # Change for testing if desired.
        if 'TEST_EMAIL_ADDRESS' in os.environ:
            email = os.environ['TEST_EMAIL_ADDRESS']
        elif app_EMAIL_SUPPORT:
            # will blow up if you don't have the module installed on your local SDK
            from subprocess import Popen, PIPE

            try:
                cmd_output = Popen(['hg', 'config', 'ui.username'], stdout=PIPE).communicate()[0]
                match = re.match('.*<(.*)>\n', cmd_output)
                if match is not None:
                    email = match.group(1)
            except:
                pass
    else:
        email = None
    return email
app_TEST_EMAIL_ADDRESS = _TEST_EMAIL_ADDRESS()


def _SERVICE_CLIENT_SECRETS_PATH():
    if on_stage_server:
        return os.path.join(os.path.dirname(__file__), "csdata/service_stage.json")
    elif on_production_server:
        return os.path.join(os.path.dirname(__file__), "csdata/service_prod.json")
    else:
        return os.path.join(os.path.dirname(__file__), "csdata/service_int.json")
app_SERVICE_CLIENT_SECRETS_PATH = _SERVICE_CLIENT_SECRETS_PATH()

with open(_SERVICE_CLIENT_SECRETS_PATH()) as file:
    service_secrets = json.loads(file.read())


def _SERVICE_PRIVATE_KEY():
    return service_secrets['private_key']
app_SERVICE_PRIVATE_KEY = _SERVICE_PRIVATE_KEY()


def _SERVICE_CLIENT_EMAIL():
    return service_secrets['client_email']
app_SERVICE_CLIENT_EMAIL = _SERVICE_CLIENT_EMAIL()


def _APP_ROOT():
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
app_APP_ROOT = _APP_ROOT()


def _ROUTER_HOST():
    if on_development_server:
        host = 'http://localhost:9090'
    elif on_integration_server:
        host = 'https://proactiveservices-router-int.appaspot.com'
    else:
        host = 'https://proactiveservices-router.appspot.com'
    return host
app_ROUTER_HOST = _ROUTER_HOST()


def _ROUTER_STATS_URL():
    return "{}/monitor/stats".format(app_ROUTER_HOST)
app_ROUTER_STATS_URL = _ROUTER_STATS_URL()


def _RAW_FOREIGN_DOC_URL():
    return "{}/raw-foreign-event-document".format(app_ROUTER_HOST)
app_RAW_FOREIGN_DOC_URL = _RAW_FOREIGN_DOC_URL()


def _WHEEL_SCHEMATIC_PREFIX_GCS():
    return "wheel_schematics"
app_WHEEL_SCHEMATIC_PREFIX_GCS = _WHEEL_SCHEMATIC_PREFIX_GCS()


def _PA_DATETIME_FORMAT():
    return '%m/%d/%Y %I:%M %p'
app_PA_DATETIME_FORMAT = _PA_DATETIME_FORMAT()


def _PA_TIME_INTERVAL_MINUTES():
    return 300
app_PA_TIME_INTERVAL_MINUTES = _PA_TIME_INTERVAL_MINUTES()


def _PA_TIME_INTERVAL_LOOKBACK_HOUR():
    return 1
app_PA_TIME_INTERVAL_LOOKBACK_HOUR = _PA_TIME_INTERVAL_LOOKBACK_HOUR()


def _PA_MIN_NUMBER_EVENTS():
    return 50
app_PA_MIN_NUMBER_EVENTS = _PA_MIN_NUMBER_EVENTS()


def _FLEET_HQ_ENDPOINT():
    # return 'http://9ec91e68cd5d4b2aa7bd61b9475db25d.cloudapp.net/GyFleethqServices.svc/GyFleethqServices.svc'
    return 'http://529675a87ba34c808782ae0c5de94893.cloudapp.net/GyFleethqServices.svc/GyFleethqServices.svc'
app_FLEET_HQ_ENDPOINT = _FLEET_HQ_ENDPOINT()

webapp2_extras_sessions_secret_key = 'ecf3v90700L38586v138g2O90mkSI9R1'


def webapp2_extras_sessions_cookie_args():
    cookie_args = {
        'max_age': None,
        'domain': None,
        'secure': False,
        'httponly': True,
        'path': '/'
    }
    if on_development_server:
        cookie_args['secure'] = False
    return cookie_args
webapp2_extras_sessions_cookie_args = webapp2_extras_sessions_cookie_args()


def webapp_add_wsgi_middleware(app):
    from google.appengine.ext.appstats import recording

    app = recording.appstats_wsgi_middleware(app)
    return app
# Encode/Decode functions for filtering queries on db.Key fields in mapreduce
from mapreduce import model
from mapreduce.lib.pipeline import util
from google.appengine.ext import db


def _JsonEncodeDbKey(o):
    """Json encode an db.Key object."""
    return {'db_key_string': str(o)}


def _JsonDecodeDbKey(d):
    """Json decode a ndb.Key object."""
    return db.Key(encoded=d['db_key_string'])


model.JSON_DEFAULTS[db.Key] = (_JsonEncodeDbKey, _JsonDecodeDbKey)
model._TYPE_IDS['Key'] = db.Key

util.JSON_DEFAULTS[db.Key] = (_JsonEncodeDbKey, _JsonDecodeDbKey)
util._TYPE_IDS['Key'] = db.Key
