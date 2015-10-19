import json
import logging

from google.appengine.ext.deferred import deferred
from webapp2 import RequestHandler
from google.appengine.ext import ndb
from decorators import api_token_required
from ndb_mixins import PagingListHandlerMixin, KeyValidatorMixin
from restler.serializers import json_response
from chrome_os_devices_api import (refresh_device, refresh_device_by_mac_address, update_chrome_os_device)
from models import ChromeOsDevice, Tenant, Domain, TenantEntityGroup
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
            query_results = query.fetch()
            if len(query_results) > 0:
                json_response(self.response, query_results[0], strategy=CHROME_OS_DEVICE_STRATEGY)
            else:
                error_message = "Unable to find Chrome OS device by MAC address: {0}".format(device_mac_address)
                self.response.set_status(404, error_message)
        else:
            query = ChromeOsDevice.query().order(ChromeOsDevice.created)
            # query_forward = query.order(ChromeOsDevice.key)
            # query_reverse = query.order(-ChromeOsDevice.key)
            # query_results = self.fetch_page(query_forward, query_reverse)
            # json_response(self.response, query_results, strategy=CHROME_OS_DEVICE_STRATEGY)
            query_results = query.fetch(1000)
            json_response(self.response, query_results, strategy=CHROME_OS_DEVICE_STRATEGY)

    @api_token_required
    def get_devices_by_tenant(self, tenant_urlsafe_key):
        tenant_key = ndb.Key(urlsafe=tenant_urlsafe_key)
        query = ChromeOsDevice.query(ChromeOsDevice.tenant_key == tenant_key)
        query_forward = query.order(ChromeOsDevice.key)
        query_reverse = query.order(-ChromeOsDevice.key)
        result_data = self.fetch_page(query_forward, query_reverse)
        json_response(self.response, result_data, strategy=CHROME_OS_DEVICE_STRATEGY)

    @api_token_required
    def get_devices_by_distributor(self, distributor_urlsafe_key):
        device_list = []
        distributor = ndb.Key(urlsafe=distributor_urlsafe_key)
        domain_keys = Domain.query(Domain.distributor_key == distributor).fetch(100, keys_only=True)
        tenant_list = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
        tenant_list = filter(lambda x: x.active is True, tenant_list)
        domain_tenant_list = filter(lambda x: x.domain_key in domain_keys, tenant_list)
        for tenant in domain_tenant_list:
            tenant_devices = Tenant.find_devices(tenant.key)
            for tenant_device in tenant_devices:
                device_list.append(tenant_device)
        json_response(self.response, device_list, strategy=CHROME_OS_DEVICE_STRATEGY)

    @api_token_required
    def get(self, device_urlsafe_key):
        device = self.validate_and_get(device_urlsafe_key, ChromeOsDevice, abort_on_not_found=True)
        deferred.defer(refresh_device, device_urlsafe_key=device_urlsafe_key, _queue='directory-api')
        json_response(self.response, device, strategy=CHROME_OS_DEVICE_STRATEGY)

    @api_token_required
    def post(self):
        if self.request.body is not str('') and self.request.body is not None:
            status = 201
            error_message = None
            request_json = json.loads(self.request.body)
            device_mac_address = request_json.get('macAddress')
            if device_mac_address is None or device_mac_address == '':
                status = 400
                error_message = 'The macAddress parameter is invalid.'
                self.response.set_status(status, error_message)
                return
            gcm_registration_id = request_json.get('gcmRegistrationId')
            if gcm_registration_id is None or gcm_registration_id == '':
                status = 400
                error_message = 'The gcmRegistrationId parameter is invalid.'
                self.response.set_status(status, error_message)
                return
            if self.unmanaged_device_registration_token is True:
                pass
            else:
                chrome_os_device_exists = ChromeOsDevice.query(
                    ndb.OR(ChromeOsDevice.mac_address == device_mac_address,
                           ChromeOsDevice.ethernet_mac_address == device_mac_address)).count() > 0
                if chrome_os_device_exists:
                    status = 400
                    error_message = 'Cannot create because macAddress has already been assigned to this device.'
                tenant_code = request_json.get('tenantCode')
                if tenant_code is None or tenant_code == '':
                    status = 400
                    error_message = 'The tenantCode parameter is invalid.'
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
                                   _queue='directory-api',
                                   _countdown=30)
                    deferred.defer(ContentManagerApi().create_device,
                                   device_urlsafe_key=key.urlsafe(),
                                   _queue='content-server',
                                   _countdown=5)
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
            notes = request_json.get('notes')
            if notes:
                device.notes = notes
            gcm_registration_id = request_json.get('gcmRegistrationId')
            if gcm_registration_id:
                logging.info('  PUT updating the gcmRegistrationId.')
                device.gcm_registration_id = gcm_registration_id
            tenant_code = request_json.get('tenantCode')
            if tenant_code:
                tenant = Tenant.find_by_tenant_code(tenant_code)
                if tenant and tenant.key != device.tenant_key:
                    logging.info('  PUT updating the tenant.')
                    device.tenant_key = tenant.key
                    device.put()
                    deferred.defer(ContentManagerApi().update_device,
                                   device_urlsafe_key=device.key.urlsafe(),
                                   _queue='content-server',
                                   _countdown=5)
            device.put()
            deferred.defer(update_chrome_os_device,
                           device_urlsafe_key=device.key.urlsafe(),
                           _queue='directory-api')
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
