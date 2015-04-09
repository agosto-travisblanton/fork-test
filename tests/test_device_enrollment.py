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
            self.assertEquals(self.chrome_os_device.get('activeTimeRanges'), body.get('activeTimeRanges'))
            self.assertEquals(self.chrome_os_device.get('annotatedLocation'), body.get('annotatedLocation'))
            self.assertEquals(self.chrome_os_device.get('annotatedUser'), body.get('annotatedUser'))
            self.assertEquals(self.chrome_os_device.get('bootMode'), body.get('bootMode'))
            self.assertEquals(self.chrome_os_device.get('deviceId'), body.get('deviceId'))
            self.assertEquals(self.chrome_os_device.get('etag'), body.get('etag'))
            self.assertEquals(self.chrome_os_device.get('firmwareVersion'), body.get('firmwareVersion'))
            self.assertEquals(self.chrome_os_device.get('kind'), body.get('kind'))
            self.assertEquals(self.chrome_os_device.get('lastEnrollmentTime'), body.get('lastEnrollmentTime'))
            self.assertEquals(self.chrome_os_device.get('lastSync'), body.get('lastSync'))
            self.assertEquals(self.chrome_os_device.get('model'), body.get('model'))
            self.assertEquals(self.chrome_os_device.get('notes'), body.get('notes'))
            self.assertEquals(self.chrome_os_device.get('orgUnitPath'), body.get('orgUnitPath'))
            self.assertEquals(self.chrome_os_device.get('osVersion'), body.get('osVersion'))
            self.assertEquals(self.chrome_os_device.get('platformVersion'), body.get('platformVersion'))
            self.assertEquals(self.chrome_os_device.get('serialNumber'), body.get('serialNumber'))
            self.assertEquals(self.chrome_os_device.get('status'), body.get('status'))

    def loadFileContents(self, file_name):
        with open(file_name, 'r') as json_file:
            data = json_file.read().replace('\n', '')
        return data