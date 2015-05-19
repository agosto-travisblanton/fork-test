from env_setup import setup_test_paths; setup_test_paths()

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

    def testFindByName_ReturnsMatchingTenant(self):
        tenant = Tenant.create(name=self.NAME,
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               chrome_device_domain=self.CHROME_DEVICE_DOMAIN)
        expected_key = tenant.put()
        actual = Tenant.find_by_name(self.NAME)
        self.assertEqual(actual.key, expected_key)
        self.assertEqual(actual.name, self.NAME)

    def testFindByName_ReturnsNone_WhenNoMatchingTenantFound(self):
        tenant = Tenant.create(name=self.NAME,
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               chrome_device_domain=self.CHROME_DEVICE_DOMAIN)
        tenant.put()
        actual = Tenant.find_by_name('barfood tenant')
        self.assertIsNone(actual)

    def testCreate_AutoGeneratesContentServerApiKey(self):
        tenant = Tenant.create(name=self.NAME,
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               chrome_device_domain=self.CHROME_DEVICE_DOMAIN)
        tenant.put()
        tenant_created = Tenant.find_by_name(self.NAME)
        generated_key = tenant_created.content_server_api_key
        print "Generated api key: ", generated_key
        self.assertIsNotNone(generated_key)

    def testCreate_SetsTenantActiveByDefault(self):
        tenant = Tenant.create(name=self.NAME,
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               chrome_device_domain=self.CHROME_DEVICE_DOMAIN)
        tenant.put()
        tenant_created = Tenant.find_by_name(self.NAME)
        self.assertTrue(tenant_created.active)
