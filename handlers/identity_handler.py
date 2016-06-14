import random
import string
import os

from agar.sessions import SessionRequestHandler
from app_config import config
from models import User, Distributor
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response


class IdentityHandler(SessionRequestHandler, KeyValidatorMixin):
    def get(self):
        state = self.session.get('state')

        if not state:
            state = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in xrange(32))
            self.session['state'] = state

        user_info = {
            'login_url': self.uri_for('login'),
            'logout_url': self.uri_for('logout'),
            'version': os.environ['CURRENT_VERSION_ID'],
            'CLIENT_ID': config.CLIENT_ID,
            'OAUTH_CLIENT_ID': config.OAUTH_CLIENT_ID,
            'BROWSER_API_KEY': config.PUBLIC_API_SERVER_KEY,
            'STATE': state,
        }

        user_key = self.session.get('user_key')
        user = self.validate_and_get(user_key, User)

        if user:
            session_distributor = self.session.get('distributor')
            distributors_as_admin = [each_distributor.name for each_distributor in user.distributors_as_admin]
            distributors = user.distributors

            if not session_distributor and len(distributors) == 1:
                session_distributor = distributors[0].name

            distributor_names = [distributor.name for distributor in distributors]

            user_info.update({
                'email': user.email,
                'is_admin': user.is_administrator,
                'is_logged_in': True,
                'distributors': [distributor.name for distributor in
                                 Distributor.query().fetch()] if user.is_administrator else distributor_names,
                'distributors_as_admin': [
                    distributor.name for distributor in
                    Distributor.query().fetch()] if user.is_administrator else distributors_as_admin,
                'distributor': session_distributor
            })

        else:
            user_info['is_logged_in'] = False

        json_response(self.response, user_info)
