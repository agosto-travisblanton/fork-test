from env_setup import setup_test_paths
setup_test_paths()

from webtest import AppError
from webapp2 import WSGIApplication, Route
from app_config import config
from agar.test import BaseTest, WebTest


class TestDecorators(BaseTest, WebTest):
    APPLICATION = WSGIApplication(
        [Route(r'/api/v1/bogus', handler='handlers.bogus_handler.BogusHandler', name='bogus')]
    )

    def setUp(self):
        super(TestDecorators, self).setUp()

    def tearDown(self):
        pass

    ##################################################################################################################
    ## ApiTokenRequired
    ##################################################################################################################

    def testApiTokenRequired_AuthorizationSuccessful(self):
        headers = {
            'Authorization': config.API_TOKEN
        }
        response = self.app.get('/api/v1/bogus', params={}, headers=headers)
        self.assertOK(response)

    def testLimitedTokenRequired_AuthorizationSuccessful(self):
        headers = {
            'Authorization': config.LIMITED_UNMANAGED_DEVICE_REGISTRATION_API_TOKEN
        }
        response = self.app.get('/api/v1/bogus', params={}, headers=headers)
        self.assertOK(response)

    def testApiTokenRequired_IncorrectAuthorizationHeader_AuthorizationUnsuccessful(self):
        headers = {
            'Authorization': 'sdfjahsdkjhfalskjdhfaiusyduifyasdyfaosdyfaiusydfiuasyoduifyas'
        }
        with self.assertRaises(AppError) as cm:
            self.app.get('/api/v1/bogus', params={}, headers=headers)
        self.assertTrue('403 Forbidden' in cm.exception.message)

    def testApiTokenRequired_NoAuthorizationHeader_AuthorizationUnsuccessful(self):
        headers = {}
        with self.assertRaises(AppError) as cm:
            self.app.get('/api/v1/bogus', params={}, headers=headers)
        self.assertTrue('403 Forbidden' in cm.exception.message)
