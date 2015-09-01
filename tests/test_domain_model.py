from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
from models import Domain, Distributor

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestDomainModel(BaseTest):
    DISTRIBUTOR_NAME = 'agosto'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    CURRENT_CLASS_VERSION = 1

    def setUp(self):
        super(TestDomainModel, self).setUp()
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
                                              active=True)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.distributor_key,
                                    active=True)
        self.domain_key = self.domain.put()

    def test_create_sets_distributor_key(self):
        domain = Domain.find_by_name(self.CHROME_DEVICE_DOMAIN)
        self.assertEqual(domain.distributor_key, self.distributor_key)

    def test_find_by_name_returns_expected_domain_representation(self):
        domain = Domain.find_by_name(self.CHROME_DEVICE_DOMAIN)
        self.assertEqual(domain.distributor_key, self.distributor_key)
        self.assertEqual(domain.name, self.CHROME_DEVICE_DOMAIN)
        self.assertTrue(domain.active)
        self.assertIsNotNone(domain.created)

    def test_create_sets_an_inactive_domain(self):
        name = 'some domain'
        domain = Domain.create(name=name,
                               distributor_key=self.distributor_key,
                               active=False)
        domain.put()
        domain_created = Domain.find_by_name(name)
        self.assertEqual(domain_created.name, name)
        self.assertFalse(domain_created.active)

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        self.domain.class_version = 47
        self.domain.put()
        self.assertEqual(self.domain.class_version, self.CURRENT_CLASS_VERSION)
