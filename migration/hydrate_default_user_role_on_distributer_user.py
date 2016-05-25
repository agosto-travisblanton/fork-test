from migration_base import MigrationBase
from models import UserRole, DistributorUser


class HydrateDefaultUserRoleOnDistributerUser(MigrationBase):
    MIGRATION_NAME = 'hydrate_default_user_role_on_distributer_user'
    AGOSTO_DISTRIBUTOR_NAME = 'Agosto'

    def __init__(self):
        super(HydrateDefaultUserRoleOnDistributerUser, self).__init__(self.MIGRATION_NAME)

    def run(self):
        all_distributer_user_entities = DistributorUser.query().fetch()

        for each_entity in all_distributer_user_entities:
            if not each_entity.role:
                each_entity.role = UserRole.create_or_get_user_role(0).key  # 0 = basic user
                each_entity.put()