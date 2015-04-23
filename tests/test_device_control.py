from agar.test import BaseTest, WebTest
from routes import application


class TestDeviceCommandsHandler(BaseTest, WebTest):
    APPLICATION = application

    def setUp(self):
        super(TestDeviceCommandsHandler, self).setUp()
        self.device_id = '132e235a-b346-4a37-a100-de49fa753a2a'

    def tearDown(self):
        pass

    def testGet_ReturnsOKStatus(self):
        request_parameters = {}
        # uri = application.router.build(None, 'device-commands', None, {})
        uri = '/api/v1/devices/{0}/commands'.format(self.device_id)
        response = self.app.get(uri, params=request_parameters)
        self.assertOK(response)

    def testPost_ReturnsOKStatus(self):
        request_parameters = {}
        # uri = application.router.build(None, 'device-commands', None, {})
        uri = '/api/v1/devices/{0}/commands'.format(self.device_id)
        response = self.app.post(uri, params=request_parameters)
        self.assertOK(response)

    def testPut_ReturnsOKStatus(self):
        request_parameters = {}
        # uri = application.router.build(None, 'device-commands', None, {})
        uri = '/api/v1/devices/{0}/commands'.format(self.device_id)
        response = self.app.put(uri, params=request_parameters)
        self.assertOK(response)

    def testDelete_ReturnsOKStatus(self):
        request_parameters = {}
        # uri = application.router.build(None, 'device-commands', None, {})
        uri = '/api/v1/devices/{0}/commands'.format(self.device_id)
        response = self.app.delete(uri, params=request_parameters)
        self.assertOK(response)


