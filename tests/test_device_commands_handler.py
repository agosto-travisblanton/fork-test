from agar.test import BaseTest, WebTest
from app_config import config
from models import ChromeOsDevice
from routes import application
from mockito import when, any as any_matcher


class TestDeviceCommandsHandler(BaseTest, WebTest):
    APPLICATION = application

    def setUp(self):
        super(TestDeviceCommandsHandler, self).setUp()
        self.chrome_os_device = ChromeOsDevice(device_id='132e235a-b346-4a37-a100-de49fa753a2a',
                                               gcm_registration_id='d23784972038845ab3963412',
                                               tenant_code='Acme')
        self.device_key = self.chrome_os_device.put()
        self.headers = {
            'Authorization': config.API_TOKEN
        }

    def test_post_known_command_returns_ok_status(self):
        request_parameters = {'intent': 'https://www.content-manager/something'}
        uri = application.router.build(None,
                                       'device-commands',
                                       None,
                                       {'device_urlsafe_key': self.device_key.urlsafe()})
        response = self.app.post_json(uri, params=request_parameters, headers=self.headers)
        self.assertOK(response)

    def test_post_unknown_device_returns_unprocessable_entity_status(self):
        request_parameters = {'intent': 'https://www.content-manager/something'}
        uri = application.router.build(None,
                                       'device-commands',
                                       None,
                                       {'device_urlsafe_key': 'bogus key'})
        with self.assertRaises(Exception) as context:
            self.app.post_json(uri, params=request_parameters, headers=self.headers)
        self.assertTrue('Bad response: 422 Unable to find ChromeOS device by key' in str(context.exception))
