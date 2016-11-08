"""
The configuration file used by :py:mod:`agar.config` implementations and other libraries using the
`google.appengine.api.lib_config`_ configuration library. Configuration overrides go in this file.
"""
from env_setup import setup

setup()

import os
from provisioning_env import (
    on_continuous_integration_server,
    on_development_server,
    on_gamestop_server,
    on_integration_server,
    on_production_server,
    on_qa_server,
    on_server,
    on_stage_server,
    on_test_harness,
)
from agar.env import appid
from os import path
import yaml

basedir = path.abspath(path.dirname(__file__))

##############################################################################
# APPLICATION SETTINGS
##############################################################################

app_APP_ROOT = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def _APP_NAME():
    if on_development_server or on_integration_server or not on_server:
        return 'skykit-display-device-int'
    else:
        return appid


app_APP_NAME = _APP_NAME()

app_SECRET_KEY_FILE = '{}/privatekeys/{}.pem'.format(app_APP_ROOT, app_APP_NAME)


def _PRIVATE_KEY():
    with open(app_SECRET_KEY_FILE) as f:
        private_key = f.read()
    return private_key


app_PRIVATE_KEY = _PRIVATE_KEY()


def _SERVICE_ACCOUNT_EMAIL():
    if on_development_server or on_integration_server or not on_server:
        return '390010375778-87capuus77kispm64q27iah4kl0rorv4@developer.gserviceaccount.com'
    elif on_continuous_integration_server:
        return '133313126637-compute@developer.gserviceaccount.com'
    elif on_qa_server:
        # return '465572156911-compute@developer.gserviceaccount.com'
        return 'service@skykit-provisioning-qa.iam.gserviceaccount.com'
    elif on_stage_server:
        return 'service-247@skykit-provisioning-stage.iam.gserviceaccount.com'
    elif on_gamestop_server:
        return '613606096818-3hehucjfgbtj56pu8dduuo36uccccen0@developer.gserviceaccount.com'
    elif on_production_server:
        return '613606096818-3hehucjfgbtj56pu8dduuo36uccccen0@developer.gserviceaccount.com'
    else:
        raise EnvironmentError('Unknown environment for SERVICE_ACCOUNT_EMAIL in appengine_config.py')


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
    elif on_continuous_integration_server:
        return '100882018913058557387'
    elif on_qa_server:
        return '117032486283237201955'
    elif on_stage_server:
        return '106935685560101973796'
    elif on_gamestop_server:
        return '613606096818-3hehucjfgbtj56pu8dduuo36uccccen0.apps.googleusercontent.com'
    elif on_production_server:
        return '613606096818-3hehucjfgbtj56pu8dduuo36uccccen0.apps.googleusercontent.com'
    else:
        raise EnvironmentError('Unknown environment for CLIENT_ID in appengine_config.py')


app_CLIENT_ID = _CLIENT_ID()


# This is the OAuth 2 Web Client CLIENT_ID
def _OAUTH_CLIENT_ID():
    if on_development_server or not on_server:
        return '390010375778-gidaqujfhgkqrc5lat9t890mhc0nhutt.apps.googleusercontent.com'
    elif on_integration_server:
        return '390010375778-gidaqujfhgkqrc5lat9t890mhc0nhutt.apps.googleusercontent.com'
    elif on_continuous_integration_server:
        return '133313126637-u5ibnd3a4chjkhlva9i1asfi21vbbb1k.apps.googleusercontent.com'
    elif on_qa_server:
        return '465572156911-g1n43vdlpi3h225k1s1n3r7aiopucmvq.apps.googleusercontent.com'
    elif on_stage_server:
        return '1087929808190-q8s9bhpu79ju7fkqblnl3nn2th0efv57.apps.googleusercontent.com'
    elif on_gamestop_server:
        return '281350297105-9pc7cpa4chi8je9j0vp6ko4au99931rj.apps.googleusercontent.com'
    elif on_production_server:
        return '613606096818-tfkv6eedbrbc4hltamdjgc7nk25k37mk.apps.googleusercontent.com'
    else:
        raise EnvironmentError('Unknown environment for OAUTH_CLIENT_ID in appengine_config.py')


app_OAUTH_CLIENT_ID = _OAUTH_CLIENT_ID()


# def _CLIENT_SECRET():
#     if on_development_server or not on_server:
#         return '5uw_Cj78Iygf3rfnJKZ_SVVO'
#     if on_integration_server:
#         return 'h-PGaqnkAfRhjVTtbxcgSLD5'
#     if on_continuous_integration_server:
#         return 'DaHz9u5ldHlLkseLTxJvWYj0'
#     if on_qa_server:
#         return 'U5dxJM6B6rXG57l4ZSPCxnVk'
#     if on_stage_server:
#         return 'SkT2kDa3nViHTJXLuUYbSbzE'
#     if on_gamestop_server:
#         return 'H-RgqzSYZps7auL9tB9RFXZG'
#     if on_production_server:
#         return 'NWCFk0IyE8QPqD2CDwloKvjH'
#
# app_CLIENT_SECRET = _CLIENT_SECRET()

def _PUBLIC_API_SERVER_KEY():
    if on_development_server or not on_server:
        return 'AIzaSyAzS-hwl5dV-Wn4g5opG_34gGYplgJT1Fc'
    elif on_integration_server:
        return 'AIzaSyAzS-hwl5dV-Wn4g5opG_34gGYplgJT1Fc'
    elif on_continuous_integration_server:
        return 'AIzaSyBkqqGLYZUUdOXQ1yte7S27R-nY5h3BSgM'
    elif on_qa_server:
        return 'AIzaSyDpUtlntmN0AxPXvZo-wvnkWo6-fwN6AN0'
    elif on_stage_server:
        return 'AIzaSyB0mE3DWNt8iFFvZ60TQyTgl3NpKK6-BQA'
    elif on_gamestop_server:
        return 'AIzaSyDvysZi67-oEJnlbJv-EWqme-mNdSI1qD0'
    elif on_production_server:
        return 'AIzaSyBcZQf7qcJibJmBKHDaqgdRwf2XQ3MZFiY'
    else:
        raise EnvironmentError('Unknown environment for PUBLIC_API_SERVER_KEY in appengine_config.py')


app_PUBLIC_API_SERVER_KEY = _PUBLIC_API_SERVER_KEY()


def _API_TOKEN():
    if on_development_server or not on_server:
        return '6C346588BD4C6D722A1165B43C51C'
    elif on_integration_server:
        return '6C346588BD4C6D722A1165B43C51C'
    elif on_continuous_integration_server:
        return '6C346588BD4C6D722A1165B43C51C'
    elif on_qa_server:
        return '6C346588BD4C6D722A1165B43C51C'
    elif on_stage_server:
        return '6C346588BD4C6D722A1165B43C51C'
    elif on_gamestop_server:
        return '5XZHBF3mOwqJlYAlG1NeeWX0Cb72g'
    elif on_production_server:
        return '6C346588BD4C6D722A1165B43C51C'
    else:
        raise EnvironmentError('Unknown environment for API_TOKEN in appengine_config.py')


app_API_TOKEN = _API_TOKEN()


def _UNMANAGED_API_TOKEN():
    if on_development_server or not on_server:
        return 'A1365B43C51C46588BD4C6D5016C0'
    elif on_integration_server:
        return 'A1365B43C51C46588BD4C6D5016C0'
    elif on_continuous_integration_server:
        return 'A1365B43C51C46588BD4C6D5016C0'
    elif on_qa_server:
        return 'A1365B43C51C46588BD4C6D5016C0'
    elif on_stage_server:
        return 'A1365B43C51C46588BD4C6D5016C0'
    elif on_gamestop_server:
        return 'A1365B43C51C46588BD4C6D5016C0'
    elif on_production_server:
        return 'A1365B43C51C46588BD4C6D5016C0'
    else:
        raise EnvironmentError('Unknown environment for UNMANAGED_API_TOKEN in appengine_config.py')


app_UNMANAGED_API_TOKEN = _UNMANAGED_API_TOKEN()


def _UNMANAGED_REGISTRATION_TOKEN():
    if on_development_server or not on_server:
        return '43C51C8BD4C6D723A1365B6C34658'
    elif on_integration_server:
        return '43C51C8BD4C6D723A1365B6C34658'
    elif on_continuous_integration_server:
        return '43C51C8BD4C6D723A1365B6C34658'
    elif on_qa_server:
        return '43C51C8BD4C6D723A1365B6C34658'
    elif on_stage_server:
        return '43C51C8BD4C6D723A1365B6C34658'
    elif on_gamestop_server:
        return '43C51C8BD4C6D723A1365B6C34658'
    elif on_production_server:
        return '43C51C8BD4C6D723A1365B6C34658'
    else:
        raise EnvironmentError('Unknown environment for UNMANAGED_REGISTRATION_TOKEN in appengine_config.py')


app_UNMANAGED_REGISTRATION_TOKEN = _UNMANAGED_REGISTRATION_TOKEN()


def _CONTENT_MANAGER_API_SERVER_KEY():
    if on_development_server or not on_server:
        return 'EqwbumxWrJzybkDerDbm9yLBteJqZi7X'
    elif on_integration_server:
        return 'EqwbumxWrJzybkDerDbm9yLBteJqZi7X'
    elif on_continuous_integration_server:
        return 'o2EnT5qJ1q07w1DQxVfuafUYiUcJbeYJ'
    elif on_qa_server:
        return '2jI6eUVRZcvf9l5u3yxO4GAh4fnlAVhb'
    elif on_stage_server:
        return 'OTJkMGNjMmYzMmZlNjI4MDVmNGVlMjEx'
    elif on_gamestop_server:
        return ''  # Calls into CM-Sim
    elif on_production_server:
        return 'uXyQWMr3mAUvLFhvYuzYnfehkKop7ZCe'
    else:
        raise EnvironmentError('Unknown environment for CONTENT_MANAGER_API_SERVER_KEY in appengine_config.py')


app_CONTENT_MANAGER_API_SERVER_KEY = _CONTENT_MANAGER_API_SERVER_KEY()


def _DEFAULT_AGOSTO_DEVICE_DOMAIN():
    if on_development_server or not on_server:
        return 'local.agosto.com'
    elif on_integration_server:
        return 'dev.agosto.com'
    elif on_continuous_integration_server:
        return 'devci.skykit.com'
    elif on_qa_server:
        return 'devqa.skykit.com'
    elif on_stage_server:
        return 'devstaging.skykit.com'
    elif on_gamestop_server:
        return '???'
    elif on_production_server:
        return 'skykit.agosto.com'
    else:
        raise EnvironmentError('Unknown environment for DEFAULT_AGOSTO_DEVICE_DOMAIN in appengine_config.py')


app_DEFAULT_AGOSTO_DEVICE_DOMAIN = _DEFAULT_AGOSTO_DEVICE_DOMAIN()


def _GOOGLE_CUSTOMER_ID():
    if on_development_server or not on_server:
        return 'my_customer'
    elif on_integration_server:
        return 'my_customer'
    elif on_continuous_integration_server:
        return 'my_customer'
    elif on_qa_server:
        return 'my_customer'
    elif on_stage_server:
        return 'my_customer'
    elif on_gamestop_server:
        return 'my_customer'
    elif on_production_server:
        return 'my_customer'
    else:
        raise EnvironmentError('Unknown environment for GOOGLE_CUSTOMER_ID in appengine_config.py')


app_GOOGLE_CUSTOMER_ID = _GOOGLE_CUSTOMER_ID()

app_PLAYER_UNRESPONSIVE_SECONDS_THRESHOLD = 300  # 300 seconds = 5 minutes

app_DEVICE_SWEEP_PAGING_SIZE = 500

app_DEVICE_ISSUE_PLAYER_DOWN = 'Player down'

app_DEVICE_ISSUE_PLAYER_UP = 'Player up'

app_DEVICE_ISSUE_FIRST_HEARTBEAT = 'First heartbeat'

app_DEVICE_ISSUE_PLAYER_VERSION_CHANGE = 'Skykit version change'

app_DEVICE_ISSUE_TIMEZONE_CHANGE = 'Timezone change'

app_DEVICE_ISSUE_TIMEZONE_OFFSET_CHANGE = 'Timezone offset change'

app_DEVICE_ISSUE_OS_CHANGE = 'OS change'

app_DEVICE_ISSUE_OS_VERSION_CHANGE = 'OS version change'

app_DEVICE_ISSUE_MEMORY_HIGH = 'Memory usage high'

app_DEVICE_ISSUE_MEMORY_NORMAL = 'Memory normal'

app_DEVICE_ISSUE_STORAGE_LOW = 'Storage available low'

app_DEVICE_ISSUE_STORAGE_NORMAL = 'Storage normal'

app_STORAGE_UTILIZATION_THRESHOLD = 90

app_MEMORY_UTILIZATION_THRESHOLD = 98

app_LATEST_DEVICE_ISSUES_FETCH_COUNT = 250

app_PLAYER_RESET_COMMAND = 'skykit.com/skdchromeapp/reset'

app_PLAYER_RESTART_COMMAND = 'skykit.com/skdchromeapp/restart'

app_PLAYER_POST_LOG_COMMAND = 'skykit.com/skdchromeapp/postlog'

app_PLAYER_VOLUME_COMMAND = 'skykit.com/skdchromeapp/volume/'

app_PLAYER_POWER_ON_COMMAND = 'skykit.com/skdchromeapp/tv/on'

app_PLAYER_POWER_OFF_COMMAND = 'skykit.com/skdchromeapp/tv/off'

app_PLAYER_DELETE_CONTENT_COMMAND = 'skykit.com/skdchromeapp/content/delete'

app_PLAYER_UPDATE_CONTENT_COMMAND = 'skykit.com/skdchromeapp/update/content'

app_PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND = 'skykit.com/skdchromeapp/update/provisioning'

app_PLAYER_DIAGNOSTICS_TOGGLE_COMMAND = 'skykit.com/skdchromeapp/diagnostics'

app_PLAYER_HEARTBEAT_INTERVAL_MINUTES = 2

app_CHECK_FOR_CONTENT_INTERVAL_MINUTES = 1

app_ETHERNET_CONNECTION = 'Ethernet'

app_WIFI_CONNECTION = 'WiFi'

app_INTEGRATION_EVENTS_DEFAULT_FETCH_SIZE = 200

backup_BACKUP_EMAIL_SENDER = 'Backup Datastore Service <gcp.admin@agosto.com>'

app_ACCEPTABLE_ENROLLMENT_USER_PASSWORD_CHARS = "!$AaBbCcDdEeFfGgHhJjKkLlMmNnPpQqRrSsTtUuVvWwXxYyZz23456789"

app_ACCEPTABLE_ENROLLMENT_USER_PASSWORD_SIZE = 16

app_DEFAULT_TIMEZONE = 'America/Chicago'

app_DEFAULT_OU_PATH = '/skykit'

app_TENANT_CODE_UNKNOWN = 'TBD'

def _DEFAULT_CONTENT_MANAGER_URL():
    if on_development_server or not on_server:
        return 'https://skykit-contentmanager-int.appspot.com'
    elif on_integration_server:
        return 'https://skykit-contentmanager-int.appspot.com'
    elif on_continuous_integration_server:
        return 'https://skykit-contentmanager-ci.appspot.com'
    elif on_qa_server:
        return 'https://skykit-contentmanager-qa.appspot.com'
    elif on_stage_server:
        return 'https://skykit-contentmanager-stage.appspot.com'
    elif on_gamestop_server:
        return 'https://skykit-contentmanager-gamestop.appspot.com'
    elif on_production_server:
        return 'https://skykit-contentmanager.appspot.com'
    else:
        raise EnvironmentError('Unknown environment for DEFAULT_CONTENT_MANAGER_URL in appengine_config.py')


app_DEFAULT_CONTENT_MANAGER_URL = _DEFAULT_CONTENT_MANAGER_URL()


def _DEFAULT_PLAYER_CONTENT_URL():
    return '{}/content'.format(app_DEFAULT_CONTENT_MANAGER_URL)


app_DEFAULT_PLAYER_CONTENT_URL = _DEFAULT_PLAYER_CONTENT_URL()


def _STORMPATH_CLIENT():
    """
    http://docs.stormpath.com/python/quickstart/#create-a-client
    """
    if (on_test_harness or on_development_server or on_integration_server or on_continuous_integration_server or
            on_qa_server or on_stage_server):
        id = '6VYRY6TL26YRBJOAOO533W6DO'
        secret = 'oc4u1Nm0M5p3vJSOENhPZzAhNfzifAxMQS0v3J/kG/U'
    elif on_production_server or on_gamestop_server:
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
app_MAIL_API_KEY = "key-7g5zunub4weun65nb9aop2kcsgher-l0"

app_MAIL_MESSAGES_URL = "https://api.mailgun.net/v3/skykit.com/messages"

app_MAIL_EVENTS_URL = "https://api.mailgun.net/v3/skykit.com/events"

app_MAIL_FROM = "Skykit Provisioning <noreply-provisioning@skykit.com>"


def _MAIL_SERVER_QUEUED_RESPONSE_MESSAGE():
    return 'Queued. Thank you.'


app_MAIL_SERVER_QUEUED_RESPONSE_MESSAGE = _MAIL_SERVER_QUEUED_RESPONSE_MESSAGE()


def _EMAIL_SUPPORT():
    if on_development_server or not on_server:
        return True
    elif on_continuous_integration_server:
        return True
    elif on_qa_server:
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


app_EMAIL_SUPPORT = _EMAIL_SUPPORT()


##############################################################################
# Proof of Play
##############################################################################
def _SQLALCHEMY_DATABASE_URI():
    # the second arg after : is the db instance name
    if on_test_harness:
        db_uri = 'sqlite:///:memory:'
    elif on_development_server:
        db_uri = 'mysql+mysqldb://root@127.0.0.1/provisioning'
        return db_uri
    else:
        if on_integration_server:
            instance_name = 'provisioning-int-v2'
        elif on_continuous_integration_server:
            instance_name = 'sqlite:///:memory:'
        elif on_qa_server:
            instance_name = 'provisioning-qa'
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


def _DEFAULT_PROOF_OF_PLAY_URL():
    if on_development_server or not on_server:
        return 'https://skykit-display-device-int.appspot.com/proofplay/api/v1/post_new_program_play'
    elif on_integration_server:
        return 'https://skykit-display-device-int.appspot.com/proofplay/api/v1/post_new_program_play'
    elif on_continuous_integration_server:
        return 'https://skykit-display-device-ci.appspot.com/proofplay/api/v1/post_new_program_play'
    elif on_qa_server:
        return 'https://skykit-provisioning-qa.appspot.com/proofplay/api/v1/post_new_program_play'
    elif on_stage_server:
        return 'https://skykit-provisioning-stage.appspot.com/proofplay/api/v1/post_new_program_play'
    elif on_gamestop_server:
        return 'https://skykit-provisioning-gamestop.appspot.com/proofplay/api/v1/post_new_program_play'
    elif on_production_server:
        return 'https://skykit-provisioning.appspot.com/proofplay/api/v1/post_new_program_play'
    else:
        raise EnvironmentError('Unknown environment for PROOF_OF_PLAY_URL in appengine_config.py')


app_DEFAULT_PROOF_OF_PLAY_URL = _DEFAULT_PROOF_OF_PLAY_URL()
proofplay_SQLALCHEMY_DATABASE_URI = _SQLALCHEMY_DATABASE_URI()
proofplay_DAYS_TO_KEEP_RAW_EVENTS = 30



##############################################################################
# DON'T DO DIRECTORY LOOKUP ON DEV. IT CREATES A CASCADING TASK QUEUE FAILURE
##############################################################################
if on_development_server:
    from workflow import refresh_device_by_mac_address, refresh_device, update_chrome_os_device
    from workflow import update_chrome_os_device

    def _refresh_device_by_mac_address_dud(device_urlsafe_key, device_mac_address,
                                           device_has_previous_directory_api_info=False, page_token=None):
        pass


    def _refresh_device_dud(device_urlsafe_key):
        pass

    def _update_chrome_os_device(device_urlsafe_key):
        pass


    refresh_device_by_mac_address.refresh_device_by_mac_address = _refresh_device_by_mac_address_dud
    refresh_device.refresh_device = _refresh_device_dud
    update_chrome_os_device.update_chrome_os_device = _update_chrome_os_device


##############################################################################
# VERSION  sprint_number.deployment_increment.hotfix_increment e.g., 33.3.0
##############################################################################
def as_int(x):
    try:
        return int(x)
    except:
        return None


def _return_yaml_data():
    with open(os.path.join(basedir, 'snapdeploy.yaml'), 'r') as f:
        data = yaml.load(f.read())["version"]
        array_of_versions = data.split('-')
        array_of_versions_as_int = [as_int(each) for each in array_of_versions]
        return array_of_versions_as_int


snapdeploy_yaml_data = _return_yaml_data()
app_SPRINT_NUMBER = snapdeploy_yaml_data[0] if len(snapdeploy_yaml_data) > 0 else None
app_DEPLOYMENT_COUNTER = snapdeploy_yaml_data[1] if len(snapdeploy_yaml_data) > 1 else None
app_PRODUCTION_HOTFIX_COUNTER = snapdeploy_yaml_data[2] if len(snapdeploy_yaml_data) > 2 else None
