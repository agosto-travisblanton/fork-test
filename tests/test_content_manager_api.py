from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
import requests
from content_manager_api import ContentManagerApi

from mockito import when, any as any_matcher

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestContentManagerApi(BaseTest):
    def setUp(self):
        super(TestContentManagerApi, self).setUp()
        self.content_manager_api = ContentManagerApi()
        self.name = u'ABC'
        self.admin_email = u'foo@bar.com'

    def test_create_tenant_returns_tenant_key_when_status_code_created(self):
        json_response = {'tenant_key': 'some key'}
        response = requests.Response()
        response.status_code = 201
        when(response).json().thenReturn(json_response)
        when(requests).post(ContentManagerApi.CONTENT_MANAGER_API_URL,
                            any_matcher(),
                            timeout=60,
                            headers=ContentManagerApi.HEADERS).thenReturn(response)
        tenant_key = self.content_manager_api.create_tenant(self.name, self.admin_email)
        self.assertIsNotNone(tenant_key)

    def test_create_tenant_returns_none_when_status_code_unprocessable_entity(self):
        json_response = {'tenant_key': 'some key'}
        response = requests.Response()
        response.status_code = 422
        when(response).json().thenReturn(json_response)
        when(requests).post(ContentManagerApi.CONTENT_MANAGER_API_URL,
                            any_matcher(),
                            timeout=60,
                            headers=ContentManagerApi.HEADERS).thenReturn(response)
        tenant_key = self.content_manager_api.create_tenant(self.name, self.admin_email)
        self.assertIsNone(tenant_key)

    def test_create_tenant_returns_none_when_status_code_bad_request(self):
        json_response = {'tenant_key': 'some key'}
        response = requests.Response()
        response.status_code = 400
        when(response).json().thenReturn(json_response)
        when(requests).post(ContentManagerApi.CONTENT_MANAGER_API_URL,
                            any_matcher(),
                            timeout=60,
                            headers=ContentManagerApi.HEADERS).thenReturn(response)
        tenant_key = self.content_manager_api.create_tenant(self.name, self.admin_email)
        self.assertIsNone(tenant_key)

    def test_create_tenant_throws_error_when_cannot_create_tenant_in_content_manager(self):
        json_response = {'tenant_key': 'some key'}
        response = requests.Response()
        response.status_code = 0
        when(response).json().thenReturn(json_response)
        when(requests).post(ContentManagerApi.CONTENT_MANAGER_API_URL,
                            any_matcher(),
                            timeout=60,
                            headers=ContentManagerApi.HEADERS).thenReturn(response)
        with self.assertRaises(Exception) as context:
            self.content_manager_api.create_tenant(self.name, self.admin_email)
        self.assertTrue('Unable to create tenant in Content Manager. Unexpected http status code: 0'
                        in str(context.exception))
