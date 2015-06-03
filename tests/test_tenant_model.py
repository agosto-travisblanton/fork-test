from env_setup import setup_test_paths;

setup_test_paths()

from agar.test import BaseTest
from models import Tenant

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TestTenantModel(BaseTest):
    NAME = 'foobar tenant'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://www.content.com'
    CHROME_DEVICE_DOMAIN = 'bar.com'

    def setUp(self):
        super(TestTenantModel, self).setUp()

    def test_find_by_name_returns_matching_tenant(self):
        tenant = Tenant.create(name=self.NAME,
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               content_server_api_key='',
                               chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                               active=True)
        expected_key = tenant.put()
        actual = Tenant.find_by_name(self.NAME)
        self.assertEqual(actual.key, expected_key)
        self.assertEqual(actual.name, self.NAME)

    def test_find_by_name_returns_none_when_no_matching_tenant_found(self):
        tenant = Tenant.create(name=self.NAME,
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               content_server_api_key='',
                               chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                               active=True)
        tenant.put()
        actual = Tenant.find_by_name('barfood tenant')
        self.assertIsNone(actual)

    def test_create_sets_tenant_active_by_default(self):
        tenant = Tenant.create(name=self.NAME,
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               content_server_api_key='',
                               chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                               active=True)
        tenant.put()
        tenant_created = Tenant.find_by_name(self.NAME)
        self.assertTrue(tenant_created.active)
