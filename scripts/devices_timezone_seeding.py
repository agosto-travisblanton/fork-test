from models import ChromeOsDevice
from utils.timezone_util import TimezoneUtil

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'

default_timezone = 'America/Chicago'

devices = ChromeOsDevice.query(ChromeOsDevice.timezone == None).fetch()
print 'device count with unset timezones = ' + str(len(devices))
for device in devices:
  device.timezone = default_timezone
  device.timezone_offset = TimezoneUtil.get_timezone_offset(default_timezone)
  device.put()
  print 'updated timezone for ' + str(device.key.urlsafe())

devices = ChromeOsDevice.query().fetch()
print 'device count with timezone missing = ' + str(len(devices))
for device in devices:
  if not device.timezone:
    device.timezone = default_timezone
    device.timezone_offset =        TimezoneUtil.get_timezone_offset(default_timezone)
    device.put()
    print 'created timezone for ' + str(device.key.urlsafe())