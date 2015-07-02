import json
import logging

from webapp2 import RequestHandler
from google.appengine.ext import ndb

from decorators import api_token_required
from restler.serializers import json_response
from chrome_os_devices_api import ChromeOsDevicesApi
from models import ChromeOsDevice, Tenant

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>, Bob MacNeal <bob.macneal@agosto.com>'


class DeviceResourceHandler(RequestHandler):
    ADMIN_ACCOUNT_TO_IMPERSONATE = 'administrator@skykit.com'
    CUSTOMER_ID = 'my_customer'

    @api_token_required
    def get(self, device_urlsafe_key):
        device_key = ndb.Key(urlsafe=device_urlsafe_key)
        local_device = device_key.get()
        chrome_os_devices_api = ChromeOsDevicesApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)
        chrome_os_device = chrome_os_devices_api.get(self.CUSTOMER_ID, local_device.device_id)
        result = {}
        if chrome_os_device:
            result = chrome_os_device
        tenant = local_device.key.parent().get()
        result['tenantCode'] = tenant.tenant_code
        result['contentServerUrl'] = tenant.content_server_url
        result['chromeDeviceDomain'] = tenant.chrome_device_domain
        result["gcmRegistrationId"] = local_device.gcm_registration_id
        result['created'] = local_device.created.strftime('%Y-%m-%d %H:%M:%S')
        result['updated'] = local_device.updated.strftime('%Y-%m-%d %H:%M:%S')
        result['apiKey'] = local_device.api_key
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
        # TODO loop through the list then for each device_id see if we have a device_id using a query.
        #
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

    @api_token_required
    def post(self):
        if self.request.body is not str('') and self.request.body is not None:
            request_json = json.loads(self.request.body)
            device_mac_address = request_json.get(u'macAddress')
            tenant_code = request_json.get(u'tenantCode')
            tenant_key = Tenant.query(Tenant.tenant_code == tenant_code).get(keys_only=True)
            logging.info('Retrieved tenant key: {0} by tenant code: {1}'.format(str(tenant_key), tenant_code))
            chrome_os_devices_api = ChromeOsDevicesApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)
            chrome_os_devices = chrome_os_devices_api.list(self.CUSTOMER_ID)
            if chrome_os_devices is not None:
                loop_comprehension = (x for x in chrome_os_devices if x.get('macAddress') == device_mac_address or
                                      x.get('ethernetMacAddress') == device_mac_address)
                chrome_os_device = next(loop_comprehension, None)
                if chrome_os_device is not None:
                    gcm_registration_id = request_json.get('gcmRegistrationId')
                    device_id = chrome_os_device.get('deviceId')
                    local_device = ChromeOsDevice.get_by_device_id(device_id)
                    logging.info('ChromeOsDevice retrieved by device_id: {}'.format(str(local_device)))
                    if local_device is None:
                        local_device = ChromeOsDevice.create(tenant_key=tenant_key,
                                                             device_id=device_id,
                                                             gcm_registration_id=gcm_registration_id)
                        self.response.set_status(201)
                    else:
                        local_device.gcm_registration_id = gcm_registration_id
                        self.response.set_status(204)
                    device_key = local_device.put()
                    logging.info("ChromeOsDevice.key: {0}".format(str(device_key.urlsafe())))
                    logging.info("ChromeOsDevice.key.parent() key: {0}".format(str(device_key.parent())))
                    device_uri = self.request.app.router.build(None,
                                                               'manage-device',
                                                               None,
                                                               {'device_urlsafe_key': device_key.urlsafe()})
                    self.response.headers['Location'] = device_uri
                    self.response.headers.pop('Content-Type', None)
                else:
                    logging.info("Problem creating a ChromeOsDevice. ")
                    self.response.set_status(422,
                                             'Chrome OS device not associated with this customer id ( {0}'.format(
                                                 self.CUSTOMER_ID))
        else:
            logging.info("Problem creating a ChromeOsDevice. No request body.")
            self.response.set_status(422, 'Did not receive request body.')

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
            self.response.set_status(422, 'Unable to retrieve ChromeOS device by device ID: {0}'.format(
                local_device.device_id))
        else:
            local_device.key.delete()
            self.response.headers.pop('Content-Type', None)
            self.response.set_status(204)
