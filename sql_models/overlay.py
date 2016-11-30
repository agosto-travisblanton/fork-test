from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from proofplay.proofplay_models import Base


class Overlay(Base):
    __tablename__ = "overlay"

    id = Column(Integer, primary_key=True)
    # Foreign Keys
    image_id = Column(Integer, ForeignKey('image.id'), nullable=True)
    image = relationship("Image", backref="Overlay")
    # End Foreign Keys

    type = Column(String(255), unique=False, nullable=False)
    size = Column(String(255), nullable=True)
