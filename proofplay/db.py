from proofplay_config import config
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
session_factory = sessionmaker(bind=engine, expire_on_commit=False)
Session = scoped_session(session_factory)
