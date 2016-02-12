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
    LOCATION_NAME = 'Store #456'
    LOCATION_CODE = 'store_456'
    TIMEZONE = 'US/Arizona'
    TIMEZONE_OFFSET = -7

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

    def test_find_by_location_code_returns_expected_location(self):
        location = Location.create(tenant_key=self.tenant_key,
                                   name=self.LOCATION_NAME,
                                   location_code=self.LOCATION_CODE,
                                   timezone=self.TIMEZONE)
        location.put()
        actual = Location.find_by_location_code(self.LOCATION_CODE)
        self.assertEqual(actual.name, self.LOCATION_NAME)

    def test_create_returns_expected_timezone_offset(self):
        location = Location.create(tenant_key=self.tenant_key,
                                   name=self.LOCATION_NAME,
                                   location_code=self.LOCATION_CODE,
                                   timezone=self.TIMEZONE)
        location.put()
        actual = Location.find_by_location_code(self.LOCATION_CODE)
        self.assertEqual(actual.timezone_offset, self.TIMEZONE_OFFSET)

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        location = Location.create(tenant_key=self.tenant_key,
                                   name=self.LOCATION_NAME,
                                   location_code=self.LOCATION_CODE,
                                   timezone=self.TIMEZONE)
        location.class_version = 47
        location.put()
        self.assertEqual(location.class_version, self.CURRENT_CLASS_VERSION)
