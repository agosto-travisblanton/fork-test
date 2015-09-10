from env_setup import setup_test_paths
setup_test_paths()

import json
from agar.test import BaseTest, WebTest
from webtest import AppError
from models import Distributor, DISTRIBUTOR_ENTITY_GROUP_NAME
from routes import application
from app_config import config


class TestDistributorsHandler(BaseTest, WebTest):
    APPLICATION = application
    AGOSTO = 'Agosto'
    TIERNEY_BROS = 'Tierney Bros'
    INACTIVE_DISTRIBUTOR = 'Inactive Distributor'
    FORBIDDEN = '403 Forbidden'

    def setUp(self):
        super(TestDistributorsHandler, self).setUp()
        self.headers = {
            'Authorization': config.API_TOKEN
        }
        self.bad_authorization_header = {
            'Authorization': 'Forget about it!'
        }
        self.agosto = Distributor.create(name=self.AGOSTO,
                                         active=True)
        self.agosto_key = self.agosto.put()
        self.tierney_bros = Distributor.create(name=self.TIERNEY_BROS,
                                               active=True)
        self.tierney_bros_key = self.tierney_bros.put()
        self.inactive_distributor = Distributor.create(name=self.INACTIVE_DISTRIBUTOR,
                                                       active=False)
        self.inactive_distributor_key = self.inactive_distributor.put()

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
    ## post
    ##################################################################################################################
    def test_post_returns_created_status(self):
        name = u'Acme'
        request_parameters = {'name': name,
                              'active': True}
        uri = application.router.build(None, 'distributor-creator', None, {})
        response = self.app.post_json(uri, params=request_parameters, headers=self.headers)
        self.assertEqual(201, response.status_code)

    def test_post_create_new_distributor_persists_object(self):
        name = u'Acme'
        request_parameters = {'name': name,
                              'active': True}
        uri = application.router.build(None, 'distributor-creator', None, {})
        self.app.post_json(uri, params=request_parameters, headers=self.headers)
        actual = Distributor.find_by_name(request_parameters['name'])
        self.assertIsNotNone(actual)

    def test_post_create_new_distributor_persists_object_with_string_boolean(self):
        name = u'Acme'
        request_parameters = {'name': name,
                              'active': "true"}
        uri = application.router.build(None, 'distributor-creator', None, {})
        self.app.post_json(uri, params=request_parameters, headers=self.headers)
        actual = Distributor.find_by_name(request_parameters['name'])
        self.assertIsNotNone(actual)

    def test_post_fails_without_bogus_active_parameter(self):
        request_body = {'name': 'Acme',
                        'active': 'bogus'}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/distributors', json.dumps(request_body), headers=self.headers)
        self.assertTrue('Bad response: 400 The active parameter is invalid'
                        in context.exception.message)

    def test_post_fails_without_name_parameter(self):
        request_body = {'name': '',
                        'active': True}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/distributors', json.dumps(request_body), headers=self.headers)
        self.assertTrue('Bad response: 400 The name parameter is invalid'
                        in context.exception.message)

    def test_post_create_new_distributor_sets_location_header(self):
        name = u'Acme'
        request_parameters = {'name': name,
                              'active': True}
        uri = application.router.build(None, 'distributor-creator', None, {})
        response = self.app.post_json(uri, params=request_parameters, headers=self.headers)
        actual = Distributor.find_by_name(request_parameters['name'])
        distributor_uri = application.router.build(None,
                                                   'manage-distributor',
                                                   None,
                                                   {'distributor_key': actual.key.urlsafe()})
        self.assertTrue(distributor_uri in response.headers.get('Location'))

    def test_post_create_object_has_expected_parent(self):
        name = u'Acme'
        request_parameters = {'name': name,
                              'active': True}
        uri = application.router.build(None, 'distributor-creator', None, {})
        self.app.post_json(uri, params=request_parameters, headers=self.headers)
        actual = Distributor.find_by_name(request_parameters['name'])
        parent = actual.key.parent().get()
        self.assertEqual(parent.name, DISTRIBUTOR_ENTITY_GROUP_NAME)

    def test_post_fails_with_bad_authorization_token(self):
        request_parameters = {}
        uri = application.router.build(None, 'distributor-creator', None, {})
        with self.assertRaises(AppError) as context:
            self.app.post_json(uri, params=request_parameters, headers=self.bad_authorization_header)
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
        self.assertEqual(204, response.status_code)

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
        self.assertEqual(204, response.status_code)

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
