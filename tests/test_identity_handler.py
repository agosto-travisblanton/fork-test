import json

from ae_test_data import build
from agar.test import WebTest
from app_config import config
from models import User, Distributor, DistributorEntityGroup
from provisioning_base_test import ProvisioningBaseTest
from utils.web_util import build_uri


class IdentityHandlerTest(ProvisioningBaseTest):
    def setUp(self):
        super(IdentityHandlerTest, self).setUp()
        self.default_distributor_name = "my_distributor"
        self.distributor_admin_user = self.create_distributor_admin(email='john.jones@demo.agosto.com',
                                                                 distributor_name="distributor_admin_name")
        self.admin_user = self.create_platform_admin(email='jim.bob@demo.agosto.com',
                                                     distributor_name=self.default_distributor_name)
        self.user = self.create_user(email='dwight.schrute@demo.agosto.com',
                                     distributor_name=self.default_distributor_name)

        self.login_url = build_uri('login')
        self.logout_url = build_uri('logout')
        self.identity_url = build_uri('identity')

        for i in range(3):
            distributor = build(Distributor)
            distributor.name = "default_distro" + str(i)
            distributor.put()

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

    ###########################################################################
    # CREATE USER
    ###########################################################################
    def test_create_user_as_admin(self):
        uri = build_uri('make_user')
        email_to_insert = "some_user@gmail.com"
        r = self.app.post(uri, params=json.dumps({
            "user_email": email_to_insert
        }), headers={"X-Provisioning-User": self.admin_user.key.urlsafe()})
        self.assertEqual(200, r.status_int)
        response_json = json.loads(r.body)
        self.assertTrue(response_json["success"])
        a = User.query(User.email == email_to_insert).fetch()
        self.assertTrue(a)

    def test_create_user_as_distributor_admin(self):
        uri = build_uri('make_user')
        email_to_insert = "some_user@gmail.com"
        r = self.app.post(uri, params=json.dumps({
            "user_email": email_to_insert
        }), headers={"X-Provisioning-User": self.distributor_admin_user.key.urlsafe()})
        self.assertEqual(200, r.status_int)
        response_json = json.loads(r.body)
        self.assertTrue(response_json["success"])
        a = User.query(User.email == email_to_insert).fetch()
        self.assertTrue(a)

    def test_create_user_as_regular_user(self):
        email_to_insert = "some_user@gmail.com"
        r = self.post('/api/v1/make_user', json.dumps({
            "user_email": email_to_insert
        }), headers={"X-Provisioning-User": self.user.key.urlsafe()})
        self.assertForbidden(r)

    ###########################################################################
    # ADD USER TO DISTRIBUTOR
    ###########################################################################
    def test_add_user_to_distributor_as_no_user(self):
        r = self.post('/api/v1/add_user_to_distributor', json.dumps({
            "user_email": 'dwight.schrute@demo.agosto.com',
            "distributor": "asdf"
        }), headers={"X-Provisioning-User": "qwerqwerw"})
        self.assertEqual(403, r.status_int)

    def test_add_user_to_distributor_as_unprivileged_user(self):
        r = self.post('/api/v1/add_user_to_distributor', json.dumps({
            "user_email": 'dwight.schrute@demo.agosto.com',
            "distributor": "asdf"
        }), headers={"X-Provisioning-User": self.user.key.urlsafe()})
        self.assertEqual(403, r.status_int)

    def test_add_user_to_distributor_of_distributor_admin_as_distributor_admin(self):
        r = self.post('/api/v1/add_user_to_distributor', json.dumps({
            "user_email": self.user.email,
            "distributor": "distributor_admin_name"
        }), headers={"X-Provisioning-User": self.distributor_admin_user.key.urlsafe()})
        self.assertEqual(200, r.status_int)

        u = User.get_or_insert_by_email(self.user.email)
        user_distributors = [distributor.name for distributor in u.distributors]
        self.assertIn("distributor_admin_name", user_distributors)
        self.assertIn(self.default_distributor_name, user_distributors)
        self.assertLength(2, user_distributors)

    def test_add_user_to_different_distributor_as_distributor_admin(self):
        r = self.post('/api/v1/add_user_to_distributor', json.dumps({
            "user_email": self.user.email,
            "distributor": "default_distro0"
        }), headers={"X-Provisioning-User": self.distributor_admin_user.key.urlsafe()})
        self.assertEqual(403, r.status_int)


    def test_add_user_to_distributor_that_does_not_exist_as_admin(self):
        r = self.post('/api/v1/add_user_to_distributor', json.dumps({
            "user_email": 'dwight.schrute@demo.agosto.com',
            "distributor": "asdf"
        }), headers={"X-Provisioning-User": self.admin_user.key.urlsafe()})
        self.assertEqual(403, r.status_int)
        self.assertEqual('Not a valid distributor', json.loads(r.body)["error"])

    def test_add_user_to_distributor_that_already_is_linked_as_admin(self):
        r = self.post('/api/v1/add_user_to_distributor', json.dumps({
            "user_email": 'dwight.schrute@demo.agosto.com',
            "distributor": self.default_distributor_name
        }), headers={"X-Provisioning-User": self.admin_user.key.urlsafe()})
        self.assertEqual(409, r.status_int)
        self.assertEqual(
            {
                u'message': u'my_distributor is already linked to jim.bob@demo.agosto.com',
                u'success': False
            }, json.loads(r.body))

    def test_add_user_to_distributor_as_admin(self):
        distro_to_add = "default_distro0"
        r = self.post('/api/v1/add_user_to_distributor', json.dumps({
            "user_email": self.user.email,
            "distributor": distro_to_add
        }), headers={"X-Provisioning-User": self.admin_user.key.urlsafe()})

        self.assertEqual(200, r.status_int)
        self.assertEqual(True, json.loads(r.body)["success"])

        u = User.get_or_insert_by_email(self.user.email)
        user_distributors = [distributor.name for distributor in u.distributors]
        self.assertIn(distro_to_add, user_distributors)
        self.assertIn(self.default_distributor_name,user_distributors)
        self.assertLength(2, user_distributors)