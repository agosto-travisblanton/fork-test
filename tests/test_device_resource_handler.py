from google.appengine.ext import ndb
from content_manager_api import ContentManagerApi
from env_setup import setup_test_paths

setup_test_paths()

import json
from webtest import AppError
from google.appengine.ext.deferred import deferred
from mockito import when, any as any_matcher
from chrome_os_devices_api import (refresh_device, refresh_device_by_mac_address)

from agar.test import BaseTest, WebTest
from chrome_os_devices_api import ChromeOsDevicesApi
from mockito import when, any as any_matcher, verify
from routes import application
from models import ChromeOsDevice, Tenant
from app_config import config
from ae_test_data import build


class TestDeviceResourceHandler(BaseTest, WebTest):
    APPLICATION = application
    CUSTOMER_ID = 'my_customer'
    TENANT_NAME = 'Foobar, Inc,'
    TENANT_CODE = 'foobar_inc'
    ADMIN_EMAIL = 'foo@bar.com'
    ANOTHER_TENANT_NAME = 'Another, Inc,'
    ANOTHER_TENANT_CODE = 'another_inc'
    ANOTHER_ADMIN_EMAIL = 'foo@another.com'
    CONTENT_SERVER_URL = 'https://skykit-contentmanager-int.appspot.com/content'
    CONTENT_SERVER_API_KEY = 'API KEY'
    CHROME_DEVICE_DOMAIN = 'bar.com'
    DEVICE_ID = '132e235a-b346-4a37-a100-de49fa753a2a'
    GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
    MAC_ADDRESS = '54271e619346'

    def setUp(self):
        super(TestDeviceResourceHandler, self).setUp()
        self.tenant_key = self.__create_tenant(self.TENANT_CODE, self.TENANT_NAME, self.ADMIN_EMAIL)
        self.another_tenant_key = self.__create_tenant(self.ANOTHER_TENANT_CODE, self.ANOTHER_TENANT_NAME,
                                                       self.ANOTHER_ADMIN_EMAIL)
        self.device_key = self.__create_device(self.tenant_key)
        self.valid_authorization_header = {
            'Authorization': config.API_TOKEN
        }
        self.invalid_authorization_header = {}

    ##################################################################################################################
    ## get_list
    ##################################################################################################################

    def test_get_list_no_query_parameters_http_status_ok(self):
        self.__build_list_devices(tenant_key=self.tenant_key, number_to_build=1)
        request_parameters = {}
        uri = application.router.build(None, 'devices-retrieval', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_get_list_no_query_parameters_entity_body_json(self):
        self.__build_list_devices(tenant_key=self.tenant_key, number_to_build=20)
        request_parameters = {}
        uri = application.router.build(None, 'devices-retrieval', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json['objects']), 10)

    ##################################################################################################################
    ## get_devices_by_tenant
    ##################################################################################################################

    def test_get_devices_by_tenant_http_status_ok(self):
        self.__build_list_devices(tenant_key=self.tenant_key, number_to_build=20)
        request_parameters = {}
        uri = application.router.build(None, 'devices-by-tenant', None,
                                       {'tenant_urlsafe_key': self.tenant_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_get_devices_by_tenant_entity_body_json(self):
        self.__build_list_devices(tenant_key=self.tenant_key, number_to_build=20)
        request_parameters = {}
        uri = application.router.build(None, 'devices-by-tenant', None,
                                       {'tenant_urlsafe_key': self.tenant_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json['objects']), 10)

    ##################################################################################################################
    ## get
    ##################################################################################################################
    def test_get_device_by_key_http_status_ok(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'manage-device',
                                       None,
                                       {'device_urlsafe_key': self.device_key.urlsafe()})
        when(deferred).defer(any_matcher(refresh_device),
                             any_matcher(self.device_key.urlsafe())).thenReturn(None)
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_get_device_by_key_entity_body_json(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'manage-device',
                                       None,
                                       {'device_urlsafe_key': self.device_key.urlsafe()})
        when(deferred).defer(any_matcher(refresh_device),
                             any_matcher(self.device_key.urlsafe())).thenReturn(None)
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        response_json = json.loads(response.body)
        device = self.device_key.get()
        tenant = device.tenant_key.get()
        self.assertEqual(response_json['annotated_user'], device.annotated_user)
        self.assertEqual(response_json['annotated_location'], device.annotated_location)
        self.assertEqual(response_json['api_key'], device.api_key)
        self.assertEqual(response_json['boot_mode'], device.boot_mode)
        self.assertEqual(response_json['created'], device.created.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response_json['device_id'], device.device_id)
        self.assertEqual(response_json['ethernet_mac_address'], device.ethernet_mac_address)
        self.assertEqual(response_json['firmware_version'], device.firmware_version)
        self.assertEqual(response_json['gcm_registration_id'], device.gcm_registration_id)
        self.assertEqual(response_json['key'], device.key.urlsafe())
        self.assertEqual(response_json['kind'], device.kind)
        self.assertEqual(response_json['last_enrollment_time'], device.last_enrollment_time)
        self.assertEqual(response_json['last_sync'], device.last_sync)
        self.assertEqual(response_json['mac_address'], device.mac_address)
        self.assertEqual(response_json['model'], device.model)
        self.assertEqual(response_json['org_unit_path'], device.org_unit_path)
        self.assertEqual(response_json['os_version'], device.os_version)
        self.assertEqual(response_json['platform_version'], device.platform_version)
        self.assertEqual(response_json['serial_number'], device.serial_number)
        self.assertEqual(response_json['status'], device.status)
        self.assertEqual(response_json['updated'], device.updated.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response_json['tenant_key'], tenant.key.urlsafe())

    ##################################################################################################################
    ## post
    ##################################################################################################################

    def test_device_resource_handler_post_no_authorization_header_returns_forbidden(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.TENANT_CODE}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.invalid_authorization_header)
        self.assertTrue('403 Forbidden' in context.exception.message)

    def test_device_resource_handler_post_no_returns_bad_response_if_mac_address_already_assigned_to_device(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.TENANT_CODE}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertTrue('Bad response: 400 Cannot create because macAddress has already been assigned to this device.'
                        in context.exception.message)

    def test_device_resource_handler_post_no_returns_bad_response_for_empty_tenant_code(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': None}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertTrue('Bad response: 400 Invalid or inactive tenant for device.'
                        in context.exception.message)

    def test_device_resource_handler_post_no_returns_bad_response_for_empty_gcm(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': None,
                        'tenantCode': self.TENANT_CODE}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertTrue('Bad response: 400 The gcmRegistrationId parameter is invalid.'
                        in context.exception.message)

    def test_device_resource_handler_post_no_returns_bad_response_for_empty_mac_address(self):
        request_body = {'macAddress': None,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.TENANT_CODE}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertTrue('Bad response: 400 The macAddress parameter is invalid.'
                        in context.exception.message)
        
    def test_post_http_status_created(self):
        tenant = self.tenant_key.get()
        mac_address = '7889BE879f'
        request_body = {'macAddress': mac_address,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': tenant.tenant_code}
        when(deferred).defer(any_matcher(refresh_device_by_mac_address),
                             any_matcher(str),
                             any_matcher(mac_address)).thenReturn(None)
        response = self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertEqual('201 Created', response.status)

    def test_post_device_key_location_header(self):
        tenant = self.tenant_key.get()
        mac_address = '7889BE879f'
        request_body = {'macAddress': mac_address,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': tenant.tenant_code}
        when(deferred).defer(any_matcher(refresh_device_by_mac_address),
                             any_matcher(str),
                             any_matcher(mac_address)).thenReturn(None)
        response = self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        location_uri_components = str(response.headers['Location']).split('/')
        self.assertEqual(location_uri_components[5], "devices")
        self.assertEqual(48, len(location_uri_components[6]))
        device = ndb.Key(urlsafe=location_uri_components[6]).get()
        self.assertIsNotNone(device)

    ##################################################################################################################
    ## put
    ##################################################################################################################

    def test_device_resource_put_no_authorization_header_returns_forbidden(self):
        request_body = {'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.TENANT_CODE}
        when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.device_key.get())
        with self.assertRaises(Exception) as context:
            self.app.put('/api/v1/devices/{0}'.format(self.device_key.urlsafe()),
                         json.dumps(request_body), headers=self.invalid_authorization_header)
        self.assertTrue('403 Forbidden' in str(context.exception))

    ##################################################################################################################
    ## delete
    ##################################################################################################################

    def test_device_resource_delete_no_authorization_header_returns_forbidden(self):
        url = '/api/v1/devices/{0}'.format(self.device_key.urlsafe())
        with self.assertRaises(Exception) as context:
            self.app.delete(url, headers=self.invalid_authorization_header)
        self.assertTrue('403 Forbidden' in str(context.exception))

    # def test_device_resource_handler_get_by_key_returns_not_found_for_bogus_key(self):
    #     when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.chrome_os_device_json)
    #     request_parameters = {}
    #     uri = application.router.build(None, 'manage-device', None, {'device_urlsafe_key': 'bogus key'})
    #     with self.assertRaises(AppError) as context:
    #         self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
    #     self.assertTrue('404 Not Found' in context.exception.message)
    #
    # def test_device_resource_handler_get_by_key_returns_bad_request_for_missing_parent_tenant(self):
    #     when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.chrome_os_device_json)
    #     request_parameters = {}
    #     device = ChromeOsDevice(
    #         api_key='some key',
    #         device_id=self.TESTING_DEVICE_ID,
    #         gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
    #         mac_address=self.MAC_ADDRESS)
    #     key = device.put()
    #     uri = application.router.build(None, 'manage-device', None, {'device_urlsafe_key': key.urlsafe()})
    #     with self.assertRaises(AppError) as context:
    #         self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
    #     self.assertTrue('400 Bad Request' in context.exception.message)
    #
    # def test_device_resource_handler_get_by_key_returns_ok(self):
    #     when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.chrome_os_device_json)
    #     request_parameters = {}
    #     uri = application.router.build(None, 'manage-device', None, {'device_urlsafe_key':
    #                                                                      self.chrome_os_device_key.urlsafe()})
    #     response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
    #     self.assertOK(response)
    #
    # def test_device_resource_handler_no_authorization_header_returns_forbidden(self):
    #     when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.chrome_os_device_json)
    #     request_parameters = {}
    #     uri = application.router.build(None, 'manage-device', None, {'device_urlsafe_key':
    #                                                                      self.chrome_os_device_key.urlsafe()})
    #     with self.assertRaises(AppError) as context:
    #         self.app.get(uri, params=request_parameters, headers=self.bad_authorization_header)
    #     self.assertTrue('403 Forbidden' in context.exception.message)
    #
    # def test_device_resource_handler_get_by_id_returns_device_representation(self):
    #     device_key = self.create_chrome_os_device(self.tenant_key)
    #     when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.chrome_os_device_json)
    #     request_parameters = {}
    #     uri = application.router.build(None, 'manage-device', None, {'device_urlsafe_key': device_key.urlsafe()})
    #     response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
    #     response_json = json.loads(response.body)
    #     expected = device_key.get()
    #     self.assertEqual(response_json.get('deviceId'), expected.device_id)
    #     self.assertEqual(response_json.get('gcmRegistrationId'), expected.gcm_registration_id)
    #     self.assertEqual(response_json.get('created'), expected.created.strftime('%Y-%m-%d %H:%M:%S'))
    #     self.assertEqual(response_json.get('updated'), expected.updated.strftime('%Y-%m-%d %H:%M:%S'))
    #     self.assertEqual(response_json.get('apiKey'), expected.api_key)
    #     self.assertEqual(response_json.get('active'), True)
    #     self.assertEqual(response_json.get('key'), device_key.urlsafe())
    #
    # def test_device_resource_handler_get_all_devices_returns_ok(self):
    #     when(ChromeOsDevicesApi).list(any_matcher()).thenReturn(self.chrome_os_device_list_json)
    #     response = self.app.get('/api/v1/devices', params={}, headers=self.valid_authorization_header)
    #     self.assertOK(response)
    #
    # def test_device_resource_handler_get_all_devices_returns_not_found(self):
    #     when(ChromeOsDevicesApi).list(any_matcher()).thenReturn(None)
    #     with self.assertRaises(AppError) as context:
    #         self.app.get('/api/v1/devices', params={}, headers=self.valid_authorization_header)
    #     self.assertTrue('404 Not Found' in context.exception.message)
    #
    # def test_post_content_manager_api_collaboration(self):
    #     when(ChromeOsDevicesApi).list(any_matcher()).thenReturn(self.chrome_os_device_list_json)
    #     when(ContentManagerApi).create_device(any_matcher()).thenReturn(True)
    #     request_body = {'macAddress': self.chrome_os_device_json.get('macAddress'),
    #                     'gcmRegistrationId': '123',
    #                     'tenantCode': self.TENANT_CODE
    #                     }
    #     self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
    #     verify(ContentManagerApi, atleast=4).create_device(any_matcher(''))
    #
    # def test_device_resource_handler_post_returns_created_status(self):
    #     request_body = {'macAddress': self.chrome_os_device_json.get('macAddress'),
    #                     'gcmRegistrationId': '123',
    #                     'tenantCode': self.TENANT_CODE
    #                     }
    #     when(ChromeOsDevicesApi).list(any_matcher()).thenReturn(self.chrome_os_device_list_json)
    #     when(ContentManagerApi).create_device(any_matcher()).thenReturn(True)
    #     response = self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
    #     self.assertEqual('201 Created', response.status)
    #
    # def test_device_resource_handler_post_returns_device_uri_in_location_header(self):
    #     gcm_registration_id = '123'
    #     request_body = {'macAddress': self.chrome_os_device_json.get('macAddress'),
    #                     'gcmRegistrationId': gcm_registration_id,
    #                     'tenantCode': self.TENANT_CODE}
    #     when(ChromeOsDevicesApi).list(any_matcher()).thenReturn(self.chrome_os_device_list_json)
    #     when(ContentManagerApi).create_device(any_matcher()).thenReturn(True)
    #     response = self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
    #     location_uri = str(response.headers['Location'])
    #     location_uri_components = location_uri.split('/')
    #     self.assertEqual(location_uri_components[5], "devices")
    #     key_length = len(location_uri_components[6])
    #     self.assertEqual(key_length, 48)
    #
    # def test_device_resource_handler_post_persists_gcm_registration_id(self):
    #     mac_address = self.chrome_os_device_json.get('macAddress')
    #     gcm_registration_id = '123'
    #     request_body = {'macAddress': mac_address,
    #                     'gcmRegistrationId': gcm_registration_id,
    #                     'tenantCode': self.TENANT_CODE}
    #     when(ChromeOsDevicesApi).list(any_matcher()).thenReturn(self.chrome_os_device_list_json)
    #     when(ContentManagerApi).create_device(any_matcher()).thenReturn(True)
    #     self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
    #     chrome_os_device_key = ChromeOsDevice.query(ChromeOsDevice.gcm_registration_id == gcm_registration_id). \
    #         get(keys_only=True)
    #     self.assertIsNotNone(chrome_os_device_key)
    #     self.assertTrue('123' == chrome_os_device_key.get().gcm_registration_id)
    #
    # def test_device_resource_handler_post_no_authorization_header_returns_forbidden(self):
    #     request_body = {'macAddress': self.chrome_os_device_json.get('macAddress'),
    #                     'gcmRegistrationId': '123',
    #                     'tenantCode': self.TENANT_CODE}
    #     with self.assertRaises(AppError) as context:
    #         self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.bad_authorization_header)
    #     self.assertTrue('403 Forbidden' in context.exception.message)
    #
    # def test_device_resource_handler_post_returns_unprocessable_entity_status_for_empty_request_body(self):
    #     when(ChromeOsDevicesApi).list(any_matcher()).thenReturn(self.chrome_os_device_list_json)
    #     with self.assertRaises(Exception) as context:
    #         self.app.post('/api/v1/devices', headers=self.valid_authorization_header)
    #     self.assertTrue('400 Did not receive request body' in str(context.exception))
    #
    # def test_device_resource_handler_post_returns_unprocessable_entity_status_for_unassociated_device(self):
    #     request_body = {'macAddress': 'bogusMacAddress',
    #                     'gcmRegistrationId': '123',
    #                     'tenantCode': self.TENANT_CODE}
    #     when(ChromeOsDevicesApi).list(any_matcher()).thenReturn(self.chrome_os_device_list_json)
    #     with self.assertRaises(Exception) as context:
    #         self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
    #     self.assertTrue('422 Chrome OS device not associated with this customer id' in str(context.exception))
    #
    # def test_device_resource_handler_post_returns_bad_request_with_registered_device(self):
    #     request_body = {'macAddress': self.MAC_ADDRESS,
    #                     'gcmRegistrationId': '123',
    #                     'tenantCode': self.TENANT_CODE}
    #     with self.assertRaises(Exception) as context:
    #         self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
    #     self.assertTrue('400 Cannot create because MAC address has already been assigned to this device'
    #                     in str(context.exception.message))
    #
    # def test_device_resource_handler_post_returns_bad_request_with_invalid_tenant(self):
    #     mac_address = self.chrome_os_device_json.get('macAddress')
    #     request_body = {'macAddress': mac_address,
    #                     'gcmRegistrationId': '123',
    #                     'tenantCode': 'invalid_tenant'}
    #     when(ChromeOsDevicesApi).list(any_matcher()).thenReturn(self.chrome_os_device_list_json)
    #     with self.assertRaises(Exception) as context:
    #         self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
    #     self.assertTrue('400 Invalid or inactive tenant for device.' in str(context.exception))
    #
    # def test_device_resource_handler_post_returns_bad_request_with_inactive_tenant(self):
    #     inactive_tenant = Tenant.create(tenant_code='inactive_tenant',
    #                                     name='Inactive Tenant, Inc',
    #                                     admin_email='boo@inactive_tenant.com',
    #                                     content_server_url=self.CONTENT_SERVER_URL,
    #                                     chrome_device_domain='inactive_tenant.com',
    #                                     active=False)
    #     inactive_tenant_key = inactive_tenant.put()
    #     mac_address = self.chrome_os_device_json.get('macAddress')
    #     request_body = {'macAddress': mac_address,
    #                     'gcmRegistrationId': '123',
    #                     'tenantCode': inactive_tenant_key.get().tenant_code}
    #     when(ChromeOsDevicesApi).list(any_matcher()).thenReturn(self.chrome_os_device_list_json)
    #     with self.assertRaises(Exception) as context:
    #         self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
    #     self.assertTrue('400 Invalid or inactive tenant for device.' in str(context.exception))
    #
    # def test_device_resource_put_returns_no_content(self):
    #     device_key = self.create_chrome_os_device(self.tenant_key)
    #     request_body = {'gcmRegistrationId': 'd23784972038845ab3963412', 'tenantCode': 'acme'}
    #     when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.chrome_os_device_json)
    #     response = self.app.put('/api/v1/devices/{0}'.format(device_key.urlsafe()),
    #                             json.dumps(request_body),
    #                             headers=self.valid_authorization_header)
    #     self.assertEqual('204 No Content', response.status)
    #
    # def test_device_resource_put_no_authorization_header_returns_forbidden(self):
    #     request_body = {'gcmRegistrationId': '123',
    #                     'tenantCode': self.TENANT_CODE}
    #     when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.chrome_os_device_json)
    #     with self.assertRaises(Exception) as context:
    #         self.app.put('/api/v1/devices/{0}'.format(self.chrome_os_device_key.urlsafe()),
    #                      json.dumps(request_body), headers=self.bad_authorization_header)
    #     self.assertTrue('403 Forbidden' in str(context.exception))
    #
    # def test_device_resource_put_updates_gcm_registration_id(self):
    #     device_key = self.create_chrome_os_device(self.tenant_key)
    #     request_body = {'gcmRegistrationId': 'd23784972038845ab3963412',
    #                     'tenantCode': self.TENANT_CODE}
    #     when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.chrome_os_device_json)
    #     self.app.put('/api/v1/devices/{0}'.format(device_key.urlsafe()),
    #                  json.dumps(request_body),
    #                  headers=self.valid_authorization_header)
    #     actual = device_key.get()
    #     self.assertEqual('d23784972038845ab3963412', actual.gcm_registration_id)
    #
    # def test_device_resource_put_unrecognized_device_lookup_returns_not_found(self):
    #     device_key = self.create_chrome_os_device(self.tenant_key)
    #     request_body = {'gcmRegistrationId': 'd23784972038845ab3963412'}
    #     when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(None)
    #     with self.assertRaises(Exception) as context:
    #         self.app.put('/api/v1/devices/{0}'.format(device_key.urlsafe()),
    #                      json.dumps(request_body),
    #                      headers=self.valid_authorization_header)
    #     self.assertTrue('404 Unrecognized device id in Google API' in str(context.exception))
    #
    # def test_device_resource_put_bogus_key_returns_not_found(self):
    #     bogus_key = 'bogus'
    #     request_body = {'gcmRegistrationId': 'd23784972038845ab3963412'}
    #     when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(None)
    #     with self.assertRaises(Exception) as context:
    #         self.app.put('/api/v1/devices/{0}'.format(bogus_key),
    #                      json.dumps(request_body),
    #                      headers=self.valid_authorization_header)
    #     self.assertTrue("404 Unrecognized device with key: {0}".format(bogus_key) in str(context.exception))
    #
    # def test_device_resource_put_unrecognized_local_device_returns_not_found(self):
    #     bogus_key = 'ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyVgsSEVRlbmFudEVudGl0eUdyb' \
    #                 + '3VwIhF0ZW5hbnRFbnRpdHlHcm91cAwLEgZUZW5hbnQYgICAgMC1mwoMCxIOQ2hyb21lT3NEZXZpY2UYgICAgJCihwoM'
    #     request_body = {'gcmRegistrationId': 'd23784972038845ab3963412'}
    #     when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(None)
    #     with self.assertRaises(Exception) as context:
    #         self.app.put('/api/v1/devices/{0}'.format(bogus_key),
    #                      json.dumps(request_body),
    #                      headers=self.valid_authorization_header)
    #     self.assertTrue("404 Unrecognized device with key: {0}".format(bogus_key) in str(context.exception))
    #
    # def test_device_resource_delete_returns_no_content(self):
    #     url = '/api/v1/devices/{0}'.format(self.chrome_os_device_key.urlsafe())
    #     response = self.app.delete(url, headers=self.valid_authorization_header)
    #     self.assertEqual('204 No Content', response.status)
    #
    # def test_device_resource_delete_no_authorization_header_returns_forbidden(self):
    #     url = '/api/v1/devices/{0}'.format(self.chrome_os_device_key.urlsafe())
    #     with self.assertRaises(Exception) as context:
    #         self.app.delete(url, headers=self.bad_authorization_header)
    #     self.assertTrue('403 Forbidden' in str(context.exception))
    #
    # def test_device_resource_delete_removes_chrome_os_device_entity(self):
    #     url = '/api/v1/devices/{0}'.format(self.chrome_os_device_key.urlsafe())
    #     self.app.delete(url, headers=self.valid_authorization_header)
    #     actual = self.chrome_os_device_key.get()
    #     self.assertIsNone(actual)
    #
    # def test_device_resource_delete_bogus_key_returns_not_found(self):
    #     bogus_key = 'ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyVgsSEVRlbmFudEVudGl0eUdyb' \
    #                 + '3VwIhF0ZW5hbnRFbnRpdHlHcm91cAwLEgZUZW5hbnQYgICAgMC1mwoMCxIOQ2hyb21lT3NEZXZpY2UYgICAgJCihwoM'
    #     url = '/api/v1/devices/{0}'.format(bogus_key)
    #     with self.assertRaises(Exception) as context:
    #         self.app.delete(url, headers=self.valid_authorization_header)
    #     self.assertTrue("404 Unrecognized device with key: {0}".format(bogus_key) in str(context.exception))
    #
    # def test_device_resource_handler_get_by_mac_address_returns_ok(self):
    #     request_parameters = {'macAddress': self.MAC_ADDRESS}
    #     when(ChromeOsDevicesApi).list(any_matcher()).thenReturn(self.chrome_os_device_list_json)
    #     response = self.app.get('/api/v1/devices', params=request_parameters, headers=self.valid_authorization_header)
    #     self.assertOK(response)
    #
    # def test_device_resource_handler_get_by_mac_address_returns_not_found_when_not_stored(self):
    #     mac_address = '54271e6972cb'  # MAC address Google knows about, but we have not registered.
    #     request_parameters = {'macAddress': mac_address}
    #     when(ChromeOsDevicesApi).list(any_matcher()).thenReturn(self.chrome_os_device_list_json)
    #     with self.assertRaises(AppError) as context:
    #         self.app.get('/api/v1/devices', params=request_parameters, headers=self.valid_authorization_header)
    #     self.assertTrue(
    #         "Device not stored for deviceId 54eb08ad-dee3-41c2-acbc-a9c55af9a5fa and MAC address {0}".format(
    #             mac_address) in str(context.exception.message))
    #
    # def test_device_resource_handler_get_by_mac_address_no_authorization_header_returns_forbidden(self):
    #     request_parameters = {'macAddress': self.MAC_ADDRESS}
    #     when(ChromeOsDevicesApi).list(any_matcher()).thenReturn(self.chrome_os_device_list_json)
    #     with self.assertRaises(AppError) as error:
    #         self.app.get('/api/v1/devices', params=request_parameters, headers=self.bad_authorization_header)
    #     self.assertTrue('403 Forbidden' in error.exception.message)
    #
    # def test_device_resource_handler_get_by_mac_address_with_bogus_mac_address(self):
    #     request_parameters = {'macAddress': 'bogus'}
    #     when(ChromeOsDevicesApi).list(any_matcher()).thenReturn(self.chrome_os_device_list_json)
    #     with self.assertRaises(AppError) as error:
    #         self.app.get('/api/v1/devices', params=request_parameters, headers=self.valid_authorization_header)
    #     self.assertTrue('404 Not Found' in error.exception.message)
    #
    # def test_device_resource_handler_get_by_mac_address_with_no_chrome_os_devices_returned(self):
    #     request_parameters = {'macAddress': self.MAC_ADDRESS}
    #     when(ChromeOsDevicesApi).list(any_matcher()).thenReturn(None)
    #     with self.assertRaises(AppError) as error:
    #         self.app.get('/api/v1/devices', params=request_parameters, headers=self.valid_authorization_header)
    #     self.assertTrue('404 Not Found' in error.exception.message)

    @staticmethod
    def load_file_contents(file_name):
        with open(file_name, 'r') as json_file:
            data = json_file.read().replace('\n', '')
        return data

    @staticmethod
    def create_chrome_os_device(tenant_key):
        device = ChromeOsDevice.create(tenant_key=tenant_key,
                                       device_id='132e235a-b346-4a37-a100-de49fa753a2a',
                                       gcm_registration_id='some gcm registration id',
                                       mac_address='54271e619346')
        return device.put()

    def __create_tenant(self, code, name, email):
        tenant = Tenant.create(tenant_code=code,
                               name=name,
                               admin_email=email,
                               content_server_url=self.CONTENT_SERVER_URL,
                               chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                               active=True)
        return tenant.put()

    def __create_device(self, tenant_key):
        device = ChromeOsDevice.create(tenant_key=tenant_key,
                                       device_id=self.DEVICE_ID,
                                       gcm_registration_id=self.GCM_REGISTRATION_ID,
                                       mac_address=self.MAC_ADDRESS)
        return device.put()

    def __build_list_devices(self, tenant_key=None, number_to_build=10):
        results = []
        if tenant_key is None:
            tenant_key = self.__create_tenant()
        for i in range(number_to_build):
            results.append(build(ChromeOsDevice, tenant_key=tenant_key))
        return results
