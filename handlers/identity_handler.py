import random
import string
import os

from agar.sessions import SessionRequestHandler
from app_config import config
from models import User, Distributor, UserAdmin
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response
from decorators import has_admin_user_key
import json


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
                'is_admin': user.is_administrator,
                'is_logged_in': True,
                'distributors': distributor_names,
                'distributor': session_distributor
            })

        else:
            user_info['is_logged_in'] = False

        json_response(self.response, user_info)

    @has_admin_user_key
    def make_user(self):
        incoming = json.loads(self.request.body)
        user_email = incoming["user_email"]
        user = User.get_or_insert_by_email(email=user_email)

        json_response(self.response, {
            "success": True,
            "user_created": user.email
        })

    @has_admin_user_key
    def add_user_to_distributor(self):
        incoming = json.loads(self.request.body)
        user_email = incoming["user_email"]
        user = User.get_or_insert_by_email(email=user_email)
        distributor_name = incoming["distributor"]
        distributor = Distributor.find_by_name(name=distributor_name)
        if not distributor:
            self.abort()

        else:
            user.add_distributor(distributor.key)
            json_response(self.response, {
                "success": True,
                "message": 'SUCCESS! ' + user.email + ' is linked to ' + distributor.name
            })

    @has_admin_user_key
    def create_distributor(self):
        incoming = json.loads(self.request.body)
        distributor_name = incoming["distributor"]
        admin_email = incoming["admin_email"]
        distributor = Distributor.query(Distributor.name == distributor_name).get()

        if not distributor:
            distributor = Distributor.create(name=distributor_name, active=True)
            distributor.admin_email = admin_email
            distributor.put()
            json_response(
                self.response, {
                    "success": True,
                    "message": 'Distributor ' + distributor.name + ' created.'
                }
            )
        else:
            self.abort()
