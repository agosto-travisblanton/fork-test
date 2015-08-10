from env_setup import setup_test_paths

setup_test_paths()

import json
from webtest import AppError
from agar.test import BaseTest, WebTest
from app_config import config
from models import Display, Tenant
from routes import application
import device_commands_processor
from mockito import when, any as any_matcher


class TestDisplayCommandsHandler(BaseTest, WebTest):
    APPLICATION = application
    NAME = 'foobar tenant'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://www.content.com'
    CHROME_DEVICE_DOMAIN = 'bar.com'
    TENANT_CODE = 'foobar'
    DEVICE_ID = '4f099e50-6028-422b-85d2-3a629a45bf38'
    GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
    MAC_ADDRESS = '54271e619346'

    def setUp(self):
        super(TestDisplayCommandsHandler, self).setUp()
        self.tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                                    name=self.NAME,
                                    admin_email=self.ADMIN_EMAIL,
                                    content_server_url=self.CONTENT_SERVER_URL,
                                    chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                                    active=True)
        self.tenant_key = self.tenant.put()
        self.display = Display.create(tenant_key=self.tenant_key,
                                      device_id=self.DEVICE_ID,
                                      gcm_registration_id=self.GCM_REGISTRATION_ID,
                                      mac_address=self.MAC_ADDRESS)
        self.display_key = self.display.put()
        self.valid_authorization_header = {
            'Authorization': config.API_TOKEN
        }
        self.bad_authorization_header = {}
        self.some_intent = 'https://skykit-display-int.appspot.com/40289e504f09422c85d23a629a45be3d'
        self.post_uri = application.router.build(None,
                                                 'display-commands',
                                                 None,
                                                 {'display_urlsafe_key': self.display_key.urlsafe()})

    def test_post_intent_returns_ok_status(self):
        request_body = {'intent': self.some_intent}
        when(device_commands_processor).change_intent(any_matcher(str), any_matcher(str)).thenReturn(None)
        response = self.app.post(self.post_uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_post_no_authorization_header_returns_forbidden(self):
        request_body = {'intent': self.some_intent}
        with self.assertRaises(AppError) as context:
            self.app.post(self.post_uri, json.dumps(request_body), headers=self.bad_authorization_header)
        self.assertTrue('403 Forbidden' in context.exception.message)

    def test_post_none_intent_returns_bad_request(self):
        request_body = {}
        with self.assertRaises(AppError) as context:
            self.app.post(self.post_uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertTrue('400 Invalid intent' in context.exception.message)

    def test_post_empty_string_intent_returns_bad_request(self):
        request_body = {'intent': ''}
        with self.assertRaises(AppError) as context:
            self.app.post(self.post_uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertTrue('400 Invalid intent' in context.exception.message)

    def test_post_wrong_payload_returns_bad_request(self):
        request_body = {'wrong_intent': self.some_intent}
        with self.assertRaises(AppError) as context:
            self.app.post(self.post_uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertTrue('400 Invalid intent' in context.exception.message)

    def test_post_bogus_key_returns_not_found(self):
        request_body = {'intent': self.some_intent}
        bogus_key = 'bogus key'
        uri = application.router.build(None,
                                       'display-commands',
                                       None,
                                       {'display_urlsafe_key': bogus_key})
        with self.assertRaises(AppError) as context:
            self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertTrue("404 Display not found with key: {0}".format(bogus_key) in context.exception.message)
