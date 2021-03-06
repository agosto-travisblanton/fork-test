import httplib
import json

from google.appengine.ext import ndb

from env_setup import setup_test_paths
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
        self.uri = build_uri('api-device-registration',
                             params_dict={'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})

        self.uri_unmanaged = build_uri('api-device-registration',
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
    # GET /api/v1/devices/<device_urlsafe_key>
    ##################################################################################################################

    def test_get_managed_device_by_key_no_authorization_header_returns_forbidden(self):
        uri = build_uri('api-device-get', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        response = self.get(uri, headers=self.empty_header)
        self.assertForbidden(response)

    def test_get_managed_device_by_key_http_status_ok(self):
        request_parameters = {}
        uri = build_uri('api-device-get', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertOK(response)

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
        uri = build_uri('api-device-by-parameter')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertOK(response)

    def test_get_device_by_pairing_code_returns_not_found_for_non_existent_code(self):
        request_parameters = {'pairingCode': self.PAIRING_CODE}
        uri = build_uri('api-device-by-parameter')
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 404 Unable to find device by pairing code: {0}'.format(
            self.PAIRING_CODE) in context.exception.message)

    def test_get_device_by_pairing_code_returns_single_resource(self):
        self.unmanaged_device.pairing_code = self.PAIRING_CODE
        self.unmanaged_device.put()
        request_parameters = {'pairingCode': self.PAIRING_CODE}
        uri = build_uri('api-device-by-parameter')
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
        uri = build_uri('api-device-by-parameter')
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
        uri = build_uri('api-device-by-parameter')
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
        uri = build_uri('api-device-by-parameter')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertOK(response)

    def test_get_device_by_gcm_registration_id_and_mac_returns_http_status_bad_request_with_missing_mac(self):
        request_parameters = {'gcmRegistrationId': self.GCM_REGISTRATION_ID}
        uri = build_uri('api-device-by-parameter')
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 400 Bad Request' in context.exception.message)

    def test_get_device_by_gcm_registration_id_and_mac_returns_http_status_bad_request_with_missing_gcm(self):
        request_parameters = {'macAddress': self.MAC_ADDRESS}
        uri = build_uri('api-device-by-parameter')
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 400 Bad Request' in context.exception.message)

    def test_get_device_by_returns_http_status_bad_request_with_missing_parameters(self):
        request_parameters = {}
        uri = build_uri('api-device-by-parameter')
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 400 Bad Request' in context.exception.message)

    def test_get_device_by_gcm_registration_id_returns_http_status_ok_with_just_valid_mac_and_invalid_gcm(self):
        device = ChromeOsDevice.create_unmanaged(gcm_registration_id=self.GCM_REGISTRATION_ID,
                                                 mac_address=self.MAC_ADDRESS)
        device.put()
        request_parameters = {'gcmRegistrationId': 'foobar', 'macAddress': self.MAC_ADDRESS}
        uri = build_uri('api-device-by-parameter')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertOK(response)

    def test_get_list_by_gcm_registration_id_returns_zeroeth_resource(self):
        gcm_registration_id = '123123123123'
        device = ChromeOsDevice.create_unmanaged(gcm_registration_id=gcm_registration_id,
                                                 mac_address=self.MAC_ADDRESS)
        device.put()
        request_parameters = {'gcmRegistrationId': gcm_registration_id, 'macAddress': self.MAC_ADDRESS}
        uri = build_uri('api-device-by-parameter')
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
        uri = build_uri('api-device-by-parameter')
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
        uri = build_uri('api-device-by-parameter')
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
        uri = build_uri('api-device-by-parameter')
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
        uri = build_uri('api-device-by-parameter')
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
        uri = build_uri('api-device-by-parameter')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        device = unmanaged_device_key.get()
        self.assertIsNotNone(device)
        self.assertFalse(device.archived)
        response_json = json.loads(response.body)
        self.assertEqual(response_json['macAddress'], mac_address)

    ##################################################################################################################
    # PUT updates for GCM and Mac
    ##################################################################################################################
    def test_put_no_authorization_header_returns_forbidden(self):
        request_body = {'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'macAddress': self.MAC_ADDRESS}
        uri = build_uri('api-device-put', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        response = self.put(uri, params=request_body, headers=self.empty_header)
        self.assertForbidden(response)

    def test_put_http_status_no_content(self):
        request_body = {'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'macAddress': self.MAC_ADDRESS}
        uri = build_uri('api-device-put', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        response = self.put(uri, params=json.dumps(request_body),
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
        uri = build_uri('api-device-put', params_dict={'device_urlsafe_key': archived_device_key.urlsafe()})
        with self.assertRaises(AppError) as context:
            self.app.put(uri, params=json.dumps(request_body),
                         headers=self.api_token_authorization_header)
        self.assertTrue('Bad response: 404 Device with key: {0} archived.'.format(archived_device_key.urlsafe())
                        in context.exception.message)

    def test_put_updates_expected_properties(self):
        mac_address = 'new mac'
        gcm_registration_id = 'new gcm'
        request_body = {'gcmRegistrationId': gcm_registration_id, 'macAddress': mac_address}
        uri = build_uri('api-device-put', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})
        self.app.put(uri, json.dumps(request_body), headers=self.api_token_authorization_header)
        updated_display = self.managed_device_key.get()
        self.assertEqual(mac_address, updated_display.mac_address)
        self.assertEqual(gcm_registration_id, updated_display.gcm_registration_id)

