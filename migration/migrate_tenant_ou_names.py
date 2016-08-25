from migration_base import MigrationBase
from integrations.directory_api.tenant_ou_name_migration import TenantOUNameMigration

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class MigrateTenantOUNames(MigrationBase):
    MIGRATION_NAME = 'migrate_tenant_ou_names'

    def __init__(self):
        super(MigrateTenantOUNames, self).__init__(self.MIGRATION_NAME)

    def run(self):
        tenant_ou_migration = TenantOUNameMigration()
        tenant_ou_migration.migrate_all_existing_tenant_names()
