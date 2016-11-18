from env_setup import setup_test_paths

setup_test_paths()

import json
from webtest import AppError
from routes import application
from models import User
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

    ###########################################################################
    # ADD REGULAR USER TO DISTRIBUTOR
    ###########################################################################
    def test_add_user_to_distributor_as_no_user(self):
        request = self.post('/internal/v1/users', json.dumps({
            "user_email": self.user.email,
            "distributor": "asdf",
            "distributor_admin": False
        }), headers={"X-Provisioning-User": "qwerqwerw"})
        self.assertEqual(403, request.status_int)

    def test_add_user_to_distributor_as_unprivileged_user(self):
        request = self.post('/internal/v1/users', json.dumps({
            "user_email": self.user.email,
            "distributor": "asdf",
            "distributor_admin": False
        }), headers={"X-Provisioning-User": self.user.key.urlsafe()})
        self.assertEqual(403, request.status_int)

    def test_add_user_to_distributor_of_distributor_admin_as_distributor_admin(self):
        distributor_name_of_distributor_admin = self.distributor_admin_user.distributors_as_admin[0].name
        new_user = self.create_user(email="new@gmail.com", distributor_name="a new distributor")
        request = self.post('/internal/v1/users', json.dumps({
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
        request = self.post('/internal/v1/users', json.dumps({
            "user_email": self.user.email,
            "distributor": "default_distro0",
            "distributor_admin": False
        }), headers={"X-Provisioning-User": self.distributor_admin_user.key.urlsafe()})
        self.assertEqual(403, request.status_int)

    def test_add_user_to_distributor_that_does_not_exist_as_admin(self):
        request = self.post('/internal/v1/users', json.dumps({
            "user_email": self.user.email,
            "distributor": "asdf",
            "distributor_admin": False
        }), headers={"X-Provisioning-User": self.admin_user.key.urlsafe()})
        self.assertEqual(403, request.status_int)
        self.assertEqual('Not a valid distributor', json.loads(request.body)["message"])

    def test_add_user_to_distributor_that_already_is_linked_as_admin(self):
        request = self.post('/internal/v1/users', json.dumps({
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
        request = self.post('/internal/v1/users', json.dumps({
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

        request = self.post('/internal/v1/users', json.dumps({
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
        request = self.post('/internal/v1/users', json.dumps({
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
        request = self.post('/internal/v1/users', json.dumps({
            "user_email": self.user.email,
            "distributor": default_distributor,
            "distributor_admin": True
        }), headers={"X-Provisioning-User": self.distributor_admin_user.key.urlsafe()})
        self.assertEqual(403, request.status_int)
