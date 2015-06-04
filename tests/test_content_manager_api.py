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

    def test_create_tenant(self):
        name = u'ABC'
        admin_email = u'foo@bar.com'

        json_response = {'tenant_key': 'adfklajsdkfja;sdlkj0'}
        response = requests.Response()
        response.status_code = 200
        when(response).json().thenReturn(json_response)
        when(requests).post(ContentManagerApi.CONTENT_MANAGER_API_URL,
                            any_matcher(),
                            timeout=60,
                            headers=ContentManagerApi.HEADERS).thenReturn(response)
        key = self.content_manager_api.create_tenant(name, admin_email)
        self.assertIsNotNone(key)
