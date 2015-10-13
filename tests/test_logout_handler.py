from agar.sessions import SessionStore
from provisioning_base_test import ProvisioningBaseTest
from utils.web_util import build_uri


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
