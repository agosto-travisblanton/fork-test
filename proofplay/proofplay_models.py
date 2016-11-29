import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class ChromeOsDevice(Base):
    __tablename__ = "chrome_os_device"

    id = Column(Integer, primary_key=True)
    device_name = Column(String(255), nullable=False)



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
    completed = Column(Boolean, default=False)

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


class TenantCode(Base):
    __tablename__ = "tenant_code"

    id = Column(Integer, primary_key=True)
    tenant_code = Column(String(255), unique=True, nullable=False)

    def __init__(self, tenant_code):
        self.tenant_code = tenant_code


class Resource(Base):
    __tablename__ = "resource"

    id = Column(Integer, primary_key=True)
    resource_name = Column(String(255), unique=False, nullable=False)
    resource_identifier = Column(String(255), unique=True, nullable=False)
    tenant_id = Column(Integer, ForeignKey('tenant_code.id'))
    tenant = relationship("TenantCode", backref="Resource")

    def __init__(self, resource_name, resource_identifier, tenant_id):
        self.resource_name = resource_name
        self.resource_identifier = resource_identifier
        self.tenant_id = tenant_id


class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    customer_location_code = Column(String(255), nullable=True)
    dma_code = Column(String(255), nullable=True)
    state = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    tenant_id = Column(Integer, ForeignKey('tenant_code.id'))
    tenant = relationship("TenantCode", backref="Location")

    def __init__(self, customer_location_code, tenant_id, dma_code=None, state=None, city=None):
        self.customer_location_code = customer_location_code
        self.tenant_id = tenant_id
        self.dma_code = dma_code
        self.state = state
        self.city = city


class Device(Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=True)
    full_location = relationship("Location", backref="Device")
    serial_number = Column(String(255), nullable=True)
    device_key = Column(String(255), nullable=False)
    customer_display_code = Column(String(255), nullable=True)
    tenant_id = Column(Integer, ForeignKey('tenant_code.id'))
    tenant = relationship("TenantCode", backref="Device")

    def __init__(self, serial_number, tenant_id, device_key, customer_display_code, location_id=None):
        self.location_id = location_id
        self.serial_number = serial_number
        self.tenant_id = tenant_id
        self.customer_display_code = customer_display_code
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
