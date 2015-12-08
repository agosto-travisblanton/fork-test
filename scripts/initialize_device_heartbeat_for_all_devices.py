# Console script to initialize heartbeats for all devices
from datetime import datetime

from models import ChromeOsDevice

query = ChromeOsDevice.query().order(ChromeOsDevice.created)
devices = query.fetch(1000)
print 'Device count = ' + str(len(devices))
for device in devices:
    if None == device.heartbeat_updated or len(str(device.heartbeat_updated)) == 0:
        print 'Setting beat for device with key and mac_address: ' + device.key.urlsafe() + ', ' + device.mac_address
        device.storage_utilization = 0
        device.memory_utilization = 0
        device.heartbeat_updated = datetime.utcnow()
        device.program_player = '****initial****'
        device.put()
