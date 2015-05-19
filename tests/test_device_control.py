from agar.test import BaseTest, WebTest
from mock import patch
from models import ChromeOsDevice
from routes import application


class TestDeviceCommandsHandler(BaseTest, WebTest):
    APPLICATION = application

    def setUp(self):
        super(TestDeviceCommandsHandler, self).setUp()
        self.device_id = '132e235a-b346-4a37-a100-de49fa753a2a'
        self.chrome_os_device = ChromeOsDevice(device_id=self.device_id,
                                               gcm_registration_id='d23784972038845ab3963412')
        self.chrome_os_device.put()

    def test_post_known_command_returns_ok_status(self):
        request_parameters = {'command': 'change_channel',
                              'payload': {'channel': {'name': 'Quality On Demand','program': 'Program 1'}}}
        uri = application.router.build(None, 'device-commands', None, {'device_id': self.device_id})
        response = self.app.post_json(uri, params=request_parameters)
        self.assertOK(response)

    def test_post_unknown_command_returns_forbidden_status(self):
        request_parameters = {'command': 'unknown',
                              'payload': {}}
        uri = application.router.build(None, 'device-commands', None, {'device_id': self.device_id})
        response = self.app.post_json(uri, params=request_parameters, expect_errors=True)
        self.assertForbidden(response)
        with self.assertRaises(Exception) as context:
            self.app.post_json(uri, params=request_parameters)
        self.assertTrue('Bad response: 403 forbidden command' in str(context.exception))

    def test_post_invokes_processor_method(self):
        payload = {'channel': {'name': 'Quality On Demand','program': 'Program 1'}}
        request_parameters = {'command': 'change_channel', 'payload': payload}
        uri = application.router.build(None, 'device-commands', None, {'device_id': self.device_id})
        with patch('device_commands_processor.change_channel', return_value=None) as mock_command:
            self.app.post_json(uri, params=request_parameters)
        mock_command.assert_called_once_with(self.chrome_os_device.gcm_registration_id, payload)
