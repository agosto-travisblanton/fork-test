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
    SECRET_KEY_FILE = None
    PRIVATE_KEY = None
    SERVICE_ACCOUNT_EMAIL = None
    CLIENT_ID = None
    # CLIENT_SECRET = None


config = AppConfig.get_config()
