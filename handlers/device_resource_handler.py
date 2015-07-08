import json
import logging

from webapp2 import RequestHandler

from google.appengine.ext import ndb

from decorators import api_token_required
from restler.serializers import json_response
from chrome_os_devices_api import ChromeOsDevicesApi
from models import ChromeOsDevice, Tenant
from strategy import CHROME_OS_DEVICE_STRATEGY

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>, Bob MacNeal <bob.macneal@agosto.com>'


class DeviceResourceHandler(RequestHandler):
    ADMIN_ACCOUNT_TO_IMPERSONATE = 'administrator@skykit.com'
    CUSTOMER_ID = 'my_customer'

    @api_token_required
    def get_devices_by_tenant(self, tenant_urlsafe_key):
        tenant_key = ndb.Key(urlsafe=tenant_urlsafe_key)
        tenant = tenant_key.get()
        if tenant is not None:
            chrome_os_devices = ChromeOsDevice.query(ancestor=tenant_key).fetch()
            json_response(self.response, chrome_os_devices, strategy=CHROME_OS_DEVICE_STRATEGY)
            self.response.set_status(200)
        else:
            message = 'Unable to retrieve the parent tenant by key: {0}'.format(tenant_urlsafe_key)
            json_response(self.response, {'error': message}, status_code=404)

    @api_token_required
    def get(self, device_urlsafe_key):
        try:
            device_key = ndb.Key(urlsafe=device_urlsafe_key)
        except Exception, e:
            logging.exception(e)
            logging.info('Unrecognized device with device key: {0}'.format(device_urlsafe_key))
            return self.response.set_status(404)
        local_device = device_key.get()
        chrome_os_devices_api = ChromeOsDevicesApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)
        chrome_os_device = chrome_os_devices_api.get(self.CUSTOMER_ID, local_device.device_id)
        result = {}
        if chrome_os_device:
            result = chrome_os_device
        try:
            tenant = local_device.key.parent().get()
        except Exception, e:
            logging.exception(e)
            logging.info('No tenant for device key: {0}'.format(device_urlsafe_key))
            return self.response.set_status(400)
        result['tenantCode'] = tenant.tenant_code
        result['contentServerUrl'] = tenant.content_server_url
        result['chromeDeviceDomain'] = tenant.chrome_device_domain
        result["gcmRegistrationId"] = local_device.gcm_registration_id
        result['created'] = local_device.created.strftime('%Y-%m-%d %H:%M:%S')
        result['updated'] = local_device.updated.strftime('%Y-%m-%d %H:%M:%S')
        result['apiKey'] = local_device.api_key
        result['active'] = tenant.active
        result['key'] = local_device.key.urlsafe()
        json_response(self.response, result)

    @api_token_required
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
                device_id = chrome_os_device.get('deviceId')
                local_device = ChromeOsDevice.get_by_device_id(device_id)
                if local_device is not None:
                    tenant = local_device.key.parent().get()
                    chrome_os_device['tenantCode'] = tenant.tenant_code
                    chrome_os_device['contentServerUrl'] = tenant.content_server_url
                    chrome_os_device['chromeDeviceDomain'] = tenant.chrome_device_domain
                    chrome_os_device["gcmRegistrationId"] = local_device.gcm_registration_id
                    chrome_os_device['created'] = local_device.created.strftime('%Y-%m-%d %H:%M:%S')
                    chrome_os_device['updated'] = local_device.updated.strftime('%Y-%m-%d %H:%M:%S')
                    chrome_os_device['apiKey'] = local_device.api_key
                    chrome_os_device['key'] = local_device.key.urlsafe()
                    json_response(self.response, chrome_os_device)
                else:
                    message = 'Device not stored for deviceId {0} and MAC address {1}.'.format(
                        device_id, device_mac_address)
                    json_response(self.response, {'error': message}, status_code=404)
            else:
                message = 'A ChromeOS device was not found to be associated with the MAC address: {0}.'.format(
                    device_mac_address)
                json_response(self.response, {'error': message}, status_code=404)
        else:
            message = 'Unable to retrieve a list of ChromeOS devices.'
            json_response(self.response, {'error': message}, status_code=404)

    @api_token_required
    def post(self):
        if self.request.body is not str('') and self.request.body is not None:
            status = 201
            error_message = None
            logging.info('Request body: {0}'.format(self.request.body))
            request_json = json.loads(self.request.body)
            device_mac_address = request_json.get(u'macAddress')
            device_exists = ChromeOsDevice.query(ChromeOsDevice.mac_address == device_mac_address).count() > 0
            if device_exists:
                status = 400
                error_message = 'Cannot create because MAC address has already been assigned to this device.'
            tenant_code = request_json.get(u'tenantCode')
            gcm_registration_id = request_json.get(u'gcmRegistrationId')
            if device_mac_address is None or device_mac_address == '':
                status = 400
                error_message = 'The macAddress parameter was not valid.'
            if tenant_code is None or tenant_code == '':
                status = 400
                error_message = 'The tenantCode parameter was not valid.'
            if gcm_registration_id is None or gcm_registration_id == '':
                status = 400
                error_message = 'The gcmRegistrationId parameter was not valid.'
            tenant_key = Tenant.query(Tenant.tenant_code == tenant_code, Tenant.active == True).get(keys_only=True)
            if tenant_key is None:
                status = 400
                error_message = 'Invalid or inactive tenant for device.'
            if status == 201:
                chrome_os_devices_api = ChromeOsDevicesApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)
                chrome_os_devices = chrome_os_devices_api.list(self.CUSTOMER_ID)
                if chrome_os_devices is not None:
                    loop_comprehension = (x for x in chrome_os_devices if x.get('macAddress') == device_mac_address or
                                          x.get('ethernetMacAddress') == device_mac_address)
                    chrome_os_device = next(loop_comprehension, None)
                    if chrome_os_device is not None:
                        device_id = chrome_os_device.get('deviceId')
                        local_device = ChromeOsDevice.create(tenant_key=tenant_key,
                                                             device_id=device_id,
                                                             gcm_registration_id=gcm_registration_id,
                                                             mac_address=device_mac_address)
                        device_key = local_device.put()
                        device_uri = self.request.app.router.build(None,
                                                                   'manage-device',
                                                                   None,
                                                                   {'device_urlsafe_key': device_key.urlsafe()})
                        self.response.headers['Location'] = device_uri
                        self.response.headers.pop('Content-Type', None)
                        self.response.set_status(status)
                    else:
                        self.response.set_status(422,
                                                 'Chrome OS device not associated with this customer id ( {0}'.format(
                                                     self.CUSTOMER_ID))
            else:
                self.response.set_status(status, error_message)
        else:
            logging.info("Problem creating a ChromeOsDevice. No request body.")
            self.response.set_status(400, 'Did not receive request body.')

    @api_token_required
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
            local_device.put()
            self.response.headers.pop('Content-Type', None)
            self.response.set_status(204)

    @api_token_required
    def delete(self, device_urlsafe_key):
        device_key = ndb.Key(urlsafe=device_urlsafe_key)
        local_device = device_key.get()
        if local_device is None:
            self.response.set_status(422, 'Unable to retrieve ChromeOS device with device key: {0}'.format(
                device_urlsafe_key))
        else:
            local_device.key.delete()
            self.response.headers.pop('Content-Type', None)
            self.response.set_status(204)
