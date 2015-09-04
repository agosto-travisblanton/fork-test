from env_setup import setup_test_paths

setup_test_paths()

import json
from content_manager_api import ContentManagerApi
from agar.test import BaseTest, WebTest
from models import Tenant, TENANT_ENTITY_GROUP_NAME, Distributor, Domain
from routes import application
from mockito import when, any as any_matcher
from app_config import config


class TestTenantsHandler(BaseTest, WebTest):
    APPLICATION = application
    ADMIN_EMAIL = "foo{0}@bar.com"
    API_KEY = "SOME_KEY_{0}"
    CONTENT_SERVER_URL = 'https://skykit-contentmanager-int.appspot.com/content'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    DISTRIBUTOR_NAME = 'agosto'
    IMPERSONATION_EMAIL = 'test@test.com'

    def setUp(self):
        super(TestTenantsHandler, self).setUp()
        self.headers = {
            'Authorization': config.API_TOKEN
        }
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
                                              active=True)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.distributor_key,
                                    impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                    active=True)
        self.domain_key = self.domain.put()

    def test_get_by_id_returns_ok_status(self):
        tenant_keys = self.load_tenants()
        request_parameters = {}
        uri = application.router.build(None, 'manage-tenant', None, {'tenant_key': tenant_keys[0].urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        self.assertOK(response)

    def test_get_by_id_returns_tenant_representation(self):
        tenant_keys = self.load_tenants()
        request_parameters = {}
        uri = application.router.build(None, 'manage-tenant', None, {'tenant_key': tenant_keys[0].urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        expected = tenant_keys[0].get()
        self.assertEqual(response_json.get('key'), expected.key.urlsafe())
        self.assertEqual(response_json.get('name'), expected.name)
        self.assertEqual(response_json.get('created'), expected.created.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response_json.get('updated'), expected.updated.strftime('%Y-%m-%d %H:%M:%S'))

    def test_get_returns_ok_status(self):
        self.load_tenants()
        request_parameters = {}
        uri = application.router.build(None, 'tenants', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        self.assertOK(response)

    def test_get_returns_json_resources(self):
        self.load_tenants()
        request_parameters = {}
        uri = application.router.build(None, 'tenants', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), 5)

    def test_post_returns_created_status(self):
        name = u'ABC'
        admin_email = u'foo@bar.com'
        when(ContentManagerApi).create_tenant(name, admin_email).thenReturn(str('some key'))
        when(ContentManagerApi).create_tenant(any_matcher()).thenReturn(True)
        request_parameters = {'name': name,
                              'tenant_code': 'acme',
                              'admin_email': admin_email,
                              'content_server_url': 'https://www.foo.com',
                              'chrome_device_domain': '',
                              'content_server_api_key': 'dfhajskdhahdfyyadfgdfhgjkdhlf',
                              'domain_key': self.domain_key.urlsafe(),
                              'active': True}
        uri = application.router.build(None, 'tenants', None, {})
        when(Domain).find_by_name(any_matcher()).thenReturn(self.domain)
        response = self.app.post_json(uri, params=request_parameters, headers=self.headers)
        self.assertEqual(201, response.status_code)

    def test_post_create_new_tenant_persists_object(self):
        name = u'ABC'
        admin_email = u'foo@bar.com'
        when(ContentManagerApi).create_tenant(name, admin_email).thenReturn(str('some key'))
        when(ContentManagerApi).create_tenant(any_matcher()).thenReturn(True)
        request_parameters = {'name': name,
                              'tenant_code': 'acme',
                              'admin_email': admin_email,
                              'content_server_url': 'https://www.foo.com',
                              'content_server_api_key': 'dfhajskdhahdfyyadfgdfhgjkdhlf',
                              'chrome_device_domain': '',
                              'domain_key': self.domain_key.urlsafe(),
                              'active': True}
        uri = application.router.build(None, 'tenants', None, {})
        when(Domain).find_by_name(any_matcher()).thenReturn(self.domain)
        self.app.post_json(uri, params=request_parameters, headers=self.headers)
        actual = Tenant.find_by_name(request_parameters['name'])
        self.assertIsNotNone(actual)

    def test_post_create_new_tenant_sets_location_header(self):
        name = u'ABC'
        admin_email = u'foo@bar.com'
        when(ContentManagerApi).create_tenant(name, admin_email).thenReturn(str('some key'))
        when(ContentManagerApi).create_tenant(any_matcher()).thenReturn(True)
        request_parameters = {'name': name,
                              'tenant_code': 'acme',
                              'admin_email': admin_email,
                              'content_server_url': 'https://www.foo.com',
                              'content_server_api_key': 'dfhajskdhahdfyyadfgdfhgjkdhlf',
                              'chrome_device_domain': '',
                              'domain_key': self.domain_key.urlsafe(),
                              'active': True}
        uri = application.router.build(None, 'tenants', None, {})
        when(Domain).find_by_name(any_matcher()).thenReturn(self.domain)
        response = self.app.post_json(uri, params=request_parameters, headers=self.headers)
        actual = Tenant.find_by_name(request_parameters['name'])
        tenant_uri = application.router.build(None,
                                              'manage-tenant',
                                              None,
                                              {'tenant_key': actual.key.urlsafe()})
        self.assertTrue(tenant_uri in response.headers.get('Location'))

    def test_post_create_object_has_expected_parent(self):
        name = u'ABC'
        admin_email = u'foo@bar.com'
        when(ContentManagerApi).create_tenant(name, admin_email).thenReturn(str('some key'))
        when(ContentManagerApi).create_tenant(any_matcher()).thenReturn(True)
        request_parameters = {'name': name,
                              'tenant_code': 'acme',
                              'admin_email': admin_email,
                              'content_server_url': 'https://www.foo.com',
                              'content_server_api_key': 'dfhajskdhahdfyyadfgdfhgjkdhlf',
                              'chrome_device_domain': '',
                              'domain_key': self.domain_key.urlsafe(),
                              'active': True}
        uri = application.router.build(None, 'tenants', None, {})
        when(Domain).find_by_name(any_matcher()).thenReturn(self.domain)
        self.app.post_json(uri, params=request_parameters, headers=self.headers)
        actual = Tenant.find_by_name(request_parameters['name'])
        parent = actual.key.parent().get()
        self.assertEqual(parent.name, TENANT_ENTITY_GROUP_NAME)

    # TODO put back into play after uncommenting the call to content mgr
    # def test_post_content_manager_api_collaboration(self):
    #     when(ContentManagerApi).create_tenant(any_matcher()).thenReturn(True)
    #     request_parameters = {'name': 'ABC',
    #                           'tenant_code': 'acme',
    #                           'admin_email': 'foo@bar.com',
    #                           'content_server_url': 'https://www.foo.com',
    #                           'content_server_api_key': 'dfhajskdhahdfyyadfgdfhgjkdhlf',
    #                           'chrome_device_domain': '',
    #                           'active': True}
    #     uri = application.router.build(None, 'tenants', None, {})
    #     self.app.post(uri, json.dumps(request_parameters), headers=self.headers)
    #     verify(ContentManagerApi, times=1).create_tenant(any_matcher(''))

    def test_put_returns_no_content_status(self):
        tenant_keys = self.load_tenants()
        uri = application.router.build(None, 'manage-tenant', None, {'tenant_key': tenant_keys[0].urlsafe()})
        entity_body = {
            'name': 'foobar',
            'tenant_code': 'acme',
            'admin_email': 'foo@bar.com',
            'content_server_url': 'https://www.foo.com',
            'content_server_api_key': 'some key',
            'chrome_device_domain': 'some domain',
            'active': True
        }
        response = self.app.put_json(uri, entity_body, headers=self.headers)
        self.assertEqual(204, response.status_code)

    def test_put_updates_selected_properties(self):
        tenant_keys = self.load_tenants()
        uri = application.router.build(None, 'manage-tenant', None, {'tenant_key': tenant_keys[0].urlsafe()})
        expected = tenant_keys[0].get()
        self.assertEqual(expected.name, 'Testing tenant 0')
        self.assertEqual(expected.active, True)
        entity_body = {
            'name': 'foobar',
            'tenant_code': 'acme',
            'admin_email': 'foo@bar.com',
            'content_server_url': 'https://www.foo.com',
            'content_server_api_key': 'some key',
            'chrome_device_domain': 'some domain',
            'active': False
        }
        self.app.put_json(uri, entity_body, headers=self.headers)
        self.assertEqual(expected.name, 'foobar')
        self.assertEqual(expected.active, False)

    def test_delete_returns_no_content_status(self):
        tenant_keys = self.load_tenants()
        uri = application.router.build(None, 'manage-tenant', None, {'tenant_key': tenant_keys[0].urlsafe()})
        response = self.app.delete(uri, headers=self.headers)
        self.assertEqual(204, response.status_code)

    def test_delete_soft_deletes_tenant(self):
        tenant_keys = self.load_tenants()
        url_safe_tenant_key = tenant_keys[0].urlsafe()
        request_parameters = {}
        uri = application.router.build(None, 'manage-tenant', None, {'tenant_key': url_safe_tenant_key})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertIsNotNone(response_json)

        uri = application.router.build(None, 'manage-tenant', None, {'tenant_key': url_safe_tenant_key})
        self.app.delete(uri, headers=self.headers)

        uri = application.router.build(None, 'manage-tenant', None, {'tenant_key': url_safe_tenant_key})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(response_json.get('active'), False)

    def load_tenants(self):
        tenant_keys = []
        distributor = Distributor.create(name='agosto',
                                         active=True)
        distributor_key = distributor.put()
        domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                               distributor_key=distributor_key,
                               impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                               active=True)
        domain_key = domain.put()
        for x in range(5):
            tenant = Tenant.create(tenant_code='acme',
                                   name="Testing tenant {0}".format(x),
                                   admin_email=self.ADMIN_EMAIL.format(x),
                                   content_server_url=self.CONTENT_SERVER_URL,
                                   content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                   chrome_device_domain='testing.skykit.com',
                                   domain_key=domain_key,
                                   active=True)
            tenant_key = tenant.put()
            tenant_keys.append(tenant_key)
        return tenant_keys
