import json

from agar.test import BaseTest, WebTest
from app_config import config
from models import ChromeOsDevice
from routes import application
import device_commands_processor
from mockito import when, any as any_matcher


class TestDeviceCommandsHandler(BaseTest, WebTest):
    APPLICATION = application

    def setUp(self):
        super(TestDeviceCommandsHandler, self).setUp()
        self.headers = {
            'Authorization': config.API_TOKEN
        }

    def test_post_known_command_returns_ok_status(self):
        chrome_os_device = ChromeOsDevice(device_id='132e235a-b346-4a37-a100-de49fa753a2a',
                                          gcm_registration_id='d23784972038845ab3963412',
                                          tenant_code='Acme')
        device_key = chrome_os_device.put()
        request_body = {'intent': 'https://www.content-manager/something'}
        uri = application.router.build(None,
                                       'device-commands',
                                       None,
                                       {'device_urlsafe_key': device_key.urlsafe()})
        when(device_commands_processor).change_intent(any_matcher(str), any_matcher(str)).thenReturn(None)
        response = self.app.post(uri, json.dumps(request_body), headers=self.headers)
        self.assertOK(response)

    def test_post_unknown_device_returns_unprocessable_entity_status(self):
        request_body = {'intent': 'https://www.content-manager/something'}
        uri = application.router.build(None,
                                       'device-commands',
                                       None,
                                       {'device_urlsafe_key': 'bogus key'})
        with self.assertRaises(Exception) as context:
            self.app.post(uri, json.dumps(request_body), headers=self.headers)
        self.assertTrue('Bad response: 422 Unable to find ChromeOS device by key' in str(context.exception))
