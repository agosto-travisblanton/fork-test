from sqlalchemy import Column, Integer, String, DateTime, Boolean

from proofplay.proofplay_models import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime)  # FIXME
    updated = Column(DateTime)  # FIXME
    email = Column(String(255), unique=True, nullable=False)
    is_administrator = Column(Boolean, default=True, nullable=False)
    last_login = Column(DateTime)  # FIXME
    enabled = Column(Boolean, default=True, nullable=False)
