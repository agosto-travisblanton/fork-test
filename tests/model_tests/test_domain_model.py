from app_config import config
from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
from models import Domain, Distributor

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestDomainModel(BaseTest):
    DISTRIBUTOR_NAME = 'agosto'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    CURRENT_CLASS_VERSION = 1
    IMPERSONATION_EMAIL = 'test@test.com'
    OU_PATH = '/abc/123/skykit'

    def setUp(self):
        super(TestDomainModel, self).setUp()
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
                                              active=True)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.distributor_key,
                                    impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                    active=True)
        self.domain_key = self.domain.put()

    def test_create_sets_distributor_key(self):
        domain = Domain.find_by_name(self.CHROME_DEVICE_DOMAIN)
        self.assertEqual(domain.distributor_key, self.distributor_key)

    def test_find_by_name_returns_expected_domain_representation(self):
        domain = Domain.find_by_name(self.CHROME_DEVICE_DOMAIN)
        domain.organization_path = self.OU_PATH
        self.assertEqual(domain.distributor_key, self.distributor_key)
        self.assertEqual(domain.name, self.CHROME_DEVICE_DOMAIN)
        self.assertEqual(domain.impersonation_admin_email_address, self.IMPERSONATION_EMAIL)
        self.assertTrue(domain.active)
        self.assertEqual(self.OU_PATH, domain.organization_path)
        self.assertIsNotNone(domain.created)

    def test_create_sets_an_inactive_domain(self):
        name = 'some domain'
        domain = Domain.create(name=name,
                               distributor_key=self.distributor_key,
                               impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                               active=False)
        domain.put()
        domain_created = Domain.find_by_name(name)
        self.assertEqual(domain_created.name, name)
        self.assertFalse(domain_created.active)

    def test_get_distributor_returns_distributor_representation(self):
        distributor = self.domain.get_distributor()
        self.assertEqual(distributor.name, self.DISTRIBUTOR_NAME)

    def test_get_distributor_returns_distributor_default_properties(self):
        distributor = self.domain.get_distributor()
        self.assertEqual(distributor.content_manager_url, config.DEFAULT_CONTENT_MANAGER_URL)
        self.assertEqual(distributor.player_content_url, config.DEFAULT_PLAYER_CONTENT_URL)

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        self.domain.class_version = 47
        self.domain.put()
        self.assertEqual(self.domain.class_version, self.CURRENT_CLASS_VERSION)

    def test_already_exists_for_existing_active(self):
        name = 'existing-active.skykit.com'
        domain = Domain.create(name=name,
                               distributor_key=self.distributor_key,
                               impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                               active=True)
        domain.put()
        self.assertTrue(Domain.already_exists(name))

    def test_already_exists_for_existing_active_false(self):
        name = 'existing-non-active.skykit.com'
        domain = Domain.create(name=name,
                               distributor_key=self.distributor_key,
                               impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                               active=False)
        domain.put()
        self.assertFalse(Domain.already_exists(name))

    def test_already_exists_for_non_existing(self):
        name = 'non-existing.skykit.com'
        self.assertFalse(Domain.already_exists(name))

    def test_get_impersonation_email_when_domain_name_found(self):
        expected_impersonation_email = Domain.get_impersonation_email_by_domain_name(
            domain_name=self.CHROME_DEVICE_DOMAIN)
        self.assertEqual(self.domain.impersonation_admin_email_address, expected_impersonation_email)

    def test_get_impersonation_email_when_domain_name__not_found(self):
        expected = Domain.get_impersonation_email_by_domain_name(domain_name='foobar.com')
        self.assertIsNone(expected)
