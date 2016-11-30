from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from proofplay.proofplay_models import Base


class OverlayTemplate(Base):
    __tablename__ = "overlay_template"

    id = Column(Integer, primary_key=True)
    #############################################################
    # Foreign Keys
    #############################################################
    top_left_id = Column(Integer, ForeignKey('overlay.id'))
    top_left = relationship("Overlay", backref="OverlayTemplate")

    top_right_id = Column(Integer, ForeignKey('overlay.id'))
    top_right = relationship("Overlay", backref="OverlayTemplate")

    bottom_right_id = Column(Integer, ForeignKey('overlay.id'))
    bottom_right = relationship("Overlay", backref="OverlayTemplate")

    bottom_left_id = Column(Integer, ForeignKey('overlay.id'))
    bottom_left = relationship("Overlay", backref="OverlayTemplate")

    device_id = Column(Integer, ForeignKey('device.id'))
    device = relationship("Device", backref="OverlayTemplate")

    tenant_id = Column(Integer, ForeignKey('tenant.id'))
    tenant = relationship("Tenant", backref="OverlayTemplate")
