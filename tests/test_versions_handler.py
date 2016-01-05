from env_setup import setup_test_paths

setup_test_paths()

import json
from agar.test import BaseTest, WebTest
from routes import application


class TestVersionsHandler(BaseTest, WebTest):
    APPLICATION = application

    def setUp(self):
        super(TestVersionsHandler, self).setUp()

    def test_get_returns_ok_status(self):
        uri = application.router.build(None, 'version-retrieval', None, {})
        response = self.get(uri)
        self.assertOK(response)

    def test_get_returns_web_version_name_json(self):
        uri = application.router.build(None, 'version-retrieval', None, {})
        response = self.get(uri)
        response_json = json.loads(response.body)
        self.assertEqual(response_json['web_version_name'], 'testbed-version')

    def test_get_returns_web_module_name_json(self):
        uri = application.router.build(None, 'version-retrieval', None, {})
        response = self.get(uri)
        response_json = json.loads(response.body)
        self.assertEqual(response_json['web_module_name'], 'default')

    def test_get_returns_current_instance_id_json(self):
        uri = application.router.build(None, 'version-retrieval', None, {})
        response = self.get(uri)
        response_json = json.loads(response.body)
        self.assertIsNone(response_json['current_instance_id'])

    def test_get_returns_default_version_json(self):
        uri = application.router.build(None, 'version-retrieval', None, {})
        response = self.get(uri)
        response_json = json.loads(response.body)
        self.assertEqual(response_json['default_version'], '1')

    def test_get_returns_hostname_json(self):
        uri = application.router.build(None, 'version-retrieval', None, {})
        response = self.get(uri)
        response_json = json.loads(response.body)
        self.assertEqual(response_json['hostname'], 'localhost:8080')
