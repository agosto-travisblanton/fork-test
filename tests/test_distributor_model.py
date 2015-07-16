from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
from models import Distributor

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestDistributorModel(BaseTest):
    NAME = 'Agosto'
    ENTITY_GROUP_NAME = 'distributorEntityGroup'

    def setUp(self):
        super(TestDistributorModel, self).setUp()
        self.distributor = Distributor.create(name=self.NAME,
                                              active=True)
        self.distributor_key = self.distributor.put()

    def test_create_sets_distributor_entity_group_as_parent(self):
        actual = Distributor.find_by_name(self.NAME)
        parent = actual.key.parent().get()
        self.assertEqual(parent.name, self.ENTITY_GROUP_NAME)

    def test_find_by_name_returns_matching_distributor(self):
        actual = Distributor.find_by_name(self.NAME)
        self.assertEqual(actual.key, self.distributor_key)
        self.assertEqual(actual.name, self.NAME)

    def test_find_by_name_returns_none_when_no_matching_distributor_found(self):
        actual = Distributor.find_by_name('bogus distributor')
        self.assertIsNone(actual)

    def test_create_sets_an_inactive_distributor(self):
        name = 'Inactive Distributor'
        inactive_distributor = Distributor.create(name=name,
                                                  active=False)
        inactive_distributor.put()
        distributor_created = Distributor.find_by_name(name)
        self.assertEqual(distributor_created.name, name)
        self.assertFalse(distributor_created.active)

    def test_create_sets_expected_distributor_properties(self):
        distributor_created = Distributor.find_by_name(self.NAME)
        self.assertTrue(distributor_created.active)
        self.assertEqual(self.NAME, distributor_created.name)
        self.assertTrue(distributor_created.active)
