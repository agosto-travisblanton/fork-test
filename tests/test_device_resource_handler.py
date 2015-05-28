from env_setup import setup_test_paths;

setup_test_paths()

import json

from agar.test import BaseTest, WebTest
from routes import application
from mock import patch
from models import ChromeOsDevice


class TestDeviceResourceHandler(BaseTest, WebTest):
    APPLICATION = application

    def setUp(self):
        super(TestDeviceResourceHandler, self).setUp()
        self.chrome_os_device_json = json.loads(self.load_file_contents('tests/chrome_os_device.json'))
        self.gcm_id = 'd23784972038845ab3948459'
        self.patched_chrome_os_devices_api = patch('chrome_os_devices_api.ChromeOsDevicesApi')
        self.chrome_os_devices_api_mock = self.patched_chrome_os_devices_api.start()
        self.chrome_os_devices_api_mock_instance = self.chrome_os_devices_api_mock.return_value

    def tearDown(self):
        if self.chrome_os_devices_api_mock_instance is not None:
            self.chrome_os_devices_api_mock_instance.reset_mock()
        if self.patched_chrome_os_devices_api is not None:
            self.patched_chrome_os_devices_api.stop()

    def test_device_resource_put_returns_no_content(self):
        chrome_os_device = ChromeOsDevice(device_id=self.chrome_os_device_json.get('deviceId'),
                                          gcm_registration_id='d23784972038845ab3963412')
        chrome_os_device.put()
        request_body = {'gcmRegistrationId': self.gcm_id}
        self.chrome_os_devices_api_mock_instance.get.return_value = self.load_file_contents(
            'tests/chrome_os_device.json')
        response = self.app.put('/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId')),
                                json.dumps(request_body))
        self.assertEqual('204 No Content', response.status)

    def test_device_resource_put_updates_gcm_registration_id(self):
        chrome_os_device = ChromeOsDevice(device_id=self.chrome_os_device_json.get('deviceId'),
                                          gcm_registration_id='d23784972038845ab3963412')
        key = chrome_os_device.put()
        request_body = {'gcmRegistrationId': self.gcm_id}
        self.chrome_os_devices_api_mock_instance.get.return_value = self.load_file_contents(
            'tests/chrome_os_device.json')
        url = '/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId'))
        self.app.put(url, json.dumps(request_body))
        actual = key.get()
        self.assertEqual(self.gcm_id, actual.gcm_registration_id)

    def test_device_resource_put_creates_chrome_os_device_updates_gcm_registration_id(self):
        request_body = {'gcmRegistrationId': self.gcm_id}
        self.chrome_os_devices_api_mock_instance.get.return_value = self.load_file_contents(
            'tests/chrome_os_device.json')
        url = '/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId'))
        self.app.put(url, json.dumps(request_body))
        actual = ChromeOsDevice.get_by_device_id(self.chrome_os_device_json.get('deviceId'))
        self.assertIsNotNone(actual)
        self.assertEqual(self.gcm_id, actual.gcm_registration_id)

    def test_device_resource_delete_returns_no_content(self):
        chrome_os_device = ChromeOsDevice(device_id=self.chrome_os_device_json.get('deviceId'),
                                          gcm_registration_id='d23784972038845ab3963412')
        chrome_os_device.put()
        self.chrome_os_devices_api_mock_instance.get.return_value = self.load_file_contents(
            'tests/chrome_os_device.json')
        url = '/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId'))
        response = self.app.delete(url)
        self.assertEqual('204 No Content', response.status)

    def test_device_resource_delete_removes_chrome_os_device_entity(self):
        chrome_os_device = ChromeOsDevice(device_id=self.chrome_os_device_json.get('deviceId'),
                                          gcm_registration_id='d23784972038845ab3963412')
        chrome_os_device.put()
        self.chrome_os_devices_api_mock_instance.get.return_value = self.load_file_contents(
            'tests/chrome_os_device.json')
        url = '/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId'))
        self.app.delete(url)
        actual = ChromeOsDevice.get_by_device_id(self.chrome_os_device_json.get('deviceId'))
        self.assertIsNone(actual)

    @staticmethod
    def load_file_contents(file_name):
        with open(file_name, 'r') as json_file:
            data = json_file.read().replace('\n', '')
        return data
