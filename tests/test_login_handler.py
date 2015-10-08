from datetime import datetime

from agar.sessions import SessionStore
import stormpath_api
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
