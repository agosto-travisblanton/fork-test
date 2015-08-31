import json
from ae_test_data import build
from agar.sessions import SessionStore
from app_config import config
from models import User, Distributor, DistributorEntityGroup
import stormpath_api
from datetime import datetime
from provisioning_base_test import ProvisioningBaseTest
from utils.web_util import build_uri
from mock import patch


class LoginHandlerTest(ProvisioningBaseTest):
    def setUp(self):
        super(LoginHandlerTest, self).setUp()
        self.user = self.create_user(email='dwight.schrute@demo.agosto.com')
        self.identity = self.get(build_uri('identity')).json

    def test_login_authed_user(self):
        params = {
            'email': self.user.email,
            'password': 'letmein',
        }

        timestamp = datetime.now()
        uri = build_uri('login')

        with patch.object(stormpath_api, 'cloud_login', return_value=self.user):
            resp = self.app.post_json(uri, params)
        self.assertOK(resp)
        self.assertTrue("Successful Login" in resp)
        self.assertGreaterEqual(self.user.last_login, timestamp)

        session = SessionStore(self.app).get_session()
        self.assertEqual(session.get('user_key'), self.user.key.urlsafe())
        self.assertEqual(session.get('distributor'), self.user.distributors[0].name)
        self.assertEqual(self.identity['STATE'], session.get('state'))

    def test_login_invalid_user(self):
        params = {
            'email': 'housekeeping',
            'password': 'whatever',
        }

        uri = build_uri('login')
        with patch.object(stormpath_api, 'cloud_login', return_value=None):
            resp = self.app.post_json(uri, params, expect_errors=True)
        self.assertBadRequest(resp)
        self.assertTrue('Login Failed' in resp)

        session = SessionStore(self.app).get_session()
        self.assertNotIn('user_key', session)
        self.assertNotIn('distributor', session)

    def test_login_missing_data(self):
        params = {
            'password': 'letmein',
        }
        resp = self.app.post_json(build_uri('login'), params, expect_errors=True)
        self.assertBadRequest(resp)
        self.assertTrue('Login Failed' in resp)

        params = {
            'email': self.user.email,
        }
        resp = self.app.post_json(build_uri('login'), params, expect_errors=True)
        self.assertBadRequest(resp)
        self.assertTrue('Login Failed' in resp)

        params = {
            'code': 'blah',
        }
        resp = self.app.post_json(build_uri('login'), params, expect_errors=True)
        self.assertBadRequest(resp)
        self.assertTrue('Login Failed' in resp)


class LogoutHandlerTest(ProvisioningBaseTest):
    def test_logout(self):
        user = self.create_user('dwight.shrute@demo.agosto.com')
        resp = self.app.post_json(build_uri('logout'))
        self.assertOK(resp)
        self.assertTrue("Successful Logout" in resp)

        session = SessionStore(self.app).get_session()
        self.assertNotIn('user_key', session)
        self.assertNotIn('distributor', session)
        self.assertNotIn('state', session)

        self.login(user.email)

        session = SessionStore(self.app).get_session()
        self.assertIn('user_key', session)
        self.assertIn('distributor', session)
        self.assertIn('state', session)

        resp = self.app.post_json(build_uri('logout'))
        self.assertOK(resp)
        self.assertTrue("Successful Logout" in resp)

        session = SessionStore(self.app).get_session()
        self.assertNotIn('user_key', session)
        self.assertNotIn('distributor', session)
        self.assertNotIn('state', session)


class IdentityHandlerTest(ProvisioningBaseTest):
    def setUp(self):
        super(IdentityHandlerTest, self).setUp()
        self.user = self.create_user(email='dwight.schrute@demo.agosto.com')
        self.login_url = build_uri('login')
        self.logout_url = build_uri('logout')
        self.identity_url = build_uri('identity')
        for _ in range(3):
            build(Distributor)

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
        self.assertTrue(data.get('administrator'))
        distributor_names = sorted([distributor.name for distributor in Distributor.query().fetch()])
        self.assertEqual(distributor_names, sorted(data.get('distributors')))
        self.assertEqual(self.user.distributors[0].name, data.get('distributor'))
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
        self.assertLength(1, distributor_names)
        self.assertEqual(distributor_names, sorted(data.get('distributors')))
        self.assertEqual(self.user.distributors[0].name, data.get('distributor'))
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
        self.assertLength(2, distributor_names)
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
