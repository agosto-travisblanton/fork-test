from env_setup import setup
setup()
from agar.config import Config


class ProofOfPlayConfig(Config):
    _prefix = 'proofplay'

    DAYS_TO_KEEP_RAW_EVENTS = None
    SQLALCHEMY_DATABASE_URI = None


config = ProofOfPlayConfig.get_config()
