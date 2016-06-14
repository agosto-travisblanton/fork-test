from app_config import config
from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
from models import Distributor, DISTRIBUTOR_ENTITY_GROUP_NAME

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestDistributorModel(BaseTest):
    NAME = 'Agosto'
    CURRENT_CLASS_VERSION = 1

    def setUp(self):
        super(TestDistributorModel, self).setUp()
        self.distributor = Distributor.create(name=self.NAME,
                                              active=True)
        self.distributor_key = self.distributor.put()

    def test_create_sets_distributor_entity_group_as_parent(self):
        actual = Distributor.find_by_name(self.NAME)
        parent = actual.key.parent().get()
        self.assertEqual(parent.name, DISTRIBUTOR_ENTITY_GROUP_NAME)

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
        self.assertEqual(distributor_created.content_manager_url, config.DEFAULT_CONTENT_MANAGER_URL)
        self.assertEqual(distributor_created.player_content_url, config.DEFAULT_PLAYER_CONTENT_URL)

    def test_create_can_override_default_urls(self):
        content_manager_url = 'content-manager-foo'
        player_content_url = 'player-foo'
        distributor_created = Distributor.create(name=self.NAME,
                                                 content_manager_url=content_manager_url,
                                                 player_content_url=player_content_url)
        distributor_created.put()
        self.assertEqual(distributor_created.content_manager_url, content_manager_url)
        self.assertEqual(distributor_created.player_content_url, player_content_url)

    def test_is_unique_returns_true_when_name_not_found(self):
        distributor_created = Distributor.find_by_name(self.NAME)
        self.assertTrue(distributor_created.active)
        self.assertEqual(self.NAME, distributor_created.name)
        self.assertTrue(distributor_created.active)

    def test_is_unique_returns_false_when_name_is_found(self):
        uniqueness_check = Distributor.is_unique(self.NAME)
        self.assertFalse(uniqueness_check)

    def test_is_unique_returns_true_when_name_not_found(self):
        uniqueness_check = Distributor.is_unique('Foobar')
        self.assertTrue(uniqueness_check)

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        self.distributor.class_version = 47
        self.distributor.put()
        self.assertEqual(self.distributor.class_version, self.CURRENT_CLASS_VERSION)
