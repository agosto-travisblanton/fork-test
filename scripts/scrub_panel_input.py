__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'
from models import ChromeOsDevice

device = ChromeOsDevice.query(ChromeOsDevice.serial_number == 'F9MSCX006674').get()
print 'device panel input = ' + device.panel_input
