import json

from env_setup import setup_test_paths

setup_test_paths()

from webtest import AppError
from agar.test import BaseTest, WebTest
from models import Distributor, Domain
from routes import application
from app_config import config


class TestDomainsHandler(BaseTest, WebTest):
    APPLICATION = application
    DISTRIBUTOR_NAME = 'agosto'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    CHROME_DEVICE_DOMAIN_INACTIVE = 'inactive.agosto.com'
    FORBIDDEN = '403 Forbidden'

    def setUp(self):
        super(TestDomainsHandler, self).setUp()
        self.headers = {
            'Authorization': config.API_TOKEN
        }
        self.bad_authorization_header = {
            'Authorization': 'Forget about it!'
        }
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
                                              active=True)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.distributor_key,
                                    active=True)
        self.domain_key = self.domain.put()
        self.inactive_domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN_INACTIVE,
                                             distributor_key=self.distributor_key,
                                             active=False)
        self.inactive_domain_key = self.inactive_domain.put()

    def test_post_returns_created_status(self):
        request_parameters = {'name': self.CHROME_DEVICE_DOMAIN,
                              'active': True,
                              'distributor_key': self.distributor_key.urlsafe()}
        uri = application.router.build(None, 'domains', None, {})
        response = self.app.post_json(uri, params=request_parameters, headers=self.headers)
        self.assertEqual(201, response.status_code)

    def test_post_create_new_domain_persists_object(self):
        request_parameters = {'name': self.CHROME_DEVICE_DOMAIN,
                              'active': True,
                              'distributor_key': self.distributor_key.urlsafe()}
        uri = application.router.build(None, 'domains', None, {})
        self.app.post_json(uri, params=request_parameters, headers=self.headers)
        actual = Domain.find_by_name(self.CHROME_DEVICE_DOMAIN)
        self.assertIsNotNone(actual)
        self.assertEqual(actual.name, self.CHROME_DEVICE_DOMAIN)

    def test_post_create_new_domain_sets_location_header(self):
        name = 'something.agosto.com'
        request_parameters = {'name': name,
                              'active': True,
                              'distributor_key': self.distributor_key.urlsafe()}
        uri = application.router.build(None, 'domains', None, {})
        response = self.app.post_json(uri, params=request_parameters, headers=self.headers)
        actual = Domain.find_by_name(name)
        domain_uri = application.router.build(None, 'manage-domain', None, {'domain_key': actual.key.urlsafe()})
        self.assertTrue(domain_uri in response.headers.get('Location'))

    def test_post_fails_with_bad_authorization_token(self):
        request_parameters = {}
        uri = application.router.build(None, 'domains', None, {})
        with self.assertRaises(AppError) as context:
            self.app.post_json(uri, params=request_parameters, headers=self.bad_authorization_header)
        self.assertTrue(self.FORBIDDEN in context.exception.message)

    def test_get_by_key_returns_ok_status(self):
        request_parameters = {}
        uri = application.router.build(None, 'manage-domain', None, {'domain_key': self.domain_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        self.assertOK(response)

    def test_get_by_key_returns_domain_representation(self):
        request_parameters = {}
        uri = application.router.build(None, 'manage-domain', None, {'domain_key': self.domain_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        expected = self.domain_key.get()
        self.assertEqual(response_json.get('key'), expected.key.urlsafe())
        self.assertEqual(response_json.get('name'), self.CHROME_DEVICE_DOMAIN)
        self.assertEqual(response_json.get('active'), expected.active)
        self.assertEqual(response_json.get('created'), expected.created.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response_json.get('updated'), expected.updated.strftime('%Y-%m-%d %H:%M:%S'))

    def test_get_list_returns_ok_status(self):
        request_parameters = {}
        uri = application.router.build(None, 'domains', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        self.assertOK(response)

    def test_get_list_returns_only_active_domains(self):
        request_parameters = {}
        uri = application.router.build(None, 'domains', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0].get('name'), self.CHROME_DEVICE_DOMAIN)
        self.assertTrue(response_json[0].get('active'))

    def test_get_fails_with_bad_authorization_token(self):
        request_parameters = {}
        uri = application.router.build(None, 'domains', None, {})
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.bad_authorization_header)
        self.assertTrue(self.FORBIDDEN in context.exception.message)
