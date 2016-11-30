from sqlalchemy import Column, Integer, String, DateTime, Boolean

from proofplay.proofplay_models import Base


class ManagingOrg(Base):
    __tablename__ = "managing_org"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    admin_email = Column(String(255), nullable=True)
    player_content_url = Column(String(255), nullable=True)
    content_manager_url = Column(String(255), nullable=True)
    created = Column(DateTime)  # FIXME
    updated = Column(DateTime)  # FIXME
    active = Column(Boolean, default=True, nullable=False)
