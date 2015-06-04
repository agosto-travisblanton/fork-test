__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'

from content_manager_api import ContentManagerApi
from env_setup import setup_test_paths;

setup_test_paths()

import json

from agar.test import BaseTest, WebTest

from models import Tenant, TenantEntityGroup
from routes import application
import requests

from mockito import when, verify, any as any_matcher



class TestContentManagerApi(BaseTest):

    def setUp(self):
        super(TestContentManagerApi, self).setUp()
        self.content_manager_api = ContentManagerApi()

    def test_create_tenant(self):
        name = u'ABC'
        admin_email = u'foo@bar.com'

        json_response = {"success": True,  "payload": {}}
        when(requests).post(any_matcher(str), any_matcher(str), any_matcher(),any_matcher()).thenReturn(json_response)
        key = self.content_manager_api.create_tenant(name, admin_email)
        self.assertIsNotNone(key)


