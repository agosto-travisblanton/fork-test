import json
import logging
from datetime import datetime

from google.appengine.ext import ndb
from google.appengine.ext.deferred import deferred
from webapp2 import RequestHandler

from app_config import config
from chrome_os_devices_api import (refresh_device, refresh_device_by_mac_address, update_chrome_os_device)
from content_manager_api import ContentManagerApi
from decorators import requires_api_token, requires_registration_token, requires_unmanaged_registration_token
from device_message_processor import post_unmanaged_device_info, change_intent
from models import ChromeOsDevice, Tenant, Domain, TenantEntityGroup, DeviceIssueLog
from ndb_mixins import PagingListHandlerMixin, KeyValidatorMixin
from restler.serializers import json_response
from strategy import CHROME_OS_DEVICE_STRATEGY, DEVICE_PAIRING_CODE_STRATEGY, DEVICE_ISSUE_LOG_STRATEGY

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>, Bob MacNeal <bob.macneal@agosto.com>'


class DeviceResourceHandler(RequestHandler, PagingListHandlerMixin, KeyValidatorMixin):
    @requires_api_token
    def get_list(self):
        pairing_code = self.request.get('pairingCode')
        device_mac_address = self.request.get('macAddress')
        gcm_registration_id = self.request.get('gcmRegistrationId')
        if device_mac_address:
            query = ChromeOsDevice.query(ndb.OR(ChromeOsDevice.mac_address == device_mac_address,
                                                ChromeOsDevice.ethernet_mac_address == device_mac_address))
            query_results = query.fetch()
            if len(query_results) is 1:
                json_response(self.response, query_results[0], strategy=CHROME_OS_DEVICE_STRATEGY)
            elif len(query_results) > 1:
                json_response(self.response, query_results[0], strategy=CHROME_OS_DEVICE_STRATEGY)
                error_message = "Multiple devices have MAC address {0}".format(device_mac_address)
                logging.error(error_message)
            else:
                error_message = "Unable to find Chrome OS device by MAC address: {0}".format(device_mac_address)
                self.response.set_status(404, error_message)
        elif gcm_registration_id:
            query = ChromeOsDevice.query(ChromeOsDevice.gcm_registration_id == gcm_registration_id)
            query_results = query.fetch()
            if len(query_results) is 1:
                json_response(self.response, query_results[0], strategy=CHROME_OS_DEVICE_STRATEGY)
            elif len(query_results) > 1:
                json_response(self.response, query_results[0], strategy=CHROME_OS_DEVICE_STRATEGY)
                error_message = "Multiple devices have GCM registration ID {0}".format(gcm_registration_id)
                logging.error(error_message)
            else:
                error_message = "Unable to find Chrome OS device by GCM registration ID: {0}".format(
                    gcm_registration_id)
                self.response.set_status(404, error_message)
        elif pairing_code:
            query = ChromeOsDevice.query(ChromeOsDevice.pairing_code == pairing_code)
            query_results = query.fetch()
            if len(query_results) is 1:
                json_response(self.response, query_results[0], strategy=CHROME_OS_DEVICE_STRATEGY)
            elif len(query_results) > 1:
                json_response(self.response, query_results[0], strategy=CHROME_OS_DEVICE_STRATEGY)
                error_message = "Multiple devices have pairing code {0}".format(pairing_code)
                logging.error(error_message)
            else:
                error_message = "Unable to find device by pairing code: {0}".format(pairing_code)
                self.response.set_status(404, error_message)
        else:
            query = ChromeOsDevice.query().order(ChromeOsDevice.created)
            # query_forward = query.order(ChromeOsDevice.key)
            # query_reverse = query.order(-ChromeOsDevice.key)
            # query_results = self.fetch_page(query_forward, query_reverse)
            # json_response(self.response, query_results, strategy=CHROME_OS_DEVICE_STRATEGY)
            query_results = query.fetch(1000)
            json_response(self.response, query_results, strategy=CHROME_OS_DEVICE_STRATEGY)

    @requires_api_token
    def get_devices_by_tenant(self, tenant_urlsafe_key):
        tenant_key = ndb.Key(urlsafe=tenant_urlsafe_key)
        unmanaged_filter = self.request.get('unmanaged')
        if unmanaged_filter == '' or str(unmanaged_filter) == 'false':
            unmanaged = False
        else:
            unmanaged = True
        query = ChromeOsDevice.query(
                ndb.AND(ChromeOsDevice.tenant_key == tenant_key,
                        ChromeOsDevice.is_unmanaged_device == unmanaged)
        )
        query_forward = query.order(ChromeOsDevice.key)
        query_reverse = query.order(-ChromeOsDevice.key)
        result_data = self.fetch_page(query_forward, query_reverse)
        json_response(self.response, result_data, strategy=CHROME_OS_DEVICE_STRATEGY)

    @requires_api_token
    def get_devices_by_distributor(self, distributor_urlsafe_key):
        device_list = []
        unmanaged_filter = self.request.get('unmanaged')
        if unmanaged_filter == '' or str(unmanaged_filter) == 'false':
            unmanaged = False
        else:
            unmanaged = True
        distributor = ndb.Key(urlsafe=distributor_urlsafe_key)
        domain_keys = Domain.query(Domain.distributor_key == distributor).fetch(100, keys_only=True)
        tenant_list = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
        tenant_list = filter(lambda x: x.active is True, tenant_list)
        domain_tenant_list = filter(lambda x: x.domain_key in domain_keys, tenant_list)
        for tenant in domain_tenant_list:
            tenant_devices = Tenant.find_devices(tenant.key, unmanaged)
            for tenant_device in tenant_devices:
                device_list.append(tenant_device)
        json_response(self.response, device_list, strategy=CHROME_OS_DEVICE_STRATEGY)

    @requires_api_token
    def get(self, device_urlsafe_key):
        device = self.validate_and_get(device_urlsafe_key, ChromeOsDevice, abort_on_not_found=True)
        if self.is_unmanaged_device is False:
            if None == device.device_id:
                deferred.defer(refresh_device_by_mac_address,
                               device_urlsafe_key=device_urlsafe_key,
                               device_mac_address=device.mac_address,
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
        return json_response(self.response, device, strategy=DEVICE_PAIRING_CODE_STRATEGY)

    @requires_registration_token
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
            if self.is_unmanaged_device is True:
                unmanaged_device = ChromeOsDevice.get_unmanaged_device_by_mac_address(device_mac_address)
                if None is not unmanaged_device:
                    post_unmanaged_device_info(gcm_registration_id=unmanaged_device.gcm_registration_id,
                                               device_urlsafe_key=unmanaged_device.key.urlsafe())
                    status = 409
                    error_message = 'Registration conflict because macAddress is already assigned to ' \
                                    'an unmanaged device.'
                    self.response.set_status(status, error_message)
                    return
                unmanaged_device = ChromeOsDevice.get_unmanaged_device_by_gcm_registration_id(gcm_registration_id)
                if None is not unmanaged_device:
                    post_unmanaged_device_info(gcm_registration_id=unmanaged_device.gcm_registration_id,
                                               device_urlsafe_key=unmanaged_device.key.urlsafe())
                    status = 409
                    error_message = 'Registration conflict because gcmRegistrationId is already assigned to ' \
                                    'an unmanaged device.'
                    self.response.set_status(status, error_message)
                    return
                device = ChromeOsDevice.create_unmanaged(gcm_registration_id, device_mac_address)
                device_key = device.put()
                device_uri = self.request.app.router.build(None,
                                                           'device-pairing-code',
                                                           None,
                                                           {'device_urlsafe_key': device_key.urlsafe()})
                self.response.headers['Location'] = device_uri
                self.response.headers.pop('Content-Type', None)
                self.response.set_status(status)
            else:
                if ChromeOsDevice.mac_address_already_assigned(device_mac_address):
                    status = 400
                    error_message = 'Cannot register because macAddress already assigned to managed device.'
                    self.response.set_status(status, error_message)
                    return
                tenant_code = request_json.get('tenantCode')
                if tenant_code is None or tenant_code == '':
                    status = 400
                    error_message = 'The tenantCode parameter is invalid.'
                    self.response.set_status(status, error_message)
                    return
                tenant_key = Tenant.query(Tenant.tenant_code == tenant_code, Tenant.active == True).get(keys_only=True)
                if tenant_key is None:
                    status = 400
                    error_message = 'Cannot resolve tenant from tenant code. Bad tenant code or inactive tenant.'
                    self.response.set_status(status, error_message)
                    return
                if status == 201:
                    device = ChromeOsDevice.create_managed(tenant_key=tenant_key,
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
                                                               'device',
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
        else:
            request_json = json.loads(self.request.body)
            notes = request_json.get('notes')
            if notes:
                device.notes = notes
            gcm_registration_id = request_json.get('gcmRegistrationId')
            if gcm_registration_id:
                logging.info('  PUT updating the gcmRegistrationId.')
                device.gcm_registration_id = gcm_registration_id
            panel_model = request_json.get('panelModel')
            if panel_model:
                device.panel_model = panel_model
            else:
                device.panel_model = None
            panel_input = request_json.get('panelInput')
            if panel_input:
                device.panel_input = panel_input
            else:
                device.panel_input = None
            tenant_code = request_json.get('tenantCode')
            if tenant_code:
                tenant = Tenant.find_by_tenant_code(tenant_code)
                if tenant and tenant.key != device.tenant_key:
                    device.tenant_key = tenant.key
                    if device.is_unmanaged_device:
                        logging.info(' PUT add the tenant to unmanaged device.')
                        post_unmanaged_device_info(gcm_registration_id=device.gcm_registration_id,
                                                   device_urlsafe_key=device.key.urlsafe())
                    else:
                        logging.info(' PUT update tenant on device.')
                        device.put()
                        deferred.defer(ContentManagerApi().update_device,
                                       device_urlsafe_key=device.key.urlsafe(),
                                       _queue='content-server',
                                       _countdown=5)
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
        else:
            request_json = json.loads(self.request.body)
            mac_address = request_json.get('macAddress')
            if mac_address:
                if device.is_unmanaged_device == False and ChromeOsDevice.mac_address_already_assigned(mac_address):
                    if device.ethernet_mac_address == mac_address:
                        device.connection_type = config.ETHERNET_CONNECTION
                    elif device.mac_address == mac_address:
                        device.connection_type = config.WIFI_CONNECTION
                else:
                    if device.mac_address != mac_address or device.ethernet_mac_address != mac_address:
                        info_message = \
                            "Heartbeat got an unrecognized macAddress {0} for device {1}".format(mac_address,
                                                                                                 device_urlsafe_key)
                        logging.info(info_message)
            storage = request_json.get('storage')
            if storage:
                storage = int(storage)
                if device.storage_utilization != storage:
                    device.storage_utilization = storage
            memory = request_json.get('memory')
            if memory:
                memory = int(memory)
                if device.memory_utilization != memory:
                    device.memory_utilization = memory
            program = request_json.get('program')
            if program:
                if device.program != program:
                    device.program = program
            program_id = request_json.get('programId')
            if program_id:
                if device.program_id != program_id:
                    device.program_id = program_id
            last_error = request_json.get('lastError')
            if last_error:
                if device.last_error != last_error:
                    device.last_error = last_error
            sk_player_version = request_json.get('playerVersion')
            if sk_player_version:
                if device.sk_player_version != sk_player_version:
                    device.sk_player_version = sk_player_version
            os = request_json.get('os')
            if os:
                if device.os != os:
                    device.os = os
            os_version = request_json.get('osVersion')
            if os_version:
                if device.os_version != os_version:
                    device.os_version = os_version
            timezone = request_json.get('timezone')
            if timezone:
                if device.time_zone != timezone:
                    device.time_zone = timezone
            resolved_datetime = datetime.utcnow()
            previously_down = device.up is False
            if previously_down:
                DeviceIssueLog.resolve_device_down_issues(device_key=device.key, resolved_datetime=resolved_datetime)
                new_log_entry = DeviceIssueLog.create(device_key=device.key,
                                                      category=config.DEVICE_ISSUE_PLAYER_UP,
                                                      up=True,
                                                      storage_utilization=storage,
                                                      memory_utilization=memory,
                                                      program=program,
                                                      program_id=program_id,
                                                      last_error=last_error,
                                                      resolved=True,
                                                      resolved_datetime=datetime.utcnow())
                new_log_entry.put()
            previous_memory_issues = DeviceIssueLog.device_has_unresolved_memory_issues(device.key)
            if previous_memory_issues and device.memory_utilization < config.MEMORY_UTILIZATION_THRESHOLD:
                DeviceIssueLog.resolve_device_memory_issues(device_key=device.key, resolved_datetime=resolved_datetime)
                new_log_entry = DeviceIssueLog.create(device_key=device.key,
                                                      category=config.DEVICE_ISSUE_MEMORY_NORMAL,
                                                      up=True,
                                                      storage_utilization=storage,
                                                      memory_utilization=memory,
                                                      program=program,
                                                      program_id=program_id,
                                                      last_error=last_error,
                                                      resolved=True,
                                                      resolved_datetime=resolved_datetime)
                new_log_entry.put()
            previous_storage_issues = DeviceIssueLog.device_has_unresolved_storage_issues(device.key)
            if previous_storage_issues and device.memory_utilization < config.STORAGE_UTILIZATION_THRESHOLD:
                DeviceIssueLog.resolve_device_storage_issues(device_key=device.key, resolved_datetime=resolved_datetime)
                new_log_entry = DeviceIssueLog.create(device_key=device.key,
                                                      category=config.DEVICE_ISSUE_STORAGE_NORMAL,
                                                      up=True,
                                                      storage_utilization=storage,
                                                      memory_utilization=memory,
                                                      program=program,
                                                      program_id=program_id,
                                                      last_error=last_error,
                                                      resolved=True,
                                                      resolved_datetime=resolved_datetime)
                new_log_entry.put()

            device.up = True
            device.heartbeat_updated = datetime.utcnow()
            device.put()
            self.response.headers.pop('Content-Type', None)
        self.response.set_status(status, message)

    @requires_api_token
    def get_latest_issues(self, device_urlsafe_key):
        start_epoch = int(self.request.params['start'])
        end_epoch = int(self.request.params['end'])
        start = datetime.utcfromtimestamp(start_epoch)
        end = datetime.utcfromtimestamp(end_epoch)
        device = self.validate_and_get(device_urlsafe_key, ChromeOsDevice, abort_on_not_found=True)
        query = DeviceIssueLog.query(DeviceIssueLog.device_key == device.key,
                                     ndb.AND(DeviceIssueLog.created > start),
                                     ndb.AND(DeviceIssueLog.created <= end)).order(-DeviceIssueLog.created)
        latest_issues = query.fetch(config.LATEST_DEVICE_ISSUES_FETCH_COUNT)
        return json_response(self.response, latest_issues, strategy=DEVICE_ISSUE_LOG_STRATEGY)

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
        else:
            change_intent(device.gcm_registration_id, config.PLAYER_RESET_COMMAND)
            logging.info(
                'Player reset command issued prior to deleting device with key {0}'.format(device.key.urlsafe()))
            device.key.delete()
            self.response.headers.pop('Content-Type', None)
        self.response.set_status(status, message)
