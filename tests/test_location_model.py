import uuid

from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
from models import Tenant, Distributor, Domain, Location

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestLocationModel(BaseTest):
    NAME = 'foobar tenant'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://www.content.com'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    TENANT_CODE = 'foobar'
    ENTITY_GROUP_NAME = 'tenantEntityGroup'
    CURRENT_CLASS_VERSION = 1
    DISTRIBUTOR_NAME = 'Agosto'
    IMPERSONATION_EMAIL = 'test@test.com'
    CUSTOMER_LOCATION_NAME = 'Store #456'
    CUSTOMER_LOCATION_CODE = 'store_456'

    def setUp(self):
        super(TestLocationModel, self).setUp()
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME, active=True)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.distributor_key,
                                    impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                    active=True)
        self.domain_key = self.domain.put()

        self.tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                                    name=self.NAME,
                                    admin_email=self.ADMIN_EMAIL,
                                    content_server_url=self.CONTENT_SERVER_URL,
                                    content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                    domain_key=self.domain_key,
                                    active=True)
        self.tenant_key = self.tenant.put()

    def test_find_locations_of_tenant_paginated(self):
        self.load_tenant_locations(300, self.tenant_key)
        r = Tenant.find_locations_of_tenant_paginated(self.tenant_key, prev_cursor_str=None, next_cursor_str=None)
        self.assertTrue(r["next_cursor"])
        self.assertFalse(r["prev_cursor"])
        self.assertEqual(len(r["objects"]), 25)

        new_r = Tenant.find_locations_of_tenant_paginated(self.tenant_key, prev_cursor_str=None, next_cursor_str=r["next_cursor"])
        self.assertTrue(new_r["next_cursor"])
        self.assertTrue(new_r["prev_cursor"])
        self.assertEqual(len(new_r["objects"]), 25)

        prev_r = Tenant.find_locations_of_tenant_paginated(self.tenant_key, prev_cursor_str=new_r["prev_cursor"], next_cursor_str=None)
        self.assertTrue(prev_r["next_cursor"])
        self.assertFalse(prev_r["prev_cursor"])
        self.assertEqual(len(prev_r["objects"]), 25)

    def load_tenant_locations(self, number_of_locations, tenant_key):
        for x in range(number_of_locations):
            customer_location_name = 'Store #{0}'.format(x)
            customer_location_code = 'store_{0}'.format(x)
            location = Location.create(tenant_key=tenant_key,
                                       customer_location_name=customer_location_name,
                                       customer_location_code=customer_location_code)
            location.put()

    def test_find_by_customer_location_code_returns_expected_location(self):
        location = Location.create(tenant_key=self.tenant_key,
                                   customer_location_name=self.CUSTOMER_LOCATION_NAME,
                                   customer_location_code=self.CUSTOMER_LOCATION_CODE)
        location.put()
        actual = Location.find_by_customer_location_code(self.CUSTOMER_LOCATION_CODE)
        self.assertEqual(actual.customer_location_name, self.CUSTOMER_LOCATION_NAME)

    def test_is_customer_location_code_unique_returns_false_when_code_found(self):
        location = Location.create(tenant_key=self.tenant_key,
                                   customer_location_name=self.CUSTOMER_LOCATION_NAME,
                                   customer_location_code=self.CUSTOMER_LOCATION_CODE)
        location.put()
        uniqueness_check = Location.is_customer_location_code_unique(customer_location_code=self.CUSTOMER_LOCATION_CODE,
                                                                     tenant_key=self.tenant_key)
        self.assertFalse(uniqueness_check)

    def test_is_customer_location_code_unique_returns_true_when_code_not_found(self):
        location_code = str(uuid.uuid4().hex)
        uniqueness_check = Location.is_customer_location_code_unique(customer_location_code=location_code,
                                                                     tenant_key=self.tenant_key)
        self.assertTrue(uniqueness_check)

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        location = Location.create(tenant_key=self.tenant_key,
                                   customer_location_name=self.CUSTOMER_LOCATION_NAME,
                                   customer_location_code=self.CUSTOMER_LOCATION_CODE)
        location.class_version = 47
        location.put()
        self.assertEqual(location.class_version, self.CURRENT_CLASS_VERSION)
