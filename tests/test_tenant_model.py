from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
from models import Tenant

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TestTenantModel(BaseTest):
    NAME = 'foobar tenant'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://www.content.com'
    CONTENT_SERVER_API_KEY = 'API KEY'
    CHROME_DEVICE_DOMAIN = 'bar.com'
    TENANT_CODE = 'foobar'

    def setUp(self):
        super(TestTenantModel, self).setUp()

    def test_find_by_name_returns_matching_tenant(self):
        tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                               name=self.NAME,
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               content_server_api_key=self.CONTENT_SERVER_API_KEY,
                               chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                               active=True)
        expected_key = tenant.put()
        actual = Tenant.find_by_name(self.NAME)
        self.assertEqual(actual.key, expected_key)
        self.assertEqual(actual.name, self.NAME)

    def test_find_by_name_returns_none_when_no_matching_tenant_found(self):
        tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                               name=self.NAME,
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               content_server_api_key='',
                               chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                               active=True)
        tenant.put()
        actual = Tenant.find_by_name('barfood tenant')
        self.assertIsNone(actual)

    def test_create_sets_tenant_active_by_default(self):
        tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                               name=self.NAME,
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               content_server_api_key='',
                               chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                               active=True)
        tenant.put()
        tenant_created = Tenant.find_by_name(self.NAME)
        self.assertTrue(tenant_created.active)

    def test_create_sets_tenant_properties(self):
        tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                               name=self.NAME,
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               content_server_api_key=self.CONTENT_SERVER_API_KEY,
                               chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                               active=True)
        tenant.put()
        tenant_created = Tenant.find_by_name(self.NAME)
        self.assertTrue(tenant_created.active)
        self.assertEqual(self.TENANT_CODE, tenant_created.tenant_code)
        self.assertEqual(self.ADMIN_EMAIL, tenant_created.admin_email)
        self.assertEqual(self.CONTENT_SERVER_URL, tenant_created.content_server_url)
        self.assertEqual(self.CONTENT_SERVER_API_KEY, tenant_created.content_server_api_key)
        self.assertEqual(self.CHROME_DEVICE_DOMAIN, tenant_created.chrome_device_domain)
        self.assertEqual(self.NAME, tenant_created.name)
