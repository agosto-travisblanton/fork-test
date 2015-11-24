# Console script to initialize heartbeats for all devices
from models import ChromeOsDevice, DeviceHeartbeat

query = ChromeOsDevice.query().order(ChromeOsDevice.created)
devices = query.fetch(1000)
print 'Device count = ' + str(len(devices))
query = DeviceHeartbeat.query().order(DeviceHeartbeat.created)
beats = query.fetch(1000)
print 'Initial beat count = ' + str(len(beats))
for device in devices:
    beat = DeviceHeartbeat.find_by_device_key(device.key)
    if None == beat:
        print 'Setting beat for device with key and mac_address: ' + device.key.urlsafe() + ', ' + device.mac_address
        beat = DeviceHeartbeat.create(device_key=device.key, disk_utilization=0, memory_utilization=0,
                                      program_playing='****initial****')
        beat.put()

query = DeviceHeartbeat.query().order(DeviceHeartbeat.created)
beats = query.fetch(1000)
for beat in beats:
    print beat.device_key.urlsafe() + ' playing: "' + beat.program_playing + '". (' + str(beat.updated) + ')'
query = DeviceHeartbeat.query().order(DeviceHeartbeat.created)
beats = query.fetch(1000)
print 'Final beat count = ' + str(len(beats))
