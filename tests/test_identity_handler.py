import json

from ae_test_data import build
from app_config import config
from models import User, Distributor, DistributorEntityGroup
from utils.web_util import build_uri
from provisioning_distributor_user_base_test import ProvisioningDistributorUserBase


class IdentityHandlerTest(ProvisioningDistributorUserBase):
    def setUp(self):
        super(IdentityHandlerTest, self).setUp()

    def test_anonymous_identity(self):
        self.get(self.logout_url)
        response = self.get(self.identity_url)
        self.assertOK(response)
        data = json.loads(response.body)
        self.assertEqual(self.login_url, data.get('login_url'))
        self.assertEqual(self.logout_url, data.get('logout_url'))
        self.assertFalse(data.get('is_logged_in'))
        self.assertEqual('testbed-version', data.get('version'))
        self.assertNotIn('administrator', data)
        self.assertNotIn('email', data)
        self.assertNotIn('distributor', data)
        self.assertNotIn('distributors', data)
        self.assertEqual(config.CLIENT_ID, data.get('CLIENT_ID'))
        self.assertEqual(config.PUBLIC_API_SERVER_KEY, data.get('BROWSER_API_KEY'))
        self.assertIsNotNone(data.get('STATE'))

    def test_logged_out_identity(self):
        self.login(self.user.email)
        self.app.post_json(build_uri('logout'))
        response = self.get(self.identity_url)
        self.assertOK(response)
        data = json.loads(response.body)
        self.assertEqual(self.login_url, data.get('login_url'))
        self.assertEqual(self.logout_url, data.get('logout_url'))
        self.assertFalse(data.get('is_logged_in'))
        self.assertEqual('testbed-version', data.get('version'))
        self.assertNotIn('administrator', data)
        self.assertNotIn('distributor', data)
        self.assertNotIn('distributors', data)
        self.assertNotIn('email', data)
        self.assertEqual(config.CLIENT_ID, data.get('CLIENT_ID'))
        self.assertEqual(config.PUBLIC_API_SERVER_KEY, data.get('BROWSER_API_KEY'))
        self.assertIsNotNone(data.get('STATE'))

    def test_logged_in_administrator_identity(self):
        self.user.is_administrator = True
        self.user.put()
        self.login(self.user.email, administrator=True)
        response = self.get(self.identity_url)
        self.assertOK(response)
        data = json.loads(response.body)
        self.assertEqual(self.login_url, data.get('login_url'))
        self.assertEqual(self.logout_url, data.get('logout_url'))
        self.assertTrue(data.get('is_logged_in'))
        self.assertEqual('testbed-version', data.get('version'))
        self.assertTrue(data.get('is_admin'))
        distributor_names = sorted([distributor.name for distributor in Distributor.query().fetch()])
        self.assertEqual(distributor_names, sorted(data.get('distributors')))
        self.assertEqual(self.user.email, data.get('email'))
        self.assertEqual(config.CLIENT_ID, data.get('CLIENT_ID'))
        self.assertEqual(config.PUBLIC_API_SERVER_KEY, data.get('BROWSER_API_KEY'))
        self.assertIsNotNone(data.get('STATE'))

    def test_logged_in_non_administrator_identity(self):
        self.login(self.user.email, administrator=True)  # should ignore administrator flag because user is not admin
        response = self.get(self.identity_url)
        self.assertOK(response)
        data = json.loads(response.body)
        self.assertEqual(self.login_url, data.get('login_url'))
        self.assertEqual(self.logout_url, data.get('logout_url'))
        self.assertTrue(data.get('is_logged_in'))
        self.assertEqual('testbed-version', data.get('version'))
        self.assertNotIn('administrator', data)
        distributor_names = sorted([distributor.name for distributor in self.user.distributors])
        self.assertLength(2, distributor_names)
        self.assertEqual(distributor_names, sorted(data.get('distributors')))
        self.assertEqual(None, data.get('distributor'))
        self.assertEqual(self.user.email, data.get('email'))
        self.assertEqual(config.CLIENT_ID, data.get('CLIENT_ID'))
        self.assertEqual(config.PUBLIC_API_SERVER_KEY, data.get('BROWSER_API_KEY'))
        self.assertIsNotNone(data.get('STATE'))

    def test_logged_in_non_administrator_identity_multiple_distributors(self):
        distributor = build(Distributor, parent=DistributorEntityGroup.singleton().key)

        self.user.add_distributor(distributor.key)
        self.login(self.user.email)
        response = self.get(self.identity_url)
        self.assertOK(response)
        data = json.loads(response.body)
        self.assertEqual(self.login_url, data.get('login_url'))
        self.assertEqual(self.logout_url, data.get('logout_url'))
        self.assertTrue(data.get('is_logged_in'))
        self.assertEqual('testbed-version', data.get('version'))
        self.assertNotIn('administrator', data)
        distributor_names = sorted([distributor.name for distributor in self.user.distributors])
        self.assertLength(3, distributor_names)
        self.assertEqual(distributor_names, sorted(data.get('distributors')))
        self.assertEqual(None, data.get('distributor'))
        self.assertEqual(self.user.email, data.get('email'))
        self.assertEqual(config.CLIENT_ID, data.get('CLIENT_ID'))
        self.assertEqual(config.PUBLIC_API_SERVER_KEY, data.get('BROWSER_API_KEY'))
        self.assertIsNotNone(data.get('STATE'))

    def test_logged_out_administrator_identity(self):
        self.user.is_administrator = True
        self.user.put()
        self.login(self.user.email, administrator=True)
        self.app.post_json(build_uri('logout'))
        response = self.get(self.identity_url)
        self.assertOK(response)
        data = json.loads(response.body)
        self.assertEqual(self.login_url, data.get('login_url'))
        self.assertEqual(self.logout_url, data.get('logout_url'))
        self.assertFalse(data.get('is_logged_in'))
        self.assertEqual('testbed-version', data.get('version'))
        self.assertNotIn('administrator', data)
        self.assertNotIn('distributor', data)
        self.assertNotIn('distributors', data)
        self.assertNotIn('email', data)
        self.assertEqual(config.CLIENT_ID, data.get('CLIENT_ID'))
        self.assertIsNotNone(data.get('STATE'))

    def test_logged_in_no_session_distributor(self):
        user = build(User)
        self.login(user.email)
        response = self.get(self.identity_url)
        self.assertOK(response)

        data = json.loads(response.body)
        self.assertEqual(self.login_url, data.get('login_url'))
        self.assertEqual(self.logout_url, data.get('logout_url'))
        self.assertTrue(data.get('is_logged_in'))
        self.assertEqual('testbed-version', data.get('version'))
        self.assertIsNone(data.get('distributor'))
        self.assertEqual([], data.get('distributors'))
        self.assertEqual(user.email, data.get('email'))
        self.assertEqual(config.CLIENT_ID, data.get('CLIENT_ID'))
        self.assertEqual(config.PUBLIC_API_SERVER_KEY, data.get('BROWSER_API_KEY'))
        self.assertIsNotNone(data.get('STATE'))

        new_distributor = build(Distributor)
        user.add_distributor(new_distributor.key)

        response = self.get(self.identity_url)
        self.assertOK(response)

        data = json.loads(response.body)
        self.assertEqual(new_distributor.name, data.get('distributor'))
        self.assertEqual([new_distributor.name], data.get('distributors'))
