from google.appengine.ext import ndb

TENANT_ENTITY_GROUP_NAME = 'tenantEntityGroup'
DISTRIBUTOR_ENTITY_GROUP_NAME = 'distributorEntityGroup'


class TenantEntityGroup(ndb.Model):
    name = ndb.StringProperty(required=True)
    class_version = ndb.IntegerProperty()

    @classmethod
    def singleton(cls):
        return TenantEntityGroup.get_or_insert(TENANT_ENTITY_GROUP_NAME,
                                               name=TENANT_ENTITY_GROUP_NAME)

    def _pre_put_hook(self):
        self.class_version = 1


class DistributorEntityGroup(ndb.Model):
    name = ndb.StringProperty(required=True)
    class_version = ndb.IntegerProperty()

    @classmethod
    def singleton(cls):
        return DistributorEntityGroup.get_or_insert(DISTRIBUTOR_ENTITY_GROUP_NAME,
                                                    name=DISTRIBUTOR_ENTITY_GROUP_NAME)

    def _pre_put_hook(self):
        self.class_version = 1
