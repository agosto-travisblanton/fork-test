import httplib
import json

from datetime import datetime, timedelta

import device_message_processor
from agar.test import BaseTest, WebTest
from app_config import config
from env_setup import setup_test_paths
from mockito import when, any as any_matcher
from models import ChromeOsDevice, Tenant, Distributor, Domain, DeviceIssueLog, Location, User
from routes import application
from utils.timezone_util import TimezoneUtil
from utils.web_util import build_uri
from webtest import AppError
from provisioning_distributor_user_base_test import ProvisioningDistributorUserBase

setup_test_paths()
from utils.auth_util import generate_token


class TestDeviceResourceHandler(BaseTest, WebTest):
    ADMIN_EMAIL = 'foo@bar.com'
    ANOTHER_TENANT_NAME = 'Another, Inc,'
    ANOTHER_TENANT_CODE = 'another_inc'
    ANOTHER_ADMIN_EMAIL = 'foo@another.com'
    APPLICATION = application
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    CONTENT_SERVER_URL = 'https://skykit-contentmanager-int.appspot.com/content'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
    DEVICE_ID = '132e235a-b346-4a37-a100-de49fa753a2a'
    GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
    MAC_ADDRESS = '54271e619346'
    TENANT_CODE = 'foobar_inc'
    TENANT_NAME = 'Foobar, Inc,'
    DISTRIBUTOR_NAME = 'Agosto'
    IMPERSONATION_EMAIL = 'test@test.com'
    DEVICE_NOTES = 'This is a device note'
    STORAGE_UTILIZATION = 26
    MEMORY_UTILIZATION = 63
    PROGRAM = 'some program'

    def setUp(self):
        super(TestDeviceResourceHandler, self).setUp()
        self.user = User.get_or_insert_by_email('donal@trump.gov')
        self.valid_authorization_header = {
            'Authorization': config.API_TOKEN,
            'JWT': str(generate_token(self.user))
        }
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
                                              active=True)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.distributor_key,
                                    impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                    active=True)
        self.domain_key = self.domain.put()
        self.tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                                    name=self.TENANT_NAME,
                                    admin_email=self.ADMIN_EMAIL,
                                    content_server_url=self.CONTENT_SERVER_URL,
                                    content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                    domain_key=self.domain_key,
                                    active=True)
        self.tenant_key = self.tenant.put()
        self.chrome_os_device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                                              device_id=self.DEVICE_ID,
                                                              gcm_registration_id=self.GCM_REGISTRATION_ID,
                                                              mac_address=self.MAC_ADDRESS)
        self.chrome_os_device_key = self.chrome_os_device.put()

        self.another_tenant = Tenant.create(tenant_code=self.ANOTHER_TENANT_CODE,
                                            name=self.ANOTHER_TENANT_NAME,
                                            admin_email=self.ANOTHER_ADMIN_EMAIL,
                                            content_server_url=self.CONTENT_SERVER_URL,
                                            content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                            domain_key=self.domain_key,
                                            active=True)
        self.another_tenant_key = self.another_tenant.put()
        self.unmanaged_device = ChromeOsDevice.create_unmanaged(self.GCM_REGISTRATION_ID, self.MAC_ADDRESS)
        self.unmanaged_device_key = self.unmanaged_device.put()
        self.managed_device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id=self.DEVICE_ID,
            mac_address=self.MAC_ADDRESS)
        self.managed_device_key = self.managed_device.put()

        self.unmanaged_registration_token_authorization_header = {
            'Authorization': config.UNMANAGED_REGISTRATION_TOKEN
        }

        self.api_token_authorization_header = {
            'Authorization': config.API_TOKEN,
            'JWT': str(generate_token(self.user))

        }

        self.unmanaged_api_token_authorization_header = {
            'Authorization': config.UNMANAGED_API_TOKEN
        }
        self.empty_header = {}
        self.put_uri_for_managed_device = \
            build_uri('internal-device-put', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})

    #################################################################################################################
    # GET internal device by key (managed and unmanaged)
    #################################################################################################################

    def test_get_managed_device_by_key_no_authorization_header_returns_forbidden(self):
        uri = build_uri('internal-device-get', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        response = self.get(uri, headers=self.empty_header)
        self.assertForbidden(response)

    def test_get_managed_device_by_key_http_status_ok(self):
        request_parameters = {}
        uri = build_uri('internal-device-get', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertOK(response)

    def test_get_unmanaged_device_by_key_http_status_ok(self):
        request_parameters = {}
        uri = build_uri('internal-device-get', params_dict={'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertOK(response)

    def test_get_device_by_key_returns_not_found_status_with_a_valid_key_not_found(self):
        new_device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id='4444-55555',
            mac_address='1231231321444')
        new_device_key = new_device.put()
        request_parameters = {}
        uri = build_uri('internal-device-get', params_dict={'device_urlsafe_key': new_device_key.urlsafe()})
        new_device.key.delete()
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('404 Not Found' in context.exception.message)

    def test_get_managed_device_by_key_returns_not_found_status_with_archived_true(self):
        new_device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id='2444-55550',
            mac_address='3231231321444')
        new_device.archived = True
        new_device_key = new_device.put()
        request_parameters = {}
        uri = build_uri('internal-device-get', params_dict={'device_urlsafe_key': new_device_key.urlsafe()})
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 404 Device with key: {0} archived.'.format(new_device_key.urlsafe())
                        in context.exception.message)

    def test_get_unmanaged_device_by_key_returns_not_found_status_with_archived_true(self):
        new_unmanaged_device = ChromeOsDevice.create_unmanaged(
            gcm_registration_id='EA13412341234',
            mac_address='81231223132')
        new_unmanaged_device.archived = True
        new_unmanaged_device_key = new_unmanaged_device.put()
        request_parameters = {}
        uri = build_uri('internal-device-get', params_dict={'device_urlsafe_key': new_unmanaged_device_key.urlsafe()})
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 404 Device with key: {0} archived.'.format(new_unmanaged_device_key.urlsafe())
                        in context.exception.message)

    def test_get_device_by_key_returns_bad_request_status_with_invalid_key(self):
        request_parameters = {}
        uri = build_uri('internal-device-get',
                        params_dict={'device_urlsafe_key': '0000ZXN0YmVkLXRlc3RyFAsSDkNocm9tZU9zRGV2aWNl0000'})
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('400 Bad Request' in context.exception.message)

    def test_get_device_by_key_entity_body_json(self):
        request_parameters = {}
        uri = build_uri('internal-device-get', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        device = self.managed_device_key.get()
        tenant = device.tenant_key.get()
        self.assertEqual(response_json['annotatedUser'], device.annotated_user)
        self.assertEqual(response_json['annotatedLocation'], device.annotated_location)
        self.assertEqual(response_json['apiKey'], device.api_key)
        self.assertEqual(response_json['bootMode'], device.boot_mode)
        self.assertEqual(response_json['created'], device.created.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response_json['deviceId'], device.device_id)
        self.assertEqual(response_json['ethernetMacAddress'], device.ethernet_mac_address)
        self.assertEqual(response_json['firmwareVersion'], device.firmware_version)
        self.assertEqual(response_json['gcmRegistrationId'], device.gcm_registration_id)
        self.assertEqual(response_json['key'], device.key.urlsafe())
        self.assertEqual(response_json['kind'], device.kind)
        self.assertEqual(response_json['lastEnrollmentTime'], device.last_enrollment_time)
        self.assertEqual(response_json['lastSync'], device.last_sync)
        self.assertEqual(response_json['macAddress'], device.mac_address)
        self.assertEqual(response_json['model'], device.model)
        self.assertEqual(response_json['orgUnitPath'], device.org_unit_path)
        self.assertEqual(response_json['osVersion'], device.os_version)
        self.assertEqual(response_json['platformVersion'], device.platform_version)
        self.assertEqual(response_json['serialNumber'], device.serial_number)
        self.assertEqual(response_json['status'], device.status)
        self.assertEqual(response_json['updated'], device.updated.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response_json['tenantKey'], tenant.key.urlsafe())
        self.assertEqual(response_json['chromeDeviceDomain'], self.CHROME_DEVICE_DOMAIN)
        self.assertEqual(response_json['logglyLink'], None)
        self.assertEqual(response_json['heartbeatInterval'], config.PLAYER_HEARTBEAT_INTERVAL_MINUTES)
        self.assertEqual(response_json['checkContentInterval'], config.CHECK_FOR_CONTENT_INTERVAL_MINUTES)

    def test_get_device_by_key_entity_body_json_logglyLink_when_serial_number_is_specified(self):
        self.managed_device.serial_number = "SN5552324"
        managed_device_key = self.managed_device.put()
        request_parameters = {}
        uri = build_uri('internal-device-get', params_dict={'device_urlsafe_key': managed_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        device = self.managed_device_key.get()
        self.assertEqual(response_json['logglyLink'], 'https://skykit.loggly.com/search?&terms=tag%3A"{0}"'.format(
            device.serial_number))

    ##################################################################################################################
    # PUT General internal updates
    ##################################################################################################################
    def test_put_no_authorization_header_returns_forbidden(self):
        request_body = {'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.TENANT_CODE,
                        'notes': self.DEVICE_NOTES}
        response = self.put(self.put_uri_for_managed_device, params=request_body, headers=self.empty_header)
        self.assertForbidden(response)

    def test_put_http_status_no_content(self):
        request_body = {'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.TENANT_CODE,
                        'notes': self.DEVICE_NOTES}
        response = self.put(self.put_uri_for_managed_device, params=json.dumps(request_body),
                            headers=self.api_token_authorization_header)
        self.assertEqual(httplib.NO_CONTENT, response.status_int)

    def test_put_returns_not_found_for_archived_device(self):
        archived_device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id='3444-55550',
            mac_address='9931231321444')
        archived_device.archived = True
        archived_device_key = archived_device.put()
        request_body = {}
        uri = build_uri('internal-device-put', params_dict={'device_urlsafe_key': archived_device_key.urlsafe()})
        with self.assertRaises(AppError) as context:
            self.app.put(uri, params=json.dumps(request_body),
                         headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 404 Device with key: {0} archived.'.format(archived_device_key.urlsafe())
                        in context.exception.message)

    def test_put_updates_orientation_mode(self):
        orientation_mode = '270'
        request_body = {
            'orientationMode': orientation_mode,
            'tenantCode': self.tenant_key.get().tenant_code
        }
        self.app.put(self.put_uri_for_managed_device, json.dumps(request_body),
                     headers=self.api_token_authorization_header)
        updated_display = self.managed_device_key.get()
        self.assertEqual(orientation_mode, updated_display.orientation_mode)

    def test_put_updates_device_with_an_explicit_tenant_change(self):
        new_tenant = self.another_tenant_key.get()
        request_body = {
            'tenantCode': new_tenant.tenant_code
        }
        self.app.put(self.put_uri_for_managed_device, json.dumps(request_body),
                     headers=self.api_token_authorization_header)
        updated_display = self.managed_device_key.get()
        self.assertNotEqual(self.tenant_key, updated_display.tenant_key)
        self.assertEqual(self.another_tenant_key, updated_display.tenant_key)

    def test_put_adds_tenant_key_for_unmanaged_device(self):
        device = ChromeOsDevice.create_unmanaged(gcm_registration_id=self.GCM_REGISTRATION_ID,
                                                 mac_address=self.MAC_ADDRESS)
        self.assertTrue(device.is_unmanaged_device)
        self.assertIsNone(device.tenant_key)
        key = device.put()
        request_body = {
            'tenantCode': self.TENANT_CODE
        }
        when(device_message_processor).post_unmanaged_device_info(any_matcher(self.GCM_REGISTRATION_ID),
                                                                  any_matcher(key.urlsafe())).thenReturn(None)
        uri = build_uri('internal-device-put', params_dict={'device_urlsafe_key': key.urlsafe()})
        self.app.put(uri, json.dumps(request_body), headers=self.api_token_authorization_header)
        updated_display = key.get()
        self.assertEqual(self.tenant_key, updated_display.tenant_key)

    def test_put_updates_location(self):
        location = Location.create(tenant_key=self.tenant_key,
                                   customer_location_name='Store 1234',
                                   customer_location_code='store_1234')
        location_key = location.put()
        request_body = {'locationKey': location_key.urlsafe()}
        self.app.put(self.put_uri_for_managed_device, json.dumps(request_body),
                     headers=self.api_token_authorization_header)
        updated_device = self.managed_device_key.get()
        self.assertEqual(updated_device.location_key, location_key)

    def test_put_does_not_update_non_unique_customer_display_code(self):
        customer_display_name = 'Panel in Reception'
        customer_display_code = 'panel_in_reception'
        device = self.managed_device_key.get()
        device.customer_display_name = customer_display_name
        device.customer_display_code = customer_display_code
        device.put()
        new_device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id='4444-55555',
            mac_address='555555555')
        new_device_key = new_device.put()
        request_body = {
            'customerDisplayName': customer_display_name,
            'customerDisplayCode': customer_display_code
        }
        uri = build_uri('internal-device-put', params_dict={'device_urlsafe_key': new_device_key.urlsafe()})
        with self.assertRaises(AppError) as context:
            self.app.put(uri, json.dumps(request_body), headers=self.api_token_authorization_header)
        message = 'Bad response: 409 Conflict. Customer display code "{0}" is already assigned for tenant.'.format(
            customer_display_code)
        self.assertTrue(message in context.exception.message)

    def test_put_does_not_update_non_same_customer_display_code(self):
        customer_display_name = 'Panel in Reception'
        customer_display_code = 'panel_in_reception'
        device = self.managed_device_key.get()
        device.customer_display_name = customer_display_name
        device.customer_display_code = customer_display_code
        device.put()
        new_display_name = 'Storage Room'
        request_body = {
            'customerDisplayName': new_display_name,
            'customerDisplayCode': customer_display_code
        }
        response = self.app.put(self.put_uri_for_managed_device, json.dumps(request_body),
                                headers=self.api_token_authorization_header)
        self.assertEqual(httplib.NO_CONTENT, response.status_int)
        self.assertEqual(device.customer_display_code, customer_display_code)
        self.assertEqual(device.customer_display_name, new_display_name)

    def test_put_does_not_update_invalid_heartbeat_interval(self):
        interval = 0
        request_body = {
            'heartbeatInterval': interval
        }
        self.app.put(self.put_uri_for_managed_device, json.dumps(request_body),
                     headers=self.api_token_authorization_header)
        updated_display = self.managed_device_key.get()
        self.assertEqual(config.PLAYER_HEARTBEAT_INTERVAL_MINUTES, updated_display.heartbeat_interval_minutes)

    def test_put_updates_valid_check_content_interval(self):
        interval = 3
        request_body = {
            'checkContentInterval': interval
        }
        self.app.put(self.put_uri_for_managed_device, json.dumps(request_body),
                     headers=self.api_token_authorization_header)
        updated_display = self.managed_device_key.get()
        self.assertNotEqual(config.CHECK_FOR_CONTENT_INTERVAL_MINUTES,
                            updated_display.check_for_content_interval_minutes)

    def test_put_updates_check_content_interval_zero(self):
        interval = 0
        request_body = {
            'checkContentInterval': interval
        }
        self.app.put(self.put_uri_for_managed_device, json.dumps(request_body),
                     headers=self.api_token_authorization_header)
        updated_display = self.managed_device_key.get()
        self.assertNotEqual(config.CHECK_FOR_CONTENT_INTERVAL_MINUTES,
                            updated_display.check_for_content_interval_minutes)

    def test_put_does_not_update_invalid_check_content_interval(self):
        interval = -1
        request_body = {
            'checkContentInterval': interval
        }
        self.app.put(self.put_uri_for_managed_device, json.dumps(request_body),
                     headers=self.api_token_authorization_header)
        updated_display = self.managed_device_key.get()
        self.assertEqual(config.CHECK_FOR_CONTENT_INTERVAL_MINUTES, updated_display.check_for_content_interval_minutes)

    def test_put_updates_timezone_from_default_to_explicit(self):
        default_timezone = config.DEFAULT_TIMEZONE
        explicit_timezone = 'America/Denver'
        self.assertEqual(self.managed_device.timezone_offset, TimezoneUtil.get_timezone_offset(default_timezone))
        request_body = {'timezone': explicit_timezone}
        self.app.put(self.put_uri_for_managed_device, json.dumps(request_body),
                     headers=self.api_token_authorization_header)
        updated_device = self.managed_device_key.get()
        expected_offset = TimezoneUtil.get_timezone_offset(explicit_timezone)
        self.assertEqual(updated_device.timezone, explicit_timezone)
        self.assertEqual(updated_device.timezone_offset, expected_offset)

    def test_get_following_unmanaged_tenant_update_yields_all_tenant_information_on_device(self):
        device = ChromeOsDevice.create_unmanaged(gcm_registration_id=self.GCM_REGISTRATION_ID,
                                                 mac_address=self.MAC_ADDRESS)
        self.assertTrue(device.is_unmanaged_device)
        self.assertIsNone(device.tenant_key)
        key = device.put()
        request_body = {
            'tenantCode': self.TENANT_CODE
        }
        when(device_message_processor).post_unmanaged_device_info(any_matcher(self.GCM_REGISTRATION_ID),
                                                                  any_matcher(key.urlsafe())).thenReturn(None)
        uri = build_uri('internal-device-put', params_dict={'device_urlsafe_key': key.urlsafe()})
        self.app.put(uri, json.dumps(request_body), headers=self.api_token_authorization_header)
        updated_display = key.get()
        self.assertEqual(self.tenant_key, updated_display.tenant_key)
        request_parameters = {}
        uri = build_uri('internal-device-get', params_dict={'device_urlsafe_key': key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertTrue(response_json['isUnmanagedDevice'])
        self.assertEqual(response_json['tenantCode'], self.TENANT_CODE)
        self.assertEqual(response_json['contentServerUrl'], self.CONTENT_SERVER_URL)
        self.assertEqual(response_json['gcmRegistrationId'], self.GCM_REGISTRATION_ID)
        self.assertEqual(response_json['macAddress'], self.MAC_ADDRESS)

    ##################################################################################################################
    # PUT sleep controller
    ##################################################################################################################
    def test_put_updates_sleep_controller(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                                                     any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        sleep_controller = 'rs232'
        request_body = {
            'sleepController': sleep_controller,
        }
        uri = application.router.build(None,
                                       'internal-sleep-controller',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        response = self.app.put(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertEqual(httplib.NO_CONTENT, response.status_int)
        self.assertEqual(self.chrome_os_device_key.get().sleep_controller, sleep_controller)

    ##################################################################################################################
    # PUT panel_sleep
    ##################################################################################################################

    def test_panel_sleep_returns_no_content_status(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                                                     any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        uri = application.router.build(None,
                                       'internal-panel-sleep',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {"panelSleep": True}
        response = self.app.put(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertEqual(httplib.NO_CONTENT, response.status_int)

    def test_panel_sleep_alters_device_value(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                                                     any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        device_sleep_value = self.chrome_os_device.panel_sleep
        self.assertFalse(device_sleep_value)

        uri = application.router.build(None,
                                       'internal-panel-sleep',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {"panelSleep": True}
        response = self.app.put(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertEqual(httplib.NO_CONTENT, response.status_int)
        device_sleep_value = self.chrome_os_device.panel_sleep
        self.assertTrue(device_sleep_value)

    def test_panel_sleep_with_bogus_device_key_returns_not_found_status(self):
        when(device_message_processor).change_intent(gcm_registration_id=self.chrome_os_device.gcm_registration_id,
                                                     payload=config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                                                     device_urlsafe_key=any_matcher(str),
                                                     host=any_matcher(str),
                                                     user_identifier=any_matcher(str)).thenReturn(None)
        bogus_key = '0AXC19Z0DE'
        uri = application.router.build(None,
                                       'internal-panel-sleep',
                                       None,
                                       {'device_urlsafe_key': bogus_key})
        request_body = {}
        try:

            self.app.put(uri, json.dumps(request_body), headers=self.valid_authorization_header)
            message = 'Bad response: 404 refresh_device_representation command not executed ' \
                      'because device not found with key: {1}'.format(bogus_key)
        except Exception, e:
            if e.__class__.__name__ == 'ProtocolBufferDecodeError':
                self.assertTrue(message in Exception.message)

    ##################################################################################################################
    # controls_mode
    ##################################################################################################################

    def test_controls_mode_returns_ok_status(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                                                     any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        uri = application.router.build(None,
                                       'internal-controls-mode',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {"controlsMode": 'invisible'}
        response = self.app.put(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertEqual(httplib.NO_CONTENT, response.status_int)

    def test_controls_mode_alters_device_value(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                                                     any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        device_controls_mode = self.chrome_os_device.controls_mode
        self.assertEqual('invisible', device_controls_mode)

        uri = application.router.build(None,
                                       'internal-controls-mode',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {"controlsMode": 'visible'}
        response = self.app.put(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertEqual(httplib.NO_CONTENT, response.status_int)
        device_controls_mode = self.chrome_os_device.controls_mode
        self.assertEqual(device_controls_mode, 'visible')

    def test_controls_mode_with_bogus_device_key_returns_not_found_status(self):
        when(device_message_processor).change_intent(gcm_registration_id=self.chrome_os_device.gcm_registration_id,
                                                     payload=config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                                                     device_urlsafe_key=any_matcher(str),
                                                     host=any_matcher(str),
                                                     user_identifier=any_matcher(str)).thenReturn(None)
        bogus_key = '0AXC19Z0DE'
        uri = application.router.build(None,
                                       'internal-controls-mode',
                                       None,
                                       {'device_urlsafe_key': bogus_key})
        request_body = {}
        try:
            self.app.put(uri, json.dumps(request_body), headers=self.valid_authorization_header)
            message = 'Bad response: 404 refresh_device_representation command not executed ' \
                      'because device not found with key: {1}'.format(bogus_key)
        except Exception, e:
            if e.__class__.__name__ == 'ProtocolBufferDecodeError':
                self.assertTrue(message in Exception.message)

    #################################################################################################################
    # DELETE
    #################################################################################################################

    def test_delete_no_authorization_header_returns_forbidden(self):
        uri = build_uri('internal-device-delete', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        response = self.delete(uri, headers=self.empty_header)
        self.assertForbidden(response)

    def test_delete_http_status_no_content(self):
        when(device_message_processor).change_intent(any_matcher(), config.PLAYER_RESET_COMMAND).thenReturn(None)
        uri = build_uri('internal-device-delete', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        response = self.delete(uri, headers=self.api_token_authorization_header)
        self.assertEqual(httplib.NO_CONTENT, response.status_int)

    def test_delete_archives_device(self):
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id='12312314',
            mac_address='00012341230')
        device.put()
        self.assertFalse(device.archived)
        when(device_message_processor).change_intent(any_matcher(), config.PLAYER_RESET_COMMAND).thenReturn(None)
        uri = build_uri('internal-device-delete', params_dict={'device_urlsafe_key': device.key.urlsafe()})
        self.delete(uri, headers=self.api_token_authorization_header)
        updated_device = device.key.get()
        self.assertIsNotNone(updated_device)
        self.assertTrue(updated_device.archived)

    def test_delete_returns_not_found_for_archived_device(self):
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id='3444-55550',
            mac_address='9931231321444')
        device.archived = True
        device_key = device.put()
        when(device_message_processor).change_intent(any_matcher(), config.PLAYER_RESET_COMMAND).thenReturn(None)
        uri = build_uri('internal-device-delete', params_dict={'device_urlsafe_key': device_key.urlsafe()})
        response = self.delete(uri, headers=self.api_token_authorization_header)
        self.assertEqual(httplib.NOT_FOUND, response.status_int)

    def test_archived_device_is_prevented_from_registering_again__with_same_gcm_registration_id(self):
        gcm_registration_id = 'APA91bH3BQC-a4VjIsHmXd7ZsP_CXCZcyJQdP0lHS_4qaNYcg'
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=gcm_registration_id,
            mac_address=self.MAC_ADDRESS)
        device.put()
        self.assertFalse(device.archived)
        when(device_message_processor).change_intent(any_matcher(), config.PLAYER_RESET_COMMAND).thenReturn(None)
        uri = build_uri('internal-device-delete', params_dict={'device_urlsafe_key': device.key.urlsafe()})
        self.delete(uri, headers=self.api_token_authorization_header)
        updated_device = device.key.get()
        self.assertTrue(updated_device.archived)
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': gcm_registration_id,
                        'tenantCode': self.TENANT_CODE}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body),
                          headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 409 Conflict gcm registration id is already assigned to a managed device.'
                        in context.exception.message)

    ##################################################################################################################
    # device issues
    ##################################################################################################################

    def test_get_latest_issues_without_token_returns_forbidden(self):
        request_body = {}
        uri = build_uri('internal-device-issues',
                        params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe(), 'prev_cursor_str': 'null',
                                     'next_cursor_str': 'null'})
        response = self.get(uri, params=request_body, headers=self.empty_header)
        self.assertForbidden(response)

    def test_get_latest_issues_with_token_returns_http_status_ok(self):
        start = datetime.utcnow() - timedelta(days=5)
        end = datetime.utcnow()
        start_epoch = int((start - datetime(1970, 1, 1)).total_seconds())
        end_epoch = int((end - datetime(1970, 1, 1)).total_seconds())
        request_parameters = {}
        uri = build_uri('internal-device-issues', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe(),
                                                      'start': start_epoch, 'end': end_epoch, 'next_cursor_str': 'null',
                                                      'prev_cursor_str': 'null'
                                                               })
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertOK(response)

    def test_get_latest_issues_returns_expected_elapsed_time_since_created_json(self):
        start = datetime.utcnow() - timedelta(days=5)
        end = datetime.utcnow()
        start_epoch = int((start - datetime(1970, 1, 1)).total_seconds())
        end_epoch = int((end - datetime(1970, 1, 1)).total_seconds())
        issue = DeviceIssueLog.create(device_key=self.managed_device_key,
                                      category=config.DEVICE_ISSUE_PLAYER_DOWN,
                                      up=False,
                                      storage_utilization=self.STORAGE_UTILIZATION,
                                      memory_utilization=self.MEMORY_UTILIZATION,
                                      program=self.PROGRAM,
                                      resolved=False)
        issue.created = datetime.utcnow() - timedelta(seconds=59)
        issue.put()
        request_parameters = {}
        uri = build_uri('internal-device-issues',
                        params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe(), 'prev_cursor_str': 'null',
                                     'next_cursor_str': 'null',
                                     'start': start_epoch, 'end': end_epoch})
        self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)

        issue.created = datetime.utcnow() - timedelta(seconds=90)
        issue.put()
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertEqual(response_json["issues"][0]['elapsedTime'], '1.5 minutes')

        issue.created = datetime.utcnow() - timedelta(minutes=59)
        issue.put()
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertEqual(response_json["issues"][0]['elapsedTime'], '59.0 minutes')

        issue.created = datetime.utcnow() - timedelta(minutes=90)
        issue.put()
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertEqual(response_json["issues"][0]['elapsedTime'], '1.5 hours')

        issue.created = datetime.utcnow() - timedelta(hours=23)
        issue.put()
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertEqual(response_json["issues"][0]['elapsedTime'], '23.0 hours')

        issue.created = datetime.utcnow() - timedelta(hours=48)
        issue.put()
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertEqual(response_json["issues"][0]['elapsedTime'], '2.0 days')

    def test_get_latest_issues_returns_expected_issue_order_with_latest_first(self):
        start = datetime.utcnow() - timedelta(days=5)
        end = datetime.utcnow()
        start_epoch = int((start - datetime(1970, 1, 1)).total_seconds())
        end_epoch = int((end - datetime(1970, 1, 1)).total_seconds())
        issue = DeviceIssueLog.create(device_key=self.managed_device_key,
                                      category=config.DEVICE_ISSUE_STORAGE_LOW,
                                      up=False,
                                      storage_utilization=99,
                                      memory_utilization=self.MEMORY_UTILIZATION,
                                      program=self.PROGRAM,
                                      resolved=False)
        issue.created = datetime.utcnow() - timedelta(hours=48)
        issue.put()
        issue = DeviceIssueLog.create(device_key=self.managed_device_key,
                                      category=config.DEVICE_ISSUE_MEMORY_HIGH,
                                      up=False,
                                      storage_utilization=self.STORAGE_UTILIZATION,
                                      memory_utilization=98,
                                      program=self.PROGRAM,
                                      resolved=False)
        issue.created = datetime.utcnow() - timedelta(hours=2)
        issue.put()
        issue = DeviceIssueLog.create(device_key=self.managed_device_key,
                                      category=config.DEVICE_ISSUE_PLAYER_DOWN,
                                      up=False,
                                      storage_utilization=self.STORAGE_UTILIZATION,
                                      memory_utilization=self.MEMORY_UTILIZATION,
                                      program=self.PROGRAM,
                                      resolved=False)
        issue.created = datetime.utcnow() - timedelta(minutes=10)
        issue.put()
        request_parameters = {}
        uri = build_uri('internal-device-issues',
                        params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe(), 'next_cursor_str': 'null',
                                     'prev_cursor_str': 'null',
                                     'start': start_epoch, 'end': end_epoch})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertLength(3, response_json)
        self.assertEqual(response_json["issues"][0]['category'], config.DEVICE_ISSUE_PLAYER_DOWN)
        self.assertEqual(response_json["issues"][1]['category'], config.DEVICE_ISSUE_MEMORY_HIGH)
        self.assertEqual(response_json["issues"][2]['category'], config.DEVICE_ISSUE_STORAGE_LOW)

    def test_get_latest_issues_returns_zero_issues_with_out_of_range_datetime(self):
        issue = DeviceIssueLog.create(device_key=self.managed_device_key,
                                      category=config.DEVICE_ISSUE_STORAGE_LOW,
                                      up=False,
                                      storage_utilization=99,
                                      memory_utilization=self.MEMORY_UTILIZATION,
                                      program=self.PROGRAM,
                                      resolved=False)
        issue.created = datetime.utcnow()
        issue.put()
        start = datetime.utcnow() - timedelta(days=10)
        end = datetime.utcnow() - timedelta(days=5)
        start_epoch = int((start - datetime(1970, 1, 1)).total_seconds())
        end_epoch = int((end - datetime(1970, 1, 1)).total_seconds())
        request_parameters = {}
        uri = build_uri('internal-device-issues',
                        params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe(), 'prev_cursor_str': 'null',
                                     'next_cursor_str': 'null',
                                     'start': start_epoch, 'end': end_epoch})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertLength(0, response_json["issues"])

    ##################################################################################################################
    # TENANT VIEW TESTS
    ##################################################################################################################

    def test_get_devices_by_tenant_http_status_ok(self):
        self.__build_list_devices(tenant_key=self.tenant_key, managed_number_to_build=20,
                                  unmanaged_number_to_build=0)
        request_parameters = {}

        uri = application.router.build(None, 'devices-by-tenant', None,
                                       {'tenant_urlsafe_key': self.tenant_key.urlsafe(), 'cur_prev_cursor': "null",
                                        "cur_next_cursor": "null"})

        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertOK(response)

    def test_get_devices_by_tenant_entity_body_json_and_page_forward(self):
        self.__build_list_devices(tenant_key=self.tenant_key, managed_number_to_build=201,
                                  unmanaged_number_to_build=0)

        request_parameters = {'unmanaged': 'false', 'prev_cursor': "null",
                              "next_cursor": "null"}

        uri = application.router.build(None, 'devices-by-tenant', None,
                                       {'tenant_urlsafe_key': self.tenant_key.urlsafe()})

        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertLength(10, response_json["devices"])

        next_uri = application.router.build(None, 'devices-by-tenant', None,
                                            {'tenant_urlsafe_key': self.tenant_key.urlsafe()})

        next_params = {'unmanaged': 'false', 'prev_cursor': "null",
                       "next_cursor": response_json["next_cursor"]}

        next_response = self.app.get(next_uri, params=next_params, headers=self.api_token_authorization_header)
        next_response_json = json.loads(next_response.body)
        self.assertLength(10, next_response_json["devices"])
        self.assertTrue(next_response_json["prev_cursor"])

    def test_get_filter_unmanaged_devices_by_tenant_entity_body_json(self):
        self.__build_list_devices(tenant_key=self.tenant_key, managed_number_to_build=20,
                                  unmanaged_number_to_build=0)

        request_parameters = {'unmanaged': 'true', 'prev_cursor': "null",
                              "next_cursor": "null"}

        uri = application.router.build(None, 'devices-by-tenant', None,
                                       {'tenant_urlsafe_key': self.tenant_key.urlsafe()})

        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertLength(0, response_json["devices"])

    def __create_tenant(self, code, name, email):
        tenant = Tenant.create(tenant_code=code,
                               name=name,
                               admin_email=email,
                               content_server_url=self.CONTENT_SERVER_URL,
                               content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                               chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                               domain_key=self.domain_key,
                               active=True)
        return tenant.put()

    def __build_list_devices(self, tenant_key=None, managed_number_to_build=5, unmanaged_number_to_build=5):
        results = []

        if tenant_key is None:
            tenant_key = self.__create_tenant()

        for i in range(managed_number_to_build):
            mac_address = 'm-mac{0}'.format(i)
            gcm_registration_id = 'm-gcm{0}'.format(i)
            device_id = 'd{0}'.format(i)
            device = ChromeOsDevice.create_managed(tenant_key=tenant_key,
                                                   mac_address=mac_address,
                                                   gcm_registration_id=gcm_registration_id,
                                                   device_id=device_id)
            device.archived = False
            device.put()
            results.append(device)

        for i in range(unmanaged_number_to_build):
            mac_address = 'u-mac{0}'.format(i)
            gcm_registration_id = 'u-gcm{0}'.format(i)
            device = ChromeOsDevice.create_unmanaged(gcm_registration_id=gcm_registration_id,
                                                     mac_address=mac_address)
            device.put()
            results.append(device)

        return results
