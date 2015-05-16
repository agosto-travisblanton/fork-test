import json

from webapp2 import RequestHandler

from restler.serializers import json_response
from chrome_os_devices_api import ChromeOsDevicesApi
from models import ChromeOsDevice


__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class DeviceEnrollmentHandler(RequestHandler):
    ADMIN_ACCOUNT_TO_IMPERSONATE = 'administrator@skykit.com'

    def get(self):
        expected_mac_address = self.request.get('mac_address')
        chrome_os_devices_api = ChromeOsDevicesApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)
        chrome_os_devices = chrome_os_devices_api.list('my_customer')
        if chrome_os_devices is not None:
            loop_comprehension = (x for x in chrome_os_devices if x.get('macAddress') == expected_mac_address)
            chrome_os_device = next(loop_comprehension, None)
            if chrome_os_device is not None:
                json_response(self.response, chrome_os_device)
            else:
                message = 'A ChromeOS device was not found to be associated with the MAC address: {0}.'.format(
                    expected_mac_address)
                self.abort(404, message)
        else:
            message = 'Unable to retrieve a list of ChromeOS devices.'
            self.abort(404, message)

    def post(self):
        pass

    def put(self, device_id):
        if device_id:
            chrome_os_devices_api = ChromeOsDevicesApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)
            registered_chrome_os_device = chrome_os_devices_api.get('my_customer', device_id)
            if registered_chrome_os_device is None:
                self.abort(422, 'Unable to retrieve Chrome OS device by device ID: {0}'.format(device_id))
            else:
                chrome_os_device = ChromeOsDevice.get_by_device_id(device_id)
                if chrome_os_device is None:
                    chrome_os_device = ChromeOsDevice(device_id=device_id)
                request_json = json.loads(self.request.body)
                gcm_registration_id = request_json.get('gcmRegistrationId')
                if gcm_registration_id:
                    chrome_os_device.gcm_registration_id = gcm_registration_id
                chrome_os_device.put()
                self.response.headers.pop('Content-Type', None)
                self.response.set_status(204)
        else:
            self.abort(422, 'A device_id is required to update an existing ChromeOS device entity.')

    def delete(self, device_id):
        if device_id:
            chrome_os_device = ChromeOsDevice.get_by_device_id(device_id)
            if chrome_os_device is None:
                self.abort(422, 'Unable to retrieve ChromeOS device by device ID: {0}'.format(device_id))
            else:
                chrome_os_device.key.delete()
                self.response.headers.pop('Content-Type', None)
                self.response.set_status(204)
        else:
            self.abort(422, 'A device_id is required to delete an existing ChromeOS device entity.')