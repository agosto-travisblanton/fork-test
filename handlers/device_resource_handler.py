import httplib
import json
import logging

from datetime import datetime
from google.appengine.ext import ndb
from google.appengine.ext.deferred import deferred

from app_config import config
from device_commands_handler import DeviceCommandsHandler
from device_message_processor import post_unmanaged_device_info, change_intent
from extended_session_request_handler import ExtendedSessionRequestHandler
from integrations.content_manager.content_manager_api import ContentManagerApi
from models import ChromeOsDevice, Tenant, Domain, TenantEntityGroup
from restler.serializers import json_response
from strategy import CHROME_OS_DEVICE_STRATEGY, DEVICE_ISSUE_LOG_STRATEGY, CHROME_OS_DEVICES_LIST_VIEW_STRATEGY
from utils.auth_util import requires_auth
from utils.timezone_util import TimezoneUtil
from workflow.refresh_device import refresh_device
from workflow.refresh_device_by_mac_address import refresh_device_by_mac_address
from workflow.update_chrome_os_device import update_chrome_os_device

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>, Bob MacNeal <bob.macneal@agosto.com>'


class DeviceResourceHandler(ExtendedSessionRequestHandler):

    @requires_auth
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

    @requires_auth
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
            location_urlsafe_key = request_json.get('locationKey')
            location = None
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
                        status = httplib.CONFLICT
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
                    status = httplib.BAD_REQUEST
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
            overlay_status = request_json.get('overlayStatus')
            if overlay_status != None:
                device.overlays_available = overlay_status
            controls_mode = request_json.get('controlsMode')
            if controls_mode != None:
                device.controls_mode = controls_mode
            orientation_mode = request_json.get('orientationMode')
            if orientation_mode is not None:
                if orientation_mode.lower() in ["0", "90", "180", "270"]:
                    device.orientation_mode = orientation_mode.lower()
            sleep_controller = request_json.get('sleepController')
            if sleep_controller is not None:
                if sleep_controller.lower() in ["chrome-default", "rs232"]:
                    device.sleep_controller = sleep_controller.lower()

            device.put()

            # adjust this object with values you want to spy on to do a gcm_update on when they are True
            gcm_update_on_changed_if_true = [
                controls_mode,
                overlay_status,
                orientation_mode,
                location,
                panel_input,
                panel_model,
                customer_display_code,
                customer_display_name,
                proof_of_play_logging,
                timezone,
                sleep_controller
            ]

            changes_to_device = [e for e in gcm_update_on_changed_if_true if e != None]

            if len(changes_to_device) > 0:
                change_intent(
                    gcm_registration_id=device.gcm_registration_id,
                    payload=config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                    device_urlsafe_key=device.key.urlsafe(),
                    host=self.request.host_url,
                    user_identifier='system (device update)'
                )

            if not device.is_unmanaged_device:
                deferred.defer(update_chrome_os_device,
                               device_urlsafe_key=device.key.urlsafe(),
                               _queue='directory-api')
            self.response.headers.pop('Content-Type', None)
        self.response.set_status(status, message)

    @requires_auth
    def delete(self, device_urlsafe_key):
        status = httplib.NO_CONTENT
        message = None
        device = self.validate_and_get(urlsafe_key=device_urlsafe_key,
                                       kind_cls=ChromeOsDevice,
                                       abort_on_not_found=False)
        if device is None:
            status = httplib.NOT_FOUND
            message = 'Unrecognized device with key: {0}'.format(device_urlsafe_key)
        elif device.archived:
            status = httplib.NOT_FOUND
            message = 'Device with key: {0} archived.'.format(device_urlsafe_key)
        else:
            user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
            if user_identifier is None or user_identifier == '':
                user_identifier = 'system'
            device.archived = True
            device.put()
            change_intent(
                gcm_registration_id=device.gcm_registration_id,
                payload=config.PLAYER_RESET_COMMAND,
                device_urlsafe_key=device_urlsafe_key,
                host=self.request.host_url,
                user_identifier=user_identifier)
            self.response.headers.pop('Content-Type', None)
        self.response.set_status(status, message)

    @requires_auth
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

    @requires_auth
    def update_controls_mode(self, device_urlsafe_key):
        status, message, device = DeviceCommandsHandler.resolve_device(device_urlsafe_key)
        if device:
            user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
            if user_identifier is None or user_identifier == '':
                user_identifier = 'system'

            request_json = json.loads(self.request.body)
            controls_mode = request_json["controlsMode"]
            device = ndb.Key(urlsafe=device_urlsafe_key).get()
            device.controls_mode = controls_mode
            device.put()
            status = httplib.NO_CONTENT

            change_intent(
                gcm_registration_id=device.gcm_registration_id,
                payload=config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                device_urlsafe_key=device_urlsafe_key,
                host=self.request.host_url,
                user_identifier=user_identifier)

        self.response.set_status(status, message)

    @requires_auth
    def update_panel_sleep(self, device_urlsafe_key):
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
            status = httplib.NO_CONTENT

            change_intent(
                gcm_registration_id=device.gcm_registration_id,
                payload=config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                device_urlsafe_key=device_urlsafe_key,
                host=self.request.host_url,
                user_identifier=user_identifier)

        self.response.set_status(status, message)

    @requires_auth
    def update_sleep_controller(self, device_urlsafe_key):
        status, message, device = DeviceCommandsHandler.resolve_device(device_urlsafe_key)
        if device:
            request_json = json.loads(self.request.body)
            sleep_controller = request_json.get('sleepController')
            if sleep_controller is not None:
                if sleep_controller.lower() in ["chrome-default", "rs232"]:
                    device.sleep_controller = sleep_controller.lower()
                    device.put()
                    status = httplib.NO_CONTENT

        self.response.set_status(status, message)

    ############################################################################################
    # TENANTS VIEW
    ############################################################################################
    @requires_auth
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

    @requires_auth
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
    @requires_auth
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
            strategy=CHROME_OS_DEVICES_LIST_VIEW_STRATEGY
        )

    @requires_auth
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

    @requires_auth
    def search_for_device_globally(self):
        unmanaged = self.request.get("unmanaged") == "true"
        partial_gcmid = self.request.get("partial_gcmid")
        partial_serial = self.request.get("partial_serial")
        partial_mac = self.request.get("partial_mac")
        user_key = self.request.headers.get("X-Provisioning-User")

        try:
            user_entity = ndb.Key(urlsafe=user_key).get()
        except Exception, e:
            user_entity = None
            logging.exception(e)

        if not user_entity:
            error_message = 'Bad User Key'
            self.response.set_status(httplib.BAD_REQUEST, error_message)
            return

        if not user_entity.is_administrator:
            error_message = 'User is not administrator'
            self.response.set_status(httplib.BAD_REQUEST, error_message)
            return


        else:
            if partial_gcmid:
                resulting_devices = Tenant.find_devices_with_partial_gcmid_globally(
                    unmanaged=unmanaged,
                    partial_gcmid=partial_gcmid
                )

            elif partial_serial:
                resulting_devices = Tenant.find_devices_with_partial_serial_globally(
                    unmanaged=unmanaged,
                    partial_serial=partial_serial
                )
            elif partial_mac:
                resulting_devices = Tenant.find_devices_with_partial_mac_globally(
                    unmanaged=unmanaged,
                    partial_mac=partial_mac
                )

            matches = [
                {
                    "mac": DeviceResourceHandler.ethernet_or_wifi_mac_address(device, partial_mac),
                    "serial": device.serial_number,
                    "key": device.key.urlsafe(),
                    "tenantKey": device.tenant_key.urlsafe(),
                    "gcmid": device.gcm_registration_id
                } for device in resulting_devices]

            json_response(
                self.response,
                {
                    "matches": matches
                },
            )

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

    @staticmethod
    def get_domain_tenant_list_from_distributor(distributor_urlsafe_key):
        distributor = ndb.Key(urlsafe=distributor_urlsafe_key)
        domain_keys = Domain.query(Domain.distributor_key == distributor).fetch(100, keys_only=True)
        tenant_list = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
        tenant_list = filter(lambda x: x.active is True, tenant_list)
        domain_tenant_list = filter(lambda x: x.domain_key in domain_keys, tenant_list)
        return domain_tenant_list
