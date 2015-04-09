from agar.test import BaseTest, WebTest
from routes import application
from mock import patch
import json


class TestDeviceEnrollmentHandler(BaseTest, WebTest):
    APPLICATION = application

    def setUp(self):
        super(TestDeviceEnrollmentHandler, self).setUp()
        self.chrome_os_device = json.loads(self.loadFileContents('tests/chrome_os_device.json'))
        self.gcm_id = 'd23784972038845ab3948459'
        self.uri = application.router.build(None, 'device-enrollment', None, {})

    def testDeviceEnrollment_ReturnsOKStatus(self):
        request_parameters = {'mac_address': self.chrome_os_device.get('macAddress'), 'gcm_id': self.gcm_id}
        with patch('chrome_os_devices_api.ChromeOsDevicesApi') as chrome_os_devices_api_mock:
            mock_instance = chrome_os_devices_api_mock.return_value
            mock_instance.list.return_value = self.loadFileContents('tests/chrome_os_devices_api_list.json')
            response = self.app.get(self.uri, params=request_parameters)
            self.assertOK(response)

    def testDeviceEnrollment_ReturnsChromeOsResourceRepresentation(self):
        request_parameters = {'mac_address': self.chrome_os_device.get('macAddress'), 'gcm_id': self.gcm_id}
        with patch('chrome_os_devices_api.ChromeOsDevicesApi') as chrome_os_devices_api_mock:
            mock_instance = chrome_os_devices_api_mock.return_value
            mock_instance.list.return_value = self.loadFileContents('tests/chrome_os_devices_api_list.json')
            response = self.app.get(self.uri, params=request_parameters)
            body = json.loads(response.body)
            self.assertEquals(self.chrome_os_device.get('macAddress'), body.get('macAddress'))

    def loadFileContents(self, file_name):
        with open(file_name, 'r') as json_file:
            data = json_file.read().replace('\n', '')
        return data