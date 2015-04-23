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
        self.patched_chrome_os_devices_api = patch('chrome_os_devices_api.ChromeOsDevicesApi')
        self.chrome_os_devices_api_mock = self.patched_chrome_os_devices_api.start()
        self.chrome_os_devices_api_mock_instance = self.chrome_os_devices_api_mock.return_value

    def tearDown(self):
        if self.chrome_os_devices_api_mock_instance is not None:
            self.chrome_os_devices_api_mock_instance.reset_mock()
        if self.patched_chrome_os_devices_api is not None:
            self.patched_chrome_os_devices_api.stop()

    # def testDeviceEnrollmentGet_ReturnsOKStatus(self):
    #     request_parameters = {'mac_address': self.chrome_os_device_json.get('macAddress'), 'gcm_id': self.gcm_id}
    #     self.chrome_os_devices_api_mock_instance.list.return_value = self.loadFileContents(
    #         'tests/chrome_os_devices_api_list.json')
    #     uri = application.router.build(None, 'devices', None, {})
    #     response = self.app.get(uri, params=request_parameters)
    #     self.assertOK(response)

    # def testDeviceEnrollmentGet_ReturnsChromeOsResourceRepresentation(self):
    #     request_parameters = {'mac_address': self.chrome_os_device_json.get('macAddress'), 'gcm_id': self.gcm_id}
    #     self.chrome_os_devices_api_mock_instance.list.return_value = self.loadFileContents(
    #         'tests/chrome_os_devices_api_list.json')
    #     uri = application.router.build(None, 'devices', None, {})
    #     response = self.app.get(uri, params=request_parameters)
    #     body = json.loads(response.body)
    #     self.assertEquals(self.chrome_os_device_json.get('macAddress'), body.get('macAddress'))
    #     self.assertEquals(self.chrome_os_device_json.get('activeTimeRanges'), body.get('activeTimeRanges'))
    #     self.assertEquals(self.chrome_os_device_json.get('annotatedLocation'), body.get('annotatedLocation'))
    #     self.assertEquals(self.chrome_os_device_json.get('annotatedUser'), body.get('annotatedUser'))
    #     self.assertEquals(self.chrome_os_device_json.get('bootMode'), body.get('bootMode'))
    #     self.assertEquals(self.chrome_os_device_json.get('deviceId'), body.get('deviceId'))
    #     self.assertEquals(self.chrome_os_device_json.get('etag'), body.get('etag'))
    #     self.assertEquals(self.chrome_os_device_json.get('firmwareVersion'), body.get('firmwareVersion'))
    #     self.assertEquals(self.chrome_os_device_json.get('kind'), body.get('kind'))
    #     self.assertEquals(self.chrome_os_device_json.get('lastEnrollmentTime'), body.get('lastEnrollmentTime'))
    #     self.assertEquals(self.chrome_os_device_json.get('lastSync'), body.get('lastSync'))
    #     self.assertEquals(self.chrome_os_device_json.get('model'), body.get('model'))
    #     self.assertEquals(self.chrome_os_device_json.get('notes'), body.get('notes'))
    #     self.assertEquals(self.chrome_os_device_json.get('orgUnitPath'), body.get('orgUnitPath'))
    #     self.assertEquals(self.chrome_os_device_json.get('osVersion'), body.get('osVersion'))
    #     self.assertEquals(self.chrome_os_device_json.get('platformVersion'), body.get('platformVersion'))
    #     self.assertEquals(self.chrome_os_device_json.get('serialNumber'), body.get('serialNumber'))
    #     self.assertEquals(self.chrome_os_device_json.get('status'), body.get('status'))

    def testDeviceEnrollmentPut_ReturnsNoContent(self):
        chrome_os_device = ChromeOsDevice(device_id=self.chrome_os_device_json.get('deviceId'),
                                          gcm_registration_id='d23784972038845ab3963412')
        chrome_os_device.put()
        request_body = {'gcmRegistrationId': self.gcm_id}
        self.chrome_os_devices_api_mock_instance.get.return_value = self.loadFileContents('tests/chrome_os_device.json')
        response = self.app.put('/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId')),
                                json.dumps(request_body))
        self.assertEqual('204 No Content', response.status)

    # def testDeviceEnrollmentPut_ReturnsUnprocessibleEntity(self):
    # chrome_os_device = ChromeOsDevice(device_id=self.chrome_os_device_json.get('deviceId'),
    #                                       gcm_registration_id='d23784972038845ab3963412')
    #     chrome_os_device.put()
    #     request_body = {'gcmRegistrationId': self.gcm_id}
    #     self.chrome_os_devices_api_mock_instance.get.return_value = None
    #     with self.assertRaises(AppError):
    #         self.app.put('/api/v1/devices/3278273', json.dumps(request_body))

    def testDeviceEnrollmentPut_UpdatesGcmRegistrationId(self):
        chrome_os_device = ChromeOsDevice(device_id=self.chrome_os_device_json.get('deviceId'),
                                          gcm_registration_id='d23784972038845ab3963412')
        key = chrome_os_device.put()
        request_body = {'gcmRegistrationId': self.gcm_id}
        self.chrome_os_devices_api_mock_instance.get.return_value = self.loadFileContents('tests/chrome_os_device.json')
        url = '/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId'))
        self.app.put(url, json.dumps(request_body))
        actual = key.get()
        self.assertEqual(self.gcm_id, actual.gcm_registration_id)

    def testDeviceEnrollmentPut_CreatesChromeOsDeviceUpdatesGcmRegistrationId(self):
        request_body = {'gcmRegistrationId': self.gcm_id}
        self.chrome_os_devices_api_mock_instance.get.return_value = self.loadFileContents('tests/chrome_os_device.json')
        url = '/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId'))
        self.app.put(url, json.dumps(request_body))
        actual = ChromeOsDevice.get_by_device_id(self.chrome_os_device_json.get('deviceId'))
        self.assertIsNotNone(actual)
        self.assertEqual(self.gcm_id, actual.gcm_registration_id)

    def testDeviceEnrollmentDelete_ReturnsNoContent(self):
        chrome_os_device = ChromeOsDevice(device_id=self.chrome_os_device_json.get('deviceId'),
                                          gcm_registration_id='d23784972038845ab3963412')
        chrome_os_device.put()
        self.chrome_os_devices_api_mock_instance.get.return_value = self.loadFileContents('tests/chrome_os_device.json')
        url = '/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId'))
        response = self.app.delete(url)
        self.assertEqual('204 No Content', response.status)
        # actual = ChromeOsDevice.get_by_device_id(self.chrome_os_device_json.get('deviceId'))
        # self.assertIsNone(actual)

    def testDeviceEnrollmentDelete_RemovesChromeOsDeviceEntity(self):
        chrome_os_device = ChromeOsDevice(device_id=self.chrome_os_device_json.get('deviceId'),
                                          gcm_registration_id='d23784972038845ab3963412')
        chrome_os_device.put()
        self.chrome_os_devices_api_mock_instance.get.return_value = self.loadFileContents('tests/chrome_os_device.json')
        url = '/api/v1/devices/{0}'.format(self.chrome_os_device_json.get('deviceId'))
        self.app.delete(url)
        actual = ChromeOsDevice.get_by_device_id(self.chrome_os_device_json.get('deviceId'))
        self.assertIsNone(actual)

    def loadFileContents(self, file_name):
        with open(file_name, 'r') as json_file:
            data = json_file.read().replace('\n', '')
        return data