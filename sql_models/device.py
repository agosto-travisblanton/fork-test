from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from proofplay.proofplay_models import Base


class Device(Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True)
    # Foreign Keys
    tenant_id = Column(Integer, ForeignKey('tenant.id'))
    tenant = relationship("Tenant", backref="Device")

    location_id = Column(Integer, ForeignKey('location.id'))
    location = relationship("Location", backref="Device")

    # End Foreign Keys
    created = Column(DateTime)  # FIXME
    updated = Column(DateTime)  # FIXME

    device_id = Column(String(255), unique=False, nullable=False)
    gcm_registration_id = Column(String(255), unique=False, nullable=False)
    mac_address = Column(String(255), unique=False, nullable=False)
    api_key = Column(String(255), unique=False, nullable=False)
    serial_number = Column(String(255), unique=False, nullable=False)
    status = Column(String(255), unique=False, nullable=False)
    last_sync = Column(String(255), unique=False, nullable=False)
    kind = Column(String(255), unique=False, nullable=False)
    ethernet_mac_address = Column(String(255), unique=False, nullable=False)

    org_unit_path = Column(String(255), unique=False, nullable=False)
    annotated_user = Column(String(255), unique=False, nullable=False)
    annotated_location = Column(String(255), unique=False, nullable=False)
    annotated_asset_id = Column(String(255), unique=False, nullable=False)
    boot_mode = Column(String(255), unique=False, nullable=False)
    last_enrollment_time = Column(String(255), unique=False, nullable=False)
    platform_version = Column(String(255), unique=False, nullable=False)
    model = Column(String(255), unique=False, nullable=False)
    os = Column(String(255), unique=False, nullable=False)
    platform_version = Column(String(255), unique=False, nullable=False)
    model = Column(String(255), unique=False, nullable=False)
    os = Column(String(255), unique=False, nullable=False)
    os_version = Column(String(255), unique=False, nullable=False)
    firmware_version = Column(String(255), unique=False, nullable=False)
    etag = Column(String(255), unique=False, nullable=False)

    # fixme
    # name = Column(String(255), unique=False, nullable=False)
    # fixme
    # loggly_link = Column(String(255), unique=False, nullable=False)

    is_unmanaged_device = Column(Boolean, default=True, nullable=False)
    pairing_code = Column(String(255), unique=False, nullable=False)
    panel_model = Column(String(255), unique=False, nullable=False)
    panel_input = Column(String(255), unique=False, nullable=False)
    heartbeat_updated = Column(DateTime)  # FIXME
    up = Column(Boolean, default=True, nullable=False)
    storage_utilization = Column(Integer)
    memory_utilization = Column(Integer)
    program = Column(String(255), unique=False, nullable=False)
    program_id = Column(String(255), unique=False, nullable=False)
    last_error = Column(String(255), unique=False, nullable=False)
    playlist = Column(String(255), unique=False, nullable=False)
    playlist_id = Column(String(255), unique=False, nullable=False)
    connection_type = Column(String(255), unique=False, nullable=False)
    sk_player_version = Column(String(255), unique=False, nullable=False)
    heartbeat_interval_minutes = Column(Integer)
    check_for_content_interval_minutes = Column(Integer)
    proof_of_play_logging = Column(Boolean, default=True, nullable=False)
    proof_of_play_editable = Column(Boolean, default=True, nullable=False)
    customer_display_name = Column(String(255), unique=False, nullable=False)
    customer_display_code = Column(String(255), unique=False, nullable=False)
    content_manager_display_name = Column(String(255), nullable=True)
    content_manager_location_description = Column(String(255), nullable=True)
    timezone = Column(String(255), nullable=True)
    timezone_offset = Column(Integer)
    registration_correlation_identifier = Column(String(255), nullable=True)
    archived = Column(Boolean, default=True, nullable=False)
    panel_sleep = Column(Boolean, default=True, nullable=False)
    overlays_available = Column(Boolean, default=True, nullable=False)
    controls_mode = Column(String(255), unique=False, nullable=False)
    orientation_mode = Column(String(255), unique=False, nullable=False)
    sleep_controller = Column(String(255), unique=False, nullable=False)
