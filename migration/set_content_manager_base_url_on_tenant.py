from migration_base import MigrationBase
from models import Tenant
from app_config import config

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class SetContentManagerBaseUrlOnTenant(MigrationBase):
    MIGRATION_NAME = 'set_content_manager_base_url_on_tenant'

    def __init__(self):
        super(SetContentManagerBaseUrlOnTenant, self).__init__(self.MIGRATION_NAME)

    def run(self):
        tenants = Tenant.query().fetch(500)
        for tenant in tenants:
            content_manager_base_url = 'https://skykit-contentmanager-int.appspot.com'
            if config.on_production_server:
                content_manager_base_url = 'https://skykit-contentmanager.appspot.com'
            tenant.content_manager_base_url = content_manager_base_url
            tenant.put()

