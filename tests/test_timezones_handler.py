from env_setup import setup_test_paths
from webtest import AppError

setup_test_paths()

import json
from agar.test import BaseTest, WebTest
from models import Distributor
from routes import application
from app_config import config
from provisioning_distributor_user_base_test import ProvisioningDistributorUserBase


class TestTimezonesHandler(ProvisioningDistributorUserBase):
    APPLICATION = application
    DISTRIBUTOR_NAME = 'agosto'
    FORBIDDEN = '403 Forbidden'

    def setUp(self):
        super(TestTimezonesHandler, self).setUp()
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
                                              active=True)
        self.distributor_key = self.distributor.put()
        self.headers = self.JWT_DEFAULT_HEADER


        self.bad_authorization_header = {
            'Authorization': 'Forget about it!',
            'X-Provisioning-Distributor': self.distributor_key.urlsafe()
        }


    ##################################################################################################################
    # get
    ##################################################################################################################

    def test_get_us_timezones_returns_ok(self):
        request_parameters = {}
        uri = application.router.build(None, 'us-timezones', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        self.assertOK(response)

    def test_get_us_timezones_returns_expected_list_of_timezones(self):
        request_parameters = {}
        uri = application.router.build(None, 'us-timezones', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), 30)
        self.assertEqual(response_json[0], 'America/New_York')
        self.assertEqual(response_json[10], 'America/Chicago')
        self.assertEqual(response_json[17], 'America/Denver')
        self.assertEqual(response_json[21], 'America/Los_Angeles')

    def test_get_us_timezones_fails_with_bad_authorization_token(self):
        request_parameters = {}
        uri = application.router.build(None, 'us-timezones', None, {})
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.bad_authorization_header)
        self.assertTrue(self.FORBIDDEN in context.exception.message)

    def test_get_custom_timezones_returns_expected_list_of_timezones(self):
        request_parameters = {}
        uri = application.router.build(None, 'custom-timezones', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), 394)
        self.assertEqual(response_json[0], 'US/Alaska')
        self.assertEqual(response_json[393], 'Pacific/Wallis')



