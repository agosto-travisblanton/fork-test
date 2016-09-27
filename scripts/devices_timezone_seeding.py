from app_config import config
from models import ChromeOsDevice
from utils.timezone_util import TimezoneUtil

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'

devices = ChromeOsDevice.query(ChromeOsDevice.timezone is None).fetch()
print 'device count with unset timezones = ' + str(len(devices))
for device in devices:
  device.timezone = config.DEFAULT_TIMEZONE
  device.timezone_offset = TimezoneUtil.get_timezone_offset(config.DEFAULT_TIMEZONE)
  device.put()
  print 'updated timezone for ' + str(device.key.urlsafe())

devices = ChromeOsDevice.query().fetch()
print 'device count with timezone missing = ' + str(len(devices))
for device in devices:
  if not device.timezone:
    device.timezone = config.DEFAULT_TIMEZONE
    device.timezone_offset = TimezoneUtil.get_timezone_offset(config.DEFAULT_TIMEZONE)
    device.put()
    print 'created timezone for ' + str(device.key.urlsafe())