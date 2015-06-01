from app_config import config
from env_setup import setup_test_paths

setup_test_paths()

import json
from webtest import AppError
from agar.test import BaseTest, WebTest
from chrome_os_devices_api import ChromeOsDevicesApi
from mockito import when, unstub, any as any_matcher
from routes import application
from models import ChromeOsDevice

class TestDeviceResourceHandler(BaseTest, WebTest):
    APPLICATION = application

    def setUp(self):
        super(TestDeviceResourceHandler, self).setUp()
        self.chrome_os_device_json = json.loads(self.load_file_contents('tests/chrome_os_device.json'))
        self.headers = {
            'Authorization': config.API_TOKEN
        }

    def test_device_resource_handler_get_all_devices_returns_ok(self):
        json_result = json.loads(self.load_file_contents('tests/chrome_os_devices_api_list.json'))
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(json_result)
        response = self.app.get('/api/v1/devices', params={}, headers=self.headers)
        self.assertOK(response)

    def test_device_resource_handler_get_all_devices_returns_404(self):
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(None)
        with self.assertRaises(AppError) as error:
            self.app.get('/api/v1/devices', params={}, headers=self.headers)
        self.assertTrue('404 Not Found' in error.exception.message)

    def test_device_resource_handler_get_by_mac_address(self):
        request_parameters = {'macAddress': self.chrome_os_device_json.get('macAddress')}
        json_result = json.loads(self.load_file_contents('tests/chrome_os_devices_api_list.json'))
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(json_result)
        response = self.app.get('/api/v1/devices', params=request_parameters, headers=self.headers)
        self.assertOK(response)

    def test_device_resource_handler_get_by_mac_address_with_bogus_mac_address(self):
        request_parameters = {'macAddress': 'bogus'}
        json_result = json.loads(self.load_file_contents('tests/chrome_os_devices_api_list.json'))
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(json_result)
        with self.assertRaises(AppError) as error:
            self.app.get('/api/v1/devices', params=request_parameters, headers=self.headers)
        self.assertTrue('404 Not Found' in error.exception.message)

    def test_device_resource_handler_get_by_mac_address_with_no_chrome_os_devices_returned(self):
        request_parameters = {'macAddress': self.chrome_os_device_json.get('macAddress')}
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(None)
        with self.assertRaises(AppError) as error:
            self.app.get('/api/v1/devices', params=request_parameters, headers=self.headers)
        self.assertTrue('404 Not Found' in error.exception.message)

    def test_device_resource_handler_post_does_sumptin(self):
        request_body = {'macAddress': self.chrome_os_device_json.get('macAddress'), 'gcm_registration_id': 'blah'}
        json_result = json.loads(self.load_file_contents('tests/chrome_os_devices_api_list.json'))
        when(ChromeOsDevicesApi).list(any_matcher(str)).thenReturn(json_result)
        response = self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.headers)
        self.assertEqual('201 Created', response.status)

    # def test_device_resource_put_returns_no_content(self):
    #     chrome_os_device = ChromeOsDevice(device_id=self.chrome_os_device_json.get('deviceId'),
    #                                       gcm_registration_id='d23784972038845ab3963412')
    #     chrome_os_device.put()
    #     request_body = {'gcmRegistrationId': self.gcm_id}
    #     self.chrome_os_devices_api_mock_instance.get.return_value = self.load_file_contents(
    #         'tests/chrome_os_device.json')
    #     response = self.app.put('/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId')),
    #                             json.dumps(request_body))
    #     self.assertEqual('204 No Content', response.status)

    # def test_device_resource_put_updates_gcm_registration_id(self):
    #     chrome_os_device = ChromeOsDevice(device_id=self.chrome_os_device_json.get('deviceId'),
    #                                       gcm_registration_id='d23784972038845ab3963412')
    #     key = chrome_os_device.put()
    #     request_body = {'gcmRegistrationId': self.gcm_id}
    #     self.chrome_os_devices_api_mock_instance.get.return_value = self.load_file_contents(
    #         'tests/chrome_os_device.json')
    #     url = '/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId'))
    #     self.app.put(url, json.dumps(request_body))
    #     actual = key.get()
    #     self.assertEqual(self.gcm_id, actual.gcm_registration_id)
    #
    # def test_device_resource_put_creates_chrome_os_device_updates_gcm_registration_id(self):
    #     request_body = {'gcmRegistrationId': self.gcm_id}
    #     self.chrome_os_devices_api_mock_instance.get.return_value = self.load_file_contents(
    #         'tests/chrome_os_device.json')
    #     url = '/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId'))
    #     self.app.put(url, json.dumps(request_body))
    #     actual = ChromeOsDevice.get_by_device_id(self.chrome_os_device_json.get('deviceId'))
    #     self.assertIsNotNone(actual)
    #     self.assertEqual(self.gcm_id, actual.gcm_registration_id)
    #
    # def test_device_resource_delete_returns_no_content(self):
    #     chrome_os_device = ChromeOsDevice(device_id=self.chrome_os_device_json.get('deviceId'),
    #                                       gcm_registration_id='d23784972038845ab3963412')
    #     chrome_os_device.put()
    #     self.chrome_os_devices_api_mock_instance.get.return_value = self.load_file_contents(
    #         'tests/chrome_os_device.json')
    #     url = '/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId'))
    #     response = self.app.delete(url)
    #     self.assertEqual('204 No Content', response.status)
    #
    # def test_device_resource_delete_removes_chrome_os_device_entity(self):
    #     chrome_os_device = ChromeOsDevice(device_id=self.chrome_os_device_json.get('deviceId'),
    #                                       gcm_registration_id='d23784972038845ab3963412')
    #     chrome_os_device.put()
    #     self.chrome_os_devices_api_mock_instance.get.return_value = self.load_file_contents(
    #         'tests/chrome_os_device.json')
    #     url = '/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId'))
    #     self.app.delete(url)
    #     actual = ChromeOsDevice.get_by_device_id(self.chrome_os_device_json.get('deviceId'))
    #     self.assertIsNone(actual)

    @staticmethod
    def load_file_contents(file_name):
        with open(file_name, 'r') as json_file:
            data = json_file.read().replace('\n', '')
        return data
