from content_manager_api import ContentManagerApi
from env_setup import setup_test_paths;

setup_test_paths()

import json

from agar.test import BaseTest, WebTest
from models import Tenant, TenantEntityGroup
from routes import application
from mockito import when, verify, any as any_matcher
from app_config import config


class TestTenantsHandler(BaseTest, WebTest):
    APPLICATION = application
    ADMIN_EMAIL = "foo{0}@bar.com"
    API_KEY = "SOME_KEY_{0}"
    CONTENT_SERVER_URL = 'https://www.content.com'

    def setUp(self):
        super(TestTenantsHandler, self).setUp()
        self.headers = {
            'Authorization': config.API_TOKEN
        }

    def test_get_by_id_returns_ok_status(self):
        tenant_keys = self.load_tenants()
        request_parameters = {}
        uri = application.router.build(None, 'manage-tenant', None, {'tenant_key': tenant_keys[0].urlsafe()})
        response = self.app.get(uri, params=request_parameters)
        self.assertOK(response)

    def test_get_by_id_returns_tenant_representation(self):
        tenant_keys = self.load_tenants()
        request_parameters = {}
        uri = application.router.build(None, 'manage-tenant', None, {'tenant_key': tenant_keys[0].urlsafe()})
        response = self.app.get(uri, params=request_parameters)
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
        response = self.app.get(uri, params=request_parameters)
        self.assertOK(response)

    def test_get_returns_json_resources(self):
        self.load_tenants()
        request_parameters = {}
        uri = application.router.build(None, 'tenants', None, {})
        response = self.app.get(uri, params=request_parameters)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), 5)

    def test_post_content_manager_api_collaboration(self):
        name = u'ABC'
        admin_email = u'foo@bar.com'
        when(ContentManagerApi).create_tenant(name, admin_email).thenReturn('some key')
        request_parameters = {'name': name,
                              'tenant_code': 'acme',
                              'admin_email': admin_email,
                              'content_server_url': 'https://www.foo.com',
                              'content_server_api_key': 'dfhajskdhahdfyyadfgdfhgjkdhlf',
                              'chrome_device_domain': '',
                              'active': True}
        uri = application.router.build(None, 'tenants', None, {})
        self.app.post(uri, json.dumps(request_parameters), headers=self.headers)
        verify(ContentManagerApi, times=1).create_tenant(any_matcher(''), any_matcher(''))

    def test_post_returns_created_status(self):
        name = u'ABC'
        admin_email = u'foo@bar.com'
        when(ContentManagerApi).create_tenant(name, admin_email).thenReturn(str('some key'))
        request_parameters = {'name': name,
                              'tenant_code': 'acme',
                              'admin_email': admin_email,
                              'content_server_url': 'https://www.foo.com',
                              'chrome_device_domain': '',
                              'content_server_api_key': 'dfhajskdhahdfyyadfgdfhgjkdhlf',
                              'active': True}
        uri = application.router.build(None, 'tenants', None, {})
        response = self.app.post_json(uri, params=request_parameters)
        self.assertEqual(201, response.status_code)

    def test_post_create_new_tenant_persists_object(self):
        name = u'ABC'
        admin_email = u'foo@bar.com'
        when(ContentManagerApi).create_tenant(name, admin_email).thenReturn(str('some key'))
        request_parameters = {'name': name,
                              'tenant_code': 'acme',
                              'admin_email': admin_email,
                              'content_server_url': 'https://www.foo.com',
                              'content_server_api_key': 'dfhajskdhahdfyyadfgdfhgjkdhlf',
                              'chrome_device_domain': '',
                              'active': True}
        uri = application.router.build(None, 'tenants', None, {})
        self.app.post_json(uri, params=request_parameters)
        actual = Tenant.find_by_name(request_parameters['name'])
        self.assertIsNotNone(actual)

    def test_post_create_new_tenant_persists_key_from_content_server(self):
        name = u'ABC'
        admin_email = u'foo@bar.com'
        content_server_api_key = u'key me up jeeves'
        when(ContentManagerApi).create_tenant(name, admin_email).thenReturn(content_server_api_key)
        request_parameters = {'name': name,
                              'tenant_code': 'acme',
                              'admin_email': admin_email,
                              'content_server_url': 'https://www.foo.com',
                              'content_server_api_key': content_server_api_key,
                              'chrome_device_domain': '',
                              'active': True}
        uri = application.router.build(None, 'tenants', None, {})
        self.app.post_json(uri, params=request_parameters)
        actual = Tenant.find_by_name(request_parameters['name'])
        self.assertEqual(content_server_api_key, actual.content_server_api_key)

    def test_post_create_new_tenant_sets_location_header(self):
        name = u'ABC'
        admin_email = u'foo@bar.com'
        when(ContentManagerApi).create_tenant(name, admin_email).thenReturn(str('some key'))
        request_parameters = {'name': name,
                              'tenant_code': 'acme',
                              'admin_email': admin_email,
                              'content_server_url': 'https://www.foo.com',
                              'content_server_api_key': 'dfhajskdhahdfyyadfgdfhgjkdhlf',
                              'chrome_device_domain': '',
                              'active': True}
        uri = application.router.build(None, 'tenants', None, {})
        response = self.app.post_json(uri, params=request_parameters)
        actual = Tenant.find_by_name(request_parameters['name'])
        tenant_uri = application.router.build(None,
                                              'manage-tenant',
                                              None,
                                              {'tenant_key': actual.key.urlsafe()})
        self.assertTrue(tenant_uri in response.headers.get('Location'))

    def test_post_create_when_content_manager_fails_to_return_key(self):
        name = u'ABC'
        admin_email = u'foo@bar.com'
        when(ContentManagerApi).create_tenant(name, admin_email).thenReturn(None)
        request_parameters = {'name': name,
                              'tenant_code': 'acme',
                              'admin_email': admin_email,
                              'content_server_url': 'https://www.foo.com',
                              'chrome_device_domain': '',
                              'active': True}
        uri = application.router.build(None, 'tenants', None, {})
        with self.assertRaises(Exception) as context:
            self.app.post_json(uri, params=request_parameters)
        self.assertTrue('422 Unable to obtain content server key' in str(context.exception))

    def test_put_returns_no_content_status(self):
        tenant_keys = self.load_tenants()
        uri = application.router.build(None, 'manage-tenant', None, {'tenant_key': tenant_keys[0].urlsafe()})
        response = self.app.put_json(uri, {'name': 'foobar',
                                           'tenant_code': 'acme',
                                           'admin_email': 'foo@bar.com',
                                           'content_server_url': 'https://www.foo.com',
                                           'content_server_api_key': 'some key',
                                           'chrome_device_domain': 'some domain',
                                           'active': True})
        self.assertEqual(204, response.status_code)

    def test_put_updates_selected_properties(self):
        tenant_keys = self.load_tenants()
        uri = application.router.build(None, 'manage-tenant', None, {'tenant_key': tenant_keys[0].urlsafe()})
        expected = tenant_keys[0].get()
        self.assertEqual(expected.name, 'Testing tenant 0')
        self.assertEqual(expected.active, True)
        self.app.put_json(uri, {'name': 'foobar',
                                'tenant_code': 'acme',
                                'admin_email': 'foo@bar.com',
                                'content_server_url': 'https://www.foo.com',
                                'content_server_api_key': 'some key',
                                'chrome_device_domain': 'some domain',
                                'active': False})
        self.assertEqual(expected.name, 'foobar')
        self.assertEqual(expected.active, False)

    def test_delete_returns_no_content_status(self):
        tenant_keys = self.load_tenants()
        uri = application.router.build(None, 'manage-tenant', None, {'tenant_key': tenant_keys[0].urlsafe()})
        response = self.app.delete(uri)
        self.assertEqual(204, response.status_code)

    def test_delete_soft_deletes_tenant(self):
        tenant_keys = self.load_tenants()
        url_safe_tenant_key = tenant_keys[0].urlsafe()
        request_parameters = {}
        uri = application.router.build(None, 'manage-tenant', None, {'tenant_key': url_safe_tenant_key})
        response = self.app.get(uri, params=request_parameters)
        response_json = json.loads(response.body)
        self.assertIsNotNone(response_json)

        uri = application.router.build(None, 'manage-tenant', None, {'tenant_key': url_safe_tenant_key})
        self.app.delete(uri)

        uri = application.router.build(None, 'manage-tenant', None, {'tenant_key': url_safe_tenant_key})
        response = self.app.get(uri, params=request_parameters)
        response_json = json.loads(response.body)
        self.assertEqual(response_json.get('active'), False)

    def load_tenants(self):
        tenant_keys = []
        for x in range(5):
            tenant_entity_group = TenantEntityGroup.singleton()
            tenant = Tenant(parent=tenant_entity_group.key,
                            tenant_code='acme',
                            name="Testing tenant {0}".format(x),
                            admin_email=self.ADMIN_EMAIL.format(x),
                            content_server_api_key=self.API_KEY.format(x),
                            content_server_url=self.CONTENT_SERVER_URL)
            tenant_key = tenant.put()
            tenant_keys.append(tenant_key)
        return tenant_keys
