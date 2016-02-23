from env_setup import setup_test_paths

setup_test_paths()

import json
from agar.test import BaseTest, WebTest
from models import Distributor
from routes import application
from app_config import config


class TestTimezonesHandler(BaseTest, WebTest):
    APPLICATION = application
    ADMIN_EMAIL = "foo{0}@bar.com"
    API_KEY = "SOME_KEY_{0}"
    CONTENT_SERVER_URL = 'https://skykit-contentmanager-int.appspot.com/content'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    DISTRIBUTOR_NAME = 'agosto'
    IMPERSONATION_EMAIL = 'test@test.com'
    ORIGINAL_NOTIFICATION_EMAILS = ['test@skykit.com', 'admin@skykit.com']

    def setUp(self):
        super(TestTimezonesHandler, self).setUp()
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
                                              active=True)
        self.distributor_key = self.distributor.put()
        self.headers = {
            'Authorization': config.API_TOKEN,
            'X-Provisioning-Distributor': self.distributor_key.urlsafe()
        }

    ##################################################################################################################
    ## get
    ##################################################################################################################

    def test_get_returns_ok(self):
        request_parameters = {}
        uri = application.router.build(None, 'timezones-list', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        self.assertOK(response)

    def test_get_returns_expected_list_of_timezones(self):
        request_parameters = {}
        uri = application.router.build(None, 'timezones-list', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), 30)
        self.assertEqual(response_json[0], 'America/New_York')
        self.assertEqual(response_json[10], 'America/Chicago')
        self.assertEqual(response_json[17], 'America/Denver')
        self.assertEqual(response_json[21], 'America/Los_Angeles')
