from google.appengine.ext import ndb


class UserRole(ndb.Model):
    """
    0 == regular user
    1 == distributorAdmin
    """
    role = ndb.IntegerProperty()
    class_version = ndb.IntegerProperty()

    @staticmethod
    def create_or_get_user_role(role):
        u = UserRole.query(UserRole.role == role).fetch()

        if u:
            return u[0]

        else:
            u = UserRole(
                role=role
            )

            u.put()

            return u

    def _pre_put_hook(self):
        self.class_version = 1
