from app_config import config
from env_setup import setup_test_paths

setup_test_paths()

import json
from webtest import AppError
from agar.test import BaseTest, WebTest
from chrome_os_devices_api import ChromeOsDevicesApi
from mockito import when, any as any_matcher
from routes import application
from models import ChromeOsDevice


class TestDeviceResourceHandler(BaseTest, WebTest):
    APPLICATION = application
    CUSTOMER_ID = 'my_customer'

    def setUp(self):
        super(TestDeviceResourceHandler, self).setUp()
        self.chrome_os_device_json = json.loads(self.load_file_contents('tests/chrome_os_device.json'))
        self.chrome_os_device_list_json = json.loads(self.load_file_contents('tests/chrome_os_devices_api_list.json'))
        self.headers = {
            'Authorization': config.API_TOKEN
        }

    def test_device_resource_handler_get_by_id_returns_ok_status(self):
        device_key = self.load_device()
        request_parameters = {}
        uri = application.router.build(None, 'manage-device', None, {'device_id': device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters)
        self.assertOK(response)

    def test_device_resource_handler_get_by_id_returns_device_representation(self):
        device_key = self.load_device()
        request_parameters = {}
        uri = application.router.build(None, 'manage-device', None, {'device_id': device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters)
        response_json = json.loads(response.body)
        expected = device_key.get()
        self.assertEqual(response_json.get('device_id'), expected.device_id)
        self.assertEqual(response_json.get('gcm_registration_id'), expected.gcm_registration_id)
        self.assertEqual(response_json.get('tenant_code'), expected.tenant_code)
        self.assertEqual(response_json.get('created'), expected.created.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response_json.get('updated'), expected.updated.strftime('%Y-%m-%d %H:%M:%S'))

    def test_device_resource_handler_get_all_devices_returns_ok(self):
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        response = self.app.get('/api/v1/devices', params={}, headers=self.headers)
        self.assertOK(response)

    def test_device_resource_handler_get_all_devices_returns_404(self):
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(None)
        with self.assertRaises(AppError) as error:
            self.app.get('/api/v1/devices', params={}, headers=self.headers)
        self.assertTrue('404 Not Found' in error.exception.message)

    def test_device_resource_handler_get_by_mac_address(self):
        request_parameters = {'macAddress': self.chrome_os_device_json.get('macAddress')}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        response = self.app.get('/api/v1/devices', params=request_parameters, headers=self.headers)
        self.assertOK(response)

    def test_device_resource_handler_get_by_mac_address_with_bogus_mac_address(self):
        request_parameters = {'macAddress': 'bogus'}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        with self.assertRaises(AppError) as error:
            self.app.get('/api/v1/devices', params=request_parameters, headers=self.headers)
        self.assertTrue('404 Not Found' in error.exception.message)

    def test_device_resource_handler_get_by_mac_address_with_no_chrome_os_devices_returned(self):
        request_parameters = {'macAddress': self.chrome_os_device_json.get('macAddress')}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(None)
        with self.assertRaises(AppError) as error:
            self.app.get('/api/v1/devices', params=request_parameters, headers=self.headers)
        self.assertTrue('404 Not Found' in error.exception.message)

    def test_device_resource_handler_post_returns_created_status(self):
        request_body = {'macAddress': self.chrome_os_device_json.get('macAddress'), 'gcm_registration_id': '123',
                        'tenant_code': 'Acme'}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        response = self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.headers)
        self.assertEqual('201 Created', response.status)

    def test_device_resource_handler_post_returns_gettable_device_representation_via_uri_in_location_header(self):
        gcm_registration_id = '123'
        tenant_code = 'Acme'
        request_body = {'macAddress': self.chrome_os_device_json.get('macAddress'),
                        'gcm_registration_id': gcm_registration_id,
                        'tenant_code': tenant_code}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        response = self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.headers)
        location_uri = str(response.headers['Location'])
        response = self.app.get(location_uri, params={})
        self.assertOK(response)
        response_json = json.loads(response.body)
        self.assertEqual(response_json.get('gcm_registration_id'), gcm_registration_id)
        self.assertEqual(response_json.get('tenant_code'), tenant_code)

    def test_device_resource_handler_post_returns_unprocessable_entity_status_for_empty_request_body(self):
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        with self.assertRaises(Exception) as context:
            self.app.post('/api/v1/devices', headers=self.headers)
        self.assertTrue('422 Did not receive request body' in str(context.exception))

    def test_device_resource_handler_post_returns_unprocessable_entity_status_for_unassociated_device(self):
        request_body = {'macAddress': 'bogusMacAddress', 'gcm_registration_id': '123',
                        'tenant_code': 'Acme'}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        with self.assertRaises(Exception) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.headers)
        self.assertTrue('422 Chrome OS device not associated with this customer id' in str(context.exception))

    def test_device_resource_handler_post_persists_gcm_registration_id(self):
        mac_address = self.chrome_os_device_json.get('macAddress')
        gcm_registration_id = '123'
        request_body = {'macAddress': mac_address, 'gcm_registration_id': gcm_registration_id, 'tenant_code': 'Acme'}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(self.chrome_os_device_list_json)
        self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.headers)
        chrome_os_device_key = ChromeOsDevice.query(ChromeOsDevice.gcm_registration_id == gcm_registration_id). \
            get(keys_only=True)
        self.assertIsNotNone(chrome_os_device_key)
        self.assertTrue('123' == chrome_os_device_key.get().gcm_registration_id)

    def test_device_resource_put_returns_no_content(self):
        gcm_registration_id = 'd23784972038845ab3963412'
        request_body = {'gcmRegistrationId': gcm_registration_id, 'tenantCode': 'Acme'}
        when(ChromeOsDevicesApi).get(self.CUSTOMER_ID, any_matcher(str)).thenReturn(self.chrome_os_device_json)
        response = self.app.put('/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId')),
                                json.dumps(request_body))
        self.assertEqual('204 No Content', response.status)

    def test_device_resource_put_updates_gcm_registration_id(self):
        gcm_registration_id = 'd23784972038845ab3963412'
        request_body = {'gcmRegistrationId': gcm_registration_id, 'tenantCode': 'Acme'}
        when(ChromeOsDevicesApi).get(self.CUSTOMER_ID, any_matcher(str)).thenReturn(self.chrome_os_device_json)
        device_id = self.chrome_os_device_json.get('deviceId')
        url = '/api/v1/devices/{0}'.format(device_id)
        self.app.put(url, json.dumps(request_body))
        actual = ChromeOsDevice.get_by_device_id(device_id)
        self.assertEqual(gcm_registration_id, actual.gcm_registration_id)

    def test_device_resource_put_for_failed_device_lookup(self):
        request_body = {'gcmRegistrationId': 'd23784972038845ab3963412'}
        when(ChromeOsDevicesApi).get(any_matcher(str), any_matcher(str)).thenReturn(None)
        device_id = self.chrome_os_device_json.get('deviceId')
        with self.assertRaises(Exception) as context:
            self.app.put('/api/v1/devices/{0}'.format(device_id), json.dumps(request_body))
        self.assertTrue('422 Unable to retrieve Chrome OS device by device ID: {0}'.format(device_id) in
                        str(context.exception))

    def test_device_resource_delete_returns_no_content(self):
        chrome_os_device = ChromeOsDevice(device_id=self.chrome_os_device_json.get('deviceId'),
                                          gcm_registration_id='d23784972038845ab3963412',
                                          tenant_code='Acme')
        chrome_os_device.put()
        when(ChromeOsDevicesApi).get(self.CUSTOMER_ID, any_matcher(str)).thenReturn(self.chrome_os_device_json)
        url = '/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId'))
        response = self.app.delete(url)
        self.assertEqual('204 No Content', response.status)

    def test_device_resource_delete_removes_chrome_os_device_entity(self):
        chrome_os_device = ChromeOsDevice(device_id=self.chrome_os_device_json.get('deviceId'),
                                          gcm_registration_id='d23784972038845ab3963412')
        chrome_os_device.put()
        when(ChromeOsDevicesApi).get(self.CUSTOMER_ID, any_matcher(str)).thenReturn(self.chrome_os_device_json)
        device_id = self.chrome_os_device_json.get('deviceId')
        url = '/api/v1/devices/{0}'.format(device_id)
        self.app.delete(url)
        actual = ChromeOsDevice.get_by_device_id(device_id)
        self.assertIsNone(actual)

    def test_device_resource_delete_removes_chrome_os_device_entity(self):
        when(ChromeOsDevicesApi).get(self.CUSTOMER_ID, any_matcher(str)).thenReturn(self.chrome_os_device_json)
        bogus_device_id = 'bogus_device_id'
        url = '/api/v1/devices/{0}'.format(bogus_device_id)
        with self.assertRaises(Exception) as context:
            self.app.delete(url)
        self.assertTrue('422 Unable to retrieve ChromeOS device by device ID: {0}'.format(bogus_device_id) in
                        str(context.exception))

    @staticmethod
    def load_file_contents(file_name):
        with open(file_name, 'r') as json_file:
            data = json_file.read().replace('\n', '')
        return data

    @staticmethod
    def load_device():
        device = ChromeOsDevice(
            device_id='some device id',
            gcm_registration_id='some gcm registration id',
            tenant_code='some tenant code'
        )
        device_key = device.put()
        return device_key
