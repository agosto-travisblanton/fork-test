from env_setup import setup_test_paths

setup_test_paths()

import json
from ae_test_data import build
from utils.web_util import build_uri
from agar.test import BaseTest, WebTest
from webtest import AppError
from models import Distributor, DISTRIBUTOR_ENTITY_GROUP_NAME, Domain, User, DistributorUser
from routes import application
from provisioning_base_test import ProvisioningBaseTest
from app_config import config

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>, Christopher Bartling <chris.bartling@agosto.com>'


class TestDistributorsHandler(ProvisioningBaseTest):
    APPLICATION = application
    AGOSTO = 'Agosto'
    TIERNEY_BROS = 'Tierney Bros'
    INACTIVE_DISTRIBUTOR = 'Inactive Distributor'
    FORBIDDEN = '403 Forbidden'
    CHROME_DEVICE_DOMAIN_BOB = 'bob.agosto.com'
    CHROME_DEVICE_DOMAIN_FOO = 'foo.agosto.com'
    IMPERSONATION_EMAIL = 'admin@skykit.com'

    def setUp(self):
        super(TestDistributorsHandler, self).setUp()
        self.headers = {
            'Authorization': config.API_TOKEN
        }
        self.bad_authorization_header = {
            'Authorization': 'Forget about it!'
        }
        self.user = User(email="chris@mycompany.com")
        self.user_key = self.user.put()
        self.agosto = Distributor.create(name=self.AGOSTO,
                                         active=True)
        self.agosto_key = self.agosto.put()
        self.tierney_bros = Distributor.create(name=self.TIERNEY_BROS,
                                               active=True)
        self.tierney_bros_key = self.tierney_bros.put()
        self.inactive_distributor = Distributor.create(name=self.INACTIVE_DISTRIBUTOR,
                                                       active=False)
        self.inactive_distributor_key = self.inactive_distributor.put()

        self.domain_bob = Domain.create(name=self.CHROME_DEVICE_DOMAIN_BOB,
                                        distributor_key=self.agosto_key,
                                        impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                        active=True)
        self.domain_bob.put()
        self.domain_foo = Domain.create(name=self.CHROME_DEVICE_DOMAIN_FOO,
                                        distributor_key=self.agosto_key,
                                        impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                        active=True)
        self.domain_foo.put()
        self.domain_inactive = Domain.create(name=self.CHROME_DEVICE_DOMAIN_BOB,
                                             distributor_key=self.agosto_key,
                                             impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                             active=False)
        self.domain_inactive.put()
        self.default_distributor = self.agosto_key.get()

        self.distributor_admin_user = self.create_distributor_admin(email='john.jones@demo.agosto.com',
                                                                    distributor_name="distributor_admin_name")

        self.admin_user = self.create_platform_admin(email='jim.bob@demo.agosto.com',
                                                     distributor_name=self.default_distributor.name)

        self.user = self.create_user(email='dwight.schrute@demo.agosto.com',
                                     distributor_name=self.default_distributor.name)

        self.login_url = build_uri('login')
        self.logout_url = build_uri('logout')
        self.identity_url = build_uri('identity')

        for i in range(3):
            distributor = build(Distributor)
            distributor.name = "default_distro" + str(i)
            distributor.put()

    ##################################################################################################################
    ## get
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
    ## get_list
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
    ## get_list_by_user
    ##################################################################################################################
    def test_get_list_by_user_returns_ok_status(self):
        self._create_distributor_user_associations()
        request_parameters = {}
        uri = application.router.build(None, 'get-distributors-by-user', None, {
            'user_urlsafe_key': self.user_key.urlsafe()
        })
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        self.assertOK(response)

    def test_get_list_returns_distributors_associated_to_user(self):
        self._create_distributor_user_associations()
        request_parameters = {}
        uri = application.router.build(None, 'get-distributors-by-user', None, {
            'user_urlsafe_key': self.user_key.urlsafe()
        })
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), 2)
        self.assertEqual(response_json[0].get('name'), self.AGOSTO)
        self.assertTrue(response_json[0].get('active'))
        self.assertEqual(response_json[1].get('name'), self.TIERNEY_BROS)
        self.assertTrue(response_json[1].get('active'))

    def test_get_list_fails_with_bad_authorization_token(self):
        self._create_distributor_user_associations()
        request_parameters = {}
        uri = application.router.build(None, 'get-distributors-by-user', None, {
            'user_urlsafe_key': self.user_key.urlsafe()
        })
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.bad_authorization_header)
        self.assertTrue(self.FORBIDDEN in context.exception.message)

    ##################################################################################################################
    ## put
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
    ## delete
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
    ## get_domains
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

    def _create_distributor_user_associations(self):
        distributor_user1 = DistributorUser.create(user_key=self.user_key, distributor_key=self.agosto_key)
        distributor_user1.put()
        distributor_user2 = DistributorUser.create(user_key=self.user_key, distributor_key=self.tierney_bros_key)
        distributor_user2.put()

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
    def test_get_users_of_distributer(self):
        self.create_user_of_distributer(self.user, self.agosto, role=1)
        url = '/api/v1/distributors/analytics/users/' + self.agosto_key.urlsafe()
        r = self.get(url, headers=self.headers)
        r_json = json.loads(r.body)
        self.assertEqual(200, r.status_int)
        self.assertEqual(1, len(r_json))
        self.assertEqual(self.user.email, r_json[0]["email"])

    def test_get_users_of_distributer_multiple(self):
        self.create_user_of_distributer(self.user, self.agosto, role=1)
        self.create_user_of_distributer(self.admin_user, self.agosto, role=0)
        url = '/api/v1/distributors/analytics/users/' + self.agosto_key.urlsafe()
        r = self.get(url, headers=self.headers)
        r_json = json.loads(r.body)
        self.assertEqual(200, r.status_int)
        self.assertEqual(2, len(r_json))
        self.assertTrue(len([d for d in r_json if d["email"] == self.user.email]) == 1)
        self.assertTrue(len([d for d in r_json if d["email"] == self.admin_user.email]) == 1)

    ##########################################################################
    # GET ALL DISTRIBUTORS
    ##########################################################################
    def test_get_all_distributors(self):
        results = [u'distributor_admin_name', u'Agosto', u'Agosto', u'default_distro0', u'default_distro1',
                   u'default_distro2', u'Agosto', u'Tierney Bros', u'Inactive Distributor']
        url = '/api/v1/distributors/analytics/all'
        r = self.get(url, headers={"X-Provisioning-User": self.admin_user.key.urlsafe()})
        r_json = json.loads(r.body)
        self.assertEqual(200, r.status_int)
        self.assertEqual(results, r_json)

        new_distributor_name = "NEW"
        Distributor.create(name=new_distributor_name,
                           active=True).put()
        r = self.get(url, headers={"X-Provisioning-User": self.admin_user.key.urlsafe()})
        r_json = json.loads(r.body)
        self.assertEqual(200, r.status_int)
        self.assertTrue(new_distributor_name in r_json)
        r_json.remove(new_distributor_name)
        self.assertEqual(results, r_json)
