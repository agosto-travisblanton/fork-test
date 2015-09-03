from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
from models import Tenant, Distributor, TENANT_ENTITY_GROUP_NAME, Domain

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TestTenantModel(BaseTest):
    NAME = 'foobar tenant'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://www.content.com'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
    CONTENT_SERVER_API_KEY = 'API KEY'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    TENANT_CODE = 'foobar'
    ENTITY_GROUP_NAME = 'tenantEntityGroup'
    CURRENT_CLASS_VERSION = 1
    DISTRIBUTOR_NAME = 'Agosto'
    IMPERSONATION_EMAIL = 'test@test.com'

    def setUp(self):
        super(TestTenantModel, self).setUp()
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
                                    chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                                    domain_key=self.domain_key,
                                    active=True)
        self.tenant_key = self.tenant.put()

    def test_create_sets_tenant_entity_group_as_parent(self):
        actual = Tenant.find_by_name(self.NAME)
        parent = actual.key.parent().get()
        self.assertEqual(parent.name, TENANT_ENTITY_GROUP_NAME)

    def test_find_by_name_returns_matching_tenant(self):
        actual = Tenant.find_by_name(self.NAME)
        self.assertEqual(actual.key, self.tenant_key)
        self.assertEqual(actual.name, self.NAME)

    def test_find_by_name_returns_none_when_no_matching_tenant_found(self):
        actual = Tenant.find_by_name('barfood tenant')
        self.assertIsNone(actual)

    def test_create_sets_an_inactive_tenant(self):
        name = 'Inactive Tenant'
        inactive_tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                                        name=name,
                                        admin_email=self.ADMIN_EMAIL,
                                        content_server_url=self.CONTENT_SERVER_URL,
                                        content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                        chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                                        domain_key=self.domain_key,
                                        active=False)
        inactive_tenant.put()
        tenant_created = Tenant.find_by_name(name)
        self.assertEqual(tenant_created.name, name)
        self.assertFalse(tenant_created.active)

    def test_create_sets_tenant_properties(self):
        tenant_created = Tenant.find_by_name(self.NAME)
        self.assertTrue(tenant_created.active)
        self.assertEqual(self.TENANT_CODE, tenant_created.tenant_code)
        self.assertEqual(self.ADMIN_EMAIL, tenant_created.admin_email)
        self.assertEqual(self.CONTENT_SERVER_URL, tenant_created.content_server_url)
        self.assertEqual(self.CONTENT_MANAGER_BASE_URL, tenant_created.content_manager_base_url)
        self.assertEqual(self.CHROME_DEVICE_DOMAIN, tenant_created.chrome_device_domain)
        self.assertEqual(self.NAME, tenant_created.name)
        self.assertEqual(self.domain_key, tenant_created.domain_key)

    def test_is_unique_returns_false_when_name_is_found(self):
        uniqueness_check = Tenant.is_unique(self.NAME)
        self.assertFalse(uniqueness_check)

    def test_is_unique_returns_true_when_name_not_found(self):
        uniqueness_check = Tenant.is_unique('Foobar')
        self.assertTrue(uniqueness_check)

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        self.tenant.class_version = 47
        self.tenant.put()
        self.assertEqual(self.tenant.class_version, self.CURRENT_CLASS_VERSION)

    def test_find_by_tenant_code_returns_entity_instance(self):
        actual = Tenant.find_by_tenant_code(self.tenant.tenant_code)
        self.assertEqual(actual.key, self.tenant.key)

    def test_find_by_tenant_code_returns_none(self):
        actual = Tenant.find_by_tenant_code('kdjfashdfjkah')
        self.assertIsNone(actual)
