from app_config import config
from migration_base import MigrationBase
from models import Tenant

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class SetContentManagerBaseUrlOnTenant(MigrationBase):
    MIGRATION_NAME = 'set_content_manager_base_url_on_tenant'

    def __init__(self):
        super(SetContentManagerBaseUrlOnTenant, self).__init__(self.MIGRATION_NAME)

    def run(self):
        tenants = Tenant.query().fetch(500)
        for tenant in tenants:
            tenant.content_manager_base_url = config.DEFAULT_CONTENT_MANAGER_URL
            tenant.put()

