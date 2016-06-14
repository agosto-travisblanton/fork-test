from migration_base import MigrationBase
from models import User

from provisioning_env import (
    on_development_server,
    on_integration_server,
)

DEFAULT_PROD_ADMIN_USERS = [
    "marla.geary@agosto.com",
    "michael.allen@agosto.com",
    "thomas.blade@agosto.com",
    "bob.macneal@agosto.com"
]

DEFAULT_INT_ADMIN_USERS = [
    "marla.geary@agosto.com",
    "joy.islam@agosto.com",
    "yulia.martin@agosto.com",
    "daniel.ternyak@agosto.com",
    "bob.macneal@agosto.com"
]


class SetDefaultAdminUsers(MigrationBase):
    MIGRATION_NAME = 'set_default_admin_users'

    def __init__(self):
        super(SetDefaultAdminUsers, self).__init__(self.MIGRATION_NAME)

    def run(self):
        if on_development_server or on_integration_server:
            users = DEFAULT_INT_ADMIN_USERS
        else:
            users = DEFAULT_PROD_ADMIN_USERS

        for each_user in users:
            user = User.get_or_insert_by_email(each_user)
            user.is_administrator = True
            user.put()
