from env_setup import setup_test_paths

setup_test_paths()

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
                                    chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                                    active=True)
        self.tenant_key = self.tenant.put()
        self.device = ChromeOsDevice.create(tenant_key=self.tenant_key,
                                            device_id='f7ds8970dfasd8f70ad987',
                                            gcm_registration_id='fad7f890ad7f8ad0s7fa8s',
                                            mac_address='54271e619346')
        self.device_key = self.device.put()

    def test_create_tenant_success(self):
        when(HttpClient).post(any_matcher(HttpClientRequest)).thenReturn(HttpClientResponse(status_code=201))
        result = self.content_manager_api.create_tenant(self.tenant)
        self.assertTrue(result)

    def test_unsuccessful_create_tenant_raises_error(self):
        error_code = 400
        when(HttpClient).post(any_matcher(HttpClientRequest)).thenReturn(HttpClientResponse(status_code=error_code))
        with self.assertRaises(RuntimeError) as context:
            self.content_manager_api.create_tenant(self.tenant)
        error_message = 'Unable to create tenant {0} in Content Manager. Status code: {1}'.format(
            self.NAME, error_code)
        self.assertEqual(error_message, str(context.exception))

    def test_create_device_success(self):
        when(HttpClient).post(any_matcher(HttpClientRequest)).thenReturn(HttpClientResponse(status_code=201))
        result = self.content_manager_api.create_device(self.device)
        self.assertTrue(result)

    def test_unsuccessful_create_device_raises_error(self):
        error_code = 400
        when(HttpClient).post(any_matcher(HttpClientRequest)).thenReturn(HttpClientResponse(status_code=error_code))
        with self.assertRaises(RuntimeError) as context:
            self.content_manager_api.create_device(self.device)
        error_message = 'Unable to create device in Content Manager with tenant code {0}. Status code: {1}'.format(
            self.TENANT_CODE, error_code)
        self.assertEqual(error_message, str(context.exception))
