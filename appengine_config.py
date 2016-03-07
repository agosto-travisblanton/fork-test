"""
The configuration file used by :py:mod:`agar.config` implementations and other libraries using the
`google.appengine.api.lib_config`_ configuration library. Configuration overrides go in this file.
"""
from env_setup import setup
setup()

import os
from provisioning_env import (
    on_production_server,
    on_stage_server,
    on_development_server,
    on_integration_server,
    on_gamestop_server,
    on_server,
    on_test_harness)
from agar.env import appid


##############################################################################
# APPLICATION SETTINGS
##############################################################################

def _APP_ROOT():
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


app_APP_ROOT = _APP_ROOT()


def _APP_NAME():
    if on_development_server or on_integration_server or not on_server:
        return 'skykit-display-device-int'
    else:
        return appid


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
    elif on_stage_server:
        return 'service-247@skykit-provisioning-stage.iam.gserviceaccount.com'
    elif on_gamestop_server:
        return 'service@skykit-provisioning-gamestop.iam.gserviceaccount.com'
    elif on_production_server:
        return '613606096818-3hehucjfgbtj56pu8dduuo36uccccen0@developer.gserviceaccount.com'
    else:
        raise EnvironmentError('Unknown environment for SERVICE_ACCOUNT_EMAIL in appengine_config.py')
    return None


app_SERVICE_ACCOUNT_EMAIL = _SERVICE_ACCOUNT_EMAIL()


def _GCM_TEST_MODE():
    if on_development_server or not on_server:
        return True
    else:
        return False


app_GCM_TEST_MODE = _GCM_TEST_MODE()


# This is the Service Account CLIENT_ID
def _CLIENT_ID():
    if on_development_server or not on_server:
        return '390010375778-87capuus77kispm64q27iah4kl0rorv4.apps.googleusercontent.com'
    elif on_integration_server:
        return '390010375778-87capuus77kispm64q27iah4kl0rorv4.apps.googleusercontent.com'
    elif on_stage_server:
        return '106935685560101973796'
    elif on_gamestop_server:
        return '281350297105-9pc7cpa4chi8je9j0vp6ko4au99931rj.apps.googleusercontent.com'
    elif on_production_server:
        return '613606096818-3hehucjfgbtj56pu8dduuo36uccccen0.apps.googleusercontent.com'
    else:
        raise EnvironmentError('Unknown environment for CLIENT_ID in appengine_config.py')
    return None


app_CLIENT_ID = _CLIENT_ID()


# This is the OAuth 2 Web Client CLIENT_ID
def _OAUTH_CLIENT_ID():
    if on_development_server or not on_server:
        return '390010375778-gidaqujfhgkqrc5lat9t890mhc0nhutt.apps.googleusercontent.com'
    elif on_integration_server:
        return '390010375778-gidaqujfhgkqrc5lat9t890mhc0nhutt.apps.googleusercontent.com'
    elif on_stage_server:
        return '1087929808190-q8s9bhpu79ju7fkqblnl3nn2th0efv57.apps.googleusercontent.com'
    elif on_gamestop_server:
        return '281350297105-9pc7cpa4chi8je9j0vp6ko4au99931rj.apps.googleusercontent.com'
    elif on_production_server:
        return '613606096818-tfkv6eedbrbc4hltamdjgc7nk25k37mk.apps.googleusercontent.com'
    else:
        raise EnvironmentError('Unknown environment for OAUTH_CLIENT_ID in appengine_config.py')
    return None


app_OAUTH_CLIENT_ID = _OAUTH_CLIENT_ID()


# def _CLIENT_SECRET():
#     if on_development_server or not on_server:
#         return '5uw_Cj78Iygf3rfnJKZ_SVVO'
#     if on_integration_server:
#         return 'h-PGaqnkAfRhjVTtbxcgSLD5'
#     if on_stage_server:
#         return 'SkT2kDa3nViHTJXLuUYbSbzE'
#     if on_gamestop_server:
#         return 'H-RgqzSYZps7auL9tB9RFXZG'
#     if on_production_server:
#         return 'NWCFk0IyE8QPqD2CDwloKvjH'
#     return None
# app_CLIENT_SECRET = _CLIENT_SECRET()

def _PUBLIC_API_SERVER_KEY():
    if on_development_server or not on_server:
        return 'AIzaSyAzS-hwl5dV-Wn4g5opG_34gGYplgJT1Fc'
    elif on_integration_server:
        return 'AIzaSyAzS-hwl5dV-Wn4g5opG_34gGYplgJT1Fc'
    elif on_stage_server:
        return 'AIzaSyB0mE3DWNt8iFFvZ60TQyTgl3NpKK6-BQA'
    elif on_gamestop_server:
        return 'AIzaSyDvysZi67-oEJnlbJv-EWqme-mNdSI1qD0'
    elif on_production_server:
        return 'AIzaSyBcZQf7qcJibJmBKHDaqgdRwf2XQ3MZFiY'
    else:
        raise EnvironmentError('Unknown environment for PUBLIC_API_SERVER_KEY in appengine_config.py')
    return None


app_PUBLIC_API_SERVER_KEY = _PUBLIC_API_SERVER_KEY()


def _API_TOKEN():
    if on_development_server or not on_server:
        return '6C346588BD4C6D722A1165B43C51C'
    elif on_integration_server:
        return '6C346588BD4C6D722A1165B43C51C'
    elif on_stage_server:
        return '6C346588BD4C6D722A1165B43C51C'
    elif on_gamestop_server:
        return '5XZHBF3mOwqJlYAlG1NeeWX0Cb72g'
    elif on_production_server:
        return '6C346588BD4C6D722A1165B43C51C'
    else:
        raise EnvironmentError('Unknown environment for API_TOKEN in appengine_config.py')
    return None


app_API_TOKEN = _API_TOKEN()


def _UNMANAGED_API_TOKEN():
    if on_development_server or not on_server:
        return 'A1365B43C51C46588BD4C6D5016C0'
    elif on_integration_server:
        return 'A1365B43C51C46588BD4C6D5016C0'
    elif on_stage_server:
        return 'A1365B43C51C46588BD4C6D5016C0'
    elif on_gamestop_server:
        return 'A1365B43C51C46588BD4C6D5016C0'
    elif on_production_server:
        return 'A1365B43C51C46588BD4C6D5016C0'
    else:
        raise EnvironmentError('Unknown environment for UNMANAGED_API_TOKEN in appengine_config.py')
    return None


app_UNMANAGED_API_TOKEN = _UNMANAGED_API_TOKEN()


def _UNMANAGED_REGISTRATION_TOKEN():
    if on_development_server or not on_server:
        return '43C51C8BD4C6D723A1365B6C34658'
    elif on_integration_server:
        return '43C51C8BD4C6D723A1365B6C34658'
    elif on_stage_server:
        return '43C51C8BD4C6D723A1365B6C34658'
    elif on_gamestop_server:
        return '43C51C8BD4C6D723A1365B6C34658'
    elif on_production_server:
        return '43C51C8BD4C6D723A1365B6C34658'
    else:
        raise EnvironmentError('Unknown environment for UNMANAGED_REGISTRATION_TOKEN in appengine_config.py')
    return None


app_UNMANAGED_REGISTRATION_TOKEN = _UNMANAGED_REGISTRATION_TOKEN()


def _CONTENT_MANAGER_API_SERVER_KEY():
    if on_development_server or not on_server:
        return 'EqwbumxWrJzybkDerDbm9yLBteJqZi7X'
    elif on_integration_server:
        return 'EqwbumxWrJzybkDerDbm9yLBteJqZi7X'
    elif on_stage_server:
        return 'OTJkMGNjMmYzMmZlNjI4MDVmNGVlMjEx'
    elif on_gamestop_server:
        return '???'
    elif on_production_server:
        return 'uXyQWMr3mAUvLFhvYuzYnfehkKop7ZCe'
    else:
        raise EnvironmentError('Unknown environment for CONTENT_MANAGER_API_SERVER_KEY in appengine_config.py')
    return None


app_CONTENT_MANAGER_API_SERVER_KEY = _CONTENT_MANAGER_API_SERVER_KEY()


def _DEFAULT_AGOSTO_DEVICE_DOMAIN():
    if on_development_server or not on_server:
        return 'local.agosto.com'
    elif on_integration_server:
        return 'dev.agosto.com'
    elif on_stage_server:
        return 'devstaging.skykit.com'
    elif on_gamestop_server:
        return '???'
    elif on_production_server:
        return 'skykit.agosto.com'
    else:
        raise EnvironmentError('Unknown environment for DEFAULT_AGOSTO_DEVICE_DOMAIN in appengine_config.py')
    return None


app_DEFAULT_AGOSTO_DEVICE_DOMAIN = _DEFAULT_AGOSTO_DEVICE_DOMAIN()


def _GOOGLE_CUSTOMER_ID():
    if on_development_server or not on_server:
        return 'my_customer'
    elif on_integration_server:
        return 'my_customer'
    elif on_stage_server:
        return 'my_customer'
    elif on_gamestop_server:
        return 'my_customer'
    elif on_production_server:
        return 'my_customer'
    else:
        raise EnvironmentError('Unknown environment for GOOGLE_CUSTOMER_ID in appengine_config.py')
    return None


app_GOOGLE_CUSTOMER_ID = _GOOGLE_CUSTOMER_ID()


def _PLAYER_UNRESPONSIVE_SECONDS_THRESHOLD():
    return 300  # 300 seconds = 5 minutes


app_PLAYER_UNRESPONSIVE_SECONDS_THRESHOLD = _PLAYER_UNRESPONSIVE_SECONDS_THRESHOLD()


def _DEVICE_SWEEP_PAGING_SIZE():
    return 500


app_DEVICE_SWEEP_PAGING_SIZE = _DEVICE_SWEEP_PAGING_SIZE()


def _DEVICE_ISSUE_PLAYER_DOWN():
    return 'Player down'


app_DEVICE_ISSUE_PLAYER_DOWN = _DEVICE_ISSUE_PLAYER_DOWN()


def _DEVICE_ISSUE_PLAYER_UP():
    return 'Player up'


app_DEVICE_ISSUE_PLAYER_UP = _DEVICE_ISSUE_PLAYER_UP()


def _DEVICE_ISSUE_FIRST_HEARTBEAT():
    return 'First heartbeat'


app_DEVICE_ISSUE_FIRST_HEARTBEAT = _DEVICE_ISSUE_FIRST_HEARTBEAT()


def _DEVICE_ISSUE_PLAYER_VERSION_CHANGE():
    return 'Skykit version change'


app_DEVICE_ISSUE_PLAYER_VERSION_CHANGE = _DEVICE_ISSUE_PLAYER_VERSION_CHANGE()


def _DEVICE_ISSUE_TIMEZONE_CHANGE():
    return 'Timezone change'


app_DEVICE_ISSUE_TIMEZONE_CHANGE = _DEVICE_ISSUE_TIMEZONE_CHANGE()


def _DEVICE_ISSUE_OS_CHANGE():
    return 'OS change'


app_DEVICE_ISSUE_OS_CHANGE = _DEVICE_ISSUE_OS_CHANGE()


def _DEVICE_ISSUE_OS_VERSION_CHANGE():
    return 'OS version change'


app_DEVICE_ISSUE_OS_VERSION_CHANGE = _DEVICE_ISSUE_OS_VERSION_CHANGE()


def _DEVICE_ISSUE_MEMORY_HIGH():
    return 'Memory usage high'


app_DEVICE_ISSUE_MEMORY_HIGH = _DEVICE_ISSUE_MEMORY_HIGH()


def _DEVICE_ISSUE_MEMORY_NORMAL():
    return 'Memory normal'


app_DEVICE_ISSUE_MEMORY_NORMAL = _DEVICE_ISSUE_MEMORY_NORMAL()


def _DEVICE_ISSUE_STORAGE_LOW():
    return 'Storage available low'


app_DEVICE_ISSUE_STORAGE_LOW = _DEVICE_ISSUE_STORAGE_LOW()


def _DEVICE_ISSUE_STORAGE_NORMAL():
    return 'Storage normal'


app_DEVICE_ISSUE_STORAGE_NORMAL = _DEVICE_ISSUE_STORAGE_NORMAL()


def _STORAGE_UTILIZATION_THRESHOLD():
    return 90


app_STORAGE_UTILIZATION_THRESHOLD = _STORAGE_UTILIZATION_THRESHOLD()


def _MEMORY_UTILIZATION_THRESHOLD():
    return 90


app_MEMORY_UTILIZATION_THRESHOLD = _MEMORY_UTILIZATION_THRESHOLD()


def _LATEST_DEVICE_ISSUES_FETCH_COUNT():
    return 250


app_LATEST_DEVICE_ISSUES_FETCH_COUNT = _LATEST_DEVICE_ISSUES_FETCH_COUNT()


def _PLAYER_RESET_COMMAND():
    return 'skykit.com/skdchromeapp/reset'


app_PLAYER_RESET_COMMAND = _PLAYER_RESET_COMMAND()


def _PLAYER_VOLUME_COMMAND():
    return 'skykit.com/skdchromeapp/volume/'


app_PLAYER_VOLUME_COMMAND = _PLAYER_VOLUME_COMMAND()


def _PLAYER_POWER_ON_COMMAND():
    return 'skykit.com/skdchromeapp/tv/on'


app_PLAYER_POWER_ON_COMMAND = _PLAYER_POWER_ON_COMMAND()


def _PLAYER_POWER_OFF_COMMAND():
    return 'skykit.com/skdchromeapp/tv/off'


app_PLAYER_POWER_OFF_COMMAND = _PLAYER_POWER_OFF_COMMAND()


def _PLAYER_DELETE_CONTENT_COMMAND():
    return 'skykit.com/skdchromeapp/content/delete'


app_PLAYER_DELETE_CONTENT_COMMAND = _PLAYER_DELETE_CONTENT_COMMAND()


def _PLAYER_HEARTBEAT_INTERVAL_MINUTES():
    return 2


app_PLAYER_HEARTBEAT_INTERVAL_MINUTES = _PLAYER_HEARTBEAT_INTERVAL_MINUTES()


def _CHECK_FOR_CONTENT_INTERVAL_MINUTES():
    return 1


app_CHECK_FOR_CONTENT_INTERVAL_MINUTES = _CHECK_FOR_CONTENT_INTERVAL_MINUTES()

def _ETHERNET_CONNECTION():
    return 'Ethernet'


app_ETHERNET_CONNECTION = _ETHERNET_CONNECTION()


def _WIFI_CONNECTION():
    return 'WiFi'


app_WIFI_CONNECTION = _WIFI_CONNECTION()


def _DEFAULT_CONTENT_MANAGER_URL():
    if on_development_server or not on_server:
        return 'https://skykit-contentmanager-int.appspot.com'
    elif on_integration_server:
        return 'https://skykit-contentmanager-int.appspot.com'
    elif on_stage_server:
        return 'https://skykit-contentmanager-stage.appspot.com'
    elif on_gamestop_server:
        return 'https://skykit-contentmanager-gamestop.appspot.com'
    elif on_production_server:
        return 'https://skykit-contentmanager.appspot.com'
    else:
        raise EnvironmentError('Unknown environment for DEFAULT_CONTENT_MANAGER_URL in appengine_config.py')
    return None


app_DEFAULT_CONTENT_MANAGER_URL = _DEFAULT_CONTENT_MANAGER_URL()


def _DEFAULT_PLAYER_CONTENT_URL():
    return '{}/content'.format(app_DEFAULT_CONTENT_MANAGER_URL)


app_DEFAULT_PLAYER_CONTENT_URL = _DEFAULT_PLAYER_CONTENT_URL()


def _STORMPATH_CLIENT():
    """
    http://docs.stormpath.com/python/quickstart/#create-a-client
    """
    if on_test_harness or on_development_server or on_integration_server or on_stage_server or on_gamestop_server:
        id = '6VYRY6TL26YRBJOAOO533W6DO'
        secret = 'oc4u1Nm0M5p3vJSOENhPZzAhNfzifAxMQS0v3J/kG/U'
    elif on_production_server:
        id = 'IY5YOGP105D4HGY07GK2IT62X'
        secret = '8jPFs33PKDFuAz++gDeokLO7zAyfi1LSciL9xL0tEJk'
    else:
        raise EnvironmentError("Unknown environment for Stormpath: {} in appengine_config.py".format(appid))

    api_key = {
        'id': id,
        'secret': secret
    }

    # NOTE: must use scheme='basic' - only one that works on GAE
    from stormpath.client import Client
    return Client(api_key=api_key, scheme='basic')


app_STORMPATH_CLIENT = _STORMPATH_CLIENT()


def _STORMPATH_AUTH_APP():
    return appid


app_STORMPATH_AUTH_APP = _STORMPATH_AUTH_APP()

webapp2_extras_sessions_secret_key = '94eda847-0ea9-4f49-b96c-1434ec318563'


##############################################################################
# MAIL SETTINGS
##############################################################################

def _MAIL_API_KEY():
    return "key-7g5zunub4weun65nb9aop2kcsgher-l0"


app_MAIL_API_KEY = _MAIL_API_KEY()


def _MAIL_MESSAGES_URL():
    return "https://api.mailgun.net/v3/skykit.com/messages"


app_MAIL_MESSAGES_URL = _MAIL_MESSAGES_URL()


def _MAIL_EVENTS_URL():
    return "https://api.mailgun.net/v3/skykit.com/events"


app_MAIL_EVENTS_URL = _MAIL_EVENTS_URL()


def _MAIL_FROM():
    return "Skykit Provisioning <noreply-provisioning@skykit.com>"


app_MAIL_FROM = _MAIL_FROM()


def _EMAIL_SUPPORT():
    if on_development_server or not on_server:
        return True
    elif on_integration_server:
        return True
    elif on_stage_server:
        return True
    elif on_gamestop_server:
        return True
    elif on_production_server:
        return True
    else:
        raise EnvironmentError('Unknown environment for EMAIL_SUPPORT in appengine_config.py')
    return None


app_EMAIL_SUPPORT = _EMAIL_SUPPORT()


def _SQLALCHEMY_DATABASE_URI():
    # the second arg after : is the db instance name
    if on_test_harness:
        db_uri = 'sqlite:///:memory:'
    elif on_development_server:
        db_uri = 'mysql+mysqldb://root@localhost/provisioning'
    else:
        if on_integration_server:
            instance_name = 'provisioning-int'
        elif on_stage_server:
            instance_name = 'provisioning-stage'
        elif on_gamestop_server:
            instance_name = 'provisioning-gamestop'
        elif on_production_server:
            instance_name = 'provisioning-prod'
        else:
            instance_name = None

        assert instance_name is not None, "Unknown environment"

        # "provisioning" is the database name
        db_uri = "mysql+mysqldb://root@/provisioning?unix_socket=/cloudsql/{}:{}".format(appid, instance_name)
    return db_uri


proofplay_SQLALCHEMY_DATABASE_URI = _SQLALCHEMY_DATABASE_URI()


##############################################################################
# VERSION  sprint_number.deployment_increment.hotfix_increment e.g., 30.1.0
##############################################################################
def _SPRINT_NUMBER():
    return 31


app_SPRINT_NUMBER = _SPRINT_NUMBER()


def _DEPLOYMENT_COUNTER():
    return 4


app_DEPLOYMENT_COUNTER = _DEPLOYMENT_COUNTER()


def _PRODUCTION_HOTFIX_COUNTER():
    return 0


app_PRODUCTION_HOTFIX_COUNTER = _PRODUCTION_HOTFIX_COUNTER()
