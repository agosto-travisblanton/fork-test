from env_setup import setup_test_paths
from models import DistributorEntityGroup

setup_test_paths()

from agar.test import BaseTest

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestDistributorEntityGroup(BaseTest):
    CURRENT_CLASS_VERSION = 1

    def setUp(self):
        super(TestDistributorEntityGroup, self).setUp()
        self.distributor_entity_group = DistributorEntityGroup.singleton()
        self.distributor_entity_group_key = self.distributor_entity_group.put()

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        self.distributor_entity_group.class_version = 47
        self.distributor_entity_group.put()
        self.assertEqual(self.distributor_entity_group.class_version, self.CURRENT_CLASS_VERSION)
