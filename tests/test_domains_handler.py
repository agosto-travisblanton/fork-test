from env_setup import setup_test_paths
from utils.web_util import build_uri
from webtest import AppError

setup_test_paths()

import json
from tests.provisioning_base_test import ProvisioningBaseTest
from routes import application
from models import Distributor, Domain
from app_config import config


class TestDomainsHandler(ProvisioningBaseTest):
    APPLICATION = application
    DISTRIBUTOR_NAME = 'agosto'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    CHROME_DEVICE_DOMAIN_INACTIVE = 'inactive.agosto.com'
    FORBIDDEN = '403 Forbidden'
    IMPERSONATION_EMAIL = 'test@test.com'

    def setUp(self):
        super(TestDomainsHandler, self).setUp()
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
                                              active=True)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.distributor_key,
                                    impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                    active=True)
        self.domain_key = self.domain.put()
        self.inactive_domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN_INACTIVE,
                                             distributor_key=self.distributor_key,
                                             impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                             active=False)
        self.inactive_domain_key = self.inactive_domain.put()
        self.headers = {
            'Authorization': config.API_TOKEN,
            'X-Provisioning-Distributor': self.distributor_key.urlsafe()
        }
        self.bad_authorization_header = {
            'Authorization': 'Forget about it!',
            'X-Provisioning-Distributor': self.distributor_key.urlsafe()
        }

    ##################################################################################################################
    ## post
    ##################################################################################################################
    def test_post_returns_created_status(self):
        request_parameters = {'name': 'dev1.agosto.com',
                              'active': True,
                              'impersonation_admin_email_address': self.IMPERSONATION_EMAIL,
                              'distributor_key': self.distributor_key.urlsafe()}
        uri = application.router.build(None, 'domains', None, {})
        response = self.app.post_json(uri, params=request_parameters, headers=self.headers)
        self.assertEqual(201, response.status_int)

    def test_post_create_new_domain_persists_object(self):
        request_parameters = {'name': 'dev2.agosto.com',
                              'active': True,
                              'impersonation_admin_email_address': self.IMPERSONATION_EMAIL,
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
                              'impersonation_admin_email_address': self.IMPERSONATION_EMAIL,
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

    def test_post_fails_without_distributor_key(self):
        headers = {
            'Authorization': config.API_TOKEN,
            'X-Provisioning-Distributor': ''
        }

        request_body = {'name': 'dev3.agosto.com',
                        'active': True,
                        'impersonation_admin_email_address': self.IMPERSONATION_EMAIL}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/domains', json.dumps(request_body), headers=headers)
        self.assertTrue('Bad response: 400 The distributor_key parameter is invalid.'
                        in context.exception.message)

    def test_post_fails_without_name_parameter(self):
        request_body = {'name': None,
                        'active': True,
                        'impersonation_admin_email_address': self.IMPERSONATION_EMAIL,
                        'distributor_key': self.distributor_key.urlsafe()}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/domains', json.dumps(request_body), headers=self.headers)
        self.assertTrue('Bad response: 400 The name parameter is invalid.'
                        in context.exception.message)

    def test_post_fails_without_active_parameter(self):
        request_body = {'name': 'dev4.agosto.com',
                        'active': None,
                        'impersonation_admin_email_address': self.IMPERSONATION_EMAIL,
                        'distributor_key': self.distributor_key.urlsafe()}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/domains', json.dumps(request_body), headers=self.headers)
        self.assertTrue('Bad response: 400 The active parameter is invalid.'
                        in context.exception.message)

    def test_post_fails_without_impersonation_admin_email_address_parameter(self):
        request_body = {'name': 'dev5.agosto.com',
                        'active': True,
                        'impersonation_admin_email_address': None,
                        'distributor_key': self.distributor_key.urlsafe()}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/domains', json.dumps(request_body), headers=self.headers)
        self.assertTrue('Bad response: 400 The impersonation_admin_email_address parameter is invalid.'
                        in context.exception.message)

    def test_post_fails_without_request_body(self):
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/domains', {}, headers=self.headers)
        self.assertTrue('Bad response: 400 Did not receive request body.'
                        in context.exception.message)

    def test_post_fails_with_existing_domain(self):
        request_parameters = {'name': self.CHROME_DEVICE_DOMAIN,
                              'active': True,
                              'impersonation_admin_email_address': self.IMPERSONATION_EMAIL,
                              'distributor_key': self.distributor_key.urlsafe()}
        uri = application.router.build(None, 'domains', None, {})
        with self.assertRaises(AppError) as context:
            self.app.post_json(uri, params=request_parameters, headers=self.headers)
        self.assertTrue('409 Conflict. Domain name "{0}" is in use.'.format(self.CHROME_DEVICE_DOMAIN)
                        in context.exception.message)

    ##################################################################################################################
    ## get
    ##################################################################################################################
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
        response = self.get(uri, params=request_parameters, headers=self.headers)
        self.assertOK(response)

    def test_get_list_returns_only_active_domains(self):
        request_parameters = {}
        uri = application.router.build(None, 'domains', None, {})
        response = self.get(uri, params=request_parameters, headers=self.headers)
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

    ##################################################################################################################
    ## put
    ##################################################################################################################

    def test_device_resource_put_no_authorization_header_returns_forbidden(self):
        request_body = {'active': True}
        uri = build_uri('manage-domain', params_dict={'domain_key': self.domain_key.urlsafe()})
        response = self.put(uri, params=request_body, headers=self.bad_authorization_header)
        self.assertForbidden(response)

    def test_put_http_status_no_content(self):
        request_body = {'active': True}
        uri = build_uri('manage-domain', params_dict={'domain_key': self.domain_key.urlsafe()})
        response = self.put(uri, params=json.dumps(request_body), headers=self.headers)
        self.assertEqual('204 No Content', response.status)

    def test_put_updates_domain_entity_active_to_false(self):
        active = False
        request_body = {'active': active}
        uri = build_uri('manage-domain', params_dict={'domain_key': self.domain_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.headers)
        updated_domain = self.domain_key.get()
        self.assertFalse(updated_domain.active)

    ##################################################################################################################
    ## delete
    ##################################################################################################################

    def test_delete_returns_no_content_status(self):
        uri = build_uri('manage-domain', params_dict={'domain_key': self.domain_key.urlsafe()})
        response = self.delete(uri, headers=self.headers)
        self.assertEqual(204, response.status_int)

    def test_delete_soft_deletes_domain(self):
        request_parameters = {}
        uri = build_uri('manage-domain', params_dict={'domain_key': self.domain_key.urlsafe()})
        response = self.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(response_json.get('active'), True)

        self.delete(uri, headers=self.headers)

        response = self.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(response_json.get('active'), False)
