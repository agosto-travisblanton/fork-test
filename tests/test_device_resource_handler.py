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
