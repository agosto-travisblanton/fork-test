from env_setup import setup_test_paths

setup_test_paths()

import json
from webtest import AppError
from models import Distributor
from routes import application
from app_config import config
from provisioning_distributor_user_base_test import ProvisioningDistributerUserBase

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>, Christopher Bartling <chris.bartling@agosto.com>'


class TestDistributorsHandler(ProvisioningDistributerUserBase):
    def setUp(self):
        super(TestDistributorsHandler, self).setUp()

    ##################################################################################################################
    # get
    ##################################################################################################################
    def test_get_by_key_returns_ok_status(self):
        request_parameters = {}
        uri = application.router.build(None, 'manage-distributor', None, {'distributor_key': self.agosto_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        self.assertOK(response)

    def test_get_by_key_returns_distributor_representation(self):
        request_parameters = {}
        uri = application.router.build(None, 'manage-distributor', None, {'distributor_key': self.agosto_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        expected = self.agosto_key.get()
        self.assertEqual(response_json.get('key'), expected.key.urlsafe())
        self.assertEqual(response_json.get('name'), self.AGOSTO)
        self.assertEqual(response_json.get('active'), expected.active)
        self.assertEqual(response_json.get('content_manager_url'), config.DEFAULT_CONTENT_MANAGER_URL)
        self.assertEqual(response_json.get('player_content_url'), config.DEFAULT_PLAYER_CONTENT_URL)
        self.assertEqual(response_json.get('created'), expected.created.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response_json.get('updated'), expected.updated.strftime('%Y-%m-%d %H:%M:%S'))

    def test_get_by_key_returns_inactive_distributor_representation(self):
        request_parameters = {}
        uri = application.router.build(None, 'manage-distributor', None,
                                       {'distributor_key': self.inactive_distributor_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        expected = self.inactive_distributor_key.get()
        self.assertEqual(response_json.get('key'), expected.key.urlsafe())
        self.assertEqual(response_json.get('name'), self.INACTIVE_DISTRIBUTOR)
        self.assertFalse(response_json.get('active'))

    ##################################################################################################################
    # get_list
    ##################################################################################################################
    def test_get_list_returns_ok_status(self):
        request_parameters = {}
        uri = application.router.build(None, 'distributors', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        self.assertOK(response)

    def test_get_list_returns_active_distributors(self):
        request_parameters = {}
        uri = application.router.build(None, 'distributors', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), 2)
        self.assertEqual(response_json[0].get('name'), self.AGOSTO)
        self.assertTrue(response_json[0].get('active'))
        self.assertEqual(response_json[1].get('name'), self.TIERNEY_BROS)
        self.assertTrue(response_json[1].get('active'))

    def test_get_list_fails_with_bad_authorization_token(self):
        request_parameters = {}
        uri = application.router.build(None, 'distributors', None, {})
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.bad_authorization_header)
        self.assertTrue(self.FORBIDDEN in context.exception.message)

    def test_get_list_by_name_returns_agosto(self):
        request_parameters = {'distributorName': self.AGOSTO}
        uri = application.router.build(None, 'distributors', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0].get('name'), self.AGOSTO)

    def test_get_list_by_name_returns_tierney(self):
        request_parameters = {'distributorName': self.TIERNEY_BROS}
        uri = application.router.build(None, 'distributors', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0].get('name'), self.TIERNEY_BROS)

    def test_get_list_by_name_returns_inactive(self):
        request_parameters = {'distributorName': self.INACTIVE_DISTRIBUTOR}
        uri = application.router.build(None, 'distributors', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0].get('name'), self.INACTIVE_DISTRIBUTOR)

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
        print response_json
        self.assertEqual(len(response_json), 2)
        self.assertEqual(response_json[0].get('name'), self.AGOSTO)
        self.assertTrue(response_json[0].get('active'))
        self.assertEqual(response_json[1].get('name'), self.TIERNEY_BROS)
        self.assertTrue(response_json[1].get('active'))

    def test_get_list_fails_with_bad_authorization_token_v2(self):
        request_parameters = {}
        uri = application.router.build(None, 'get-distributors-by-user', None, {
            'user_urlsafe_key': self.user_key.urlsafe()
        })
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.bad_authorization_header)
        self.assertTrue(self.FORBIDDEN in context.exception.message)

    ##################################################################################################################
    # put
    ##################################################################################################################
    def test_put_returns_no_content_status(self):
        uri = application.router.build(None, 'manage-distributor', None, {'distributor_key': self.agosto_key.urlsafe()})
        entity_body = {
            'name': self.AGOSTO,
            'active': True
        }
        response = self.app.put_json(uri, entity_body, headers=self.headers)
        self.assertEqual('204 No Content', response.status)

    def test_put_updates_active_property(self):
        uri = application.router.build(None, 'manage-distributor', None, {'distributor_key': self.agosto_key.urlsafe()})
        expected = self.agosto_key.get()
        self.assertEqual(expected.name, self.AGOSTO)
        self.assertEqual(expected.active, True)
        active = False
        entity_body = {
            'name': self.AGOSTO,
            'active': active
        }
        self.app.put_json(uri, entity_body, headers=self.headers)
        self.assertEqual(expected.name, self.AGOSTO)
        self.assertEqual(expected.active, active)

    def test_put_updates_name_property(self):
        uri = application.router.build(None, 'manage-distributor', None, {'distributor_key': self.agosto_key.urlsafe()})
        expected = self.agosto_key.get()
        self.assertEqual(expected.name, self.AGOSTO)
        self.assertEqual(expected.active, True)
        new_name = "Super {0}".format(self.AGOSTO)
        active = True
        entity_body = {
            'name': new_name,
            'active': active
        }
        self.app.put_json(uri, entity_body, headers=self.headers)
        self.assertEqual(expected.name, new_name)
        self.assertEqual(expected.active, active)

    def test_put_fails_with_bad_authorization_token(self):
        uri = application.router.build(None, 'manage-distributor', None, {'distributor_key': self.agosto_key.urlsafe()})
        entity_body = {}
        with self.assertRaises(AppError) as context:
            self.app.put_json(uri, entity_body, headers=self.bad_authorization_header)
        self.assertTrue(self.FORBIDDEN in context.exception.message)

    ##################################################################################################################
    # delete
    ##################################################################################################################
    def test_delete_returns_no_content_status(self):
        url_safe_distributor_key = self.tierney_bros_key.urlsafe()
        uri = application.router.build(None, 'manage-distributor', None,
                                       {'distributor_key': url_safe_distributor_key})
        response = self.app.delete(uri, headers=self.headers)
        self.assertEqual(204, response.status_int)

    def test_delete_soft_deletes_distributor(self):
        url_safe_distributor_key = self.tierney_bros_key.urlsafe()
        request_parameters = {}
        uri = application.router.build(None, 'manage-distributor', None, {'distributor_key': url_safe_distributor_key})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertIsNotNone(response_json)

        uri = application.router.build(None, 'manage-distributor', None, {'distributor_key': url_safe_distributor_key})
        self.app.delete(uri, headers=self.headers)

        uri = application.router.build(None, 'manage-distributor', None, {'distributor_key': url_safe_distributor_key})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(response_json.get('active'), False)

    def test_delete_fails_with_bad_authorization_token(self):
        url_safe_distributor_key = self.tierney_bros_key.urlsafe()
        uri = application.router.build(None, 'manage-distributor', None,
                                       {'distributor_key': url_safe_distributor_key})
        with self.assertRaises(AppError) as context:
            self.app.delete(uri, headers=self.bad_authorization_header)
        self.assertTrue(self.FORBIDDEN in context.exception.message)

    ##################################################################################################################
    # get_domains
    ##################################################################################################################

    def test_get_domains_returns_ok_status(self):
        request_parameters = {}
        uri = application.router.build(None, 'distributor-domains', None,
                                       {'distributor_key': self.agosto_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        self.assertOK(response)

    def test_get_domains_returns_only_active_domains_associated_with_agosto(self):
        request_parameters = {}
        uri = application.router.build(None, 'distributor-domains', None,
                                       {'distributor_key': self.agosto_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), 2)

    def test_get_domains_returns_active_domains_with_expected_properties_associated_with_agosto(self):
        request_parameters = {}
        uri = application.router.build(None, 'distributor-domains', None,
                                       {'distributor_key': self.agosto_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(response_json[0].get('name'), self.CHROME_DEVICE_DOMAIN_BOB)
        self.assertEqual(response_json[0].get('impersonation_admin_email_address'), self.IMPERSONATION_EMAIL)
        self.assertEqual(response_json[1].get('name'), self.CHROME_DEVICE_DOMAIN_FOO)
        self.assertEqual(response_json[1].get('impersonation_admin_email_address'), self.IMPERSONATION_EMAIL)

    def test_get_domains_returns_no_domains_associated_with_tierney_bros(self):
        request_parameters = {}
        uri = application.router.build(None, 'distributor-domains', None,
                                       {'distributor_key': self.tierney_bros_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), 0)

    def test_get_domains_returns_no_domains_associated_with_inactive_distributor(self):
        request_parameters = {}
        uri = application.router.build(None, 'distributor-domains', None,
                                       {'distributor_key': self.inactive_distributor_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), 0)

    ###########################################################################
    # MAKE DISTRIBUTOR
    ###########################################################################
    def test_create_new_distributor_as_admin(self):
        distro_to_add = "new"
        r = self.post('/api/v1/distributors', json.dumps({
            "admin_email": self.user.email,
            "distributor": distro_to_add,
        }), headers={"X-Provisioning-User": self.admin_user.key.urlsafe()})

        self.assertEqual(200, r.status_int)
        self.assertTrue(json.loads(r.body)["success"])
        self.assertFalse(Distributor.is_unique(distro_to_add))

    def test_create_same_distributor_as_admin(self):
        self.test_create_new_distributor_as_admin()
        distro_to_add = "new"
        r = self.post('/api/v1/distributors', json.dumps({
            "admin_email": self.user.email,
            "distributor": distro_to_add,
        }), headers={"X-Provisioning-User": self.admin_user.key.urlsafe()})

        self.assertEqual(409, r.status_int)

    def test_create_new_distributor_as_distributor_admin(self):
        distro_to_add = "new"
        r = self.post('/api/v1/distributors', json.dumps({
            "admin_email": self.user.email,
            "distributor": distro_to_add,
        }), headers={"X-Provisioning-User": self.distributor_admin_user.key.urlsafe()})

        self.assertEqual(403, r.status_int)

    ###########################################################################
    # MAKE DISTRIBUTOR
    ###########################################################################
    def test_get_users_of_distributor_multiple(self):
        self.create_user_of_distributor(self.user, self.agosto, role=1)
        self.create_user_of_distributor(self.admin_user, self.agosto)
        url = '/api/v1/analytics/distributors/{}/users'.format(self.agosto_key.urlsafe())
        request = self.get(url, headers=self.headers)
        request_json = json.loads(request.body)
        self.assertEqual(200, request.status_int)
        self.assertEqual(3, len(request_json))
        self.assertTrue(len([d for d in request_json if d["email"] == self.user.email]) == 1)
        self.assertTrue(len([d for d in request_json if d["email"] == self.admin_user.email]) == 1)
