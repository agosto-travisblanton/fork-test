from env_setup import setup_test_paths
from models import TenantEntityGroup

setup_test_paths()

from agar.test import BaseTest

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestTenantEntityGroup(BaseTest):
    CURRENT_CLASS_VERSION = 1

    def setUp(self):
        super(TestTenantEntityGroup, self).setUp()
        self.tenant_entity_group = TenantEntityGroup.singleton()
        self.tenant_entity_group_key = self.tenant_entity_group.put()

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        self.tenant_entity_group.class_version = 47
        self.tenant_entity_group.put()
        self.assertEqual(self.tenant_entity_group.class_version, self.CURRENT_CLASS_VERSION)
