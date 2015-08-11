from env_setup import setup_test_paths
from migration.migration_models import MigrationOperation

setup_test_paths()

from agar.test import BaseTest

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestMigrationOperationModel(BaseTest):
    MIGRATION_TAG = 'Device-to-Display'
    CURRENT_CLASS_VERSION = 1

    def setUp(self):
        super(TestMigrationOperationModel, self).setUp()
        self.migration_operation = MigrationOperation.get_or_insert_by_name(self.MIGRATION_TAG)
        self.migration_operation_key = self.migration_operation.put()

    def test_get_or_insert_by_name_returns_expected_migration_name(self):
        self.assertEqual(self.migration_operation.name, self.MIGRATION_TAG)

    def test_get_by_name_returns_expected_representation(self):
        migration = MigrationOperation.get_by_name(self.MIGRATION_TAG)
        self.assertEqual(migration.status, 'Queued')
        self.assertIsNone(migration.start_time)
        self.assertIsNone(migration.finish_time)
        self.assertIsNone(migration.debug_info)

    def test_fail_updates_status_and_finish_time(self):
        migration = self.migration_operation.fail(self.MIGRATION_TAG)
        self.assertEqual(migration.status, 'Failed')
        self.assertIsNotNone(migration.finish_time)

    def test_complete_updates_status_and_finish_time(self):
        migration = self.migration_operation.start(self.MIGRATION_TAG)
        self.assertEqual(migration.status, 'Running')
        self.assertIsNone(migration.finish_time)
        migration = self.migration_operation.complete(self.MIGRATION_TAG)
        self.assertEqual(migration.status, 'Completed')
        self.assertIsNotNone(migration.finish_time)

    def test_set_debug_info_populates_expected_property(self):
        debug_info = 'Your op is hosed'
        migration = self.migration_operation.set_debug_info(self.MIGRATION_TAG, debug_info)
        self.assertEqual(migration.debug_info, debug_info)

    def test_migration_operation_class_version_is_only_set_by_pre_put_hook_method(self):
        self.migration_operation.class_version = 47
        self.migration_operation.put()
        self.assertEqual(self.migration_operation.class_version, self.CURRENT_CLASS_VERSION)
