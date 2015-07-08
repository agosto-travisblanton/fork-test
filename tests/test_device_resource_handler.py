from env_setup import setup_test_paths

setup_test_paths()

import json
from webtest import AppError
from agar.test import BaseTest, WebTest
from chrome_os_devices_api import ChromeOsDevicesApi
from mockito import when, any as any_matcher
from routes import application
from models import ChromeOsDevice, Tenant
from app_config import config


class TestDeviceResourceHandler(BaseTest, WebTest):
    APPLICATION = application
    CUSTOMER_ID = 'my_customer'
    NAME = 'foobar tenant'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://www.content.com'
    CONTENT_SERVER_API_KEY = 'API KEY'
    CHROME_DEVICE_DOMAIN = 'bar.com'
    TENANT_CODE = 'foobar'
    TESTING_DEVICE_ID = '4f099e50-6028-422b-85d2-3a629a45bf38'
    TEST_GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
    MAC_ADDRESS = '54271e619346'

    def setUp(self):
        super(TestDeviceResourceHandler, self).setUp()
        self.tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                                    name=self.NAME,
                                    admin_email=self.ADMIN_EMAIL,
                                    content_server_url=self.CONTENT_SERVER_URL,
                                    chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                                    active=True)
        self.tenant_key = self.tenant.put()
        self.chrome_os_device = ChromeOsDevice.create(tenant_key=self.tenant_key,
                                                      device_id=self.TESTING_DEVICE_ID,
                                                      gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                                      mac_address=self.MAC_ADDRESS)
        self.chrome_os_device_key = self.chrome_os_device.put()

        self.chrome_os_device_json = json.loads(self.load_file_contents('tests/chrome_os_device.json'))
        self.chrome_os_device_list_json = json.loads(self.load_file_contents('tests/chrome_os_devices_api_list.json'))
        self.valid_authorization_header = {
            'Authorization': config.API_TOKEN
        }
        self.bad_authorization_header = {}

    def test_device_resource_handler_get_by_key_returns_not_found_for_bogus_key(self):
        when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.chrome_os_device_json)
        request_parameters = {}
        uri = application.router.build(None, 'manage-device', None, {'device_urlsafe_key': 'bogus key'})
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        self.assertTrue('404 Not Found' in context.exception.message)

    def test_device_resource_handler_get_by_key_returns_bad_request_for_missing_parent_tenant(self):
        when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.chrome_os_device_json)
        request_parameters = {}
        device = ChromeOsDevice(
            api_key='some key',
            device_id=self.TESTING_DEVICE_ID,
            gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
            mac_address=self.MAC_ADDRESS)
        key = device.put()
        uri = application.router.build(None, 'manage-device', None, {'device_urlsafe_key': key.urlsafe()})
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        self.assertTrue('400 Bad Request' in context.exception.message)

    def test_device_resource_handler_get_by_key_returns_ok(self):
        when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.chrome_os_device_json)
        request_parameters = {}
        uri = application.router.build(None, 'manage-device', None, {'device_urlsafe_key':
                                                                         self.chrome_os_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_device_resource_handler_no_authorization_header_returns_forbidden(self):
        when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.chrome_os_device_json)
        request_parameters = {}
        uri = application.router.build(None, 'manage-device', None, {'device_urlsafe_key':
                                                                         self.chrome_os_device_key.urlsafe()})
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.bad_authorization_header)
        self.assertTrue('403 Forbidden' in context.exception.message)

    def test_device_resource_handler_get_by_id_returns_device_representation(self):
        device_key = self.create_chrome_os_device(self.tenant_key)
        when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.chrome_os_device_json)
        request_parameters = {}
        uri = application.router.build(None, 'manage-device', None, {'device_urlsafe_key': device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        response_json = json.loads(response.body)
        expected = device_key.get()
        self.assertEqual(response_json.get('deviceId'), expected.device_id)
        self.assertEqual(response_json.get('gcmRegistrationId'), expected.gcm_registration_id)
        self.assertEqual(response_json.get('created'), expected.created.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response_json.get('updated'), expected.updated.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response_json.get('apiKey'), expected.api_key)
        self.assertEqual(response_json.get('active'), True)
        self.assertEqual(response_json.get('key'), device_key.urlsafe())

    def test_device_resource_handler_get_all_devices_returns_ok(self):
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        response = self.app.get('/api/v1/devices', params={}, headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_device_resource_handler_get_all_devices_returns_not_found(self):
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(None)
        with self.assertRaises(AppError) as context:
            self.app.get('/api/v1/devices', params={}, headers=self.valid_authorization_header)
        self.assertTrue('404 Not Found' in context.exception.message)

    def test_device_resource_handler_post_returns_created_status(self):
        request_body = {'macAddress': self.chrome_os_device_json.get('macAddress'),
                        'gcmRegistrationId': '123',
                        'tenantCode': 'foobar'
                        }
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        response = self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertEqual('201 Created', response.status)

    def test_device_resource_handler_post_no_authorization_header_returns_forbidden(self):
        request_body = {'macAddress': self.chrome_os_device_json.get('macAddress'),
                        'gcmRegistrationId': '123',
                        'tenantCode': 'Acme'}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.bad_authorization_header)
        self.assertTrue('403 Forbidden' in context.exception.message)

    def test_device_resource_handler_post_returns_device_uri_in_location_header(self):
        gcm_registration_id = '123'
        request_body = {'macAddress': self.chrome_os_device_json.get('macAddress'),
                        'gcmRegistrationId': gcm_registration_id,
                        'tenantCode': self.TENANT_CODE}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        response = self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        location_uri = str(response.headers['Location'])
        location_uri_components = location_uri.split('/')
        self.assertEqual(location_uri_components[5], "devices")
        key_length = len(location_uri_components[6])
        self.assertEqual(key_length, 118)

    def test_device_resource_handler_post_returns_unprocessable_entity_status_for_empty_request_body(self):
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        with self.assertRaises(Exception) as context:
            self.app.post('/api/v1/devices', headers=self.valid_authorization_header)
        self.assertTrue('400 Did not receive request body' in str(context.exception))

    def test_device_resource_handler_post_returns_unprocessable_entity_status_for_unassociated_device(self):
        request_body = {'macAddress': 'bogusMacAddress',
                        'gcmRegistrationId': '123',
                        'tenantCode': 'foobar'}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        with self.assertRaises(Exception) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertTrue('422 Chrome OS device not associated with this customer id' in str(context.exception))

    def test_device_resource_handler_post_persists_gcm_registration_id(self):
        mac_address = self.chrome_os_device_json.get('macAddress')
        gcm_registration_id = '123'
        request_body = {'macAddress': mac_address,
                        'gcmRegistrationId': gcm_registration_id,
                        'tenantCode': self.TENANT_CODE}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        chrome_os_device_key = ChromeOsDevice.query(ChromeOsDevice.gcm_registration_id == gcm_registration_id). \
            get(keys_only=True)
        self.assertIsNotNone(chrome_os_device_key)
        self.assertTrue('123' == chrome_os_device_key.get().gcm_registration_id)

    def test_device_resource_handler_post_links_tenant_as_chrome_os_device_parent(self):
        mac_address = self.chrome_os_device_json.get('macAddress')
        gcm_registration_id = '123'
        request_body = {'macAddress': mac_address,
                        'gcmRegistrationId': gcm_registration_id,
                        'tenantCode': self.tenant.tenant_code}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        chrome_os_device_key = ChromeOsDevice.query(ChromeOsDevice.gcm_registration_id == gcm_registration_id). \
            get(keys_only=True)
        parent_tenant_key = chrome_os_device_key.parent()
        self.assertIsNotNone(parent_tenant_key)

    def test_device_resource_handler_post_returns_bad_request_with_registered_device(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': '123',
                        'tenantCode': self.TENANT_CODE}
        with self.assertRaises(Exception) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertTrue('400 Cannot create because MAC address has already been assigned to this device'
                        in str(context.exception.message))

    def test_device_resource_handler_post_returns_bad_request_with_invalid_tenant(self):
        mac_address = self.chrome_os_device_json.get('macAddress')
        request_body = {'macAddress': mac_address,
                        'gcmRegistrationId': '123',
                        'tenantCode': 'invalid_tenant'}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        with self.assertRaises(Exception) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertTrue('400 Invalid or inactive tenant for device.' in str(context.exception))

    def test_device_resource_handler_post_returns_bad_request_with_inactive_tenant(self):
        inactive_tenant = Tenant.create(tenant_code='inactive_tenant',
                                        name='Inactive Tenant, Inc',
                                        admin_email='boo@inactive_tenant.com',
                                        content_server_url=self.CONTENT_SERVER_URL,
                                        chrome_device_domain='inactive_tenant.com',
                                        active=False)
        inactive_tenant_key = inactive_tenant.put()
        mac_address = self.chrome_os_device_json.get('macAddress')
        request_body = {'macAddress': mac_address,
                        'gcmRegistrationId': '123',
                        'tenantCode': inactive_tenant_key.get().tenant_code}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        with self.assertRaises(Exception) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertTrue('400 Invalid or inactive tenant for device.' in str(context.exception))

    def test_device_resource_put_returns_no_content(self):
        device_key = self.create_chrome_os_device(self.tenant_key)
        request_body = {'gcmRegistrationId': 'd23784972038845ab3963412', 'tenantCode': 'acme'}
        when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.chrome_os_device_json)
        response = self.app.put('/api/v1/devices/{0}'.format(device_key.urlsafe()),
                                json.dumps(request_body),
                                headers=self.valid_authorization_header)
        self.assertEqual('204 No Content', response.status)

    def test_device_resource_put_no_authorization_header_returns_forbidden(self):
        request_body = {'gcmRegistrationId': '123',
                        'tenantCode': self.TENANT_CODE}
        when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.chrome_os_device_json)
        with self.assertRaises(Exception) as context:
            self.app.put('/api/v1/devices/{0}'.format(self.chrome_os_device_key.urlsafe()),
                         json.dumps(request_body), headers=self.bad_authorization_header)
        self.assertTrue('403 Forbidden' in str(context.exception))

    def test_device_resource_put_updates_gcm_registration_id(self):
        device_key = self.create_chrome_os_device(self.tenant_key)
        request_body = {'gcmRegistrationId': 'd23784972038845ab3963412',
                        'tenantCode': self.TENANT_CODE}
        when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.chrome_os_device_json)
        self.app.put('/api/v1/devices/{0}'.format(device_key.urlsafe()),
                     json.dumps(request_body),
                     headers=self.valid_authorization_header)
        actual = device_key.get()
        self.assertEqual('d23784972038845ab3963412', actual.gcm_registration_id)

    def test_device_resource_put_for_failed_device_lookup(self):
        device_key = self.create_chrome_os_device(self.tenant_key)
        request_body = {'gcmRegistrationId': 'd23784972038845ab3963412'}
        when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(None)
        with self.assertRaises(Exception) as context:
            self.app.put('/api/v1/devices/{0}'.format(device_key.urlsafe()),
                         json.dumps(request_body),
                         headers=self.valid_authorization_header)
        self.assertTrue(
            '422 Unable to retrieve Chrome OS device by device id: 132e235a-b346-4a37-a100-de49fa753a2a' in str(
                context.exception))

    def test_device_resource_delete_returns_no_content(self):
        url = '/api/v1/devices/{0}'.format(self.chrome_os_device_key.urlsafe())
        response = self.app.delete(url, headers=self.valid_authorization_header)
        self.assertEqual('204 No Content', response.status)

    def test_device_resource_delete_no_authorization_header_returns_forbidden(self):
        url = '/api/v1/devices/{0}'.format(self.chrome_os_device_key.urlsafe())
        with self.assertRaises(Exception) as context:
            self.app.delete(url, headers=self.bad_authorization_header)
        self.assertTrue('403 Forbidden' in str(context.exception))

    def test_device_resource_delete_removes_chrome_os_device_entity(self):
        url = '/api/v1/devices/{0}'.format(self.chrome_os_device_key.urlsafe())
        self.app.delete(url, headers=self.valid_authorization_header)
        actual = self.chrome_os_device_key.get()
        self.assertIsNone(actual)

    def test_device_resource_handler_get_by_mac_address_returns_ok(self):
        request_parameters = {'macAddress': self.MAC_ADDRESS}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        response = self.app.get('/api/v1/devices', params=request_parameters, headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_device_resource_handler_get_by_mac_address_returns_not_found_when_not_stored(self):
        mac_address = '54271e6972cb'  # MAC address Google knows about, but we have not registered.
        request_parameters = {'macAddress': mac_address}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        with self.assertRaises(AppError) as context:
            self.app.get('/api/v1/devices', params=request_parameters, headers=self.valid_authorization_header)
        self.assertTrue(
            "Device not stored for deviceId 54eb08ad-dee3-41c2-acbc-a9c55af9a5fa and MAC address {0}".format(
                mac_address) in str(context.exception.message))

    def test_device_resource_handler_get_by_mac_address_no_authorization_header_returns_forbidden(self):
        request_parameters = {'macAddress': self.MAC_ADDRESS}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        with self.assertRaises(AppError) as error:
            self.app.get('/api/v1/devices', params=request_parameters, headers=self.bad_authorization_header)
        self.assertTrue('403 Forbidden' in error.exception.message)

    def test_device_resource_handler_get_by_mac_address_with_bogus_mac_address(self):
        request_parameters = {'macAddress': 'bogus'}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        with self.assertRaises(AppError) as error:
            self.app.get('/api/v1/devices', params=request_parameters, headers=self.valid_authorization_header)
        self.assertTrue('404 Not Found' in error.exception.message)

    def test_device_resource_handler_get_by_mac_address_with_no_chrome_os_devices_returned(self):
        request_parameters = {'macAddress': self.MAC_ADDRESS}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(None)
        with self.assertRaises(AppError) as error:
            self.app.get('/api/v1/devices', params=request_parameters, headers=self.valid_authorization_header)
        self.assertTrue('404 Not Found' in error.exception.message)

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
