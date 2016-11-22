import httplib
import json
import logging

from datetime import datetime
from google.appengine.ext.deferred import deferred

from app_config import config
from decorators import requires_api_token, requires_registration_token, requires_unmanaged_registration_token
from device_message_processor import post_unmanaged_device_info, change_intent
from extended_session_request_handler import ExtendedSessionRequestHandler
from model_entities.integration_events_log_model import IntegrationEventLog
from models import ChromeOsDevice, Tenant, DeviceIssueLog
from restler.serializers import json_response
from strategy import CHROME_OS_DEVICE_STRATEGY, DEVICE_PAIRING_CODE_STRATEGY
from utils.email_notify import EmailNotify
from utils.timezone_util import TimezoneUtil
from workflow.refresh_device import refresh_device
from workflow.refresh_device_by_mac_address import refresh_device_by_mac_address
from workflow.register_device import register_device

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class DeviceHandler(ExtendedSessionRequestHandler):

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
                    self.response.set_status(httplib.NOT_FOUND, message)
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
                        self.__archive(query_results[0])
                        error_message = "Rogue unmanaged device with MAC address: {0} no longer exists.".format(
                            device_mac_address)
                        self.response.set_status(httplib.NOT_FOUND, error_message)
                    else:
                        json_response(self.response, query_results[0], strategy=CHROME_OS_DEVICE_STRATEGY)
                elif len(query_results) > 1:
                    json_response(self.response, query_results[0], strategy=CHROME_OS_DEVICE_STRATEGY)
                    error_message = "Multiple devices have MAC address {0}".format(device_mac_address)
                    logging.error(error_message)
                else:
                    error_message = "Unable to find device by GCM registration ID: {0} or MAC address: {1}".format(
                        gcm_registration_id, device_mac_address)
                    self.response.set_status(httplib.NOT_FOUND, error_message)
        else:
            self.response.set_status(httplib.BAD_REQUEST)
        return

    @requires_api_token
    def get(self, device_urlsafe_key):
        device = self.validate_and_get(device_urlsafe_key, ChromeOsDevice, abort_on_not_found=True,
                                       use_app_engine_memcache=False)
        if device.archived:
            status = httplib.NOT_FOUND
            message = 'Device with key: {0} archived.'.format(device_urlsafe_key)
            return self.response.set_status(status, message)
        if device.timezone:
            device.timezone_offset = TimezoneUtil.get_timezone_offset(device.timezone)
        else:
            device.timezone_offset = TimezoneUtil.get_timezone_offset(config.DEFAULT_TIMEZONE)
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

    @requires_registration_token
    def post(self):
        if self.request.body is not '' and self.request.body is not None:
            status = httplib.CREATED
            error_message = None
            request_json = json.loads(self.request.body)
            device_mac_address = self.check_and_get_field('macAddress')
            gcm_registration_id = self.check_and_get_field('gcmRegistrationId')
            timezone = request_json.get('timezone')
            if timezone is None or timezone == '':
                timezone = config.DEFAULT_TIMEZONE

            correlation_id = IntegrationEventLog.generate_correlation_id()

            if self.is_unmanaged_device:
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
                    self.response.set_status(httplib.CONFLICT, error_message)
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
                    self.response.set_status(httplib.CONFLICT, error_message)
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

            # not an unmanaged device (so its a managed device)
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
                    self.response.set_status(httplib.CONFLICT, error_message)
                    return
                tenant_code = request_json.get('tenantCode')
                if tenant_code:
                    has_tenant = True
                    tenant = Tenant.find_by_tenant_code(tenant_code)
                    if tenant is None:
                        status = httplib.BAD_REQUEST
                        error_message = 'Cannot resolve tenant from tenant code. Bad tenant code or inactive tenant.'
                        self.response.set_status(status, error_message)
                        bad_registration_request_event = IntegrationEventLog.create(
                            event_category='Registration',
                            component_name='Player',
                            workflow_step='Player payload to create a managed device',
                            mac_address=device_mac_address,
                            gcm_registration_id=gcm_registration_id,
                            correlation_identifier=correlation_id,
                            details=error_message)
                        bad_registration_request_event.put()
                        registration_request_event.details = error_message
                        registration_request_event.put()
                        self.response.set_status(status, error_message)
                        logging.error('Cannot resolve tenant_code {0}. Bad tenant code or inactive tenant.'.format(
                            tenant_code))
                        return
                    else:
                        tenant_key = tenant.key
                    chrome_domain = None
                else:
                    chrome_domain = request_json.get('domain')
                    if chrome_domain is None:
                        status = httplib.BAD_REQUEST
                        error_message = 'Did not detect a tenantCode or a domain in device registration payload.'
                        self.response.set_status(status, error_message)
                        registration_request_event.details = error_message
                        registration_request_event.put()
                        bad_registration_request_event = IntegrationEventLog.create(
                            event_category='Registration',
                            component_name='Player',
                            workflow_step='Player payload to create a managed device',
                            mac_address=device_mac_address,
                            gcm_registration_id=gcm_registration_id,
                            correlation_identifier=correlation_id,
                            details=error_message)
                        bad_registration_request_event.put()
                        self.response.set_status(status, error_message)
                        logging.error(error_message)
                        return
                    has_tenant = False
                    tenant_key = None

                if status == httplib.CREATED:
                    device = ChromeOsDevice.create_managed(tenant_key=tenant_key,
                                                           gcm_registration_id=gcm_registration_id,
                                                           mac_address=device_mac_address,
                                                           timezone=timezone,
                                                           registration_correlation_identifier=correlation_id)
                    key = device.put()

                    registration_request_event.device_urlsafe_key = key.urlsafe()
                    registration_request_event.mac_address = device_mac_address
                    registration_request_event.gcm_registration_id = gcm_registration_id
                    if has_tenant:
                        registration_request_event.tenant_code = tenant_code
                        registration_request_event.details = 'Tenant code present in request'
                    else:
                        registration_request_event.details = 'Tenant code not present in request. Domain = {0}'.format(
                            chrome_domain)
                    registration_request_event.put()
                    deferred.defer(register_device,
                                   urlsafe_key=key.urlsafe(),
                                   mac_address=device_mac_address,
                                   gcm_registration_id=gcm_registration_id,
                                   correlation_id=correlation_id,
                                   domain_name=chrome_domain,
                                   _queue='directory-api',
                                   _countdown=60)
                    device_uri = self.request.app.router.build(None,
                                                               'api-device-get',
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
                        device_urlsafe_key=key.urlsafe(),
                        details='Device resource uri {0} returned in response Location header.'.format(device_uri))
                    registration_response_event.put()
                else:
                    self.response.set_status(status, error_message)
        else:
            logging.info("Problem creating Device. No request body.")
            self.response.set_status(httplib.BAD_REQUEST, 'Did not receive request body.')

    @requires_api_token
    def put(self, device_urlsafe_key):
        status = httplib.NO_CONTENT
        message = None
        device = self.validate_and_get(device_urlsafe_key, ChromeOsDevice, abort_on_not_found=True)
        if device.archived:
            status = httplib.NOT_FOUND
            message = 'Device with key: {0} archived.'.format(device_urlsafe_key)
            return self.response.set_status(status, message)
        else:
            request_json = json.loads(self.request.body)
            gcm_registration_id = request_json.get('gcmRegistrationId')
            if gcm_registration_id:
                device.gcm_registration_id = gcm_registration_id
                device.put()
            mac_address = request_json.get('macAddress')
            if mac_address:
                device.mac_address = mac_address
                device.put()
            self.response.headers.pop('Content-Type', None)
        self.response.set_status(status, message)

    @requires_api_token
    def heartbeat(self, device_urlsafe_key):
        status = httplib.NO_CONTENT
        message = None
        device = None
        try:
            device = self.validate_and_get(device_urlsafe_key, ChromeOsDevice, abort_on_not_found=False,
                                           use_app_engine_memcache=False)
        except Exception, e:
            logging.exception(e)
        if device is None:
            status = httplib.NOT_FOUND
            message = 'Unrecognized heartbeat device_key: {0}'.format(device_urlsafe_key)
            return self.response.set_status(status, message)
        elif device.archived:
            status = httplib.NOT_FOUND
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

    @requires_unmanaged_registration_token
    def get_pairing_code(self, device_urlsafe_key):
        device = self.validate_and_get(device_urlsafe_key, ChromeOsDevice, abort_on_not_found=True)
        if device is None:
            status = httplib.NOT_FOUND
            message = 'Unrecognized device_key: {0}'.format(device_urlsafe_key)
            return self.response.set_status(status, message)
        elif device.archived:
            status = httplib.NOT_FOUND
            message = 'Device with key: {0} archived.'.format(device_urlsafe_key)
            return self.response.set_status(status, message)
        return json_response(self.response, device, strategy=DEVICE_PAIRING_CODE_STRATEGY)

    def __archive(self, device):
        user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
        if user_identifier is None or user_identifier == '':
            user_identifier = 'system'
        device.archived = True
        device.put()
        change_intent(
            gcm_registration_id=device.gcm_registration_id,
            payload=config.PLAYER_RESET_COMMAND,
            device_urlsafe_key=device.key.urlsafe(),
            host=self.request.host_url,
            user_identifier=user_identifier)
