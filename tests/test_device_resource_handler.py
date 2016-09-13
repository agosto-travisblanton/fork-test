import json

from datetime import datetime, timedelta
from google.appengine.ext import ndb

import device_message_processor
from agar.test import BaseTest, WebTest
from app_config import config
from env_setup import setup_test_paths
from mockito import when, any as any_matcher
from models import ChromeOsDevice, Tenant, Distributor, Domain, DeviceIssueLog, Location
from routes import application
from utils.email_notify import EmailNotify
from utils.timezone_util import TimezoneUtil
from utils.web_util import build_uri
from webtest import AppError

setup_test_paths()


class TestDeviceResourceHandler(BaseTest, WebTest):
    ADMIN_EMAIL = 'foo@bar.com'
    ANOTHER_TENANT_NAME = 'Another, Inc,'
    ANOTHER_TENANT_CODE = 'another_inc'
    ANOTHER_ADMIN_EMAIL = 'foo@another.com'
    APPLICATION = application
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    CONTENT_SERVER_API_KEY = 'API KEY'
    CONTENT_SERVER_URL = 'https://skykit-contentmanager-int.appspot.com/content'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
    DEVICE_ID = '132e235a-b346-4a37-a100-de49fa753a2a'
    GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
    MAC_ADDRESS = '54271e619346'
    ETHERNET_MAC_ADDRESS = '8e271e619346'
    TENANT_CODE = 'foobar_inc'
    TENANT_NAME = 'Foobar, Inc,'
    DISTRIBUTOR_NAME = 'agosto'
    IMPERSONATION_EMAIL = 'test@test.com'
    DEVICE_NOTES = 'This is a device note'
    PAIRING_CODE = '0e8f-fc4e-d632-09dc'
    STORAGE_UTILIZATION = 26
    MEMORY_UTILIZATION = 63
    PROGRAM = 'some program'
    PROGRAM_ID = 'ID-512341234'
    PLAYLIST = 'some playlist'
    PLAYLIST_ID = 'Playlist Id'
    LAST_ERROR = 'some error'

    def setUp(self):
        super(TestDeviceResourceHandler, self).setUp()
        self.valid_authorization_header = {
            'Authorization': config.API_TOKEN
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
            'Authorization': config.API_TOKEN
        }
        self.unmanaged_api_token_authorization_header = {
            'Authorization': config.UNMANAGED_API_TOKEN
        }

        self.empty_header = {}

    ##################################################################################################################
    # post ChromeOsDevice
    ##################################################################################################################

    def test_post_managed_device_http_status_created(self):
        when(EmailNotify).device_enrolled(tenant_code=any_matcher(),
                                          tenant_name=any_matcher(),
                                          device_mac_address=any_matcher(),
                                          timestamp=any_matcher()).thenReturn(None)

        tenant = self.tenant_key.get()
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': 'foobar',
                        'tenantCode': tenant.tenant_code}
        response = self.app.post('/api/v1/devices', json.dumps(request_body),
                                 headers=self.api_token_authorization_header)
        self.assertEqual('201 Created', response.status)
        self.assertEqual(201, response.status_int)

    def test_post_managed_device_returns_resource_url_in_location_header(self):
        when(EmailNotify).device_enrolled(tenant_code=any_matcher(),
                                          tenant_name=any_matcher(),
                                          device_mac_address=any_matcher(),
                                          timestamp=any_matcher()).thenReturn(None)

        tenant = self.tenant_key.get()
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': 'foobar',
                        'tenantCode': tenant.tenant_code}
        response = self.app.post('/api/v1/devices', json.dumps(request_body),
                                 headers=self.api_token_authorization_header)
        location_uri_components = str(response.headers['Location']).split('/')
        self.assertEqual(location_uri_components[5], "devices")
        device = ndb.Key(urlsafe=location_uri_components[6]).get()
        self.assertIsNotNone(device)

    def test_device_resource_handler_post_no_authorization_header_returns_forbidden(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.TENANT_CODE}
        uri = build_uri('device-creator')
        response = self.post(uri, params=request_body, headers=self.empty_header)
        self.assertForbidden(response)

    def test_device_resource_handler_post_no_returns_conflict_if_gcm_id_is_already_assigned_to_device(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.TENANT_CODE}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body),
                          headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 409 Conflict gcm registration id is already assigned to a managed device.'
                        in context.exception.message)

    def test_device_resource_handler_post_no_returns_bad_response_for_empty_tenant_code(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': 'foobar',
                        'tenantCode': None}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body),
                          headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 400 The tenantCode parameter is invalid.'
                        in context.exception.message)

    def test_device_resource_handler_post_no_returns_bad_response_for_empty_gcm(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': None,
                        'tenantCode': self.TENANT_CODE}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body),
                          headers=self.api_token_authorization_header)
        self.assertTrue('required field gcmRegistrationId not found'
                        in context.exception.message)

    def test_device_resource_handler_post_no_returns_bad_response_for_empty_mac_address(self):
        request_body = {'macAddress': None,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.TENANT_CODE}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body),
                          headers=self.api_token_authorization_header)
        print context.exception.message
        self.assertTrue('required field macAddress not found'
                        in context.exception.message)

    def test_post_managed_device_when_cannot_resolve_tenant(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': 'foobar',
                        'tenantCode': 'unresolvable_tenant_code'}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body),
                          headers=self.api_token_authorization_header)
        print context.exception.message
        self.assertTrue('400 Cannot resolve tenant from tenant code. Bad tenant code or inactive tenant.'
                        in context.exception.message)

    def test_post_managed_device_creates_device_with_default_timezone_and_expected_offset(self):
        when(EmailNotify).device_enrolled(tenant_code=any_matcher(),
                                          tenant_name=any_matcher(),
                                          device_mac_address=any_matcher(),
                                          timestamp=any_matcher()).thenReturn(None)
        tenant = self.tenant_key.get()
        mac_address = self.MAC_ADDRESS
        request_body = {'macAddress': mac_address,
                        'gcmRegistrationId': 'foobar',
                        'tenantCode': tenant.tenant_code}
        response = self.app.post('/api/v1/devices', json.dumps(request_body),
                                 headers=self.api_token_authorization_header)
        location_uri_components = str(response.headers['Location']).split('/')
        device = ndb.Key(urlsafe=location_uri_components[6]).get()
        default_timezone = config.DEFAULT_TIMEZONE
        self.assertEqual(device.timezone_offset, TimezoneUtil.get_timezone_offset(default_timezone))
        self.assertEqual(device.timezone, default_timezone)

    def test_post_managed_device_creates_device_with_explicit_timezone_and_expected_offset(self):
        when(EmailNotify).device_enrolled(tenant_code=any_matcher(),
                                          tenant_name=any_matcher(),
                                          device_mac_address=any_matcher(),
                                          timestamp=any_matcher()).thenReturn(None)

        tenant = self.tenant_key.get()
        explicit_timezone = 'America/Denver'
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': 'foobar',
                        'tenantCode': tenant.tenant_code,
                        'timezone': explicit_timezone}
        response = self.app.post('/api/v1/devices', json.dumps(request_body),
                                 headers=self.api_token_authorization_header)
        location_uri_components = str(response.headers['Location']).split('/')
        device = ndb.Key(urlsafe=location_uri_components[6]).get()
        self.assertEqual(device.timezone_offset, TimezoneUtil.get_timezone_offset(explicit_timezone))
        self.assertEqual(device.timezone, explicit_timezone)

    ##################################################################################################################
    # post unmanaged device
    ##################################################################################################################
    def test_device_resource_handler_unmanaged_post_returns_created_status_code(self):
        new_mac_address = '1111111111'
        new_gcm_registration_id = '222222222'
        request_body = {'macAddress': new_mac_address,
                        'gcmRegistrationId': new_gcm_registration_id}
        response = self.app.post('/api/v1/devices', json.dumps(request_body),
                                 headers=self.unmanaged_registration_token_authorization_header)
        self.assertEqual('201 Created', response.status)
        self.assertEqual(201, response.status_int)

    def test_device_resource_handler_unmanaged_post_returns_cannot_register_when_gcm_already_assigned(self):
        request_body = {'macAddress': '123',
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body),
                          headers=self.unmanaged_registration_token_authorization_header)
        self.assertTrue('Bad response: 409 Conflict gcm registration id is already assigned to an unmanaged device' in
                        context.exception.message)

    def test_device_resource_handler_unmanaged_post_returns_cannot_register_when_mac_already_assigned(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': '23413423'}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body),
                          headers=self.unmanaged_registration_token_authorization_header)
        self.assertTrue('Bad response: 409 Conflict mac address is already assigned to an unmanaged device' in
                        context.exception.message)

    def test_device_resource_handler_unmanaged_post_returns_bad_response_for_empty_gcm(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': None}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body),
                          headers=self.unmanaged_registration_token_authorization_header)
        self.assertTrue('required field gcmRegistrationId not found'
                        in context.exception.message)

    def test_device_resource_handler_unmanaged_post_returns_bad_response_for_empty_mac_address(self):
        request_body = {'macAddress': None,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body),
                          headers=self.unmanaged_registration_token_authorization_header)
        self.assertTrue('required field macAddress not found'
                        in context.exception.message)

    def test_device_resource_handler_unmanaged_post_populates_location_header(self):
        new_mac_address = '1111111111'
        new_gcm_registration_id = '222222222'
        request_body = {'macAddress': new_mac_address,
                        'gcmRegistrationId': new_gcm_registration_id}
        response = self.app.post('/api/v1/devices', json.dumps(request_body),
                                 headers=self.unmanaged_registration_token_authorization_header)
        self.assertIsNotNone(response.headers['Location'])

    def test_device_resource_handler_unmanaged_post_populates_location_header_with_devices_route(self):
        new_mac_address = '1111111111'
        new_gcm_registration_id = '222222222'
        request_body = {'macAddress': new_mac_address,
                        'gcmRegistrationId': new_gcm_registration_id}
        response = self.app.post('/api/v1/devices', json.dumps(request_body),
                                 headers=self.unmanaged_registration_token_authorization_header)
        location_uri_components = str(response.headers['Location']).split('/')
        self.assertEqual(location_uri_components[5], "devices")

    def test_device_resource_handler_unmanaged_post_populates_location_header_with_resolvable_resource(self):
        new_mac_address = '1111111111'
        new_gcm_registration_id = '222222222'
        request_body = {'macAddress': new_mac_address,
                        'gcmRegistrationId': new_gcm_registration_id}
        response = self.app.post('/api/v1/devices', json.dumps(request_body),
                                 headers=self.unmanaged_registration_token_authorization_header)
        uri = response.headers['Location']
        request_parameters = {}
        response = self.app.get(uri, params=request_parameters,
                                headers=self.unmanaged_registration_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertLength(3, response_json)
        self.assertIsNotNone(response_json['pairingCode'])
        self.assertEqual(response_json['gcmRegistrationId'], new_gcm_registration_id)
        self.assertEqual(response_json['macAddress'], new_mac_address)

     #################################################################################################################
    # get_device_by_parameter - pairing code lookup
    #################################################################################################################

    def test_get_device_by_pairing_code_returns_http_status_ok(self):
        self.unmanaged_device.pairing_code = self.PAIRING_CODE
        self.unmanaged_device.put()
        request_parameters = {'pairingCode': self.PAIRING_CODE}
        uri = build_uri('devices-retrieval')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertOK(response)

    def test_get_device_by_pairing_code_returns_not_found_for_non_existent_code(self):
        request_parameters = {'pairingCode': self.PAIRING_CODE}
        uri = build_uri('devices-retrieval')
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 404 Unable to find device by pairing code: {0}'.format(
            self.PAIRING_CODE) in context.exception.message)

    def test_get_device_by_pairing_code_returns_single_resource(self):
        self.unmanaged_device.pairing_code = self.PAIRING_CODE
        self.unmanaged_device.put()
        request_parameters = {'pairingCode': self.PAIRING_CODE}
        uri = build_uri('devices-retrieval')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertEqual(response_json['pairingCode'], self.PAIRING_CODE)
        device = self.managed_device_key.get()
        self.assertEqual(response_json['gcmRegistrationId'], device.gcm_registration_id)

    def test_get_device_by_pairing_code_with_archived_true_returns_http_status_not_found(self):
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id=self.DEVICE_ID,
            mac_address=self.MAC_ADDRESS)
        device.archived = True
        device.put()
        request_parameters = {'pairingCode': self.PAIRING_CODE}
        uri = build_uri('devices-retrieval')
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue("Unable to find device by pairing code: {0}".format(self.PAIRING_CODE) in
                        context.exception.message)

    def test_get_device_by_pairing_code_returns_zeroeth_resource_when_dupes(self):
        device_1 = ChromeOsDevice.create_unmanaged(
            gcm_registration_id='g1111',
            mac_address='m1111')
        device_1.pairing_code = self.PAIRING_CODE
        device_1.put()
        device_2 = ChromeOsDevice.create_unmanaged(
            gcm_registration_id='g2222',
            mac_address='m2222')
        device_2.pairing_code = self.PAIRING_CODE
        device_2.put()
        request_parameters = {'pairingCode': self.PAIRING_CODE}
        uri = build_uri('devices-retrieval')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertEqual(response_json['pairingCode'], self.PAIRING_CODE)
        self.assertEqual(response_json['gcmRegistrationId'], 'g1111')
        self.assertEqual(response_json['macAddress'], 'm1111')

    #################################################################################################################
    # get_device_by_parameter - gcm_registration_id and mac_address lookup
    #################################################################################################################

    def test_get_device_by_gcm_registration_id_and_mac_returns_http_status_ok_with_valid_parameters(self):
        device = ChromeOsDevice.create_unmanaged(gcm_registration_id=self.GCM_REGISTRATION_ID,
                                                 mac_address=self.MAC_ADDRESS)
        device.put()
        request_parameters = {'gcmRegistrationId': self.GCM_REGISTRATION_ID, 'macAddress': self.MAC_ADDRESS}
        uri = build_uri('devices-retrieval')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertOK(response)

    def test_get_device_by_gcm_registration_id_and_mac_returns_http_status_bad_request_with_missing_mac(self):
        request_parameters = {'gcmRegistrationId': self.GCM_REGISTRATION_ID}
        uri = build_uri('devices-retrieval')
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 400 Bad Request' in context.exception.message)

    def test_get_device_by_gcm_registration_id_and_mac_returns_http_status_bad_request_with_missing_gcm(self):
        request_parameters = {'macAddress': self.MAC_ADDRESS}
        uri = build_uri('devices-retrieval')
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 400 Bad Request' in context.exception.message)

    def test_get_device_by_returns_http_status_bad_request_with_missing_parameters(self):
        request_parameters = {}
        uri = build_uri('devices-retrieval')
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 400 Bad Request' in context.exception.message)

    def test_get_device_by_gcm_registration_id_returns_http_status_ok_with_just_valid_mac_and_invalid_gcm(self):
        device = ChromeOsDevice.create_unmanaged(gcm_registration_id=self.GCM_REGISTRATION_ID,
                                                 mac_address=self.MAC_ADDRESS)
        device.put()
        request_parameters = {'gcmRegistrationId': 'foobar', 'macAddress': self.MAC_ADDRESS}
        uri = build_uri('devices-retrieval')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertOK(response)

    def test_get_list_by_gcm_registration_id_returns_zeroeth_resource(self):
        gcm_registration_id = '123123123123'
        device = ChromeOsDevice.create_unmanaged(gcm_registration_id=gcm_registration_id,
                                                 mac_address=self.MAC_ADDRESS)
        device.put()
        request_parameters = {'gcmRegistrationId': gcm_registration_id, 'macAddress': self.MAC_ADDRESS}
        uri = build_uri('devices-retrieval')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertEqual(response_json['gcmRegistrationId'], device.gcm_registration_id)

    def test_get_device_with_bogus_gcm_registration_id_and_bogus_mac_returns_http_status_not_found(self):
        gcm_registration_id = 'foobar'
        mac_address = 'goober'
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=gcm_registration_id,
            device_id=self.DEVICE_ID,
            mac_address=self.MAC_ADDRESS)
        device.archived = True
        device.put()
        request_parameters = {'gcmRegistrationId': gcm_registration_id, 'macAddress': mac_address}
        uri = build_uri('devices-retrieval')
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        error_message = '404 Unable to find device by GCM registration ID: {0} or MAC address: {1}'.format(
            gcm_registration_id, mac_address)
        self.assertTrue(error_message in context.exception.message)

    def test_get_device_by_gcm_registration_id_with_archived_true_returns_http_status_not_found(self):
        mac_address = '123303042'
        gcm_registration_id = 'AGG343K123JE12'
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=gcm_registration_id,
            device_id=self.DEVICE_ID,
            mac_address=mac_address)
        device.archived = True
        device.put()
        request_parameters = {'macAddress': mac_address,
                              'gcmRegistrationId': gcm_registration_id}
        uri = build_uri('devices-retrieval')
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        error_message = '404 Unable to find device by GCM registration ID: {0} or MAC address: {1}'.format(
            gcm_registration_id, mac_address)
        self.assertTrue(error_message in context.exception.message)

    def test_get_device_by_mac_address_with_archived_false_returns_expected_device(self):
        mac_address = '2342342342342'
        gcm_registration_id = 'AG123JKLKJ2123'
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=gcm_registration_id,
            device_id=self.DEVICE_ID,
            mac_address=mac_address)
        device.put()
        request_parameters = {'macAddress': mac_address, 'gcmRegistrationId':gcm_registration_id}
        uri = build_uri('devices-retrieval')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertEqual(response_json['macAddress'], mac_address)
        self.assertEqual(response_json['gcmRegistrationId'], gcm_registration_id)

    def test_get_device_by_mac_address_with_rogue_unmanaged_device_should_archive_device(self):
        mac_address = '1123123132'
        gcm_registration_id_1 = '1AG123JKLKJ2123WE'
        gcm_registration_id_2 = '2AG123JKLKJ2123WE'
        rogue = ChromeOsDevice.create_unmanaged(gcm_registration_id_1, mac_address)
        rogue.pairing_code = 'pairing-code'
        rogue_key = rogue.put()
        self.assertTrue(ChromeOsDevice.get_unmanaged_device_by_mac_address(mac_address))
        self.assertFalse(rogue.archived)
        request_parameters = {'macAddress': mac_address, 'gcmRegistrationId':gcm_registration_id_2}
        uri = build_uri('devices-retrieval')
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue("Bad response: 404 Rogue unmanaged device with MAC address: {0} no longer exists.".format(
            mac_address) in context.exception.message)
        archived_device = rogue_key.get()
        self.assertTrue(archived_device.archived)

    def test_get_device_by_mac_address_with_rogue_unmanged_device_with_tenant_key_does_not_delete_device(self):
        mac_address = '2e871e619346'
        gcm_registration_id_1 = '1BG123JKLKJ2123EDF'
        gcm_registration_id_2 = '2BG123JKLKJ2123EDF'
        unmanaged_device = ChromeOsDevice.create_unmanaged(gcm_registration_id_1, mac_address)
        unmanaged_device.tenant_key = self.tenant_key
        unmanaged_device_key = unmanaged_device.put()
        self.assertIsNotNone(unmanaged_device.tenant_key)
        self.assertIsNotNone(unmanaged_device)
        self.assertFalse(unmanaged_device.archived)
        request_parameters = {'macAddress': mac_address, 'gcmRegistrationId':gcm_registration_id_2}
        uri = build_uri('devices-retrieval')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        device = unmanaged_device_key.get()
        self.assertIsNotNone(device)
        self.assertFalse(device.archived)
        response_json = json.loads(response.body)
        self.assertEqual(response_json['macAddress'], mac_address)

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
        self.assertLength(25, response_json["devices"])

        next_uri = application.router.build(None, 'devices-by-tenant', None,
                                            {'tenant_urlsafe_key': self.tenant_key.urlsafe()})

        next_params = {'unmanaged': 'false', 'prev_cursor': "null",
                       "next_cursor": response_json["next_cursor"]}

        next_response = self.app.get(next_uri, params=next_params, headers=self.api_token_authorization_header)
        next_response_json = json.loads(next_response.body)
        self.assertLength(25, next_response_json["devices"])
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

    #################################################################################################################
    # get managed device
    #################################################################################################################

    def test_get_device_by_key_no_authorization_header_returns_forbidden(self):
        uri = build_uri('device', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        response = self.get(uri, headers=self.empty_header)
        self.assertForbidden(response)

    def test_get_device_by_key_http_status_ok(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': new_device_key.urlsafe()})
        new_device.key.delete()
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('404 Not Found' in context.exception.message)

    def test_get_device_by_key_returns_not_found_status_with_archived_true(self):
        new_device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id='2444-55550',
            mac_address='3231231321444')
        new_device.archived = True
        new_device_key = new_device.put()
        request_parameters = {}
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': new_device_key.urlsafe()})
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 404 Device with key: {0} archived.'.format(new_device_key.urlsafe())
                        in context.exception.message)

    def test_get_device_by_key_returns_bad_request_status_with_invalid_key(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': '0000ZXN0YmVkLXRlc3RyFAsSDkNocm9tZU9zRGV2aWNl0000'})
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('400 Bad Request' in context.exception.message)

    def test_get_device_by_key_entity_body_json(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': managed_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        device = self.managed_device_key.get()
        self.assertEqual(response_json['logglyLink'], 'https://skykit.loggly.com/search?&terms=tag%3A"{0}"'.format(
            device.serial_number))

    ##################################################################################################################
    # get unmanaged device
    ##################################################################################################################

    def test_get_unmanaged_device_by_key_http_status_ok(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters,
                                headers=self.unmanaged_api_token_authorization_header)
        self.assertOK(response)

    def test_get_unmanaged_device_by_key_returns_not_found_status_with_a_key_for_a_soft_deleted_device(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})
        self.unmanaged_device.archived = True
        self.unmanaged_device.put()
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters,
                         headers=self.unmanaged_api_token_authorization_header)
        self.assertTrue('Device with key: {0} archived.'.format(self.unmanaged_device_key.urlsafe())
                        in context.exception.message)

    ##################################################################################################################
    # get pairing code
    ##################################################################################################################

    def test_get_get_pairing_code_returns_status_ok(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'device-pairing-code',
                                       None,
                                       {'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters,
                                headers=self.unmanaged_registration_token_authorization_header)
        self.assertOK(response)

    def test_get_get_pairing_code_returns_expected_property_count_in_json(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'device-pairing-code',
                                       None,
                                       {'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters,
                                headers=self.unmanaged_registration_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertLength(3, response_json)

    def test_get_get_pairing_code_returns_pairing_code_in_json(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'device-pairing-code',
                                       None,
                                       {'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters,
                                headers=self.unmanaged_registration_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertIsNotNone(response_json['pairingCode'])

    def test_get_get_pairing_code_returns_gcm_registration_id_in_json(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'device-pairing-code',
                                       None,
                                       {'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters,
                                headers=self.unmanaged_registration_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertIsNotNone(response_json['gcmRegistrationId'])

    def test_get_get_pairing_code_returns_mac_address_in_json(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'device-pairing-code',
                                       None,
                                       {'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters,
                                headers=self.unmanaged_registration_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertIsNotNone(response_json['macAddress'])

    def test_get_get_pairing_code_with_wrong_token(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'device-pairing-code',
                                       None,
                                       {'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})

        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters,
                         headers=self.unmanaged_api_token_authorization_header)
        self.assertTrue('Bad response: 403 Forbidden' in context.exception.message)

    def test_get_get_pairing_code_returns_not_found_for_archived_device(self):
        device = ChromeOsDevice.create_unmanaged(
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            mac_address='9931231321444')
        device.archived = True
        device_key = device.put()
        request_parameters = {}
        uri = application.router.build(None,
                                       'device-pairing-code',
                                       None,
                                       {'device_urlsafe_key': device_key.urlsafe()})
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters,
                         headers=self.unmanaged_registration_token_authorization_header)
        self.assertTrue('Bad response: 404 Device with key: {0} archived.'.format(device_key.urlsafe())
                        in context.exception.message)

    ##################################################################################################################
    # put
    ##################################################################################################################
    ##################################################################################################################
    # panel_sleep
    ##################################################################################################################

    def test_panel_sleep_returns_ok_status(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                                                     any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        uri = application.router.build(None,
                                       'panel_sleep',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {"panelSleep": True}
        response = self.app.put(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_panel_sleep_alters_device_value(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                                                     any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        device_sleep_value = self.chrome_os_device.panel_sleep
        self.assertFalse(device_sleep_value)

        uri = application.router.build(None,
                                       'panel_sleep',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {"panelSleep": True}
        response = self.app.put(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertOK(response)
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
                                       'panel_sleep',
                                       None,
                                       {'device_urlsafe_key': bogus_key})
        request_body = {}
        try:

            self.app.put(uri, json.dumps(request_body), headers=self.valid_authorization_header)
            message = 'Bad response: 404 refresh_device_representation command not executed because device not found with key: {1}'.format(
                bogus_key
            )
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
                                       'controls_mode',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {"controlsMode": 'invisible'}
        response = self.app.put(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_controls_mode_alters_device_value(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                                                     any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        device_controls_mode = self.chrome_os_device.controls_mode
        self.assertEqual('invisible', device_controls_mode)

        uri = application.router.build(None,
                                       'controls_mode',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {"controlsMode": 'visible'}
        response = self.app.put(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertOK(response)
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
                                       'controls_mode',
                                       None,
                                       {'device_urlsafe_key': bogus_key})
        request_body = {}
        try:
            self.app.put(uri, json.dumps(request_body), headers=self.valid_authorization_header)
            message = 'Bad response: 404 refresh_device_representation command not executed because device not found with key: {1}'.format(
                bogus_key
            )
        except Exception, e:
            if e.__class__.__name__ == 'ProtocolBufferDecodeError':
                self.assertTrue(message in Exception.message)


    def test_put_no_authorization_header_returns_forbidden(self):
        request_body = {'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.TENANT_CODE,
                        'notes': self.DEVICE_NOTES}
        uri = build_uri('device', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        response = self.put(uri, params=request_body, headers=self.empty_header)
        self.assertForbidden(response)

    def test_put_http_status_no_content(self):
        request_body = {'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.tenant_key.get().tenant_code,
                        'notes': self.DEVICE_NOTES
                        }
        response = self.app.put('/api/v1/devices/{0}'.format(self.managed_device_key.urlsafe()),
                                json.dumps(request_body),
                                headers=self.api_token_authorization_header)
        self.assertEqual('204 No Content', response.status)
        self.assertEqual(204, response.status_int)

    def test_put_returns_not_found_for_archived_device(self):
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id='3444-55550',
            mac_address='9931231321444')
        device.archived = True
        device_key = device.put()
        request_body = {}
        with self.assertRaises(AppError) as context:
            self.app.put('/api/v1/devices/{0}'.format(device_key.urlsafe()),
                         json.dumps(request_body),
                         headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 404 Device with key: {0} archived.'.format(device_key.urlsafe())
                        in context.exception.message)

    def test_put_updates_device_notes(self):
        new_note = 'new note'
        request_body = {
            'notes': new_note
        }
        self.app.put('/api/v1/devices/{0}'.format(self.managed_device_key.urlsafe()),
                     json.dumps(request_body),
                     headers=self.api_token_authorization_header)
        updated_display = self.managed_device_key.get()
        self.assertNotEqual(self.DEVICE_NOTES, updated_display.notes)
        self.assertEqual(new_note, updated_display.notes)

    def test_put_updates_device_gcm_registration_id(self):
        gcm_registration_id = 'd23784972038845ab3963412'
        request_body = {
            'gcmRegistrationId': gcm_registration_id,
            'tenantCode': self.tenant_key.get().tenant_code
        }
        self.app.put('/api/v1/devices/{0}'.format(self.managed_device_key.urlsafe()),
                     json.dumps(request_body),
                     headers=self.api_token_authorization_header)
        updated_display = self.managed_device_key.get()
        self.assertNotEqual(self.GCM_REGISTRATION_ID, updated_display.gcm_registration_id)
        self.assertEqual(gcm_registration_id, updated_display.gcm_registration_id)

    def test_put_updates_device_with_an_explicit_tenant_change(self):
        new_tenant = self.another_tenant_key.get()
        request_body = {
            'tenantCode': new_tenant.tenant_code
        }
        self.app.put('/api/v1/devices/{0}'.format(self.managed_device_key.urlsafe()),
                     json.dumps(request_body),
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
        self.app.put('/api/v1/devices/{0}'.format(key.urlsafe()),
                     json.dumps(request_body),
                     headers=self.api_token_authorization_header)
        updated_display = key.get()
        self.assertEqual(self.tenant_key, updated_display.tenant_key)

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
        self.app.put('/api/v1/devices/{0}'.format(key.urlsafe()),
                     json.dumps(request_body),
                     headers=self.api_token_authorization_header)
        updated_display = key.get()
        self.assertEqual(self.tenant_key, updated_display.tenant_key)

        request_parameters = {}
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertTrue(response_json['isUnmanagedDevice'])
        self.assertEqual(response_json['tenantCode'], self.TENANT_CODE)
        self.assertEqual(response_json['contentServerUrl'], self.CONTENT_SERVER_URL)
        self.assertEqual(response_json['gcmRegistrationId'], self.GCM_REGISTRATION_ID)
        self.assertEqual(response_json['macAddress'], self.MAC_ADDRESS)

    def test_put_updates_location(self):
        location = Location.create(tenant_key=self.tenant_key,
                                   customer_location_name='Store 1234',
                                   customer_location_code='store_1234')
        location_key = location.put()
        request_body = {'locationKey': location_key.urlsafe()}
        self.app.put('/api/v1/devices/{0}'.format(self.managed_device_key.urlsafe()),
                     json.dumps(request_body),
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
        with self.assertRaises(AppError) as context:
            self.app.put('/api/v1/devices/{0}'.format(new_device_key.urlsafe()),
                         json.dumps(request_body),
                         headers=self.api_token_authorization_header)
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
        response = self.app.put('/api/v1/devices/{0}'.format(self.managed_device_key.urlsafe()),
                                json.dumps(request_body),
                                headers=self.api_token_authorization_header)
        self.assertEqual('204 No Content', response.status)
        self.assertEqual(device.customer_display_code, customer_display_code)
        self.assertEqual(device.customer_display_name, new_display_name)

    def test_put_does_not_update_invalid_heartbeat_interval(self):
        interval = 0
        request_body = {
            'heartbeatInterval': interval
        }
        self.app.put('/api/v1/devices/{0}'.format(self.managed_device_key.urlsafe()),
                     json.dumps(request_body),
                     headers=self.api_token_authorization_header)
        updated_display = self.managed_device_key.get()
        self.assertEqual(config.PLAYER_HEARTBEAT_INTERVAL_MINUTES, updated_display.heartbeat_interval_minutes)

    def test_put_updates_valid_check_content_interval(self):
        interval = 3
        request_body = {
            'checkContentInterval': interval
        }
        self.app.put('/api/v1/devices/{0}'.format(self.managed_device_key.urlsafe()),
                     json.dumps(request_body),
                     headers=self.api_token_authorization_header)
        updated_display = self.managed_device_key.get()
        self.assertNotEqual(config.CHECK_FOR_CONTENT_INTERVAL_MINUTES,
                            updated_display.check_for_content_interval_minutes)

    def test_put_updates_check_content_interval_zero(self):
        interval = 0
        request_body = {
            'checkContentInterval': interval
        }
        self.app.put('/api/v1/devices/{0}'.format(self.managed_device_key.urlsafe()),
                     json.dumps(request_body),
                     headers=self.api_token_authorization_header)
        updated_display = self.managed_device_key.get()
        self.assertNotEqual(config.CHECK_FOR_CONTENT_INTERVAL_MINUTES,
                            updated_display.check_for_content_interval_minutes)

    def test_put_does_not_update_invalid_check_content_interval(self):
        interval = -1
        request_body = {
            'checkContentInterval': interval
        }
        self.app.put('/api/v1/devices/{0}'.format(self.managed_device_key.urlsafe()),
                     json.dumps(request_body),
                     headers=self.api_token_authorization_header)
        updated_display = self.managed_device_key.get()
        self.assertEqual(config.CHECK_FOR_CONTENT_INTERVAL_MINUTES, updated_display.check_for_content_interval_minutes)

    def test_put_updates_timezone_from_default_to_explicit(self):
        default_timezone = config.DEFAULT_TIMEZONE
        explicit_timezone = 'America/Denver'
        self.assertEqual(self.managed_device.timezone_offset, TimezoneUtil.get_timezone_offset(default_timezone))
        request_body = {'timezone': explicit_timezone}
        self.app.put('/api/v1/devices/{0}'.format(self.managed_device_key.urlsafe()),
                     json.dumps(request_body),
                     headers=self.api_token_authorization_header)
        updated_device = self.managed_device_key.get()
        expected_offset = TimezoneUtil.get_timezone_offset(explicit_timezone)
        self.assertEqual(updated_device.timezone, explicit_timezone)
        self.assertEqual(updated_device.timezone_offset, expected_offset)

    ##################################################################################################################
    # delete
    ##################################################################################################################

    def test_delete_no_authorization_header_returns_forbidden(self):
        uri = build_uri('device', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        response = self.delete(uri, headers=self.empty_header)
        self.assertForbidden(response)

    def test_delete_http_status_no_content(self):
        request_body = {}
        when(device_message_processor).change_intent(any_matcher(), config.PLAYER_RESET_COMMAND).thenReturn(None)
        response = self.app.delete('/api/v1/devices/{0}'.format(self.managed_device_key.urlsafe()),
                                   json.dumps(request_body),
                                   headers=self.api_token_authorization_header)
        self.assertEqual('204 No Content', response.status)

    def test_delete_archives_device(self):
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id='12312314',
            mac_address='00012341230')
        device.put()
        request_body = {}
        self.assertFalse(device.archived)
        when(device_message_processor).change_intent(any_matcher(), config.PLAYER_RESET_COMMAND).thenReturn(None)
        self.app.delete('/api/v1/devices/{0}'.format(device.key.urlsafe()),
                        json.dumps(request_body),
                        headers=self.api_token_authorization_header)
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
        request_body = {}
        when(device_message_processor).change_intent(any_matcher(), config.PLAYER_RESET_COMMAND).thenReturn(None)
        with self.assertRaises(AppError) as context:
            self.app.delete('/api/v1/devices/{0}'.format(device_key.urlsafe()),
                            json.dumps(request_body),
                            headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 404 Device with key: {0} archived.'.format(device_key.urlsafe())
                        in context.exception.message)

    def test_archived_device_is_prevented_from_registering_again__with_same_gcm_registration_id(self):
        gcm_registration_id = 'APA91bH3BQC-a4VjIsHmXd7ZsP_CXCZcyJQdP0lHS_4qaNYcg'
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=gcm_registration_id,
            mac_address=self.MAC_ADDRESS)
        device.put()
        request_body = {}
        self.assertFalse(device.archived)
        when(device_message_processor).change_intent(any_matcher(), config.PLAYER_RESET_COMMAND).thenReturn(None)
        self.app.delete('/api/v1/devices/{0}'.format(device.key.urlsafe()),
                        json.dumps(request_body),
                        headers=self.api_token_authorization_header)
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
    # heartbeat
    ##################################################################################################################

    def test_put_heartbeat_no_authorization_header_returns_forbidden_not_gcm(self):
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM}
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        response = self.put(uri, params=request_body, headers=self.empty_header)
        self.assertForbidden(response)

    def test_put_heartbeat_http_status_no_content(self):
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM}
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        response = self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        self.assertEqual('204 No Content', response.status)

    def test_put_heartbeat_updates_storage_utilization(self):
        self.__initialize_heartbeat_info()
        request_body = {'storage': self.STORAGE_UTILIZATION - 1,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        }
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        updated_heartbeat = self.managed_device_key.get()
        self.assertNotEqual(updated_heartbeat.storage_utilization, self.STORAGE_UTILIZATION)

    def test_put_heartbeat_updates_memory_utilization(self):
        self.__initialize_heartbeat_info()
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION - 1,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        }
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        updated_heartbeat = self.managed_device_key.get()
        self.assertNotEqual(updated_heartbeat.memory_utilization, self.MEMORY_UTILIZATION)

    def test_put_heartbeat_updates_program(self):
        self.__initialize_heartbeat_info()
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': 'Chronicles of Narnia',
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        }
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        updated_heartbeat = self.managed_device_key.get()
        self.assertNotEqual(updated_heartbeat.program, self.PROGRAM)
        self.assertEqual(updated_heartbeat.program, 'Chronicles of Narnia')

    def test_put_heartbeat_updates_program_id(self):
        self.__initialize_heartbeat_info()
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': 'new program id',
                        'lastError': self.LAST_ERROR,
                        }
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        updated_heartbeat = self.managed_device_key.get()
        self.assertNotEqual(updated_heartbeat.program_id, self.PROGRAM_ID)
        self.assertEqual(updated_heartbeat.program_id, 'new program id')

    def test_put_heartbeat_updates_playlist(self):
        self.__initialize_heartbeat_info()
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'playlist': 'new playlist',
                        'playlistId': self.PLAYLIST_ID,
                        'lastError': self.LAST_ERROR,
                        }
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        updated_heartbeat = self.managed_device_key.get()
        self.assertNotEqual(updated_heartbeat.playlist, self.PLAYLIST)
        self.assertEqual(updated_heartbeat.playlist, 'new playlist')

    def test_put_heartbeat_updates_playlist_id(self):
        self.__initialize_heartbeat_info()
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'playListId': self.PLAYLIST_ID,
                        'playlist': self.PLAYLIST,
                        'playlistId': 'new playlist id',
                        'lastError': self.LAST_ERROR,
                        }
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        updated_heartbeat = self.managed_device_key.get()
        self.assertNotEqual(updated_heartbeat.playlist_id, self.PLAYLIST_ID)
        self.assertEqual(updated_heartbeat.playlist_id, 'new playlist id')

    def test_put_heartbeat_updates_last_error(self):
        self.__initialize_heartbeat_info()
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': 'Houston, we have a problem'
                        }
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        updated_heartbeat = self.managed_device_key.get()
        self.assertNotEqual(updated_heartbeat.last_error, self.LAST_ERROR)

    def test_put_heartbeat_cannot_update_up_status(self):
        self.__initialize_heartbeat_info()
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        }
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        updated_heartbeat = self.managed_device_key.get()
        self.assertEqual(updated_heartbeat.up, updated_heartbeat.up)

    def test_put_heartbeat_updates_heartbeat_timestamp(self):
        self.__initialize_heartbeat_info()
        original_heartbeat_timestamp = self.managed_device.heartbeat_updated
        self.assertIsNotNone(original_heartbeat_timestamp)
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        }
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        device = self.managed_device_key.get()
        self.assertGreater(device.heartbeat_updated, original_heartbeat_timestamp)

    def test_put_heartbeat_invokes_a_device_issue_log_up_toggle_if_device_was_previously_down(self):
        self.__initialize_heartbeat_info(up=False)
        issues = DeviceIssueLog.get_all_by_device_key(self.managed_device.key)
        self.assertLength(0, issues)
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        }
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        issues = DeviceIssueLog.get_all_by_device_key(self.managed_device.key)
        self.assertLength(2, issues)
        self.assertEqual(issues[0].category, config.DEVICE_ISSUE_FIRST_HEARTBEAT)
        self.assertTrue(issues[1].up)
        self.assertEqual(issues[1].category, config.DEVICE_ISSUE_PLAYER_UP)
        self.assertEqual(issues[1].storage_utilization, self.STORAGE_UTILIZATION)
        self.assertEqual(issues[1].memory_utilization, self.MEMORY_UTILIZATION)
        self.assertEqual(issues[1].program, self.PROGRAM)
        self.assertEqual(issues[1].program_id, self.PROGRAM_ID)
        self.assertEqual(issues[1].last_error, self.LAST_ERROR)

    def test_put_heartbeat_invokes_a_device_issue_log_up_toggle_if_device_was_previously_down(self):
        self.__initialize_heartbeat_info(up=False)
        issues = DeviceIssueLog.get_all_by_device_key(self.managed_device.key)
        self.assertLength(0, issues)
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        }
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        issues = DeviceIssueLog.get_all_by_device_key(self.managed_device.key)
        self.assertLength(2, issues)
        self.assertEqual(issues[0].category, config.DEVICE_ISSUE_FIRST_HEARTBEAT)
        self.assertTrue(issues[1].up)
        self.assertEqual(issues[1].category, config.DEVICE_ISSUE_PLAYER_UP)
        self.assertEqual(issues[1].storage_utilization, self.STORAGE_UTILIZATION)
        self.assertEqual(issues[1].memory_utilization, self.MEMORY_UTILIZATION)
        self.assertEqual(issues[1].program, self.PROGRAM)
        self.assertEqual(issues[1].program_id, self.PROGRAM_ID)
        self.assertEqual(issues[1].last_error, self.LAST_ERROR)

    def test_put_heartbeat_can_resolve_previous_down_issues(self):
        self.managed_device.up = False
        self.managed_device.put()
        issue = DeviceIssueLog.create(device_key=self.managed_device_key,
                                      category=config.DEVICE_ISSUE_PLAYER_DOWN,
                                      up=False,
                                      storage_utilization=self.STORAGE_UTILIZATION,
                                      memory_utilization=self.MEMORY_UTILIZATION,
                                      program=self.PROGRAM,
                                      resolved=False)
        issue.put()
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        }
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        issues = DeviceIssueLog.get_all_by_device_key(self.managed_device_key)
        self.assertLength(2, issues)
        self.assertEqual(issues[0].category, config.DEVICE_ISSUE_PLAYER_DOWN)
        self.assertEqual(issues[1].category, config.DEVICE_ISSUE_PLAYER_UP)
        self.assertTrue(issues[0].resolved)
        self.assertTrue(issues[1].resolved)
        self.assertIsNotNone(issues[0].resolved_datetime)
        self.assertIsNotNone(issues[1].resolved_datetime)

    def test_put_heartbeat_can_resolve_previous_memory_issues(self):
        issue = DeviceIssueLog.create(device_key=self.managed_device_key,
                                      category=config.DEVICE_ISSUE_MEMORY_HIGH,
                                      up=True,
                                      storage_utilization=self.STORAGE_UTILIZATION,
                                      memory_utilization=config.MEMORY_UTILIZATION_THRESHOLD + 1,
                                      program=self.PROGRAM,
                                      resolved=False)
        issue.put()
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        }
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        issues = DeviceIssueLog.get_all_by_device_key(self.managed_device_key)
        self.assertLength(2, issues)
        self.assertEqual(issues[0].category, config.DEVICE_ISSUE_MEMORY_HIGH)
        self.assertEqual(issues[1].category, config.DEVICE_ISSUE_MEMORY_NORMAL)
        self.assertTrue(issues[0].resolved)
        self.assertTrue(issues[1].resolved)
        self.assertIsNotNone(issues[0].resolved_datetime)
        self.assertIsNotNone(issues[1].resolved_datetime)

    def test_put_heartbeat_can_resolve_previous_storage_issues(self):
        issue = DeviceIssueLog.create(device_key=self.managed_device_key,
                                      category=config.DEVICE_ISSUE_STORAGE_LOW,
                                      up=True,
                                      storage_utilization=config.STORAGE_UTILIZATION_THRESHOLD + 1,
                                      memory_utilization=self.MEMORY_UTILIZATION,
                                      program=self.PROGRAM,
                                      resolved=False)
        issue.put()
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        }
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        issues = DeviceIssueLog.get_all_by_device_key(self.managed_device_key)
        self.assertLength(2, issues)
        self.assertEqual(issues[0].category, config.DEVICE_ISSUE_STORAGE_LOW)
        self.assertEqual(issues[1].category, config.DEVICE_ISSUE_STORAGE_NORMAL)
        self.assertTrue(issues[0].resolved)
        self.assertTrue(issues[1].resolved)
        self.assertIsNotNone(issues[0].resolved_datetime)
        self.assertIsNotNone(issues[1].resolved_datetime)

    def test_put_heartbeat_populates_device_connection_type_for_ethernet_mac_address(self):
        self.managed_device.ethernet_mac_address = self.ETHERNET_MAC_ADDRESS
        self.managed_device.put()
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        'macAddress': self.ETHERNET_MAC_ADDRESS
                        }
        self.assertIsNone(self.managed_device.connection_type)
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        self.assertIsNotNone(self.managed_device.connection_type)
        self.assertEqual(self.managed_device.connection_type, config.ETHERNET_CONNECTION)

    def test_put_heartbeat_populates_device_connection_type_for_wifi_mac_address(self):
        self.managed_device.mac_address = self.MAC_ADDRESS
        self.managed_device.put()
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        'macAddress': self.MAC_ADDRESS
                        }
        self.assertIsNone(self.managed_device.connection_type)
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        self.assertIsNotNone(self.managed_device.connection_type)
        self.assertEqual(self.managed_device.connection_type, config.WIFI_CONNECTION)

    def test_put_heartbeat_does_not_populate_device_connection_type_for_unrecognized_mac_address(self):
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        'macAddress': '22234234234'
                        }
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        self.assertIsNone(self.managed_device.connection_type)

    def test_put_heartbeat_records_first_heartbeat_for_new_device(self):
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id='1231231',
            mac_address='2313412341230')
        device_key = device.put()
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        'macAddress': '2313412341230'}
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        log_entry = DeviceIssueLog.query(DeviceIssueLog.device_key == device_key,
                                         ndb.AND(DeviceIssueLog.category == config.DEVICE_ISSUE_FIRST_HEARTBEAT),
                                         ndb.AND(DeviceIssueLog.storage_utilization == self.STORAGE_UTILIZATION),
                                         ndb.AND(DeviceIssueLog.memory_utilization == self.MEMORY_UTILIZATION),
                                         ndb.AND(DeviceIssueLog.up == True),
                                         ndb.AND(DeviceIssueLog.resolved == True)
                                         ).get()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.category, config.DEVICE_ISSUE_FIRST_HEARTBEAT)

    def test_put_heartbeat_records_os_change(self):
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id='1231231',
            mac_address='2313412341239')
        device.os = 'Windows'
        device_key = device.put()
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        'macAddress': '2313412341239',
                        'os': 'Linux'}
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        log_entry = DeviceIssueLog.query(DeviceIssueLog.device_key == device_key,
                                         ndb.AND(DeviceIssueLog.category == config.DEVICE_ISSUE_OS_CHANGE)).get()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.category, config.DEVICE_ISSUE_OS_CHANGE)

    def test_put_heartbeat_records_os_version_change(self):
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id='1231231',
            mac_address='2313412341233')
        device.os_version = '8.3'
        device_key = device.put()
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        'macAddress': '2313412341233',
                        'osVersion': '10.0'}
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        log_entry = DeviceIssueLog.query(DeviceIssueLog.device_key == device_key,
                                         ndb.AND(
                                             DeviceIssueLog.category == config.DEVICE_ISSUE_OS_VERSION_CHANGE)).get()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.category, config.DEVICE_ISSUE_OS_VERSION_CHANGE)

    def test_put_heartbeat_records_to_timezone_change(self):
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id='1231231',
            mac_address='2313412341233')
        device.timezone = 'America/Denver'
        device_key = device.put()
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        'macAddress': '2313412341233',
                        'osVersion': '10.0',
                        'timezone': 'America/Boise'}
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        log_entry = DeviceIssueLog.query(DeviceIssueLog.device_key == device_key,
                                         ndb.AND(
                                             DeviceIssueLog.category ==
                                             config.DEVICE_ISSUE_TIMEZONE_CHANGE)).get()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.category, config.DEVICE_ISSUE_TIMEZONE_CHANGE)

    def test_put_heartbeat_records_to_timezone_offset_change(self):
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id='1231231',
            mac_address='2313412341233')
        device.timezone = config.DEFAULT_TIMEZONE
        device_key = device.put()
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        'macAddress': '2313412341233',
                        'osVersion': '10.0',
                        'timezone': config.DEFAULT_TIMEZONE,
                        'timezoneOffset': TimezoneUtil.get_timezone_offset(config.DEFAULT_TIMEZONE) + 3}
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': device_key.urlsafe()})
        when(device_message_processor).change_intent(
            any_matcher(), config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND).thenReturn(None)
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        log_entry = DeviceIssueLog.query(DeviceIssueLog.device_key == device_key,
                                         ndb.AND(
                                             DeviceIssueLog.category ==
                                             config.DEVICE_ISSUE_TIMEZONE_OFFSET_CHANGE)).get()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.category, config.DEVICE_ISSUE_TIMEZONE_OFFSET_CHANGE)

        request_parameters = {}
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})
        self.unmanaged_device.archived = True
        self.unmanaged_device.put()
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters,
                         headers=self.unmanaged_api_token_authorization_header)
        self.assertTrue('Device with key: {0} archived.'.format(self.unmanaged_device_key.urlsafe())
                        in context.exception.message)

    def test_put_heartbeat_returns_not_found_for_archived_device(self):
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id='3444-55550',
            mac_address='9931231321444')
        device.archived = True
        device_key = device.put()
        request_body = {}
        uri = build_uri('devices-heartbeat', params_dict={'device_urlsafe_key': device_key.urlsafe()})
        response = self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        self.assertEqual('404 Device with key: {0} archived.'.format(device_key.urlsafe()), response.status)

    ##################################################################################################################
    # device issues
    ##################################################################################################################

    def test_get_latest_issues_without_token_returns_forbidden(self):
        request_body = {}
        uri = build_uri('device-issues',
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
        uri = build_uri('device-issues', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe(),
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
        uri = build_uri('device-issues',
                        params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe(), 'prev_cursor_str': 'null',
                                     'next_cursor_str': 'null',
                                     'start': start_epoch, 'end': end_epoch})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)

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
        uri = build_uri('device-issues',
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
        uri = build_uri('device-issues',
                        params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe(), 'prev_cursor_str': 'null',
                                     'next_cursor_str': 'null',
                                     'start': start_epoch, 'end': end_epoch})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertLength(0, response_json["issues"])

    def __initialize_heartbeat_info(self, up=True):
        self.managed_device.storage_utilization = self.STORAGE_UTILIZATION
        self.managed_device.memory_utilization = self.MEMORY_UTILIZATION
        self.managed_device.program = self.PROGRAM
        self.managed_device.program_id = self.PROGRAM_ID
        self.managed_device.last_error = self.LAST_ERROR
        self.managed_device.playlist = self.PLAYLIST
        self.managed_device.playlist_id = self.PLAYLIST_ID
        self.managed_device.up = up
        self.managed_device.put()

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

    def __build_list_devices_with_serials(self, tenant_key=None, managed_number_to_build=5,
                                          unmanaged_number_to_build=5):
        results = []
        if tenant_key is None:
            tenant_key = self.__create_tenant()
        for i in range(managed_number_to_build):
            mac_address = 'm-mac{0}'.format(i)
            gcm_registration_id = 'm-gcm{0}'.format(i)
            device_id = 'd{0}'.format(i)
            serial_number = 'm-serial{0}'.format(i)
            device = ChromeOsDevice.create_managed(tenant_key=tenant_key,
                                                   mac_address=mac_address,
                                                   gcm_registration_id=gcm_registration_id,
                                                   device_id=device_id,
                                                   serial_number=serial_number)
            device.put()
            results.append(device)

        for i in range(unmanaged_number_to_build):
            mac_address = 'u-mac{0}'.format(i)
            gcm_registration_id = 'u-gcm{0}'.format(i)
            serial_number = 'u-serial{0}'.format(i)
            device = ChromeOsDevice.create_unmanaged(gcm_registration_id=gcm_registration_id,
                                                     mac_address=mac_address,
                                                     serial_number=serial_number)
            device.put()
            results.append(device)
        return results

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

    def __setup_distributor_with_two_tenants_with_n_devices(self, distributor_key, tenant_1_device_count,
                                                            tenant_2_device_count):
        domain_1 = Domain.create(name='dev.acme.com',
                                 distributor_key=distributor_key,
                                 impersonation_admin_email_address='fred@acme.com',
                                 active=True)
        domain_key_1 = domain_1.put()
        domain_2 = Domain.create(name='test.acme.com',
                                 distributor_key=distributor_key,
                                 impersonation_admin_email_address='fred@acme.com',
                                 active=True)
        domain_key_2 = domain_2.put()
        tenant_1 = Tenant.create(tenant_code='foobar_inc',
                                 name='Foobar, Inc',
                                 admin_email='bill@foobar.com',
                                 content_server_url=self.CONTENT_SERVER_URL,
                                 content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                 domain_key=domain_key_1,
                                 active=True)
        tenant_key_1 = tenant_1.put()
        self.__build_list_devices(tenant_key=tenant_key_1, managed_number_to_build=tenant_1_device_count,
                                  unmanaged_number_to_build=0)
        tenant_2 = Tenant.create(tenant_code='goober_inc',
                                 name='Goober, Inc',
                                 admin_email='bill@goober.com',
                                 content_server_url=self.CONTENT_SERVER_URL,
                                 content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                 domain_key=domain_key_2,
                                 active=True)
        tenant_key_2 = tenant_2.put()
        self.__build_list_devices(tenant_key=tenant_key_2, managed_number_to_build=tenant_2_device_count,
                                  unmanaged_number_to_build=0)

    def __setup_distributor_with_two_tenants_with_n_devices_with_serials(self, distributor_key, tenant_1_device_count,
                                                                         tenant_2_device_count):
        domain_1 = Domain.create(name='dev.acme.com',
                                 distributor_key=distributor_key,
                                 impersonation_admin_email_address='fred@acme.com',
                                 active=True)
        domain_key_1 = domain_1.put()
        domain_2 = Domain.create(name='test.acme.com',
                                 distributor_key=distributor_key,
                                 impersonation_admin_email_address='fred@acme.com',
                                 active=True)
        domain_key_2 = domain_2.put()
        tenant_1 = Tenant.create(tenant_code='foobar_inc',
                                 name='Foobar, Inc',
                                 admin_email='bill@foobar.com',
                                 content_server_url=self.CONTENT_SERVER_URL,
                                 content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                 domain_key=domain_key_1,
                                 active=True)
        tenant_key_1 = tenant_1.put()

        self.__build_list_devices_with_serials(tenant_key=tenant_key_1, managed_number_to_build=tenant_1_device_count,
                                               unmanaged_number_to_build=0)
        tenant_2 = Tenant.create(tenant_code='goober_inc',
                                 name='Goober, Inc',
                                 admin_email='bill@goober.com',
                                 content_server_url=self.CONTENT_SERVER_URL,
                                 content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                 domain_key=domain_key_2,
                                 active=True)
        tenant_key_2 = tenant_2.put()
        self.__build_list_devices_with_serials(tenant_key=tenant_key_2, managed_number_to_build=tenant_2_device_count,
                                               unmanaged_number_to_build=0)
