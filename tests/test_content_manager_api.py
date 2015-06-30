from env_setup import setup_test_paths

setup_test_paths()

import json
from http_client import HttpClient, HttpClientRequest, HttpClientResponse
from models import Tenant, ChromeOsDevice
from agar.test import BaseTest
from content_manager_api import ContentManagerApi

from mockito import when, any as any_matcher

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>, Christopher Bartling <chris.bartling@agosto.com>'


class TestContentManagerApi(BaseTest):
    NAME = 'foobar tenant'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://www.content.com'
    CONTENT_SERVER_API_KEY = 'API KEY'
    CHROME_DEVICE_DOMAIN = 'bar.com'
    TENANT_CODE = 'foobar'

    def setUp(self):
        super(TestContentManagerApi, self).setUp()
        self.content_manager_api = ContentManagerApi()
        self.tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                               name=self.NAME,
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               content_server_api_key=self.CONTENT_SERVER_API_KEY,
                               chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                               active=True)
        self.tenant_key = self.tenant.put()
        self.device = ChromeOsDevice.create(tenant_key=self.tenant_key,
                                       device_id='f7ds8970dfasd8f70ad987',
                                       gcm_registration_id='fad7f890ad7f8ad0s7fa8sd7fa809sd7fas89d7f0sa98df7as89d7fs8f')
        self.device_key = self.device.put()


    def test_create_tenant_returns_tenant_key_when_status_code_created(self):
        json_response = {'tenant_key': 'some key'}
        when(HttpClient). \
            post(any_matcher(HttpClientRequest)). \
            thenReturn(HttpClientResponse(status_code=201,
                                          content=json.dumps(json_response)))
        tenant_key = self.content_manager_api.create_tenant(self.tenant)
        self.assertIsNotNone(tenant_key)

    def test_create_tenant_returns_none_when_status_code_unprocessable_entity(self):
        json_response = {'tenant_key': 'some key'}
        when(HttpClient). \
            post(any_matcher(HttpClientRequest)). \
            thenReturn(HttpClientResponse(status_code=422,
                                          content=json.dumps(json_response)))
        tenant_key = self.content_manager_api.create_tenant(self.tenant)
        self.assertIsNone(tenant_key)

    def test_create_tenant_returns_none_when_status_code_bad_request(self):
        when(HttpClient).post(any_matcher(HttpClientRequest)).thenReturn(HttpClientResponse(status_code=400))
        tenant_key = self.content_manager_api.create_tenant(self.tenant)
        self.assertIsNone(tenant_key)

    def test_create_tenant_throws_error_when_cannot_create_tenant_in_content_manager(self):
        when(HttpClient).post(any_matcher(HttpClientRequest)).thenReturn(HttpClientResponse(status_code=0))
        with self.assertRaises(Exception) as context:
            self.content_manager_api.create_tenant(self.tenant)
        self.assertTrue('Unable to create tenant in Content Manager. Unexpected http status code: 0'
                        in str(context.exception))

    def test_create_device_success(self):
        when(HttpClient).post(any_matcher(HttpClientRequest)).thenReturn(HttpClientResponse(status_code=201))
        result = self.content_manager_api.create_device(self.device)
        self.assertIsNone(result)

    def test_create_device_raises_error(self):
        when(HttpClient).post(any_matcher(HttpClientRequest)).thenReturn(HttpClientResponse(status_code=422))
        with self.assertRaises(RuntimeError) as context:
            self.content_manager_api.create_device(self.device)
        self.assertTrue(
            'Unable to create device in Content Manager. Unexpected http status code: 422' in str(context.exception))
