import httplib
import json

from google.appengine.ext import ndb

import device_message_processor
from env_setup import setup_test_paths
from model_entities.chrome_os_device_model_and_overlays import DeviceIssueLog
from utils.timezone_util import TimezoneUtil

setup_test_paths()

from agar.test import BaseTest, WebTest
from app_config import config
from mockito import when, any as any_matcher
from models import ChromeOsDevice, Tenant, Distributor, Domain
from routes import application
from utils.email_notify import EmailNotify
from utils.web_util import build_uri
from webtest import AppError


class TestDeviceHandler(BaseTest, WebTest):
    APPLICATION = application
    ADMIN_EMAIL = 'foo@bar.com'
    ANOTHER_TENANT_NAME = 'Another, Inc,'
    ANOTHER_TENANT_CODE = 'another_inc'
    ANOTHER_ADMIN_EMAIL = 'foo@another.com'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
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
    PAIRING_CODE = '0e8f-fc4e-d632-09dc'
    STORAGE_UTILIZATION = 26
    MEMORY_UTILIZATION = 63
    PROGRAM = 'some program'
    PROGRAM_ID = 'ID-512341234'
    PLAYLIST = 'some playlist'
    PLAYLIST_ID = 'Playlist Id'
    LAST_ERROR = 'some error'

    def setUp(self):
        super(TestDeviceHandler, self).setUp()
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
        self.uri = build_uri('device-registration',
                             params_dict={'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})

        self.uri_unmanaged = build_uri('device-registration',
                                       params_dict={'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})

        self.empty_header = {}

    ##################################################################################################################
    # POST /api/v1/devices (managed)
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
        response = self.app.post(self.uri, json.dumps(request_body), headers=self.api_token_authorization_header)
        self.assertEqual(httplib.CREATED, response.status_int)

    def test_post_managed_device_returns_resource_url_in_location_header(self):
        when(EmailNotify).device_enrolled(tenant_code=any_matcher(),
                                          tenant_name=any_matcher(),
                                          device_mac_address=any_matcher(),
                                          timestamp=any_matcher()).thenReturn(None)
        tenant = self.tenant_key.get()
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': 'foobar',
                        'tenantCode': tenant.tenant_code}
        response = self.app.post(self.uri, json.dumps(request_body), headers=self.api_token_authorization_header)
        location_uri_components = str(response.headers['Location']).split('/')
        self.assertEqual(location_uri_components[5], "devices")
        device = ndb.Key(urlsafe=location_uri_components[6]).get()
        self.assertIsNotNone(device)

    def test_device_resource_handler_post_no_authorization_header_returns_forbidden(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.TENANT_CODE}
        response = self.post(self.uri, params=request_body, headers=self.empty_header)
        self.assertForbidden(response)

    def test_device_resource_handler_post_no_returns_conflict_if_gcm_id_is_already_assigned_to_device(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.TENANT_CODE}
        with self.assertRaises(AppError) as context:
            self.app.post(self.uri, json.dumps(request_body),
                          headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 409 Conflict gcm registration id is already assigned to a managed device.'
                        in context.exception.message)

    def test_device_resource_handler_post_no_returns_bad_response_for_empty_gcm(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': None,
                        'tenantCode': self.TENANT_CODE}
        with self.assertRaises(AppError) as context:
            self.app.post(self.uri, json.dumps(request_body),
                          headers=self.api_token_authorization_header)
        self.assertTrue('required field gcmRegistrationId not found'
                        in context.exception.message)

    def test_device_resource_handler_post_no_returns_bad_response_for_empty_mac_address(self):
        request_body = {'macAddress': None,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.TENANT_CODE}
        with self.assertRaises(AppError) as context:
            self.app.post(self.uri, json.dumps(request_body),
                          headers=self.api_token_authorization_header)
        print context.exception.message
        self.assertTrue('required field macAddress not found'
                        in context.exception.message)

    def test_post_managed_device_when_cannot_resolve_tenant(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': 'foobar',
                        'tenantCode': 'unresolvable_tenant_code'}
        with self.assertRaises(AppError) as context:
            self.app.post(self.uri, json.dumps(request_body),
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
        response = self.app.post(self.uri, json.dumps(request_body),
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
        response = self.app.post(self.uri, json.dumps(request_body),
                                 headers=self.api_token_authorization_header)
        location_uri_components = str(response.headers['Location']).split('/')
        device = ndb.Key(urlsafe=location_uri_components[6]).get()
        self.assertEqual(device.timezone_offset, TimezoneUtil.get_timezone_offset(explicit_timezone))
        self.assertEqual(device.timezone, explicit_timezone)

    def test_post_managed_device_with_domain_and_tenant_in_payload_sets_tenant(self):
        tenant = self.tenant_key.get()
        mac_address = '12345678'
        request_body = {'macAddress': mac_address,
                        'gcmRegistrationId': 'foobar',
                        'domain': 'dev.agosto.com',
                        'tenantCode': tenant.tenant_code}
        response = self.app.post(self.uri, json.dumps(request_body),
                                 headers=self.api_token_authorization_header)
        results = ChromeOsDevice.query(ChromeOsDevice.mac_address == mac_address,
                                       ndb.AND(ChromeOsDevice.archived == False)).fetch()
        self.assertIsNotNone(results[0].tenant_key)
        self.assertEqual(httplib.CREATED, response.status_int)

    def test_post_managed_device_with_domain_only_does_not_set_tenant(self):
        mac_address = '012345678'
        request_body = {'macAddress': mac_address,
                        'gcmRegistrationId': 'foobar',
                        'domain': 'dev.agosto.com'}
        response = self.app.post(self.uri, json.dumps(request_body),
                                 headers=self.api_token_authorization_header)
        results = ChromeOsDevice.query(ChromeOsDevice.mac_address == mac_address,
                                       ndb.AND(ChromeOsDevice.archived == False)).fetch()
        self.assertIsNone(results[0].tenant_key)
        self.assertEqual(httplib.CREATED, response.status_int)

    def test_post_managed_device_without_tenant_code_or_domain_in_payload(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': 'foobar'}
        with self.assertRaises(AppError) as context:
            self.app.post(self.uri, json.dumps(request_body), headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 400 Did not detect a tenantCode or a domain in device registration payload.' in
                        context.exception.message)

    ##################################################################################################################
    # POST /api/v1/devices (un-managed)
    ##################################################################################################################
    def test_device_resource_handler_unmanaged_post_returns_created_status_code(self):
        new_mac_address = '1111111111'
        new_gcm_registration_id = '222222222'
        request_body = {'macAddress': new_mac_address,
                        'gcmRegistrationId': new_gcm_registration_id}
        response = self.app.post(self.uri_unmanaged, json.dumps(request_body),
                                 headers=self.unmanaged_registration_token_authorization_header)
        self.assertEqual(httplib.CREATED, response.status_int)

    def test_device_resource_handler_unmanaged_post_returns_cannot_register_when_gcm_already_assigned(self):
        request_body = {'macAddress': '123',
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID}
        with self.assertRaises(AppError) as context:
            self.app.post(self.uri_unmanaged, json.dumps(request_body),
                          headers=self.unmanaged_registration_token_authorization_header)
        self.assertTrue('Bad response: 409 Conflict gcm registration id is already assigned to an unmanaged device' in
                        context.exception.message)

    def test_device_resource_handler_unmanaged_post_returns_cannot_register_when_mac_already_assigned(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': '23413423'}
        with self.assertRaises(AppError) as context:
            self.app.post(self.uri_unmanaged, json.dumps(request_body),
                          headers=self.unmanaged_registration_token_authorization_header)
        self.assertTrue('Bad response: 409 Conflict mac address is already assigned to an unmanaged device' in
                        context.exception.message)

    def test_device_resource_handler_unmanaged_post_returns_bad_response_for_empty_gcm(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': None}
        with self.assertRaises(AppError) as context:
            self.app.post(self.uri_unmanaged, json.dumps(request_body),
                          headers=self.unmanaged_registration_token_authorization_header)
        self.assertTrue('required field gcmRegistrationId not found'
                        in context.exception.message)

    def test_device_resource_handler_unmanaged_post_returns_bad_response_for_empty_mac_address(self):
        request_body = {'macAddress': None,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID}
        with self.assertRaises(AppError) as context:
            self.app.post(self.uri_unmanaged, json.dumps(request_body),
                          headers=self.unmanaged_registration_token_authorization_header)
        self.assertTrue('required field macAddress not found'
                        in context.exception.message)

    def test_device_resource_handler_unmanaged_post_populates_location_header(self):
        new_mac_address = '1111111111'
        new_gcm_registration_id = '222222222'
        request_body = {'macAddress': new_mac_address,
                        'gcmRegistrationId': new_gcm_registration_id}
        response = self.app.post(self.uri_unmanaged, json.dumps(request_body),
                                 headers=self.unmanaged_registration_token_authorization_header)
        self.assertIsNotNone(response.headers['Location'])

    def test_device_resource_handler_unmanaged_post_populates_location_header_with_devices_route(self):
        new_mac_address = '1111111111'
        new_gcm_registration_id = '222222222'
        request_body = {'macAddress': new_mac_address,
                        'gcmRegistrationId': new_gcm_registration_id}
        response = self.app.post(self.uri_unmanaged, json.dumps(request_body),
                                 headers=self.unmanaged_registration_token_authorization_header)
        location_uri_components = str(response.headers['Location']).split('/')
        self.assertEqual(location_uri_components[5], "devices")

    def test_device_resource_handler_unmanaged_post_populates_location_header_with_resolvable_resource(self):
        new_mac_address = '1111111111'
        new_gcm_registration_id = '222222222'
        request_body = {'macAddress': new_mac_address,
                        'gcmRegistrationId': new_gcm_registration_id}
        response = self.app.post(self.uri_unmanaged, json.dumps(request_body),
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

    ##################################################################################################################
    # GET /api/v1/devices/<device_urlsafe_key>/pairing
    ##################################################################################################################

    def test_get_get_pairing_code_returns_status_ok(self):
        request_parameters = {}
        uri = build_uri('device-pairing-code',
                        params_dict={'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters,
                                headers=self.unmanaged_registration_token_authorization_header)
        self.assertOK(response)

    def test_get_get_pairing_code_returns_expected_property_count_in_json(self):
        request_parameters = {}
        uri = build_uri('device-pairing-code',
                        params_dict={'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters,
                                headers=self.unmanaged_registration_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertLength(3, response_json)

    def test_get_get_pairing_code_returns_pairing_code_in_json(self):
        request_parameters = {}
        uri = build_uri('device-pairing-code',
                        params_dict={'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters,
                                headers=self.unmanaged_registration_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertIsNotNone(response_json['pairingCode'])

    def test_get_get_pairing_code_returns_gcm_registration_id_in_json(self):
        request_parameters = {}
        uri = build_uri('device-pairing-code',
                        params_dict={'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters,
                                headers=self.unmanaged_registration_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertIsNotNone(response_json['gcmRegistrationId'])

    def test_get_get_pairing_code_returns_mac_address_in_json(self):
        request_parameters = {}
        uri = build_uri('device-pairing-code',
                        params_dict={'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters,
                                headers=self.unmanaged_registration_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertIsNotNone(response_json['macAddress'])

    def test_get_get_pairing_code_with_wrong_token(self):
        request_parameters = {}
        uri = build_uri('device-pairing-code',
                        params_dict={'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})
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
        uri = build_uri('device-pairing-code',
                        params_dict={'device_urlsafe_key': device_key.urlsafe()})
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters,
                         headers=self.unmanaged_registration_token_authorization_header)
        self.assertTrue('Bad response: 404 Device with key: {0} archived.'.format(device_key.urlsafe())
                        in context.exception.message)

    #################################################################################################################
    # GET /api/v1/devices get_device_by_parameter (pairing code lookup)
    #################################################################################################################

    def test_get_device_by_pairing_code_returns_http_status_ok(self):
        self.unmanaged_device.pairing_code = self.PAIRING_CODE
        self.unmanaged_device.put()
        request_parameters = {'pairingCode': self.PAIRING_CODE}
        uri = build_uri('device-by-parameter')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertOK(response)

    def test_get_device_by_pairing_code_returns_not_found_for_non_existent_code(self):
        request_parameters = {'pairingCode': self.PAIRING_CODE}
        uri = build_uri('device-by-parameter')
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 404 Unable to find device by pairing code: {0}'.format(
            self.PAIRING_CODE) in context.exception.message)

    def test_get_device_by_pairing_code_returns_single_resource(self):
        self.unmanaged_device.pairing_code = self.PAIRING_CODE
        self.unmanaged_device.put()
        request_parameters = {'pairingCode': self.PAIRING_CODE}
        uri = build_uri('device-by-parameter')
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
        uri = build_uri('device-by-parameter')
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
        uri = build_uri('device-by-parameter')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertEqual(response_json['pairingCode'], self.PAIRING_CODE)
        self.assertEqual(response_json['gcmRegistrationId'], 'g1111')
        self.assertEqual(response_json['macAddress'], 'm1111')

    #################################################################################################################
    # GET /api/v1/devices get_device_by_parameter (gcm_registration_id and mac_address lookup)
    #################################################################################################################

    def test_get_device_by_gcm_registration_id_and_mac_returns_http_status_ok_with_valid_parameters(self):
        device = ChromeOsDevice.create_unmanaged(gcm_registration_id=self.GCM_REGISTRATION_ID,
                                                 mac_address=self.MAC_ADDRESS)
        device.put()
        request_parameters = {'gcmRegistrationId': self.GCM_REGISTRATION_ID, 'macAddress': self.MAC_ADDRESS}
        uri = build_uri('device-by-parameter')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertOK(response)

    def test_get_device_by_gcm_registration_id_and_mac_returns_http_status_bad_request_with_missing_mac(self):
        request_parameters = {'gcmRegistrationId': self.GCM_REGISTRATION_ID}
        uri = build_uri('device-by-parameter')
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 400 Bad Request' in context.exception.message)

    def test_get_device_by_gcm_registration_id_and_mac_returns_http_status_bad_request_with_missing_gcm(self):
        request_parameters = {'macAddress': self.MAC_ADDRESS}
        uri = build_uri('device-by-parameter')
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 400 Bad Request' in context.exception.message)

    def test_get_device_by_returns_http_status_bad_request_with_missing_parameters(self):
        request_parameters = {}
        uri = build_uri('device-by-parameter')
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 400 Bad Request' in context.exception.message)

    def test_get_device_by_gcm_registration_id_returns_http_status_ok_with_just_valid_mac_and_invalid_gcm(self):
        device = ChromeOsDevice.create_unmanaged(gcm_registration_id=self.GCM_REGISTRATION_ID,
                                                 mac_address=self.MAC_ADDRESS)
        device.put()
        request_parameters = {'gcmRegistrationId': 'foobar', 'macAddress': self.MAC_ADDRESS}
        uri = build_uri('device-by-parameter')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertOK(response)

    def test_get_list_by_gcm_registration_id_returns_zeroeth_resource(self):
        gcm_registration_id = '123123123123'
        device = ChromeOsDevice.create_unmanaged(gcm_registration_id=gcm_registration_id,
                                                 mac_address=self.MAC_ADDRESS)
        device.put()
        request_parameters = {'gcmRegistrationId': gcm_registration_id, 'macAddress': self.MAC_ADDRESS}
        uri = build_uri('device-by-parameter')
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
        uri = build_uri('device-by-parameter')
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
        uri = build_uri('device-by-parameter')
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
        request_parameters = {'macAddress': mac_address, 'gcmRegistrationId': gcm_registration_id}
        uri = build_uri('device-by-parameter')
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
        request_parameters = {'macAddress': mac_address, 'gcmRegistrationId': gcm_registration_id_2}
        uri = build_uri('device-by-parameter')
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
        request_parameters = {'macAddress': mac_address, 'gcmRegistrationId': gcm_registration_id_2}
        uri = build_uri('device-by-parameter')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        device = unmanaged_device_key.get()
        self.assertIsNotNone(device)
        self.assertFalse(device.archived)
        response_json = json.loads(response.body)
        self.assertEqual(response_json['macAddress'], mac_address)

    ##################################################################################################################
    # PUT /api/v1/devices/<device_urlsafe_key>/heartbeat
    ##################################################################################################################

    def test_put_heartbeat_no_authorization_header_returns_forbidden_not_gcm(self):
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM}
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        response = self.put(uri, params=request_body, headers=self.empty_header)
        self.assertForbidden(response)

    def test_put_heartbeat_http_status_no_content(self):
        request_body = {'storage': self.STORAGE_UTILIZATION,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM}
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        response = self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        self.assertEqual(httplib.NO_CONTENT, response.status_int)

    def test_put_heartbeat_updates_storage_utilization(self):
        self.__initialize_heartbeat_info()
        request_body = {'storage': self.STORAGE_UTILIZATION - 1,
                        'memory': self.MEMORY_UTILIZATION,
                        'program': self.PROGRAM,
                        'programId': self.PROGRAM_ID,
                        'lastError': self.LAST_ERROR,
                        }
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': device_key.urlsafe()})
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
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': device_key.urlsafe()})
        when(device_message_processor).change_intent(
            any_matcher(), config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND).thenReturn(None)
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        log_entry = DeviceIssueLog.query(DeviceIssueLog.device_key == device_key,
                                         ndb.AND(
                                             DeviceIssueLog.category ==
                                             config.DEVICE_ISSUE_TIMEZONE_OFFSET_CHANGE)).get()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.category, config.DEVICE_ISSUE_TIMEZONE_OFFSET_CHANGE)

    def test_put_heartbeat_returns_not_found_for_archived_device(self):
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id='3444-55550',
            mac_address='9931231321444')
        device.archived = True
        device_key = device.put()
        request_body = {}
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': device_key.urlsafe()})
        response = self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        self.assertEqual('404 Device with key: {0} archived.'.format(device_key.urlsafe()), response.status)

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

