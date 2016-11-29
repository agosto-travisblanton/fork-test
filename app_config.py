from agar.config import Config


class AppConfig(Config):
    """
    :py:class:`~agar.config.Config` settings for the application.
    Settings are under the ``app`` namespace.

    To override ``application`` settings, define values in the ``appengine_config.py`` file in the root of your project.
    """
    _prefix = 'app'

    APP_ROOT = None
    APP_NAME = ''
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100
    SECRET_KEY_FILE = None
    PRIVATE_KEY = None
    SERVICE_ACCOUNT_EMAIL = None
    CLIENT_ID = None
    PUBLIC_API_SERVER_KEY = None
    API_TOKEN = None
    UNMANAGED_API_TOKEN = None
    UNMANAGED_REGISTRATION_TOKEN = None
    CONTENT_MANAGER_API_SERVER_KEY = None
    GCM_TEST_MODE = None
    GOOGLE_CUSTOMER_ID = None
    STORMPATH_AUTH_APP = None
    STORMPATH_CLIENT = None
    OAUTH_CLIENT_ID = None
    JWT_SECRET_KEY = None
    DEFAULT_AGOSTO_DEVICE_DOMAIN = None
    PLAYER_RESET_COMMAND = None
    PLAYER_RESTART_COMMAND = None
    PLAYER_POST_LOG_COMMAND = None
    PLAYER_VOLUME_COMMAND = None
    PLAYER_POWER_ON_COMMAND = None
    PLAYER_POWER_OFF_COMMAND = None
    PLAYER_DELETE_CONTENT_COMMAND = None
    PLAYER_UPDATE_CONTENT_COMMAND = None
    PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND = None
    PLAYER_DIAGNOSTICS_TOGGLE_COMMAND = None
    PLAYER_UNRESPONSIVE_SECONDS_THRESHOLD = None
    PLAYER_HEARTBEAT_INTERVAL_MINUTES = None

    CHECK_FOR_CONTENT_INTERVAL_MINUTES = None

    DEVICE_ISSUE_PLAYER_DOWN = None
    DEVICE_ISSUE_PLAYER_UP = None
    DEVICE_ISSUE_MEMORY_HIGH = None
    DEVICE_ISSUE_MEMORY_NORMAL = None
    DEVICE_ISSUE_STORAGE_LOW = None
    DEVICE_ISSUE_STORAGE_NORMAL = None
    DEVICE_ISSUE_FIRST_HEARTBEAT = None
    DEVICE_ISSUE_PLAYER_VERSION_CHANGE = None
    DEVICE_ISSUE_OS_CHANGE = None
    DEVICE_ISSUE_OS_VERSION_CHANGE = None
    DEVICE_ISSUE_TIMEZONE_CHANGE = None
    DEVICE_ISSUE_TIMEZONE_OFFSET_CHANGE = None
    DEVICE_ISSUE_PROGRAM_CHANGE = None
    DEVICE_ISSUE_PLAYLIST_CHANGE = None


    DEVICE_SWEEP_PAGING_SIZE = None

    STORAGE_UTILIZATION_THRESHOLD = None
    MEMORY_UTILIZATION_THRESHOLD = None

    LATEST_DEVICE_ISSUES_FETCH_COUNT = None

    ETHERNET_CONNECTION = None
    WIFI_CONNECTION = None

    MAIL_MESSAGES_URL = None
    MAIL_EVENTS_URL = None
    MAIL_API_KEY = None
    MAIL_FROM = None
    MAIL_SERVER_QUEUED_RESPONSE_MESSAGE = 'Queued. Thank you.'

    EMAIL_SUPPORT = False

    DEFAULT_CONTENT_MANAGER_URL = False
    DEFAULT_PLAYER_CONTENT_URL = False

    DEFAULT_PROOF_OF_PLAY_URL = None

    SPRINT_NUMBER = None
    DEPLOYMENT_COUNTER = None
    PRODUCTION_HOTFIX_COUNTER = None

    INTEGRATION_EVENTS_DEFAULT_FETCH_SIZE = None

    ACCEPTABLE_ENROLLMENT_USER_PASSWORD_CHARS = None
    ACCEPTABLE_ENROLLMENT_USER_PASSWORD_SIZE = None

    DEFAULT_TIMEZONE = None

    DEFAULT_OU_PATH = None

    TENANT_CODE_UNKNOWN = None

config = AppConfig.get_config()
