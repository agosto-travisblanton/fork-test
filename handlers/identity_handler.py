import random
import string
import os

from agar.sessions import SessionRequestHandler
from app_config import config
from models import User, Distributor, UserAdmin
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response


class IdentityHandler(SessionRequestHandler, KeyValidatorMixin):
    def get(self):
        app_version = os.environ['CURRENT_VERSION_ID']

        state = self.session.get('state')
        if state is None:
            state = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in xrange(32))
            self.session['state'] = state

        user_info = {
            'login_url': self.uri_for('login'),
            'logout_url': self.uri_for('logout'),
            'version': app_version,
            'CLIENT_ID': config.CLIENT_ID,
            'OAUTH_CLIENT_ID': config.OAUTH_CLIENT_ID,
            'BROWSER_API_KEY': config.PUBLIC_API_SERVER_KEY,
            'STATE': state,
        }

        user_key = self.session.get('user_key')
        user = self.validate_and_get(user_key, User)

        if user:
            session_distributor = self.session.get('distributor')

            if self.session.get('is_administrator') is True:
                user_info['administrator'] = True
                distributors = Distributor.query().fetch()

            else:
                distributors = user.distributors

            if session_distributor is None and len(distributors) == 1:
                session_distributor = distributors[0].name

            distributor_names = [distributor.name for distributor in distributors]
            user_info.update({
                'email': user.email,
                'is_logged_in': True,
                'distributors': distributor_names,
                'distributor': session_distributor
            })

        else:
            user_info['is_logged_in'] = False

        json_response(self.response, user_info)

    def make_admins(self):
        default_admins = ["daniel.ternyak@agosto.com"]
        [UserAdmin.insert_email_if_not_exist(email) for email in default_admins]

        json_response(self.response, {
            "admins_created": [user.email for user in UserAdmin.get_all()]
        })

    def apply_admins(self):
        all_admin_emails = [admin.email for admin in UserAdmin.get_all()]
        [User.migrate_user_to_admin(admin_email) for admin_email in all_admin_emails]

        json_response(self.response, {
            "admins_applied": all_admin_emails
        })
