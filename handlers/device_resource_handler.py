import json

from webapp2 import RequestHandler
from google.appengine.ext import ndb

from restler.serializers import json_response
from chrome_os_devices_api import ChromeOsDevicesApi
from models import ChromeOsDevice

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>, Bob MacNeal <bob.macneal@agosto.com>'


class DeviceResourceHandler(RequestHandler):
    ADMIN_ACCOUNT_TO_IMPERSONATE = 'administrator@skykit.com'
    CUSTOMER_ID = 'my_customer'

    def get(self, device_urlsafe_key):
        device_key = ndb.Key(urlsafe=device_urlsafe_key)
        local_device = device_key.get()
        chrome_os_devices_api = ChromeOsDevicesApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)
        chrome_os_device = chrome_os_devices_api.get(self.CUSTOMER_ID, local_device.device_id)
        result = {}
        if chrome_os_device:
            result = chrome_os_device
        result['gcmRegistrationId'] = local_device.gcm_registration_id
        result['tenantCode'] = local_device.tenant_code
        result['created'] = local_device.created.strftime('%Y-%m-%d %H:%M:%S')
        result['updated'] = local_device.updated.strftime('%Y-%m-%d %H:%M:%S')
        json_response(self.response, result)

    def get_list(self):
        device_mac_address = self.request.get('macAddress')
        if not device_mac_address:
            self.get_all_devices()
        else:
            self.get_device_by_mac_address(device_mac_address)

    def get_all_devices(self):
        chrome_os_devices_api = ChromeOsDevicesApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)
        chrome_os_devices = chrome_os_devices_api.list(self.CUSTOMER_ID)
        if chrome_os_devices is not None:
            json_response(self.response, chrome_os_devices)
            self.response.set_status(200)
        else:
            message = 'Unable to retrieve a list of ChromeOS devices.'
            json_response(self.response, {'error': message}, status_code=404)

    def get_device_by_mac_address(self, device_mac_address):
        chrome_os_devices_api = ChromeOsDevicesApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)
        chrome_os_devices = chrome_os_devices_api.list(self.CUSTOMER_ID)
        if chrome_os_devices is not None:
            lowercase_device_mac_address = device_mac_address.lower()
            loop_comprehension = (x for x in chrome_os_devices if x.get('macAddress') == lowercase_device_mac_address or
                                  x.get('ethernetMacAddress') == lowercase_device_mac_address)
            chrome_os_device = next(loop_comprehension, None)
            if chrome_os_device is not None:
                json_response(self.response, chrome_os_device)
            else:
                message = 'A ChromeOS device was not found to be associated with the MAC address: {0}.'.format(
                    device_mac_address)
                json_response(self.response, {'error': message}, status_code=404)
        else:
            message = 'Unable to retrieve a list of ChromeOS devices.'
            json_response(self.response, {'error': message}, status_code=404)

    def post(self):
        if self.request.body is not str('') and self.request.body is not None:
            request_json = json.loads(self.request.body)
            device_mac_address = request_json.get(u'macAddress')
            chrome_os_devices_api = ChromeOsDevicesApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)
            chrome_os_devices = chrome_os_devices_api.list(self.CUSTOMER_ID)
            if chrome_os_devices is not None:
                loop_comprehension = (x for x in chrome_os_devices if x.get('macAddress') == device_mac_address or
                                      x.get('ethernetMacAddress') == device_mac_address)
                chrome_os_device = next(loop_comprehension, None)
                if chrome_os_device is not None:
                    device_id = chrome_os_device.get('deviceId')
                    device = ChromeOsDevice.get_by_device_id(device_id)
                    if device is None:
                        gcm_registration_id = request_json.get('gcmRegistrationId')
                        tenant_code = request_json.get('tenantCode')
                        device = ChromeOsDevice(device_id=device_id,
                                                gcm_registration_id=gcm_registration_id,
                                                tenant_code=tenant_code)
                    device_key = device.put()
                    device_uri = self.request.app.router.build(None,
                                                               'manage-device',
                                                               None,
                                                               {'device_urlsafe_key': device_key.urlsafe()})
                    self.response.headers['Location'] = device_uri
                    self.response.headers.pop('Content-Type', None)
                    self.response.set_status(201)
                else:
                    self.response.set_status(422,
                                             'Chrome OS device not associated with this customer id ( {0}'.format(
                                                 self.CUSTOMER_ID))
        else:
            self.response.set_status(422, 'Did not receive request body.')

    def put(self, device_urlsafe_key):
        device_key = ndb.Key(urlsafe=device_urlsafe_key)
        local_device = device_key.get()
        chrome_os_devices_api = ChromeOsDevicesApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)
        registered_chrome_os_device = chrome_os_devices_api.get(self.CUSTOMER_ID, local_device.device_id)
        if registered_chrome_os_device is None:
            self.response.set_status(422, 'Unable to retrieve Chrome OS device by device id: {0}'.
                                     format(local_device.device_id))
        else:
            request_json = json.loads(self.request.body)
            gcm_registration_id = request_json.get('gcmRegistrationId')
            if gcm_registration_id:
                local_device.gcm_registration_id = gcm_registration_id
            tenant_code = request_json.get('tenantCode')
            if tenant_code:
                local_device.tenant_code = tenant_code
            local_device.put()
            self.response.headers.pop('Content-Type', None)
            self.response.set_status(204)

    def delete(self, device_urlsafe_key):
        device_key = ndb.Key(urlsafe=device_urlsafe_key)
        local_device = device_key.get()
        if local_device is None:
            self.response.set_status(422, 'Unable to retrieve ChromeOS device by device ID: {0}'.format(local_device.device_id))
        else:
            local_device.key.delete()
            self.response.headers.pop('Content-Type', None)
            self.response.set_status(204)
