from agar.config import Config


class AppConfig(Config):
    """
    :py:class:`~agar.config.Config` settings for the application.
    Settings are under the ``app`` namespace.

    To override ``application`` settings, define values in the ``appengine_config.py`` file in the root of your project.
    """
    _prefix = 'app'

    APP_ROOT = None
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100

    MAILGUN_MESSAGES_URL = None
    MAILGUN_STATS_URL = None
    MAILGUN_APIKEY = None
    MAILGUN_DEADLINE = 15

    PA_DATETIME_FORMAT = None
    PA_TIME_INTERVAL_MINUTES = 0
    PA_TIME_INTERVAL_LOOKBACK_HOUR = 0
    PA_MIN_NUMBER_EVENTS = 0

    STORMPATH_APIKEY_ID = None
    STORMPATH_APIKEY_SECRET = None
    STORMPATH_AUTH_APP = None

    BOOTSTRAP_SPREADSHEET_KEY = None
    BOOTSTRAP_SPREADSHEET_USER = None
    BOOTSTRAP_SPREADSHEET_PASSWORD = None

    BUCKET_NAME = None
    IMAGE_DOMAIN = None
    MAPS_API_KEY = None

    EMAIL_SUPPORT = False
    TEST_EMAIL_ADDRESS = None

    ROUTER_HOST = None
    RAW_FOREIGN_DOC_URL = None
    ROUTER_STATS_URL = None

    SERVICE_CLIENT_SECRETS_PATH = None
    SERVICE_PRIVATE_KEY = None
    SERVICE_CLIENT_EMAIL = None

    WHEEL_SCHEMATIC_PREFIX_GCS = None

    SCHEDULE_REPORT_WINDOW_START = 17  # 5pm Central
    SCHEDULE_REPORT_WINDOW_STOP = 18  # 6pm Central

    FLEET_HQ_ENDPOINT = None


config = AppConfig.get_config()
