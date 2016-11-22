from env_setup import setup_test_paths
setup_test_paths()

from webtest import AppError
from webapp2 import WSGIApplication, Route
from app_config import config
from agar.test import BaseTest, WebTest


class TestDecorators(BaseTest, WebTest):
    APPLICATION = WSGIApplication(
        [Route(r'/internal/v1/bogus', handler='handlers.bogus_handler.BogusHandler', name='bogus')]
    )

    def setUp(self):
        super(TestDecorators, self).setUp()

    def tearDown(self):
        pass

    ##################################################################################################################
    # @requires_api_token on GET
    ##################################################################################################################

    def testApiTokenRequired_AuthorizationSuccessful(self):
        headers = {
            'Authorization': config.API_TOKEN
        }
        response = self.app.get('/internal/v1/bogus', params={}, headers=headers)
        self.assertOK(response)

    def testUnmanagedDeviceCreateTokenRequired_AuthorizationSuccessful(self):
        headers = {
            'Authorization': config.UNMANAGED_API_TOKEN
        }
        response = self.app.get('/internal/v1/bogus', params={}, headers=headers)
        self.assertOK(response)

    def testApiTokenRequired_IncorrectAuthorizationHeader_AuthorizationUnsuccessful(self):
        headers = {
            'Authorization': 'sdfjahsdkjhfalskjdhfaiusyduifyasdyfaosdyfaiusydfiuasyoduifyas'
        }
        with self.assertRaises(AppError) as cm:
            self.app.get('/internal/v1/bogus', params={}, headers=headers)
        self.assertTrue('403 Forbidden' in cm.exception.message)

    def testApiTokenRequired_NoAuthorizationHeader_AuthorizationUnsuccessful(self):
        headers = {}
        with self.assertRaises(AppError) as cm:
            self.app.get('/internal/v1/bogus', params={}, headers=headers)
        self.assertTrue('403 Forbidden' in cm.exception.message)

    ##################################################################################################################
    # @requires_registration_token on POST
    ##################################################################################################################

    def testRequiresRegistrationToken_Unmanaged_AuthorizationSuccessful(self):
        headers = {
            'Authorization': config.UNMANAGED_REGISTRATION_TOKEN
        }
        response = self.app.post('/internal/v1/bogus', params={}, headers=headers)
        self.assertOK(response)

    def testRequiresRegistrationToken_Managed_AuthorizationSuccessful(self):
        headers = {
            'Authorization': config.API_TOKEN
        }
        response = self.app.post('/internal/v1/bogus', params={}, headers=headers)
        self.assertOK(response)

    ##################################################################################################################
    # @requires_unmanaged_registration_token on PUT
    ##################################################################################################################

    def testRequiresUnmanagedRegistrationTokenOnly_AuthorizationSuccessful(self):
        headers = {
            'Authorization': config.UNMANAGED_REGISTRATION_TOKEN
        }
        response = self.app.put('/internal/v1/bogus', params={}, headers=headers)
        self.assertOK(response)

    def testRequiresUnmanagedRegistrationTokenOnly_AuthorizationUnsuccessful(self):
        headers = {
            'Authorization': 'sdfjahsdkjhfalskjdhfaiusyduifyasdyfaosdyfaiusydfiuasyoduifyas'
        }
        with self.assertRaises(AppError) as cm:
            self.app.put('/internal/v1/bogus', params={}, headers=headers)
        self.assertTrue('403 Forbidden' in cm.exception.message)
