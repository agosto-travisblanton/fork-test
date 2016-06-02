from app_config import config
from entity_groups import DistributorEntityGroup

import logging
from google.appengine.ext import ndb

from restler.decorators import ae_ndb_serializer
from user_role_model import UserRole


@ae_ndb_serializer
class Distributor(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=True)
    admin_email = ndb.StringProperty(required=False, indexed=True)
    player_content_url = ndb.StringProperty(required=False, indexed=True)
    content_manager_url = ndb.StringProperty(required=False, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    active = ndb.BooleanProperty(default=True, required=True, indexed=True)
    class_version = ndb.IntegerProperty()

    @classmethod
    def find_by_name(cls, name):
        if name:
            distributor_query = Distributor.query().fetch()

            match = None

            for item in distributor_query:
                if item.name.lower() == name.lower():
                    match = item
            return match

    @classmethod
    def is_unique(cls, name):
        return not cls.find_by_name(name)

    @classmethod
    def create(cls,
               name,
               active=True,
               content_manager_url=config.DEFAULT_CONTENT_MANAGER_URL,
               player_content_url=config.DEFAULT_PLAYER_CONTENT_URL):
        distributor_entity_group = DistributorEntityGroup.singleton()
        return cls(parent=distributor_entity_group.key,
                   name=name,
                   content_manager_url=content_manager_url,
                   player_content_url=player_content_url,
                   active=active)

    def _pre_put_hook(self):
        self.class_version = 1


@ae_ndb_serializer
class User(ndb.Model):
    class_version = ndb.IntegerProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    email = ndb.StringProperty(required=True)
    is_administrator = ndb.BooleanProperty(default=False)  # platform administrator
    stormpath_account_href = ndb.StringProperty()
    last_login = ndb.DateTimeProperty()
    enabled = ndb.BooleanProperty(default=True)

    def _pre_put_hook(self):
        self.class_version = 1
        if self.key is None or self.key.id() is None:
            self.key = ndb.Key(User, self.email.lower())

    @classmethod
    def get_user_from_urlsafe_key(cls, key):
        try:
            user = ndb.Key(urlsafe=key).get()
            return user

        except TypeError as e:
            logging.error(e)
            return False

    @classmethod
    def _build_key(cls, email):
        key = ndb.Key(User, email.lower())
        return key

    @classmethod
    def get_or_insert_by_email(cls, email, stormpath_account_href=None):
        user = cls.get_by_email(email)
        if not user:
            key = cls._build_key(email)
            user = User(key=key, email=email, stormpath_account_href=stormpath_account_href)
            user.put()
        else:
            if user.stormpath_account_href != stormpath_account_href and stormpath_account_href is not None:
                user.stormpath_account_href = stormpath_account_href
                user.put()
        return user

    @classmethod
    def get_by_email(cls, email):
        key = cls._build_key(email)
        return key.get()

    @classmethod
    def update_or_create_with_api_account(cls, account):
        user = None
        if account and account.href:
            user = cls.query(cls.stormpath_account_href == account.href).get()
            if not user:
                user = cls.get_or_insert_by_email(account.email, stormpath_account_href=account.href)
        return user

    @classmethod
    def test_create(cls, email, stormpath_account_href='https://api.stormpath.com/v1/accounts/'):
        return cls(email=email,
                   stormpath_account_href=stormpath_account_href)

    @property
    def distributor_keys(self):
        dist_user_keys = DistributorUser.query(DistributorUser.user_key == self.key).fetch(keys_only=True)
        dist_users = ndb.get_multi(dist_user_keys)
        return [dist_user.distributor_key for dist_user in dist_users]

    @property
    def distributors(self):
        if self.is_administrator:
            return Distributor.query().fetch()
        else:
            return ndb.get_multi(self.distributor_keys)

    @property
    def distributors_as_admin(self):
        if self.is_administrator:
            return Distributor.query().fetch()
        else:
            distributor_users = DistributorUser.query(DistributorUser.user_key == self.key).fetch()
            return [each.distributor_key.get() for each in distributor_users if each.is_distributor_administrator]

    @property
    def is_distributor_administrator(self):
        if self.is_administrator:
            return True
        else:
            role = UserRole.create_or_get_user_role(1)
            return DistributorUser.query(DistributorUser.user_key == self.key).filter(
                DistributorUser.role == role.key).count() > 0

    def is_distributor_administrator_of_distributor(self, distributor_name):
        if self.is_administrator:
            return True
        else:
            distributor_key = Distributor.find_by_name(name=distributor_name).key
            distributor_user_pair = DistributorUser.query(DistributorUser.user_key == self.key).filter(
                DistributorUser.distributor_key == distributor_key).fetch()
            if distributor_user_pair:
                return distributor_user_pair[0].is_distributor_administrator
            else:
                return False

    def add_distributor(self, distributor_key, role=0):
        if distributor_key not in self.distributor_keys:
            dist_user = DistributorUser.create(
                user_key=self.key,
                distributor_key=distributor_key,
                role=role)
            dist_user.put()


@ae_ndb_serializer
class DistributorUser(ndb.Model):
    """
    Many-to-many relationship between Distributor and User.  Similar to Tenant-User relationship ("Permit") in SKD
    Is there a better name for this?
    """
    class_version = ndb.IntegerProperty()
    distributor_key = ndb.KeyProperty(kind=Distributor, required=True)
    user_key = ndb.KeyProperty(kind=User, required=True)
    role = ndb.KeyProperty(kind=UserRole, required=True)

    @classmethod
    def create(cls, distributor_key, user_key, role=0):
        user_role = UserRole.create_or_get_user_role(role)
        distributor_user = cls(
            user_key=user_key,
            role=user_role.key,
            distributor_key=distributor_key)
        return distributor_user

    @staticmethod
    def users_of_distributor(distributor_key):
        return DistributorUser.query(DistributorUser.distributor_key == distributor_key).fetch()

    @property
    def is_distributor_administrator(self):
        if self.user_key.get().is_administrator:
            return True
        else:
            return self.role.get().role == 1

    def _pre_put_hook(self):
        self.class_version = 1
