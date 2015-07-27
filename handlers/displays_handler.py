import json
import logging

from google.appengine.ext.deferred import deferred
from webapp2 import RequestHandler

from google.appengine.ext import ndb

from decorators import api_token_required
from ndb_mixins import PagingListHandlerMixin, KeyValidatorMixin
from restler.serializers import json_response
from chrome_os_devices_api import (refresh_display,
                                   refresh_display_by_mac_address,
                                   update_chrome_os_device)
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

    @api_token_required
    def get_displays_by_tenant(self, tenant_urlsafe_key):
        tenant_key = ndb.Key(urlsafe=tenant_urlsafe_key)
        query = Display.query(Display.tenant_key == tenant_key)
        query_forward = query.order(Display.key)
        query_reverse = query.order(-Display.key)
        result_data = self.fetch_page(query_forward, query_reverse)
        json_response(self.response, result_data, strategy=DISPLAY_STRATEGY)

    @api_token_required
    def get(self, display_urlsafe_key):
        try:
            key = ndb.Key(urlsafe=display_urlsafe_key)
        except Exception, e:
            logging.exception(e)
            return self.response.set_status(404)
        display = key.get()
        if display is None:
            return self.response.set_status(404)
        deferred.defer(refresh_display, display_urlsafe_key=display_urlsafe_key)
        json_response(self.response, display, strategy=DISPLAY_STRATEGY)

    @api_token_required
    def post(self):
        if self.request.body is not str('') and self.request.body is not None:
            status = 201
            error_message = None
            request_json = json.loads(self.request.body)
            display_mac_address = request_json.get('macAddress')
            device_exists = Display.query(ndb.OR(Display.mac_address == display_mac_address,
                                                 Display.ethernet_mac_address == display_mac_address)).count() > 0
            if device_exists:
                status = 400
                error_message = 'Cannot create because MAC address has already been assigned to this display.'
            tenant_code = request_json.get('tenantCode')
            gcm_registration_id = request_json.get('gcmRegistrationId')
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
                display = Display.create(tenant_key=tenant_key,
                                         gcm_registration_id=gcm_registration_id,
                                         mac_address=display_mac_address,
                                         managed_display=True)
                key = display.put()
                deferred.defer(refresh_display_by_mac_address,
                               display_urlsafe_key=key.urlsafe(),
                               device_mac_address=display_mac_address)
                display_uri = self.request.app.router.build(None,
                                                            'manage-display',
                                                            None,
                                                            {'display_urlsafe_key': key.urlsafe()})
                self.response.headers['Location'] = display_uri
                self.response.headers.pop('Content-Type', None)
                self.response.set_status(status)
            else:
                self.response.set_status(status, error_message)
        else:
            logging.info("Problem creating Display. No request body.")
            self.response.set_status(400, 'Did not receive request body.')

    @api_token_required
    def put(self, display_urlsafe_key):
        status = 204
        message = None
        display = None
        try:
            display = ndb.Key(urlsafe=display_urlsafe_key).get()
        except Exception, e:
            logging.exception(e)
        if display is None:
            status = 404
            message = 'Unrecognized display with key: {0}'.format(display_urlsafe_key)
        else:
            request_json = json.loads(self.request.body)
            gcm_registration_id = request_json.get('gcmRegistrationId')
            if gcm_registration_id:
                display.gcm_registration_id = gcm_registration_id
            display.put()
            deferred.defer(update_chrome_os_device, display_urlsafe_key=display.key.urlsafe())
            self.response.headers.pop('Content-Type', None)
        self.response.set_status(status, message)

    @api_token_required
    def delete(self, display_urlsafe_key):
        status = 204
        message = None
        display = None
        try:
            display = ndb.Key(urlsafe=display_urlsafe_key).get()
        except Exception, e:
            logging.exception(e)
        if display is None:
            status = 404
            message = 'Unrecognized display with key: {0}'.format(display_urlsafe_key)
        else:
            display.key.delete()
            self.response.headers.pop('Content-Type', None)
        self.response.set_status(status, message)
