from env_setup import setup_test_paths
from utils.web_util import build_uri

setup_test_paths()

import json
from agar.test import BaseTest, WebTest
from routes import application


class TestVersionHandler(BaseTest, WebTest):
    APPLICATION = application

    def setUp(self):
        super(TestVersionHandler, self).setUp()

    def test_get_returns_ok_status(self):
        uri = build_uri('version-retrieval')
        response = self.get(uri)
        self.assertOK(response)

    def test_get_returns_json_version(self):
        uri = build_uri('version-retrieval')
        response = self.get(uri)
        response_json = json.loads(response.body)
        self.assertIsInstance(int(response_json['version']), int)

    def test_get_returns_json_tag(self):
        uri = build_uri('version-retrieval')
        response = self.get(uri)
        response_json = json.loads(response.body)
        self.assertEqual(10, len(response_json['tag']))
