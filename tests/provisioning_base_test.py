from ae_test_data import build

from env_setup import setup_test_paths, setup

setup_test_paths()
setup()


import json
import stormpath_api
from agar.test import BaseTest, WebTest
from ndb_mixins import KeyValidatorMixin
from routes import application
from utils.web_util import build_uri
from models import (
    Distributor,
    User,
)




class MockStormpathResponse:
    def __init__(self, email):
        self.email = email
        self.href = 'https://fake.stormpath.com/{}'.format(email)


class ProvisioningBaseTest(BaseTest, WebTest, KeyValidatorMixin):
    APPLICATION = application

    def setUp(self):
        super(ProvisioningBaseTest, self).setUp()

    def tearDown(self):
        super(ProvisioningBaseTest, self).tearDown()

    def create_user(self, email, distributor_name=None):
        if distributor_name:
            distributor = Distributor.get_or_insert_by_name(distributor_name)
        else:
            distributor = build(Distributor)

        user = User.update_or_create_with_api_account(MockStormpathResponse(email))
        user.add_distributor(distributor.key)
        return user

    def create_platform_admin(self, email, distributor_name=None):
        if distributor_name:
            distributor = Distributor.get_or_insert_by_name(distributor_name)
        else:
            distributor = build(Distributor)

        user = User.update_or_create_with_api_account(MockStormpathResponse(email))
        user.is_administrator = True
        user.add_distributor(distributor.key)
        return user

    def create_distributor_admin(self, email, distributor_name=None):
        if distributor_name:
            distributor = Distributor.get_or_insert_by_name(distributor_name)
        else:
            distributor = build(Distributor)

        user = User.update_or_create_with_api_account(MockStormpathResponse(email))
        user.is_distributor_administrator = True
        user.add_distributor(distributor.key)
        return user

    def login(self, email, administrator=False):

        identity_url = build_uri('identity')
        response = self.get(identity_url)
        self.assertOK(response)

        body = json.loads(response.body)
        state = body.get('STATE')
        params = {
            'state': state,
            'administrator': administrator
        }

        user = User.update_or_create_with_api_account(MockStormpathResponse(email))

        from mock import patch
        with patch.object(stormpath_api, 'google_login', return_value=user):
            resp = self.app.post_json(build_uri('login'), params)
        self.assertTrue("Successful Login" in resp)
