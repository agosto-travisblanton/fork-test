from agar.test import BaseTest, WebTest
from routes import application
from utils.web_util import build_uri


class VersionHandlerTest(BaseTest, WebTest):
    APPLICATION = application

    def test_get(self):
        uri = build_uri('versions')
        response = self.get(uri)
        self.assertOK(response)

        versions = response.json

        # the test only returns a version for default
        self.assertLength(1, versions)
        self.assertEqual(1, int(versions.get('default')))
