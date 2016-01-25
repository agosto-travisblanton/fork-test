__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'
from models import ChromeOsDevice
from google.appengine.ext import ndb
device = ChromeOsDevice.query(ChromeOsDevice.api_key == '1c562bdcfe0e4396a74f8fa470c04f53').get()
device.geo_location = ndb.GeoPt(44.983579,-93.277544)
device.put()
print 'Device seeded with geoLocation'
