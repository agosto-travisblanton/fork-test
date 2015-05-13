from agar.test import BaseTest
from models import Tenant

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TestTenantModel(BaseTest):
    NAME = 'foobar tenant'

    def setUp(self):
        super(TestTenantModel, self).setUp()

    def testFindByName_ReturnsMatchingTenant(self):
        tenant = Tenant(name=self.NAME)
        expected_key = tenant.put()
        actual = Tenant.find_by_name(self.NAME)
        self.assertEqual(actual.key, expected_key)
        self.assertEqual(actual.name, self.NAME)

    def testFindByName_ReturnsNone_WhenNoMatchingTenantFound(self):
        tenant = Tenant(name=self.NAME)
        expected_key = tenant.put()
        actual = Tenant.find_by_name('barfood tenant')
        self.assertIsNone(actual)
