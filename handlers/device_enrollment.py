from webapp2 import RequestHandler

from restler.serializers import json_response
from chrome_os_devices_api import ChromeOsDevicesApi
import json


__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class DeviceEnrollmentHandler(RequestHandler):
    ADMIN_ACCOUNT_TO_IMPERSONATE = 'administrator@skykit.com'

    def get(self):
        expected_mac_address = self.request.get('mac_address')
        chrome_os_devices_api = ChromeOsDevicesApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)
        chrome_os_devices = json.loads(chrome_os_devices_api.list('my_customer'))
        loop_comprehension = (x for x in chrome_os_devices if x.get('macAddress') == expected_mac_address)
        chrome_os_device = next(loop_comprehension, None)
        json_response(self.response, chrome_os_device)

