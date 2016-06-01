from env_setup import setup_test_paths

setup_test_paths()

import json
from webtest import AppError
from models import Distributor, DistributorUser
from routes import application
from app_config import config
from provisioning_distributor_user_base_test import ProvisioningDistributorUserBase

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>, Christopher Bartling <chris.bartling@agosto.com>'


class TestUsersHandler(ProvisioningDistributorUserBase):
    def setUp(self):
        super(TestUsersHandler, self).setUp()

    ##################################################################################################################
    # get_list_by_user
    ##################################################################################################################

    def test_get_list_by_user_returns_ok_status(self):
        request_parameters = {}
        uri = application.router.build(None, 'get-distributors-by-user', None, {
            'user_urlsafe_key': self.user_key.urlsafe()
        })
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        self.assertOK(response)

    def test_get_list_returns_distributors_associated_to_user(self):
        request_parameters = {}
        uri = application.router.build(None, 'get-distributors-by-user', None, {
            'user_urlsafe_key': self.user_key.urlsafe()
        })
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), 2)
        self.assertEqual(response_json[0].get('name'), self.AGOSTO)
        self.assertTrue(response_json[0].get('active'))
        self.assertEqual(response_json[1].get('name'), self.DISTRIBUTOR)
        self.assertTrue(response_json[1].get('active'))

    def test_get_list_fails_with_bad_authorization_token_v2(self):
        request_parameters = {}
        uri = application.router.build(None, 'get-distributors-by-user', None, {
            'user_urlsafe_key': self.user_key.urlsafe()
        })
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.bad_authorization_header)
        self.assertTrue(self.FORBIDDEN in context.exception.message)
