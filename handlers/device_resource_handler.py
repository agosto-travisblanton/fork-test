import json
import logging

from datetime import datetime
from google.appengine.ext import ndb
from google.appengine.ext.deferred import deferred
from webapp2 import RequestHandler

from app_config import config
from decorators import requires_api_token, requires_registration_token, requires_unmanaged_registration_token
from device_commands_handler import DeviceCommandsHandler
from device_message_processor import post_unmanaged_device_info, change_intent
from integrations.content_manager.content_manager_api import ContentManagerApi
from model_entities.integration_events_log_model import IntegrationEventLog
from models import ChromeOsDevice, Tenant, Domain, TenantEntityGroup, DeviceIssueLog
from ndb_mixins import PagingListHandlerMixin, KeyValidatorMixin
from restler.serializers import json_response
from strategy import CHROME_OS_DEVICE_STRATEGY, DEVICE_PAIRING_CODE_STRATEGY, DEVICE_ISSUE_LOG_STRATEGY
from utils.email_notify import EmailNotify
from utils.timezone_util import TimezoneUtil
from workflow.refresh_device import refresh_device
from workflow.refresh_device_by_mac_address import refresh_device_by_mac_address
from workflow.register_device import register_device
from workflow.update_chrome_os_device import update_chrome_os_device

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>, Bob MacNeal <bob.macneal@agosto.com>'


class DeviceResourceHandler(RequestHandler, PagingListHandlerMixin, KeyValidatorMixin):
    MAILGUN_QUEUED_MESSAGE = 'Queued. Thank you.'

    ############################################################################################
    # HELPER METHODS
    ############################################################################################
    @staticmethod
    def ethernet_or_wifi_mac_address(device, partial_mac):
        if partial_mac and partial_mac in device.mac_address:
            return device.mac_address
        elif partial_mac == "null":
            return device.mac_address
        else:
            return device.ethernet_mac_address

    ############################################################################################
    # TENANTS VIEW
    ############################################################################################
    @requires_api_token
    def search_for_device_by_tenant(self, tenant_urlsafe_key):
        unmanaged = self.request.get("unmanaged") == "true"
        partial_gcmid = self.request.get("partial_gcmid")
        partial_serial = self.request.get("partial_serial")
        partial_mac = self.request.get("partial_mac")
        tenant_key = ndb.Key(urlsafe=tenant_urlsafe_key)

        if partial_gcmid:
            resulting_devices = Tenant.find_devices_with_partial_gcmid(
                tenant_keys=[tenant_key],
                unmanaged=unmanaged,
                partial_gcmid=partial_gcmid
            )

        elif partial_serial:
            resulting_devices = Tenant.find_devices_with_partial_serial(
                tenant_keys=[tenant_key],
                unmanaged=unmanaged,
                partial_serial=partial_serial
            )
        elif partial_mac:
            resulting_devices = Tenant.find_devices_with_partial_mac(
                tenant_keys=[tenant_key],
                unmanaged=unmanaged,
                partial_mac=partial_mac
            )

        json_response(
            self.response,
            {
                "matches": [
                    {
                        "serial": device.serial_number,
                        "mac": DeviceResourceHandler.ethernet_or_wifi_mac_address(device, partial_mac),
                        "key": device.key.urlsafe(),
                        "tenantKey": device.tenant_key.urlsafe(),
                        "gcmid": device.gcm_registration_id
                    } for device in resulting_devices]
            },
        )

    @requires_api_token
    def get_devices_by_tenant(self, tenant_urlsafe_key):
        tenant_key = ndb.Key(urlsafe=tenant_urlsafe_key)
        next_cursor = self.request.get("next_cursor")
        prev_cursor = self.request.get("prev_cursor")
        cur_next_cursor = next_cursor if next_cursor != "null" else None
        cur_prev_cursor = prev_cursor if prev_cursor != "null" else None
        unmanaged_filter = self.request.get('unmanaged')
        unmanaged = not bool(unmanaged_filter == '' or str(unmanaged_filter) == 'false')

        tenant_devices = Tenant.find_devices_paginated(
            tenant_keys=[tenant_key],
            unmanaged=unmanaged,
            prev_cursor_str=cur_prev_cursor,
            next_cursor_str=cur_next_cursor,
        )

        json_response(
            self.response,
            {
                "devices": tenant_devices["objects"],
                "next_cursor": tenant_devices["next_cursor"],
                "prev_cursor": tenant_devices["prev_cursor"],
            },
            strategy=CHROME_OS_DEVICE_STRATEGY
        )

    ############################################################################################
    # (DISTRIBUTOR) DEVICES VIEW
    ############################################################################################
    @requires_api_token
    def get_devices_by_distributor(self, distributor_urlsafe_key):
        next_cursor = self.request.get("next_cursor")
        prev_cursor = self.request.get("prev_cursor")
        cur_next_cursor = next_cursor if next_cursor != "null" else None
        cur_prev_cursor = prev_cursor if prev_cursor != "null" else None
        unmanaged_filter = self.request.get('unmanaged')

        unmanaged = not bool(unmanaged_filter == '' or str(unmanaged_filter) == 'false')
        domain_tenant_list = DeviceResourceHandler.get_domain_tenant_list_from_distributor(distributor_urlsafe_key)
        tenant_keys = [tenant.key for tenant in domain_tenant_list]

        distributor_devices = Tenant.find_devices_paginated(
            tenant_keys=tenant_keys,
            unmanaged=unmanaged,
            prev_cursor_str=cur_prev_cursor,
            next_cursor_str=cur_next_cursor
        )

        prev_cursor = distributor_devices["prev_cursor"]
        next_cursor = distributor_devices["next_cursor"]
        devices = distributor_devices["objects"]

        json_response(
            self.response,
            {
                "devices": devices,
                "next_cursor": next_cursor,
                "prev_cursor": prev_cursor,

            },
            strategy=CHROME_OS_DEVICE_STRATEGY
        )

    @requires_api_token
    def search_for_device(self, distributor_urlsafe_key):
        unmanaged = self.request.get("unmanaged") == "true"
        partial_gcmid = self.request.get("partial_gcmid")
        partial_serial = self.request.get("partial_serial")
        partial_mac = self.request.get("partial_mac")

        if partial_gcmid:
            resulting_devices = Tenant.find_devices_with_partial_gcmid_of_distributor(
                distributor_urlsafe_key=distributor_urlsafe_key,
                unmanaged=unmanaged,
                partial_gcmid=partial_gcmid
            )

        elif partial_serial:
            resulting_devices = Tenant.find_devices_with_partial_serial_of_distributor(
                distributor_urlsafe_key=distributor_urlsafe_key,
                unmanaged=unmanaged,
                partial_serial=partial_serial
            )
        elif partial_mac:
            resulting_devices = Tenant.find_devices_with_partial_mac_of_distributor(
                distributor_urlsafe_key=distributor_urlsafe_key,
                unmanaged=unmanaged,
                partial_mac=partial_mac
            )

        json_response(
            self.response,
            {
                "matches": [
                    {
                        "mac": DeviceResourceHandler.ethernet_or_wifi_mac_address(device, partial_mac),
                        "serial": device.serial_number,
                        "key": device.key.urlsafe(),
                        "tenantKey": device.tenant_key.urlsafe(),
                        "gcmid": device.gcm_registration_id
                    } for device in resulting_devices]
            },
        )

    ############################################################################################
    # END DEVICES VIEW
    ############################################################################################
    @requires_api_token
    def get_device_by_parameter(self):
        pairing_code = self.request.get('pairingCode')
        gcm_registration_id = self.request.get('gcmRegistrationId')
        device_mac_address = self.request.get('macAddress')
        has_pairing_code = pairing_code is not None and str(pairing_code) is not ''
        has_gcm_registration_id = gcm_registration_id is not None and str(gcm_registration_id) is not ''
        has_device_mac_address = device_mac_address is not None and str(device_mac_address) is not ''
        valid_input = has_pairing_code or (has_gcm_registration_id and has_device_mac_address)
        if valid_input:
            if pairing_code:
                query_results = ChromeOsDevice.get_by_pairing_code(pairing_code)
                if len(query_results) == 1:
                    json_response(self.response, query_results[0], strategy=CHROME_OS_DEVICE_STRATEGY)
                elif len(query_results) > 1:
                    json_response(self.response, query_results[0], strategy=CHROME_OS_DEVICE_STRATEGY)
                    error_message = "Multiple devices have pairing code {0}".format(pairing_code)
                    logging.error(error_message)
                else:
                    message = "Unable to find device by pairing code: {0}".format(pairing_code)
                    self.response.set_status(404, message)
                return

            query_results = ChromeOsDevice.get_by_gcm_registration_id(gcm_registration_id)
            if len(query_results) == 1:
                json_response(self.response, query_results[0], strategy=CHROME_OS_DEVICE_STRATEGY)
            elif len(query_results) > 1:
                json_response(self.response, query_results[0], strategy=CHROME_OS_DEVICE_STRATEGY)
                error_message = "Multiple devices have GCM registration ID {0}".format(gcm_registration_id)
                logging.error(error_message)
            else:
                query_results = ChromeOsDevice.get_by_mac_address(device_mac_address)
                if len(query_results) == 1:
                    if ChromeOsDevice.is_rogue_unmanaged_device(device_mac_address):
                        self.delete(query_results[0].key.urlsafe())
                        error_message = "Rogue unmanaged device with MAC address: {0} no longer exists.".format(
                            device_mac_address)
                        self.response.set_status(404, error_message)
                    else:
                        json_response(self.response, query_results[0], strategy=CHROME_OS_DEVICE_STRATEGY)
                elif len(query_results) > 1:
                    json_response(self.response, query_results[0], strategy=CHROME_OS_DEVICE_STRATEGY)
                    error_message = "Multiple devices have MAC address {0}".format(device_mac_address)
                    logging.error(error_message)
                else:
                    error_message = "Unable to find device by GCM registration ID: {0} or MAC address: {1}".format(
                        gcm_registration_id, device_mac_address)
                    self.response.set_status(404, error_message)
        else:
            self.response.set_status(400)
        return

    @requires_api_token
    def get(self, device_urlsafe_key):
        device = self.validate_and_get(device_urlsafe_key, ChromeOsDevice, abort_on_not_found=True,
                                       use_app_engine_memcache=False)
        if device.archived:
            status = 404
            message = 'Device with key: {0} archived.'.format(device_urlsafe_key)
            return self.response.set_status(status, message)
        if device.timezone:
            device.timezone_offset = TimezoneUtil.get_timezone_offset(device.timezone)
        else:
            device.timezone_offset = TimezoneUtil.get_timezone_offset('America/Chicago')
        if self.is_unmanaged_device is False:
            if not device.device_id:
                deferred.defer(refresh_device_by_mac_address,
                               device_urlsafe_key=device_urlsafe_key,
                               device_mac_address=device.mac_address,
                               device_has_previous_directory_api_info=False,
                               _queue='directory-api',
                               _countdown=5)
            else:
                deferred.defer(refresh_device,
                               device_urlsafe_key=device_urlsafe_key,
                               _queue='directory-api',
                               _countdown=5)
        return json_response(self.response, device, strategy=CHROME_OS_DEVICE_STRATEGY)

    @requires_unmanaged_registration_token
    def get_pairing_code(self, device_urlsafe_key):
        device = self.validate_and_get(device_urlsafe_key, ChromeOsDevice, abort_on_not_found=True)
        if device is None:
            status = 404
            message = 'Unrecognized device_key: {0}'.format(device_urlsafe_key)
            return self.response.set_status(status, message)
        elif device.archived:
            status = 404
            message = 'Device with key: {0} archived.'.format(device_urlsafe_key)
            return self.response.set_status(status, message)
        return json_response(self.response, device, strategy=DEVICE_PAIRING_CODE_STRATEGY)

    @requires_registration_token
    def post(self):
        if self.request.body is not '' and self.request.body is not None:
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
            timezone = request_json.get('timezone')
            if timezone is None or timezone == '':
                timezone = 'America/Chicago'
            correlation_id = IntegrationEventLog.generate_correlation_id()
            if self.is_unmanaged_device is True:
                registration_request_event = IntegrationEventLog.create(
                    event_category='Registration',
                    component_name='Player - unmanaged',
                    workflow_step='Request from Player to create an umanaged device',
                    mac_address=device_mac_address,
                    gcm_registration_id=gcm_registration_id,
                    correlation_identifier=correlation_id)
                registration_request_event.put()
                if ChromeOsDevice.gcm_registration_id_already_assigned(
                        gcm_registration_id=gcm_registration_id,
                        is_unmanaged_device=True):
                    error_message = 'Conflict gcm registration id is already assigned to an unmanaged device.'
                    self.response.set_status(409, error_message)
                    registration_request_event.details = error_message
                    registration_request_event.put()
                    device = ChromeOsDevice.get_unmanaged_device_by_gcm_registration_id(
                        gcm_registration_id=gcm_registration_id)
                    if device:
                        post_unmanaged_device_info(gcm_registration_id=device.gcm_registration_id,
                                                   device_urlsafe_key=device.key.urlsafe(),
                                                   host=self.request.host_url)
                    registration_request_event.details = "{0}. Messaging device key to player".format(error_message)
                    registration_request_event.put()
                    return
                if ChromeOsDevice.mac_address_already_assigned(
                        device_mac_address=device_mac_address,
                        is_unmanaged_device=True):
                    error_message = 'Conflict mac address is already assigned to an unmanaged device.'
                    self.response.set_status(409, error_message)
                    registration_request_event.details = error_message
                    registration_request_event.put()
                    device = ChromeOsDevice.get_unmanaged_device_by_mac_address(mac_address=device_mac_address)
                    if device:
                        post_unmanaged_device_info(gcm_registration_id=device.gcm_registration_id,
                                                   device_urlsafe_key=device.key.urlsafe(),
                                                   host=self.request.host_url)
                    registration_request_event.details = "{0}. Messaging device key to player".format(error_message)
                    registration_request_event.put()
                    return
                device = ChromeOsDevice.create_unmanaged(gcm_registration_id=gcm_registration_id,
                                                         mac_address=device_mac_address,
                                                         timezone=timezone,
                                                         registration_correlation_identifier=correlation_id)
                device_key = device.put()
                device_uri = self.request.app.router.build(None,
                                                           'device-pairing-code',
                                                           None,
                                                           {'device_urlsafe_key': device_key.urlsafe()})
                self.response.headers['Location'] = device_uri
                self.response.headers.pop('Content-Type', None)
                self.response.set_status(status)
            else:
                registration_request_event = IntegrationEventLog.create(
                    event_category='Registration',
                    component_name='Player',
                    workflow_step='Request from Player to create a managed device',
                    mac_address=device_mac_address,
                    gcm_registration_id=gcm_registration_id,
                    correlation_identifier=correlation_id)
                registration_request_event.put()
                if ChromeOsDevice.gcm_registration_id_already_assigned(gcm_registration_id=gcm_registration_id,
                                                                       is_unmanaged_device=False):
                    error_message = 'Conflict gcm registration id is already assigned to a managed device.'
                    registration_request_event.details = error_message
                    registration_request_event.put()
                    self.response.set_status(409, error_message)
                    return
                tenant_code = request_json.get('tenantCode')
                if tenant_code is None or tenant_code == '':
                    status = 400
                    error_message = 'The tenantCode parameter is invalid.'
                    self.response.set_status(status, error_message)
                    registration_request_event.details = error_message
                    registration_request_event.put()
                    self.response.set_status(status, error_message)
                    return
                tenant = Tenant.find_by_tenant_code(tenant_code)
                if tenant is None:
                    status = 400
                    error_message = 'Cannot resolve tenant from tenant code. Bad tenant code or inactive tenant.'
                    self.response.set_status(status, error_message)
                    registration_request_event.details = error_message
                    registration_request_event.put()
                    self.response.set_status(status, error_message)
                    return
                if status == 201:
                    device = ChromeOsDevice.create_managed(tenant_key=tenant.key,
                                                           gcm_registration_id=gcm_registration_id,
                                                           mac_address=device_mac_address,
                                                           timezone=timezone,
                                                           registration_correlation_identifier=correlation_id)
                    key = device.put()
                    registration_request_event.device_urlsafe_key = key.urlsafe()
                    registration_request_event.details = 'register_device: tenant code={0}, mac address={1}, ' \
                                                         'gcm id = {2}, ' \
                                                         'device key = {3}'.format(tenant_code, device_mac_address,
                                                                                   gcm_registration_id, key.urlsafe())
                    registration_request_event.put()
                    deferred.defer(register_device,
                                   device_urlsafe_key=key.urlsafe(),
                                   device_mac_address=device_mac_address,
                                   gcm_registration_id=gcm_registration_id,
                                   correlation_id=correlation_id,
                                   _queue='directory-api',
                                   _countdown=3)
                    device_uri = self.request.app.router.build(None,
                                                               'device',
                                                               None,
                                                               {'device_urlsafe_key': key.urlsafe()})
                    self.response.headers['Location'] = device_uri
                    self.response.headers.pop('Content-Type', None)
                    self.response.set_status(status)
                    registration_response_event = IntegrationEventLog.create(
                        event_category='Registration',
                        component_name='Provisioning',
                        workflow_step='Response to Player after creating a managed device',
                        mac_address=device_mac_address,
                        gcm_registration_id=gcm_registration_id,
                        correlation_identifier=correlation_id,
                        details='Device resource uri {0} returned in response Location header.'.format(device_uri))
                    registration_response_event.put()
                    notifier = EmailNotify()
                    notifier.device_enrolled(tenant_code=tenant_code,
                                             tenant_name=device.get_tenant().name,
                                             device_mac_address=device_mac_address,
                                             timestamp=datetime.utcnow())
                else:
                    self.response.set_status(status, error_message)
        else:
            logging.info("Problem creating Device. No request body.")
            self.response.set_status(400, 'Did not receive request body.')

    @requires_api_token
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
            return self.response.set_status(status, message)
        elif device.archived:
            status = 404
            message = 'Device with key: {0} archived.'.format(device_urlsafe_key)
            return self.response.set_status(status, message)
        else:
            request_json = json.loads(self.request.body)
            location_urlsafe_key = request_json.get('locationKey')
            if location_urlsafe_key:
                try:
                    location = ndb.Key(urlsafe=location_urlsafe_key).get()
                    device.location_key = location.key
                except Exception, e:
                    logging.exception(e)
            check_for_content_interval_minutes = request_json.get('checkContentInterval')
            if check_for_content_interval_minutes is not None and check_for_content_interval_minutes > -1:
                if device.check_for_content_interval_minutes != check_for_content_interval_minutes:
                    device.check_for_content_interval_minutes = check_for_content_interval_minutes
                    user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
                    if user_identifier is None or user_identifier == '':
                        user_identifier = 'system'
                    change_intent(
                        gcm_registration_id=device.gcm_registration_id,
                        payload=config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                        device_urlsafe_key=device_urlsafe_key,
                        host=self.request.host_url,
                        user_identifier=user_identifier)
            customer_display_name = request_json.get('customerDisplayName')
            if customer_display_name:
                device.customer_display_name = customer_display_name
            customer_display_code = request_json.get('customerDisplayCode')
            if customer_display_code:
                if device.customer_display_code != customer_display_code:
                    if ChromeOsDevice.is_customer_display_code_unique(
                            customer_display_code=customer_display_code,
                            tenant_key=device.tenant_key):
                        device.customer_display_code = customer_display_code
                    else:
                        status = 409
                        message = "Conflict. Customer display code \"{0}\" is already assigned for tenant.".format(
                            customer_display_code)
                        self.response.set_status(status, message)
                        return
            notes = request_json.get('notes')
            if notes:
                device.notes = notes
            gcm_registration_id = request_json.get('gcmRegistrationId')
            if gcm_registration_id:
                device.gcm_registration_id = gcm_registration_id
            panel_model = request_json.get('panelModelNumber')
            if panel_model:
                device.panel_model = panel_model
            else:
                device.panel_model = None
            panel_input = request_json.get('panelSerialInput')
            if panel_input:
                device.panel_input = panel_input
            else:
                device.panel_input = None
            tenant_code = request_json.get('tenantCode')
            if tenant_code:
                tenant = Tenant.find_by_tenant_code(tenant_code)
                if tenant:
                    if tenant.key != device.tenant_key:
                        device.tenant_key = tenant.key
                        device.put()
                        if device.is_unmanaged_device:
                            post_unmanaged_device_info(gcm_registration_id=device.gcm_registration_id,
                                                       device_urlsafe_key=device.key.urlsafe(),
                                                       host=self.request.host_url)
                        else:
                            deferred.defer(ContentManagerApi().update_device,
                                           device_urlsafe_key=device.key.urlsafe(),
                                           _queue='content-server',
                                           _countdown=5)
                else:
                    status = 400
                    message = "Attempt to update an invalid tenant code: \"{0}\".".format(
                        tenant_code)
                    self.response.set_status(status, message)
                    return

            proof_of_play_logging = request_json.get('proofOfPlayLogging')
            if str(proof_of_play_logging).lower() == 'true' or str(proof_of_play_logging).lower() == 'false':
                device.proof_of_play_logging = bool(proof_of_play_logging)
            timezone = request_json.get('timezone')
            if timezone:
                device.timezone = timezone
                device.timezone_offset = TimezoneUtil.get_timezone_offset(timezone)
            device.put()
            if not device.is_unmanaged_device:
                deferred.defer(update_chrome_os_device,
                               device_urlsafe_key=device.key.urlsafe(),
                               _queue='directory-api')
            self.response.headers.pop('Content-Type', None)
        self.response.set_status(status, message)

    @requires_api_token
    def heartbeat(self, device_urlsafe_key):
        status = 204
        message = None
        device = None
        try:
            device = self.validate_and_get(device_urlsafe_key, ChromeOsDevice, abort_on_not_found=True)
        except Exception, e:
            logging.exception(e)
        if device is None:
            status = 404
            message = 'Unrecognized heartbeat device_key: {0}'.format(device_urlsafe_key)
            return self.response.set_status(status, message)
        elif device.archived:
            status = 404
            message = 'Device with key: {0} archived.'.format(device_urlsafe_key)
            return self.response.set_status(status, message)
        else:
            request_json = json.loads(self.request.body)
            storage = request_json.get('storage')
            memory = request_json.get('memory')
            mac_address = request_json.get('macAddress')
            program = request_json.get('program')
            program_id = request_json.get('programId')
            last_error = request_json.get('lastError')
            timezone = request_json.get('timezone')
            timezone_offset = request_json.get('timezoneOffset')
            sk_player_version = request_json.get('playerVersion')
            os = request_json.get('os')
            os_version = request_json.get('osVersion')
            playlist = request_json.get('playlist')
            playlist_id = request_json.get('playlistId')
            utc_now = datetime.utcnow()

            if DeviceIssueLog.device_not_reported_yet(device_key=device.key):
                new_log_entry = DeviceIssueLog.create(device_key=device.key,
                                                      category=config.DEVICE_ISSUE_FIRST_HEARTBEAT,
                                                      up=True,
                                                      storage_utilization=storage,
                                                      memory_utilization=memory,
                                                      program=program,
                                                      program_id=program_id,
                                                      playlist=playlist,
                                                      playlist_id=playlist_id,
                                                      last_error=last_error,
                                                      resolved=True,
                                                      resolved_datetime=utc_now)
                new_log_entry.put()

            if mac_address:
                if not device.is_unmanaged_device and \
                        ChromeOsDevice.mac_address_already_assigned(mac_address, is_unmanaged_device=False):
                    if device.ethernet_mac_address == mac_address:
                        device.connection_type = config.ETHERNET_CONNECTION
                    elif device.mac_address == mac_address:
                        device.connection_type = config.WIFI_CONNECTION
                else:
                    if device.mac_address != mac_address or device.ethernet_mac_address != mac_address:
                        info_message = "Heartbeat got an unrecognized macAddress {0} for device {1}".format(
                            mac_address,
                            device_urlsafe_key
                        )
                        logging.info(info_message)

            if storage is not None:
                storage = int(storage)
                if device.storage_utilization != storage:
                    device.storage_utilization = storage

            if memory is not None:
                memory = int(memory)
                if device.memory_utilization != memory:
                    device.memory_utilization = memory

            if program:
                if device.program != program:
                    device.program = program

            if program_id:
                if device.program_id != program_id:
                    device.program_id = program_id

            if playlist:
                if device.playlist != playlist:
                    device.playlist = playlist

            if playlist_id:
                if device.playlist_id != playlist_id:
                    device.playlist_id = playlist_id

            if last_error:
                if device.last_error != last_error:
                    device.last_error = last_error

            if timezone:
                if device.timezone != timezone:
                    new_log_entry = DeviceIssueLog.create(device_key=device.key,
                                                          category=config.DEVICE_ISSUE_TIMEZONE_CHANGE,
                                                          up=True,
                                                          storage_utilization=storage,
                                                          memory_utilization=memory,
                                                          program=program,
                                                          program_id=program_id,
                                                          playlist=playlist,
                                                          playlist_id=playlist_id,
                                                          last_error=last_error,
                                                          resolved=True,
                                                          resolved_datetime=utc_now)
                    new_log_entry.put()

            if timezone_offset and timezone:
                if timezone_offset != TimezoneUtil.get_timezone_offset(timezone):
                    change_intent(
                        gcm_registration_id=device.gcm_registration_id,
                        payload=config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                        device_urlsafe_key=device_urlsafe_key,
                        host=self.request.host_url,
                        user_identifier='system (player heartbeat)')
                    new_log_entry = DeviceIssueLog.create(device_key=device.key,
                                                          category=config.DEVICE_ISSUE_TIMEZONE_OFFSET_CHANGE,
                                                          up=True,
                                                          storage_utilization=storage,
                                                          memory_utilization=memory,
                                                          program=program,
                                                          program_id=program_id,
                                                          playlist=playlist,
                                                          playlist_id=playlist_id,
                                                          last_error=last_error,
                                                          resolved=True,
                                                          resolved_datetime=utc_now)
                    new_log_entry.put()

            if sk_player_version:
                if device.sk_player_version != sk_player_version:
                    device.sk_player_version = sk_player_version
                    new_log_entry = DeviceIssueLog.create(device_key=device.key,
                                                          category=config.DEVICE_ISSUE_PLAYER_VERSION_CHANGE,
                                                          up=True,
                                                          storage_utilization=storage,
                                                          memory_utilization=memory,
                                                          program=program,
                                                          program_id=program_id,
                                                          playlist=playlist,
                                                          playlist_id=playlist_id,
                                                          last_error=last_error,
                                                          resolved=True,
                                                          resolved_datetime=utc_now)
                    new_log_entry.put()

            if os:
                if device.os != os:
                    device.os = os
                    new_log_entry = DeviceIssueLog.create(device_key=device.key,
                                                          category=config.DEVICE_ISSUE_OS_CHANGE,
                                                          up=True,
                                                          storage_utilization=storage,
                                                          memory_utilization=memory,
                                                          program=program,
                                                          program_id=program_id,
                                                          playlist=playlist,
                                                          playlist_id=playlist_id,
                                                          last_error=last_error,
                                                          resolved=True,
                                                          resolved_datetime=utc_now)
                    new_log_entry.put()

            if os_version:
                if device.os_version != os_version:
                    device.os_version = os_version
                    new_log_entry = DeviceIssueLog.create(device_key=device.key,
                                                          category=config.DEVICE_ISSUE_OS_VERSION_CHANGE,
                                                          up=True,
                                                          storage_utilization=storage,
                                                          memory_utilization=memory,
                                                          program=program,
                                                          program_id=program_id,
                                                          playlist=playlist,
                                                          playlist_id=playlist_id,
                                                          last_error=last_error,
                                                          resolved=True,
                                                          resolved_datetime=utc_now)
                    new_log_entry.put()

            previously_down = device.up is False
            if previously_down:
                DeviceIssueLog.resolve_device_down_issues(device_key=device.key, resolved_datetime=utc_now)
                notifier = EmailNotify()
                tenant = device.get_tenant()
                notifier.device_up(tenant_code=tenant.tenant_code,
                                   tenant_name=tenant.name,
                                   device_serial_number=device.serial_number)
                new_log_entry = DeviceIssueLog.create(device_key=device.key,
                                                      category=config.DEVICE_ISSUE_PLAYER_UP,
                                                      up=True,
                                                      storage_utilization=storage,
                                                      memory_utilization=memory,
                                                      program=program,
                                                      program_id=program_id,
                                                      playlist=playlist,
                                                      playlist_id=playlist_id,
                                                      last_error=last_error,
                                                      resolved=True,
                                                      resolved_datetime=utc_now)
                new_log_entry.put()

            previous_memory_issues = DeviceIssueLog.device_has_unresolved_memory_issues(device.key)
            if previous_memory_issues and device.memory_utilization < config.MEMORY_UTILIZATION_THRESHOLD:
                DeviceIssueLog.resolve_device_memory_issues(device_key=device.key, resolved_datetime=utc_now)
                new_log_entry = DeviceIssueLog.create(device_key=device.key,
                                                      category=config.DEVICE_ISSUE_MEMORY_NORMAL,
                                                      up=True,
                                                      storage_utilization=storage,
                                                      memory_utilization=memory,
                                                      program=program,
                                                      program_id=program_id,
                                                      playlist=playlist,
                                                      playlist_id=playlist_id,
                                                      last_error=last_error,
                                                      resolved=True,
                                                      resolved_datetime=utc_now)
                new_log_entry.put()

            previous_storage_issues = DeviceIssueLog.device_has_unresolved_storage_issues(device.key)
            if previous_storage_issues and device.memory_utilization < config.STORAGE_UTILIZATION_THRESHOLD:
                DeviceIssueLog.resolve_device_storage_issues(device_key=device.key, resolved_datetime=utc_now)
                new_log_entry = DeviceIssueLog.create(device_key=device.key,
                                                      category=config.DEVICE_ISSUE_STORAGE_NORMAL,
                                                      up=True,
                                                      storage_utilization=storage,
                                                      memory_utilization=memory,
                                                      program=program,
                                                      program_id=program_id,
                                                      playlist=playlist,
                                                      playlist_id=playlist_id,
                                                      last_error=last_error,
                                                      resolved=True,
                                                      resolved_datetime=utc_now)
                new_log_entry.put()

            initial_heartbeat = device.heartbeat_updated is None
            if initial_heartbeat:
                correlation_identifier = IntegrationEventLog.get_correlation_identifier_for_registration(
                    device_urlsafe_key)
                if correlation_identifier:
                    initial_heartbeat_event = IntegrationEventLog.create(
                        event_category='Registration',
                        component_name='Player',
                        workflow_step=config.DEVICE_ISSUE_FIRST_HEARTBEAT,
                        mac_address=device.mac_address,
                        gcm_registration_id=device.gcm_registration_id,
                        device_urlsafe_key=device_urlsafe_key,
                        correlation_identifier=correlation_identifier,
                        details='Program playing: '.format(program))
                    initial_heartbeat_event.put()
                else:
                    message = '{0} event detected for device_key={1}, but no correlation identifier!'.format(
                        config.DEVICE_ISSUE_FIRST_HEARTBEAT, device_urlsafe_key)
                    logging.info(message)
            device.up = True
            device.heartbeat_updated = utc_now
            device.put()
            self.response.headers.pop('Content-Type', None)

        self.response.set_status(status, message)

    @requires_api_token
    def get_latest_issues(self, device_urlsafe_key, prev_cursor_str, next_cursor_str):
        start_epoch = int(self.request.params['start'])
        end_epoch = int(self.request.params['end'])
        next_cursor_str = next_cursor_str if next_cursor_str != "null" else None
        prev_cursor_str = prev_cursor_str if prev_cursor_str != "null" else None
        start = datetime.utcfromtimestamp(start_epoch)
        end = datetime.utcfromtimestamp(end_epoch)
        device = self.validate_and_get(device_urlsafe_key, ChromeOsDevice, abort_on_not_found=True)
        paginated_results = Tenant.find_issues_paginated(start, end, device, prev_cursor_str=prev_cursor_str,
                                                         next_cursor_str=next_cursor_str)
        return json_response(self.response, {
            "issues": paginated_results["objects"],
            "prev": paginated_results["prev_cursor"],
            "next": paginated_results["next_cursor"]
        }, strategy=DEVICE_ISSUE_LOG_STRATEGY)

    @requires_api_token
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
        elif device.archived:
            status = 404
            message = 'Device with key: {0} archived.'.format(device_urlsafe_key)
        else:
            user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
            if user_identifier is None or user_identifier == '':
                user_identifier = 'system'
            change_intent(
                gcm_registration_id=device.gcm_registration_id,
                payload=config.PLAYER_RESET_COMMAND,
                device_urlsafe_key=device_urlsafe_key,
                host=self.request.host_url,
                user_identifier=user_identifier)
            device.archived = True
            device.put()
            self.response.headers.pop('Content-Type', None)
        self.response.set_status(status, message)

    @requires_api_token
    def panel_sleep(self, device_urlsafe_key):
        status, message, device = DeviceCommandsHandler.resolve_device(device_urlsafe_key)
        if device:
            user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
            if user_identifier is None or user_identifier == '':
                user_identifier = 'system'

            request_json = json.loads(self.request.body)
            panel_sleep = request_json["panelSleep"]
            device = ndb.Key(urlsafe=device_urlsafe_key).get()
            device.panel_sleep = panel_sleep
            device.put()

            change_intent(
                gcm_registration_id=device.gcm_registration_id,
                payload=config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                device_urlsafe_key=device_urlsafe_key,
                host=self.request.host_url,
                user_identifier=user_identifier)

        self.response.set_status(status, message)

    @staticmethod
    def get_domain_tenant_list_from_distributor(distributor_urlsafe_key):
        distributor = ndb.Key(urlsafe=distributor_urlsafe_key)
        domain_keys = Domain.query(Domain.distributor_key == distributor).fetch(100, keys_only=True)
        tenant_list = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
        tenant_list = filter(lambda x: x.active is True, tenant_list)
        domain_tenant_list = filter(lambda x: x.domain_key in domain_keys, tenant_list)
        return domain_tenant_list
