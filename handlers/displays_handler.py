import json
import logging

from webapp2 import RequestHandler
from google.appengine.ext import ndb

from app_config import config
from decorators import api_token_required
from ndb_mixins import PagingListHandlerMixin, KeyValidatorMixin
from restler.serializers import json_response
from chrome_os_devices_api import ChromeOsDevicesApi
from models import Display, Tenant
from strategy import DISPLAY_STRATEGY

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>, Bob MacNeal <bob.macneal@agosto.com>'


class DisplaysHandler(RequestHandler, PagingListHandlerMixin, KeyValidatorMixin):

    @api_token_required
    def get_list(self):
        mac_address = self.request.get('macAddress')
        if not mac_address:
            query = Display.query()
        else:
            query = Display.query(ndb.OR(Display.mac_address == mac_address,
                                    Display.ethernet_mac_address == mac_address))
        query_forward = query.order(Display.key)
        query_reverse = query.order(-Display.key)
        result_data = self.fetch_page(query_forward, query_reverse)
        json_response(self.response, result_data, strategy=DISPLAY_STRATEGY)


    # @api_token_required
    # def get_devices_by_tenant(self, tenant_urlsafe_key):
    #     tenant_key = ndb.Key(urlsafe=tenant_urlsafe_key)
    #     tenant = tenant_key.get()
    #     if tenant is not None:
    #         displays = Display.query(Display.tenant_key == tenant.key ).fetch()
    #         json_response(self.response, displays, strategy=DISPLAY_STRATEGY)
    #         self.response.set_status(200)
    #     else:
    #         message = 'Unable to retrieve by the device tenant_key: {0}'.format(tenant_urlsafe_key)
    #         json_response(self.response, {'error': message}, status_code=404)

    # @api_token_required
    # def get(self, device_urlsafe_key):
    #     try:
    #         key = ndb.Key(urlsafe=device_urlsafe_key)
    #     except Exception, e:
    #         logging.exception(e)
    #         return self.response.set_status(404)
    #     stored_display = key.get()
    #     if stored_display is None:
    #         return self.response.set_status(404)
    #     chrome_os_devices_api = ChromeOsDevicesApi(config.IMPERSONATION_ADMIN_EMAIL_ADDRESS)
    #     managed_display = chrome_os_devices_api.get(config.GOOGLE_CUSTOMER_ID, stored_display.device_id)
    #     result = {}
    #     if managed_display:
    #         result = managed_display
    #     try:
    #         tenant = stored_display.tenant_key.get()
    #     except Exception, e:
    #         logging.exception(e)
    #         return self.response.set_status(400)
    #     result['tenantCode'] = tenant.tenant_code
    #     result['contentServerUrl'] = tenant.content_server_url
    #     result['chromeDeviceDomain'] = tenant.chrome_device_domain
    #     result["gcmRegistrationId"] = stored_display.gcm_registration_id
    #     result["serialNumber"] = stored_display.serial_number
    #     result["managedDisplay"] = stored_display.managed_display
    #     result['created'] = stored_display.created.strftime('%Y-%m-%d %H:%M:%S')
    #     result['updated'] = stored_display.updated.strftime('%Y-%m-%d %H:%M:%S')
    #     result['apiKey'] = stored_display.api_key
    #     result['active'] = tenant.active
    #     result['key'] = stored_display.key.urlsafe()
    #     json_response(self.response, result)


    def get_all_managed_displays(self):
        chrome_os_devices_api = ChromeOsDevicesApi(config.IMPERSONATION_ADMIN_EMAIL_ADDRESS)
        managed_chrome_os_devices = chrome_os_devices_api.list(config.GOOGLE_CUSTOMER_ID)
        if managed_chrome_os_devices is not None:
            json_response(self.response, managed_chrome_os_devices)
            self.response.set_status(200)
        else:
            message = 'Unable to retrieve a list of ChromeOS devices.'
            json_response(self.response, {'error': message}, status_code=404)

    def get_display_by_mac_address(self, device_mac_address):
        chrome_os_devices_api = ChromeOsDevicesApi(config.IMPERSONATION_ADMIN_EMAIL_ADDRESS)
        managed_displays = chrome_os_devices_api.list(config.GOOGLE_CUSTOMER_ID)
        if managed_displays is not None:
            lowercase_device_mac_address = device_mac_address.lower()
            loop_comprehension = (x for x in managed_displays if x.get('macAddress') == lowercase_device_mac_address or
                                  x.get('ethernetMacAddress') == lowercase_device_mac_address)
            managed_display = next(loop_comprehension, None)
            if managed_display is not None:
                device_id = managed_display.get('deviceId')
                local_device = Display.get_by_device_id(device_id)
                if local_device is not None:
                    tenant = local_device.tenant_key.get()
                    managed_display['tenantCode'] = tenant.tenant_code
                    managed_display['contentServerUrl'] = tenant.content_server_url
                    managed_display['chromeDeviceDomain'] = tenant.chrome_device_domain
                    managed_display["gcmRegistrationId"] = local_device.gcm_registration_id
                    managed_display["serialNumber"] = local_device.serial_number
                    managed_display["managedDisplay"] = True
                    managed_display['created'] = local_device.created.strftime('%Y-%m-%d %H:%M:%S')
                    managed_display['updated'] = local_device.updated.strftime('%Y-%m-%d %H:%M:%S')
                    managed_display['apiKey'] = local_device.api_key
                    managed_display['key'] = local_device.key.urlsafe()
                    json_response(self.response, managed_display)
                else:
                    message = 'Device not stored for deviceId {0} and MAC address {1}.'.format(
                        device_id, device_mac_address)
                    json_response(self.response, {'error': message}, status_code=404)
            else:
                message = 'A ChromeOS display was not found to be associated with the MAC address: {0}.'.format(
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
            request_json = json.loads(self.request.body)
            display_mac_address = request_json.get(u'macAddress')
            device_exists = Display.query(Display.mac_address == display_mac_address).count() > 0
            if device_exists:
                status = 400
                error_message = 'Cannot create because MAC address has already been assigned to this display.'
            tenant_code = request_json.get(u'tenantCode')
            gcm_registration_id = request_json.get(u'gcmRegistrationId')
            if display_mac_address is None or display_mac_address == '':
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
                error_message = 'Invalid or inactive tenant for display.'
            if status == 201:
                chrome_os_devices_api = ChromeOsDevicesApi(config.IMPERSONATION_ADMIN_EMAIL_ADDRESS)
                managed_displays = chrome_os_devices_api.list(config.GOOGLE_CUSTOMER_ID)
                if managed_displays is not None:
                    loop_comprehension = (x for x in managed_displays if x.get('macAddress') == display_mac_address or
                                          x.get('ethernetMacAddress') == display_mac_address)
                    managed_display = next(loop_comprehension, None)
                    if managed_display is not None:
                        device_id = managed_display.get('deviceId')
                        display = Display.create(tenant_key=tenant_key,
                                                 device_id=device_id,
                                                 gcm_registration_id=gcm_registration_id,
                                                 mac_address=display_mac_address,
                                                 managed_display=True)
                        key = display.put()
                        display_uri = self.request.app.router.build(None,
                                                                    'manage-device',
                                                                    None,
                                                                    {'device_urlsafe_key': key.urlsafe()})
                        self.response.headers['Location'] = display_uri
                        self.response.headers.pop('Content-Type', None)
                        self.response.set_status(status)
                    else:
                        self.response.set_status(422,
                                                 'Chrome OS display not associated with this customer id ( {0}'.format(
                                                     config.GOOGLE_CUSTOMER_ID))
            else:
                self.response.set_status(status, error_message)
        else:
            logging.info("Problem creating Display. No request body.")
            self.response.set_status(400, 'Did not receive request body.')

    @api_token_required
    def put(self, device_urlsafe_key):
        status = 204
        message = None
        try:
            key = ndb.Key(urlsafe=device_urlsafe_key)
            display = key.get()
        except Exception, e:
            logging.exception(e)
            status = 404
            message = 'Unrecognized display with key: {0}'.format(device_urlsafe_key)
            return self.response.set_status(status, message)
        if display is None:
            status = 404
            message = 'Unrecognized display with key: {0}'.format(device_urlsafe_key)
        chrome_os_devices_api = ChromeOsDevicesApi(config.IMPERSONATION_ADMIN_EMAIL_ADDRESS)
        managed_chrome_os_device = chrome_os_devices_api.get(config.GOOGLE_CUSTOMER_ID, display.device_id)
        if managed_chrome_os_device is None:
            status = 404
            message = 'Unrecognized display id in Google API'
        else:
            request_json = json.loads(self.request.body)
            gcm_registration_id = request_json.get('gcmRegistrationId')
            if gcm_registration_id:
                display.gcm_registration_id = gcm_registration_id
            display.put()
            self.response.headers.pop('Content-Type', None)
        self.response.set_status(status, message)

    @api_token_required
    def delete(self, device_urlsafe_key):
        status = 204
        message = None
        try:
            key = ndb.Key(urlsafe=device_urlsafe_key)
            display = key.get()
        except Exception, e:
            logging.exception(e)
            status = 404
            message = 'Unrecognized display with key: {0}'.format(device_urlsafe_key)
            return self.response.set_status(status, message)
        if display is None:
            status = 404
            message = 'Unrecognized display with key: {0}'.format(device_urlsafe_key)
        if display is None:
            self.response.set_status(404, 'Unrecognized display with key: {0}'.format(
                device_urlsafe_key))
        else:
            display.key.delete()
            self.response.headers.pop('Content-Type', None)
        self.response.set_status(status, message)
