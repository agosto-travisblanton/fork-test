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

    def test_get_returns_json_version_name(self):
        uri = application.router.build(None, 'version-retrieval', None, {})
        response = self.get(uri)
        response_json = json.loads(response.body)
        self.assertEqual(response_json['web_module_name'], 'testbed-version')
