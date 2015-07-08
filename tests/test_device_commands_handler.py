from env_setup import setup_test_paths

setup_test_paths()

import json
from agar.test import BaseTest, WebTest
from app_config import config
from models import ChromeOsDevice, Tenant
from routes import application
import device_commands_processor
from mockito import when, any as any_matcher


class TestDeviceCommandsHandler(BaseTest, WebTest):
    APPLICATION = application

    NAME = 'foobar tenant'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://www.content.com'
    CONTENT_SERVER_API_KEY = 'API KEY'
    CHROME_DEVICE_DOMAIN = 'bar.com'
    TENANT_CODE = 'foobar'

    def setUp(self):
        super(TestDeviceCommandsHandler, self).setUp()
        self.headers = {
            'Authorization': config.API_TOKEN
        }
        self.tenant = Tenant.create(name=self.NAME,
                                    tenant_code=self.TENANT_CODE,
                                    admin_email=self.ADMIN_EMAIL,
                                    content_server_url=self.CONTENT_SERVER_URL,
                                    chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                                    active=True)
        self.tenant_key = self.tenant.put()

    def test_post_known_command_returns_ok_status(self):
        device = ChromeOsDevice.create(tenant_key=self.tenant_key,
                                       device_id='f7ds8970dfasd8f70ad987',
                                       gcm_registration_id='fad7f890ad7f8ad0s7fa8sd7fa809sd7fas89d7f0sa98df7as89d7fs8f',
                                       mac_address='54271e619346')
        device_key = device.put()
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
        self.assertTrue('Bad response: 404 Unable to find ChromeOS device by key' in str(context.exception))
