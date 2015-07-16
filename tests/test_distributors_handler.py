from env_setup import setup_test_paths

setup_test_paths()

import json
from agar.test import BaseTest, WebTest
from models import Distributor
from routes import application
from app_config import config


class TestDistributorsHandler(BaseTest, WebTest):
    APPLICATION = application
    AGOSTO = 'Agosto'
    TIERNEY_BROS = 'Tierney Bros'
    INACTIVE_DISTRIBUTOR = 'Inactive Distributor'
    ENTITY_GROUP_NAME = 'distributorEntityGroup'

    def setUp(self):
        super(TestDistributorsHandler, self).setUp()
        self.headers = {
            'Authorization': config.API_TOKEN
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

    def test_post_returns_created_status(self):
        name = u'Acme'
        request_parameters = {'name': name,
                              'active': True}
        uri = application.router.build(None, 'distributors', None, {})
        response = self.app.post_json(uri, params=request_parameters, headers=self.headers)
        self.assertEqual(201, response.status_code)

    def test_post_create_new_distributor_persists_object(self):
        name = u'Acme'
        request_parameters = {'name': name,
                              'active': True}
        uri = application.router.build(None, 'distributors', None, {})
        self.app.post_json(uri, params=request_parameters, headers=self.headers)
        actual = Distributor.find_by_name(request_parameters['name'])
        self.assertIsNotNone(actual)

    def test_post_create_new_distributor_sets_location_header(self):
        name = u'Acme'
        request_parameters = {'name': name,
                              'active': True}
        uri = application.router.build(None, 'distributors', None, {})
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
        uri = application.router.build(None, 'distributors', None, {})
        self.app.post_json(uri, params=request_parameters, headers=self.headers)
        actual = Distributor.find_by_name(request_parameters['name'])
        parent = actual.key.parent().get()
        self.assertEqual(parent.name, self.ENTITY_GROUP_NAME)
