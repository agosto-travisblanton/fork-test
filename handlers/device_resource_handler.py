import json
import logging
from google.appengine.ext.deferred import deferred
from webapp2 import RequestHandler
from google.appengine.ext import ndb
from decorators import api_token_required
from ndb_mixins import PagingListHandlerMixin, KeyValidatorMixin
from restler.serializers import json_response
from chrome_os_devices_api import (refresh_device, refresh_device_by_mac_address, update_chrome_os_device)
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
                               device_urlsafe_key=key.urlsafe(),
                               device_mac_address=device_mac_address,
                               _queue='directory-api')
                content_manager_api = ContentManagerApi()
                try:
                    deferred.defer(content_manager_api.create_device,
                                   chrome_os_device=device,
                                   _queue='content-server')
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
        device = None
        try:
            device = ndb.Key(urlsafe=device_urlsafe_key).get()
        except Exception, e:
            logging.exception(e)
        if device is None:
            status = 404
            message = 'Unrecognized device with key: {0}'.format(device_urlsafe_key)
        else:
            request_json = json.loads(self.request.body)
            gcm_registration_id = request_json.get('gcm_registration_id')
            if gcm_registration_id:
                logging.info('  PUT updating the gcm_registration_id.')
                device.gcm_registration_id = gcm_registration_id
            tenant_key = ndb.Key(urlsafe=request_json.get('tenant_key'))
            if tenant_key != device.tenant_key:
                logging.info('  PUT updating the tenant.')
                device.tenant_key = tenant_key
            device.put()
            deferred.defer(update_chrome_os_device, device_urlsafe_key=device.key.urlsafe())
            self.response.headers.pop('Content-Type', None)
        self.response.set_status(status, message)

    @api_token_required
    def delete(self, device_urlsafe_key):
        status = 204
        message = None
        device = None
        try:
            device = ndb.Key(urlsafe=device_urlsafe_key).get()
        except Exception, e:
            logging.exception(e)
        if device is None:
            status = 404
            message = 'Unrecognized device with key: {0}'.format(device_urlsafe_key)
        else:
            device.key.delete()
            self.response.headers.pop('Content-Type', None)
        self.response.set_status(status, message)
