from datetime import datetime
from env_setup import setup_test_paths
from models import AppliedMigration

setup_test_paths()

from agar.test import BaseTest

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestAppliedMigrationModel(BaseTest):
    MIGRATION_TAG = '0001-Device-to-Display'
    CURRENT_CLASS_VERSION = 1

    def setUp(self):
        super(TestAppliedMigrationModel, self).setUp()
        self.migration_operation = AppliedMigration.create(tag_name=self.MIGRATION_TAG)
        self.migration_operation_key = self.migration_operation.put()

    def test_migration_operation_create_returns_expected_migration_tag(self):
        self.assertEqual(self.migration_operation.tag_name, self.MIGRATION_TAG)

    def test_migration_operation_has_auto_generated_timestamp(self):
        self.assertEqual(self.migration_operation.timestamp.date(), datetime.now().date())

    def test_migration_operation_has_been_run_affirmative(self):
        result = AppliedMigration.has_been_run(self.MIGRATION_TAG)
        self.assertTrue(result)

    def test_migration_operation_has_been_run_negative(self):
        result = AppliedMigration.has_been_run('Migration that has not been run')
        self.assertFalse(result)

    def test_migration_operation_class_version_is_only_set_by_pre_put_hook_method(self):
        self.migration_operation.class_version = 47
        self.migration_operation.put()
        self.assertEqual(self.migration_operation.class_version, self.CURRENT_CLASS_VERSION)
