from webapp2 import RequestHandler

from restler.serializers import json_response
from chrome_os_devices_api import ChromeOsDevicesApi


__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class DeviceEnrollmentHandler(RequestHandler):
    ADMIN_ACCOUNT_TO_IMPERSONATE = 'administrator@skykit.com'

    def get(self):
        chrome_os_devices_api = ChromeOsDevicesApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)
        chrome_os_devices = chrome_os_devices_api.list('my_customer')
        self.response.out.write('Hello from skykit-display-device/device registration!')
        json_response(self.response, None)

