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
    CONTENT_MANAGER_API_SERVER_KEY = None
    GCM_TEST_MODE = None
    GOOGLE_CUSTOMER_ID = None
    STORMPATH_AUTH_APP = None
    STORMPATH_CLIENT = None
    OAUTH_CLIENT_ID = None
    DEFAULT_AGOSTO_DEVICE_DOMAIN = None
    PLAYER_RESET_COMMAND = None
    PLAYER_VOLUME_COMMAND = None
    LIMITED_UNMANAGED_DEVICE_REGISTRATION_API_TOKEN = None


config = AppConfig.get_config()
