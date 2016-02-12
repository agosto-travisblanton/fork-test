import datetime
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class ProgramPlayEvent(Base):
    __tablename__ = "program_play_event"

    id = Column(Integer, primary_key=True)
    resource_name = Column(String(255), nullable=False)
    resource_id = Column(String(255), nullable=False)
    serial_number = Column(String(255), nullable=False)
    device_key = Column(String(255), nullable=False)
    tenant_code = Column(String(255), nullable=False)
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=False)
    completed = Column(Boolean, unique=False, default=False)

    def __init__(self, resource_name, resource_id, serial_number, device_key, tenant_code, started_at, ended_at,
                 completed=False):
        self.resource_name = resource_name
        self.resource_id = resource_id
        self.serial_number = serial_number
        self.device_key = device_key
        self.tenant_code = tenant_code
        self.started_at = started_at
        self.ended_at = ended_at
        self.completed = completed


class GamestopStoreLocation(Base):
    __tablename__ = "gamestop_store_location"

    id = Column(Integer, primary_key=True)
    location_name = Column(String(255), nullable=False)
    serial_number = Column(String(255), unique=True, nullable=False)

    def __init__(self, location_name, serial_number):
        self.location_name = location_name
        self.serial_number = serial_number


class ScheduleWentLive(Base):
    __tablename__ = "schedule_went_live"

    id = Column(Integer, primary_key=True)
    schedule = Column(String(255), unique=True, nullable=False)
    played_at = Column(DateTime, nullable=False)
    device_id = Column(Integer, ForeignKey('device.id'), nullable=False)
    full_device = relationship("Device", backref="ScheduleWentLive")

    def __init__(self, schedule, played_at, device_id):
        self.schedule = schedule
        self.played_at = played_at
        self.device_id = device_id


class Resource(Base):
    __tablename__ = "resource"

    id = Column(Integer, primary_key=True)
    resource_name = Column(String(255), unique=True, nullable=False)
    resource_identifier = Column(String(255), unique=True, nullable=False)

    def __init__(self, resource_name, resource_identifier):
        self.resource_name = resource_name
        self.resource_identifier = resource_identifier


class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    location_identifier = Column(String(255), unique=True, nullable=False)
    dma_code = Column(String(255), nullable=True)
    state = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)

    def __init__(self, location_identifier, dma_code=None, state=None, city=None):
        self.location_identifier = location_identifier
        self.dma_code = dma_code
        self.state = state
        self.city = city


class Device(Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=True)
    full_location = relationship("Location", backref="Device")
    serial_number = Column(String(255), nullable=False)
    device_key = Column(String(255), nullable=False)
    tenant_code = Column(String(255), nullable=False)

    def __init__(self, serial_number, tenant_code, device_key, location_id=None):
        self.location_id = location_id
        self.serial_number = serial_number
        self.tenant_code = tenant_code
        self.device_key = device_key


class ProgramRecord(Base):
    __tablename__ = "program_record"

    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=True)
    resource_id = Column(Integer, ForeignKey('resource.id'), nullable=False)
    device_id = Column(Integer, ForeignKey('device.id'), nullable=False)
    full_location = relationship("Location", backref="ProgramRecord")
    full_resource = relationship("Resource", backref="ProgramRecord")
    full_device = relationship("Device", backref="ProgramRecord")
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=False)

    created_on = Column(DateTime, nullable=False)

    def __init__(self, location_id, resource_id, device_id, started_at, ended_at):
        self.location_id = location_id
        self.resource_id = resource_id
        self.device_id = device_id
        self.started_at = started_at
        self.ended_at = ended_at
        self.created_on = datetime.datetime.now()
