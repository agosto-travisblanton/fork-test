from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from proofplay.proofplay_models import Base


class Tenant(Base):
    __tablename__ = "tenant"

    # Foreign Keys
    domain_id = Column(Integer, ForeignKey('domain.id'))
    domain = relationship("Domain", backref="Tenant")
    # End Foreign Keys

    created = Column(DateTime)  # FIXME
    updated = Column(DateTime)  # FIXME
    code = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    admin_email = Column(String(255), nullable=False)
    content_server_url = Column(String(255), nullable=False)
    content_manager_base_url = Column(String(255), nullable=False)
    chrome_device_domain = Column(String(255), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    notification_emails = Column(String(255), unique=True, nullable=False)
    proof_of_play_logging = Column(Boolean, default=True, nullable=False)
    proof_of_play_url = Column(String(255), unique=True, nullable=False)
    default_timezone = Column(String(255), unique=True, nullable=False)
    enrollment_email = Column(String(255), unique=True, nullable=False)
    enrollment_password = Column(String(255), unique=True, nullable=False)
    organization_unit_id = Column(String(255), unique=True, nullable=False)
    organization_unit_path = Column(String(255), unique=True, nullable=False)
    overlays_available = Column(Boolean, default=True, nullable=False)
    overlays_update_in_progress = Column(Boolean, default=True, nullable=False)

