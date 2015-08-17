# import json
# import logging
#
# from google.appengine.ext.deferred import deferred
# from webapp2 import RequestHandler
#
# from google.appengine.ext import ndb
#
# from app_config import config
# from chrome_os_devices_api import ChromeOsDevicesApi
# from content_manager_api import ContentManagerApi
# from decorators import api_token_required
# from ndb_mixins import PagingListHandlerMixin, KeyValidatorMixin
# from restler.serializers import json_response
# from chrome_os_devices_api import (refresh_device)
# from models import ChromeOsDevice, Tenant
# from strategy import CHROME_OS_DEVICE_STRATEGY

import json
import logging

from google.appengine.ext.deferred import deferred
from webapp2 import RequestHandler

from google.appengine.ext import ndb

from decorators import api_token_required
from ndb_mixins import PagingListHandlerMixin, KeyValidatorMixin
from restler.serializers import json_response
from chrome_os_devices_api import (refresh_device, refresh_device_by_mac_address)
from models import ChromeOsDevice, Tenant
from content_manager_api import ContentManagerApi
from strategy import CHROME_OS_DEVICE_STRATEGY

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>, Bob MacNeal <bob.macneal@agosto.com>'


class DeviceResourceHandler(RequestHandler, PagingListHandlerMixin, KeyValidatorMixin):
    @api_token_required
    def get_list(self):
        device_mac_address = self.request.get('macAddress')
        if device_mac_address:
            query = ChromeOsDevice.query(ndb.OR(ChromeOsDevice.mac_address == device_mac_address,
                                                ChromeOsDevice.ethernet_mac_address == device_mac_address))
        else:
            query = ChromeOsDevice.query()
        query_forward = query.order(ChromeOsDevice.key)
        query_reverse = query.order(-ChromeOsDevice.key)
        result_data = self.fetch_page(query_forward, query_reverse)
        json_response(self.response, result_data, strategy=CHROME_OS_DEVICE_STRATEGY)

    @api_token_required
    def get_devices_by_tenant(self, tenant_urlsafe_key):
        tenant_key = ndb.Key(urlsafe=tenant_urlsafe_key)
        query = ChromeOsDevice.query(ChromeOsDevice.tenant_key == tenant_key)
        query_forward = query.order(ChromeOsDevice.key)
        query_reverse = query.order(-ChromeOsDevice.key)
        result_data = self.fetch_page(query_forward, query_reverse)
        json_response(self.response, result_data, strategy=CHROME_OS_DEVICE_STRATEGY)

    @api_token_required
    def get(self, device_urlsafe_key):
        try:
            key = ndb.Key(urlsafe=device_urlsafe_key)
        except Exception, e:
            logging.exception(e)
            return self.response.set_status(404)
        device = key.get()
        if device is None:
            return self.response.set_status(404)
        deferred.defer(refresh_device, device_urlsafe_key=device_urlsafe_key)
        json_response(self.response, device, strategy=CHROME_OS_DEVICE_STRATEGY)

    # @api_token_required
    # def get_devices_by_tenant(self, tenant_urlsafe_key):
    #     tenant_key = ndb.Key(urlsafe=tenant_urlsafe_key)
    #     tenant = tenant_key.get()
    #     if tenant is not None:
    #         chrome_os_devices = ChromeOsDevice.query(ChromeOsDevice.tenant_key == tenant_key).fetch()
    #         json_response(self.response, chrome_os_devices, strategy=CHROME_OS_DEVICE_STRATEGY)
    #         self.response.set_status(200)
    #     else:
    #         message = 'Unable to retrieve the tenant by key: {0}'.format(tenant_urlsafe_key)
    #         json_response(self.response, {'error': message}, status_code=404)


    # @api_token_required
    # def get(self, device_urlsafe_key):
    #     try:
    #         device_key = ndb.Key(urlsafe=device_urlsafe_key)
    #     except Exception, e:
    #         logging.exception(e)
    #         logging.info('Unrecognized device with device key: {0}'.format(device_urlsafe_key))
    #         return self.response.set_status(404)
    #     local_device = device_key.get()
    #     if local_device is None:
    #         logging.info('Unrecognized device with device key: {0}'.format(device_urlsafe_key))
    #         return self.response.set_status(404)
    #     chrome_os_devices_api = ChromeOsDevicesApi(config.IMPERSONATION_ADMIN_EMAIL_ADDRESS)
    #     chrome_os_device = chrome_os_devices_api.get(config.GOOGLE_CUSTOMER_ID, local_device.device_id)
    #     result = {}
    #     if chrome_os_device:
    #         result = chrome_os_device
    #     if local_device.tenant_key:
    #         try:
    #             tenant = local_device.tenant_key.get()
    #         except Exception, e:
    #             logging.exception(e)
    #             logging.info('No parent tenant for device key: {0}'.format(device_urlsafe_key))
    #             return self.response.set_status(400)
    #     else:
    #         logging.info('No parent tenant for device key: {0}'.format(device_urlsafe_key))
    #         return self.response.set_status(400)
    #     result['tenantCode'] = tenant.tenant_code
    #     result['contentServerUrl'] = tenant.content_server_url
    #     result['chromeDeviceDomain'] = tenant.chrome_device_domain
    #     result["gcmRegistrationId"] = local_device.gcm_registration_id
    #     result['created'] = local_device.created.strftime('%Y-%m-%d %H:%M:%S')
    #     result['updated'] = local_device.updated.strftime('%Y-%m-%d %H:%M:%S')
    #     result['apiKey'] = local_device.api_key
    #     result['active'] = tenant.active
    #     result['key'] = local_device.key.urlsafe()
    #     json_response(self.response, result)

    # @api_token_required
    # def get_list(self):
    #     device_mac_address = self.request.get('macAddress')
    #     if not device_mac_address:
    #         self.get_all_devices()
    #     else:
    #         self.get_device_by_mac_address(device_mac_address)

    # def get_all_devices(self):
    #     chrome_os_devices_api = ChromeOsDevicesApi(config.IMPERSONATION_ADMIN_EMAIL_ADDRESS)
    #     chrome_os_devices = chrome_os_devices_api.list(config.GOOGLE_CUSTOMER_ID)
    #     if chrome_os_devices is not None:
    #         for chrome_os_device in chrome_os_devices:
    #             device_id = chrome_os_device.get('deviceId')
    #             local_device = ChromeOsDevice.get_by_device_id(device_id)
    #             if local_device is not None:
    #                 if local_device.tenant_key is not None:
    #                     tenant = local_device.tenant_key.get()
    #                     chrome_os_device['tenantCode'] = tenant.tenant_code
    #                     chrome_os_device['contentServerUrl'] = tenant.content_server_url
    #                     chrome_os_device['chromeDeviceDomain'] = tenant.chrome_device_domain
    #                     chrome_os_device["gcmRegistrationId"] = local_device.gcm_registration_id
    #                     chrome_os_device['created'] = local_device.created.strftime('%Y-%m-%d %H:%M:%S')
    #                     chrome_os_device['updated'] = local_device.updated.strftime('%Y-%m-%d %H:%M:%S')
    #                     chrome_os_device['apiKey'] = local_device.api_key
    #                     chrome_os_device['key'] = local_device.key.urlsafe()
    #                 else:
    #                     message = 'No tenant_key for device'
    #                     json_response(self.response, {'error': message}, status_code=422)
    #         json_response(self.response, chrome_os_devices)
    #         self.response.set_status(200)
    #     else:
    #         message = 'Unable to retrieve a list of ChromeOS devices.'
    #         json_response(self.response, {'error': message}, status_code=404)

    # def get_device_by_mac_address(self, device_mac_address):
    #     chrome_os_devices_api = ChromeOsDevicesApi(config.IMPERSONATION_ADMIN_EMAIL_ADDRESS)
    #     chrome_os_devices = chrome_os_devices_api.list(config.GOOGLE_CUSTOMER_ID)
    #     if chrome_os_devices is not None:
    #         lowercase_device_mac_address = device_mac_address.lower()
    #         loop_comprehension = (x for x in chrome_os_devices if x.get('macAddress') == lowercase_device_mac_address or
    #                               x.get('ethernetMacAddress') == lowercase_device_mac_address)
    #         chrome_os_device = next(loop_comprehension, None)
    #         if chrome_os_device is not None:
    #             device_id = chrome_os_device.get('deviceId')
    #             local_device = ChromeOsDevice.get_by_device_id(device_id)
    #             if local_device is not None:
    #                 if local_device.tenant_key is not None:
    #                     tenant = local_device.tenant_key.get()
    #                     chrome_os_device['tenantCode'] = tenant.tenant_code
    #                     chrome_os_device['contentServerUrl'] = tenant.content_server_url
    #                     chrome_os_device['chromeDeviceDomain'] = tenant.chrome_device_domain
    #                     chrome_os_device["gcmRegistrationId"] = local_device.gcm_registration_id
    #                     chrome_os_device['created'] = local_device.created.strftime('%Y-%m-%d %H:%M:%S')
    #                     chrome_os_device['updated'] = local_device.updated.strftime('%Y-%m-%d %H:%M:%S')
    #                     chrome_os_device['apiKey'] = local_device.api_key
    #                     chrome_os_device['key'] = local_device.key.urlsafe()
    #                     json_response(self.response, chrome_os_device)
    #                 else:
    #                     message = 'No tenant key for deviceId {0} and MAC address {1}.'.format(
    #                         device_id, device_mac_address)
    #                     json_response(self.response, {'error': message}, status_code=422)
    #             else:
    #                 message = 'Device not stored for deviceId {0} and MAC address {1}.'.format(
    #                     device_id, device_mac_address)
    #                 json_response(self.response, {'error': message}, status_code=404)
    #         else:
    #             message = 'A ChromeOS device was not found to be associated with the MAC address: {0}.'.format(
    #                 device_mac_address)
    #             json_response(self.response, {'error': message}, status_code=404)
    #     else:
    #         message = 'Unable to retrieve a list of ChromeOS devices.'
    #         json_response(self.response, {'error': message}, status_code=404)

    # @api_token_required
    # def post(self):
    #     if self.request.body is not str('') and self.request.body is not None:
    #         status = 201
    #         error_message = None
    #         logging.info('Request body: {0}'.format(self.request.body))
    #         request_json = json.loads(self.request.body)
    #         device_mac_address = request_json.get(u'macAddress')
    #         device_exists = ChromeOsDevice.query(ChromeOsDevice.mac_address == device_mac_address).count() > 0
    #         if device_exists:
    #             status = 400
    #             error_message = 'Cannot create because MAC address has already been assigned to this device.'
    #         tenant_code = request_json.get(u'tenantCode')
    #         gcm_registration_id = request_json.get(u'gcmRegistrationId')
    #         if device_mac_address is None or device_mac_address == '':
    #             status = 400
    #             error_message = 'The macAddress parameter was not valid.'
    #         if tenant_code is None or tenant_code == '':
    #             status = 400
    #             error_message = 'The tenantCode parameter was not valid.'
    #         if gcm_registration_id is None or gcm_registration_id == '':
    #             status = 400
    #             error_message = 'The gcmRegistrationId parameter was not valid.'
    #         tenant_key = Tenant.query(Tenant.tenant_code == tenant_code, Tenant.active == True).get(keys_only=True)
    #         if tenant_key is None:
    #             status = 400
    #             error_message = 'Invalid or inactive tenant for device.'
    #         if status == 201:
    #             chrome_os_devices_api = ChromeOsDevicesApi(config.IMPERSONATION_ADMIN_EMAIL_ADDRESS)
    #             chrome_os_devices = chrome_os_devices_api.list(config.GOOGLE_CUSTOMER_ID)
    #             if chrome_os_devices is not None:
    #                 loop_comprehension = (x for x in chrome_os_devices if x.get('macAddress') == device_mac_address or
    #                                       x.get('ethernetMacAddress') == device_mac_address)
    #                 chrome_os_device = next(loop_comprehension, None)
    #                 if chrome_os_device is not None:
    #                     device_id = chrome_os_device.get('deviceId')
    #                     model = chrome_os_device.get('model')
    #                     serial_number = chrome_os_device.get('serialNumber')
    #                     local_device = ChromeOsDevice.create(tenant_key=tenant_key,
    #                                                          device_id=device_id,
    #                                                          gcm_registration_id=gcm_registration_id,
    #                                                          mac_address=device_mac_address,
    #                                                          serial_number=serial_number,
    #                                                          model=model)
    #                     device_key = local_device.put()
    #                     content_manager_api = ContentManagerApi()
    #                     notify_content_manager = content_manager_api.create_device(local_device)
    #                     if not notify_content_manager:
    #                         logging.info('Failed to notify content manager about new device')
    #                     device_uri = self.request.app.router.build(None,
    #                                                                'manage-device',
    #                                                                None,
    #                                                                {'device_urlsafe_key': device_key.urlsafe()})
    #                     self.response.headers['Location'] = device_uri
    #                     self.response.headers.pop('Content-Type', None)
    #                     self.response.set_status(status)
    #                 else:
    #                     logging.info('Chrome OS device not associated with this customer id ( {0}'.format(
    #                         config.GOOGLE_CUSTOMER_ID))
    #                     self.response.set_status(422,
    #                                              'Chrome OS device not associated with this customer id ( {0}'.format(
    #                                                  config.GOOGLE_CUSTOMER_ID))
    #         else:
    #             logging.info('INVALID REQUEST: {0}'.format(error_message))
    #             self.response.set_status(status, error_message)
    #     else:
    #         logging.info("Problem creating a ChromeOsDevice. No request body.")
    #         self.response.set_status(400, 'Did not receive request body.')
    #

    @api_token_required
    def post(self):
        if self.request.body is not str('') and self.request.body is not None:
            status = 201
            error_message = None
            request_json = json.loads(self.request.body)
            device_mac_address = request_json.get('macAddress')
            device_exists = ChromeOsDevice.query(
                ndb.OR(ChromeOsDevice.mac_address == device_mac_address,
                       ChromeOsDevice.ethernet_mac_address == device_mac_address)).count() > 0
            if device_exists:
                status = 400
                error_message = 'Cannot create because macAddress has already been assigned to this device.'
            tenant_code = request_json.get('tenantCode')
            gcm_registration_id = request_json.get('gcmRegistrationId')
            if device_mac_address is None or device_mac_address == '':
                status = 400
                error_message = 'The macAddress parameter is invalid.'
            if tenant_code is None or tenant_code == '':
                status = 400
                error_message = 'The tenantCode parameter is invalid.'
            if gcm_registration_id is None or gcm_registration_id == '':
                status = 400
                error_message = 'The gcmRegistrationId parameter is invalid.'
            tenant_key = Tenant.query(Tenant.tenant_code == tenant_code, Tenant.active == True).get(keys_only=True)
            if tenant_key is None:
                status = 400
                error_message = 'Invalid or inactive tenant for device.'
            if status == 201:
                device = ChromeOsDevice.create(tenant_key=tenant_key,
                                               gcm_registration_id=gcm_registration_id,
                                               mac_address=device_mac_address)
                key = device.put()
                deferred.defer(refresh_device_by_mac_address,
                               display_urlsafe_key=key.urlsafe(),
                               device_mac_address=device_mac_address,
                               _countdown=30)
                content_manager_api = ContentManagerApi()
                try:
                    deferred.defer(content_manager_api.create_device,
                                   chrome_os_device=device,
                                   _countdown=30)
                except Exception, e:
                    logging.exception(e)
                device_uri = self.request.app.router.build(None,
                                                           'manage-device',
                                                           None,
                                                           {'device_urlsafe_key': key.urlsafe()})
                self.response.headers['Location'] = device_uri
                self.response.headers.pop('Content-Type', None)
                self.response.set_status(status)
            else:
                self.response.set_status(status, error_message)
        else:
            logging.info("Problem creating Device. No request body.")
            self.response.set_status(400, 'Did not receive request body.')

    @api_token_required
    def put(self, device_urlsafe_key):
        status = 204
        message = None
        try:
            device_key = ndb.Key(urlsafe=device_urlsafe_key)
            local_device = device_key.get()
        except Exception, e:
            logging.exception(e)
            status = 404
            message = 'Unrecognized device with key: {0}'.format(device_urlsafe_key)
            return self.response.set_status(status, message)
        if local_device is None:
            status = 404
            message = 'Unrecognized device with key: {0}'.format(device_urlsafe_key)
        chrome_os_devices_api = ChromeOsDevicesApi(config.IMPERSONATION_ADMIN_EMAIL_ADDRESS)
        registered_chrome_os_device = chrome_os_devices_api.get(config.GOOGLE_CUSTOMER_ID, local_device.device_id)
        if registered_chrome_os_device is None:
            status = 404
            message = 'Unrecognized device id in Google API'
        else:
            request_json = json.loads(self.request.body)
            gcm_registration_id = request_json.get('gcmRegistrationId')
            if gcm_registration_id:
                local_device.gcm_registration_id = gcm_registration_id
            local_device.put()
            self.response.headers.pop('Content-Type', None)
        self.response.set_status(status, message)

    @api_token_required
    def delete(self, device_urlsafe_key):
        status = 204
        message = None
        try:
            device_key = ndb.Key(urlsafe=device_urlsafe_key)
            local_device = device_key.get()
        except Exception, e:
            logging.exception(e)
            status = 404
            message = 'Unrecognized device with key: {0}'.format(device_urlsafe_key)
            return self.response.set_status(status, message)
        if local_device is None:
            status = 404
            message = 'Unrecognized device with key: {0}'.format(device_urlsafe_key)
        if local_device is None:
            self.response.set_status(404, 'Unrecognized device with key: {0}'.format(
                device_urlsafe_key))
        else:
            local_device.key.delete()
            self.response.headers.pop('Content-Type', None)
        self.response.set_status(status, message)
