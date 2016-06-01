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

    ###########################################################################
    # ADD REGULAR USER TO DISTRIBUTOR
    ###########################################################################
    def test_add_user_to_distributor_as_no_user(self):
        request = self.post('/api/v1/users', json.dumps({
            "user_email": self.user.email,
            "distributor": "asdf",
            "distributor_admin": False
        }), headers={"X-Provisioning-User": "qwerqwerw"})
        self.assertEqual(403, request.status_int)

    def test_add_user_to_distributor_as_unprivileged_user(self):
        request = self.post('/api/v1/users', json.dumps({
            "user_email": self.user.email,
            "distributor": "asdf",
            "distributor_admin": False
        }), headers={"X-Provisioning-User": self.user.key.urlsafe()})
        self.assertEqual(403, request.status_int)

    def test_add_user_to_distributor_of_distributor_admin_as_distributor_admin(self):
        distributor_name_of_distributor_admin = self.distributor_admin_user.distributors_as_admin[0].name
        new_user = self.create_user(email="new@gmail.com", distributor_name="a new distributor")
        request = self.post('/api/v1/users', json.dumps({
            "user_email": new_user.email,
            "distributor": distributor_name_of_distributor_admin,
            "distributor_admin": False
        }), headers={"X-Provisioning-User": self.distributor_admin_user.key.urlsafe()})
        self.assertEqual(200, request.status_int)

        user_distributors = [distributor.name for distributor in new_user.distributors]
        self.assertIn(distributor_name_of_distributor_admin, user_distributors)
        self.assertIn(self.default_distributor_name, user_distributors)
        self.assertLength(2, user_distributors)

    def test_add_user_to_different_distributor_as_distributor_admin(self):
        request = self.post('/api/v1/users', json.dumps({
            "user_email": self.user.email,
            "distributor": "default_distro0",
            "distributor_admin": False
        }), headers={"X-Provisioning-User": self.distributor_admin_user.key.urlsafe()})
        self.assertEqual(403, request.status_int)

    def test_add_user_to_distributor_that_does_not_exist_as_admin(self):
        request = self.post('/api/v1/users', json.dumps({
            "user_email": self.user.email,
            "distributor": "asdf",
            "distributor_admin": False
        }), headers={"X-Provisioning-User": self.admin_user.key.urlsafe()})
        self.assertEqual(403, request.status_int)
        self.assertEqual('Not a valid distributor', json.loads(request.body)["error"])

    def test_add_user_to_distributor_that_already_is_linked_as_admin(self):
        request = self.post('/api/v1/users', json.dumps({
            "user_email": self.user.email,
            "distributor": self.default_distributor_name,
            "distributor_admin": False
        }), headers={"X-Provisioning-User": self.admin_user.key.urlsafe()})
        self.assertEqual(409, request.status_int)
        self.assertEqual(
            {
                u'message': u'{0} is already linked to {1}'.format(self.default_distributor_name, self.user.email),
                u'success': False
            }, json.loads(request.body))

    def test_add_user_to_distributor_as_admin(self):
        distro_to_add = self.create_distributor_if_unique("new_distributor").name
        request = self.post('/api/v1/users', json.dumps({
            "user_email": self.user.email,
            "distributor": distro_to_add,
            "distributor_admin": False
        }), headers={"X-Provisioning-User": self.admin_user.key.urlsafe()})

        self.assertEqual(200, request.status_int)
        self.assertEqual(True, json.loads(request.body)["success"])

        user = User.get_or_insert_by_email(self.user.email)
        user_distributors = [distributor.name for distributor in user.distributors]
        self.assertIn(distro_to_add, user_distributors)
        self.assertIn(self.default_distributor_name, user_distributors)
        self.assertLength(3, user_distributors)

    ###########################################################################
    # ADD DISTRIBUTOR-ADMIN USER TO DISTRIBUTOR
    ###########################################################################
    def test_add_user_as_distributor_admin_to_distributor_of_distributor_admin_as_distributor_admin(self):
        distro_to_add = self.distributor_admin_user.distributors_as_admin[0].name
        new_user = self.create_user(email="new@gmail.com", distributor_name="another new distributor")

        request = self.post('/api/v1/users', json.dumps({
            "user_email": new_user.email,
            "distributor": distro_to_add,
            "distributor_admin": True
        }), headers={"X-Provisioning-User": self.distributor_admin_user.key.urlsafe()})
        self.assertEqual(200, request.status_int)

        user_distributors = [distributor.name for distributor in new_user.distributors]
        self.assertIn(distro_to_add, user_distributors)
        self.assertIn(self.default_distributor_name, user_distributors)
        self.assertLength(2, user_distributors)
        self.assertTrue(new_user.is_distributor_administrator_of_distributor(distro_to_add))

    def test_add_user_as_distributor_admin_to_distributor_as_platform_admin(self):
        new_user = self.create_user(email="new@gmail.com", distributor_name="a new distributor")
        distributor_name_of_distributor_admin = self.distributor_admin_user.distributors_as_admin[0].name
        request = self.post('/api/v1/users', json.dumps({
            "user_email": new_user.email,
            "distributor": distributor_name_of_distributor_admin,
            "distributor_admin": True
        }), headers={"X-Provisioning-User": self.distributor_admin_user.key.urlsafe()})
        self.assertEqual(200, request.status_int)

        user_distributors = [distributor.name for distributor in new_user.distributors]
        self.assertIn(distributor_name_of_distributor_admin, user_distributors)
        self.assertIn(self.default_distributor_name, user_distributors)
        self.assertLength(2, user_distributors)
        self.assertTrue(new_user.is_distributor_administrator_of_distributor(distributor_name_of_distributor_admin))

    def test_add_user_as_distributor_admin_to_different_distributor_as_distributor_admin(self):
        default_distributor = "default_distro0"
        request = self.post('/api/v1/users', json.dumps({
            "user_email": self.user.email,
            "distributor": default_distributor,
            "distributor_admin": True
        }), headers={"X-Provisioning-User": self.distributor_admin_user.key.urlsafe()})
        self.assertEqual(403, request.status_int)
