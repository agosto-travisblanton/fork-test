# Console script to initialize heartbeats for all devices
from datetime import datetime

from app_config import config
from models import ChromeOsDevice

query = ChromeOsDevice.query().order(ChromeOsDevice.created)
devices = query.fetch(1000)
print 'Initializing heartbeat on devices'
for device in devices:
    if None == device.heartbeat_updated or len(str(device.heartbeat_updated)) == 0:
        print 'Setting beat for device with key and mac_address: ' + device.key.urlsafe() + ', ' + device.mac_address
        device.up = True
        device.storage_utilization = 0
        device.memory_utilization = 0
        device.heartbeat_updated = datetime.utcnow()
        device.program = '****initial****'
        device.program_id = '****initial****'
        device.heartbeat_interval_minutes = config.PLAYER_HEARTBEAT_INTERVAL_MINUTES
        device.put()
print 'Device count = ' + str(len(devices))
