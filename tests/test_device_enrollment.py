import json

from agar.test import BaseTest, WebTest
from routes import application
from mock import patch
from models import ChromeOsDevice


class TestDeviceEnrollmentHandler(BaseTest, WebTest):
    APPLICATION = application

    def setUp(self):
        super(TestDeviceEnrollmentHandler, self).setUp()
        self.chrome_os_device_json = json.loads(self.loadFileContents('tests/chrome_os_device.json'))
        self.gcm_id = 'd23784972038845ab3948459'

    def testDeviceEnrollmentGet_ReturnsOKStatus(self):
        request_parameters = {'mac_address': self.chrome_os_device_json.get('macAddress'), 'gcm_id': self.gcm_id}
        with patch('chrome_os_devices_api.ChromeOsDevicesApi') as chrome_os_devices_api_mock:
            mock_instance = chrome_os_devices_api_mock.return_value
            mock_instance.list.return_value = self.loadFileContents('tests/chrome_os_devices_api_list.json')
            uri = application.router.build(None, 'devices', None, {})
            response = self.app.get(uri, params=request_parameters)
            self.assertOK(response)

    def testDeviceEnrollmentGet_ReturnsChromeOsResourceRepresentation(self):
        request_parameters = {'mac_address': self.chrome_os_device_json.get('macAddress'), 'gcm_id': self.gcm_id}
        with patch('chrome_os_devices_api.ChromeOsDevicesApi') as chrome_os_devices_api_mock:
            mock_instance = chrome_os_devices_api_mock.return_value
            mock_instance.list.return_value = self.loadFileContents('tests/chrome_os_devices_api_list.json')
            uri = application.router.build(None, 'devices', None, {})
            response = self.app.get(uri, params=request_parameters)
            body = json.loads(response.body)
            self.assertEquals(self.chrome_os_device_json.get('macAddress'), body.get('macAddress'))
            self.assertEquals(self.chrome_os_device_json.get('activeTimeRanges'), body.get('activeTimeRanges'))
            self.assertEquals(self.chrome_os_device_json.get('annotatedLocation'), body.get('annotatedLocation'))
            self.assertEquals(self.chrome_os_device_json.get('annotatedUser'), body.get('annotatedUser'))
            self.assertEquals(self.chrome_os_device_json.get('bootMode'), body.get('bootMode'))
            self.assertEquals(self.chrome_os_device_json.get('deviceId'), body.get('deviceId'))
            self.assertEquals(self.chrome_os_device_json.get('etag'), body.get('etag'))
            self.assertEquals(self.chrome_os_device_json.get('firmwareVersion'), body.get('firmwareVersion'))
            self.assertEquals(self.chrome_os_device_json.get('kind'), body.get('kind'))
            self.assertEquals(self.chrome_os_device_json.get('lastEnrollmentTime'), body.get('lastEnrollmentTime'))
            self.assertEquals(self.chrome_os_device_json.get('lastSync'), body.get('lastSync'))
            self.assertEquals(self.chrome_os_device_json.get('model'), body.get('model'))
            self.assertEquals(self.chrome_os_device_json.get('notes'), body.get('notes'))
            self.assertEquals(self.chrome_os_device_json.get('orgUnitPath'), body.get('orgUnitPath'))
            self.assertEquals(self.chrome_os_device_json.get('osVersion'), body.get('osVersion'))
            self.assertEquals(self.chrome_os_device_json.get('platformVersion'), body.get('platformVersion'))
            self.assertEquals(self.chrome_os_device_json.get('serialNumber'), body.get('serialNumber'))
            self.assertEquals(self.chrome_os_device_json.get('status'), body.get('status'))

    def testDeviceEnrollmentPut_ReturnsNoContent(self):
        chrome_os_device = ChromeOsDevice(device_id=self.chrome_os_device_json.get('deviceId'),
                                          gcm_registration_id='d23784972038845ab3963412')
        chrome_os_device.put()
        request_body = {'gcmRegistrationId': self.gcm_id}
        with patch('chrome_os_devices_api.ChromeOsDevicesApi') as chrome_os_devices_api_mock:
            mock_instance = chrome_os_devices_api_mock.return_value
            mock_instance.get_by_device_id.return_value = self.loadFileContents('tests/chrome_os_device.json')
            response = self.app.put('/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId')),
                                    json.dumps(request_body))
            self.assertEqual('204 No Content', response.status)

    def testDeviceEnrollmentPut_UpdatesGcmRegistrationId(self):
        chrome_os_device = ChromeOsDevice(device_id=self.chrome_os_device_json.get('deviceId'),
                                          gcm_registration_id='d23784972038845ab3963412')
        key = chrome_os_device.put()
        request_body = {'gcmRegistrationId': self.gcm_id}
        with patch('chrome_os_devices_api.ChromeOsDevicesApi') as chrome_os_devices_api_mock:
            mock_instance = chrome_os_devices_api_mock.return_value
            mock_instance.get_by_device_id.return_value = self.loadFileContents('tests/chrome_os_device.json')
            self.app.put('/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId')),
                         json.dumps(request_body))
            actual = key.get()
            self.assertEqual(self.gcm_id, actual.gcm_registration_id)

    def testDeviceEnrollmentPut_CreatesChromeOsDeviceUpdatesGcmRegistrationId(self):
        request_body = {'gcmRegistrationId': self.gcm_id}
        with patch('chrome_os_devices_api.ChromeOsDevicesApi') as chrome_os_devices_api_mock:
            mock_instance = chrome_os_devices_api_mock.return_value
            mock_instance.get_by_device_id.return_value = self.loadFileContents('tests/chrome_os_device.json')
            self.app.put('/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId')),
                         json.dumps(request_body))
            actual = ChromeOsDevice.get_by_device_id(self.chrome_os_device_json.get('deviceId'))
            self.assertIsNotNone(actual)
            self.assertEqual(self.gcm_id, actual.gcm_registration_id)

    def loadFileContents(self, file_name):
        with open(file_name, 'r') as json_file:
            data = json_file.read().replace('\n', '')
        return data