from env_setup import setup_test_paths
setup_test_paths()

from webtest import AppError
from webapp2 import WSGIApplication, Route
from ae_test_data import build
from models import User, Distributor
from app_config import config
from agar.test import BaseTest, WebTest


class TestApiTokenRequiredDecorator(BaseTest, WebTest):
    APPLICATION = WSGIApplication(
        [Route(r'/api/v1/bogus1', handler='handlers.bogus_handler.BogusHandler1', name='bogus1'),
         Route(r'/api/v1/bogus2', handler='handlers.bogus_handler.BogusHandler2', name='bogus2'),
         Route(r'/api/v1/bogus3', handler='handlers.bogus_handler.BogusHandler3', name='bogus3')],
    )

    def setUp(self):
        super(TestApiTokenRequiredDecorator, self).setUp()
        self.user = build(User)
        self.distributor = Distributor.create(name='Agosto', active=True)
        self.distributor.put()

    def tearDown(self):
        pass

    ##################################################################################################################
    ## ApiTokenRequired
    ##################################################################################################################

    def testApiTokenRequired_AuthorizationSuccessful(self):
        headers = {
            'Authorization': config.API_TOKEN
        }
        response = self.app.get('/api/v1/bogus1', params={}, headers=headers)
        self.assertOK(response)

    def testApiTokenRequired_IncorrectAuthorizationHeader_AuthorizationUnsuccessful(self):
        headers = {
            'Authorization': 'sdfjahsdkjhfalskjdhfaiusyduifyasdyfaosdyfaiusydfiuasyoduifyas'
        }
        with self.assertRaises(AppError) as cm:
            self.app.get('/api/v1/bogus1', params={}, headers=headers)
        self.assertTrue('403 Forbidden' in cm.exception.message)

    def testApiTokenRequired_NoAuthorizationHeader_AuthorizationUnsuccessful(self):
        headers = {}
        with self.assertRaises(AppError) as cm:
            self.app.get('/api/v1/bogus1', params={}, headers=headers)
        self.assertTrue('403 Forbidden' in cm.exception.message)

    ##################################################################################################################
    ## IdentityRequired
    ##################################################################################################################

    def testIdentityRequired_Resolvable_User_Key_Returns_Ok(self):
        headers = {
            'X-Provisioning-User': self.user.key.urlsafe()
        }
        response = self.app.get('/api/v1/bogus2', params={}, headers=headers)
        self.assertOK(response)

    def testIdentityRequired_Non_Resolvable_User_Key_Returns_Forbidden(self):
        headers = {
            'X-Provisioning-User': 'bad_key'
        }
        with self.assertRaises(AppError) as context:
            self.app.get('/api/v1/bogus2', params={}, headers=headers)
        self.assertTrue('403 Forbidden' in context.exception.message)

    ##################################################################################################################
    ## DistributorRequired
    ##################################################################################################################

    def testDistributorRequired_Resolvable_Distributor_Key_Returns_Ok(self):
        headers = {
            'X-Provisioning-Distributor': self.distributor.key.urlsafe()
        }
        response = self.app.get('/api/v1/bogus3', params={}, headers=headers)
        self.assertOK(response)

    def testDistributorRequired_Non_Resolvable_Distributor_Key_Returns_Forbidden(self):
        headers = {
            'X-Provisioning-Distributor': 'bad_key'
        }
        with self.assertRaises(AppError) as context:
            self.app.get('/api/v1/bogus3', params={}, headers=headers)
        self.assertTrue('403 Forbidden' in context.exception.message)
