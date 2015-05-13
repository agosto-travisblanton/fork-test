from agar.test import BaseTest
from models import Tenant

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TestTenantModel(BaseTest):
    NAME = 'foobar tenant'
    ADMIN_EMAIL = 'foo@bar.com'
    API_KEY = 'SOME_KEY'
    CONTENT_SERVER_URL = 'https://www.content.com'

    def setUp(self):
        super(TestTenantModel, self).setUp()

    def testFindByName_ReturnsMatchingTenant(self):
        tenant = Tenant(name=self.NAME,
                        admin_email=self.ADMIN_EMAIL,
                        content_server_api_key=self.API_KEY,
                        content_server_url=self.CONTENT_SERVER_URL)
        expected_key = tenant.put()
        actual = Tenant.find_by_name(self.NAME)
        self.assertEqual(actual.key, expected_key)
        self.assertEqual(actual.name, self.NAME)

    def testFindByName_ReturnsNone_WhenNoMatchingTenantFound(self):
        tenant = Tenant(name=self.NAME,
                        admin_email=self.ADMIN_EMAIL,
                        content_server_api_key=self.API_KEY,
                        content_server_url=self.CONTENT_SERVER_URL)
        tenant.put()
        actual = Tenant.find_by_name('barfood tenant')
        self.assertIsNone(actual)
