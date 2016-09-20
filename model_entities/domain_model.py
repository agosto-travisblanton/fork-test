from google.appengine.ext import ndb

from distributor_and_user_model import Distributor
from restler.decorators import ae_ndb_serializer


@ae_ndb_serializer
class Domain(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=True)
    distributor_key = ndb.KeyProperty(kind=Distributor, required=True, indexed=True)
    impersonation_admin_email_address = ndb.StringProperty(required=True, indexed=True)
    organization_path_prefix = ndb.StringProperty(required=False, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    active = ndb.BooleanProperty(default=True, required=True, indexed=True)
    class_version = ndb.IntegerProperty()

    def get_distributor(self):
        return self.distributor_key.get()

    @classmethod
    def find_by_name(cls, name):
        if name:
            key = Domain.query(Domain.name == name).get(keys_only=True)
            if key:
                return key.get()

    @classmethod
    def create(cls, name, distributor_key, impersonation_admin_email_address, active=True,
               organization_path_prefix=None):
        return cls(distributor_key=distributor_key,
                   name=name.strip().lower(),
                   impersonation_admin_email_address=impersonation_admin_email_address,
                   organization_path_prefix=organization_path_prefix,
                   active=active)

    @classmethod
    def already_exists(cls, name):
        if Domain.query(
                ndb.AND(Domain.active == True,
                        Domain.name == name.strip().lower())).get(keys_only=True):
            return True
        return False

    def _pre_put_hook(self):
        self.class_version = 1
