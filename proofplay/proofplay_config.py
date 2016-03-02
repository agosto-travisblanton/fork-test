from env_setup import setup
setup()
from agar.config import Config


class ProofOfPlayConfig(Config):
    _prefix = 'proofplay'

    SQLALCHEMY_DATABASE_URI = None


config = ProofOfPlayConfig.get_config()
