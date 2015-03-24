from webapp2 import RequestHandler

from restler.serializers import json_response
from chrome_os_devices_api import ChromeOsDevicesApi


__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class DeviceEnrollmentHandler(RequestHandler):
    def get(self):
        chrome_os_devices_api = ChromeOsDevicesApi()
        chrome_os_devices = chrome_os_devices_api.list()
        # GET https://www.googleapis.com/admin/directory/v1/customer/customerId/devices/chromeos

        # PUT https://www.googleapis.com/admin/directory/v1/customer/customerId/devices/chromeos/deviceId

        self.response.out.write('Hello from skykit-display-device/device registration!')
        json_response(self.response, None)

