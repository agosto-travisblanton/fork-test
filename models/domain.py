from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from proofplay.proofplay_models import Base


class Domain(Base):
    __tablename__ = "domain"

    id = Column(Integer, primary_key=True)
    # Foreign Keys
    managing_org_id = Column(Integer, ForeignKey('managing_org.id'))
    managing_org = relationship("ManagingOrg", backref="Domain")

    # End Foreign Keys
    impersonation_admin_email_address = Column(String(255), unique=False, nullable=False)
    organization_unit_path = Column(String(255), nullable=True)
    created = Column(DateTime)  # FIXME
    updated = Column(DateTime)  # FIXME
    active = Column(Boolean, default=True, nullable=False)
