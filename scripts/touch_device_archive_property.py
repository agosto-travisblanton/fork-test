from models import ChromeOsDevice

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'

devices = ChromeOsDevice.query().fetch(1000)
for device in devices:
    device.archived = False
    device.put()
