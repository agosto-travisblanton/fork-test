import random
import string
from agar.sessions import SessionRequestHandler
from app_config import config
from datetime import datetime
from models import User, Distributor
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response
import json
import os
import stormpath_api


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
            'WEB_APP_CLIENT_ID': config.WEB_APP_CLIENT_ID,
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


class LoginHandler(SessionRequestHandler):
    def post(self):
        user = None
        body = json.loads(self.request.body)
        email = body.get('email', '').strip()
        password = body.get('password', '').strip()
        if email and password:
            user = stormpath_api.cloud_login(email, password)
        else:
            # Ensure that the request is not a forgery and that the user sending
            # this connect request is the expected user.
            state = body.get('state', '')
            if state == self.session.get('state'):
                id_token = body.get('id_token', None)
                access_token = body.get('access_token', None)
                code = body.get('code')
                user = stormpath_api.google_login(id_token, access_token, code)

        if user is None:
            result = {'message': 'Login Failed'}
            status_code = 400
        else:
            user.last_login = datetime.now()
            user.put()
            administrator = body.get('administrator', False)
            self.session['is_administrator'] = administrator is True and user.is_administrator
            self.session['user_key'] = user.key.urlsafe()
            if len(user.distributors) == 1:
                self.session['distributor'] = user.distributors[0].name
            result = {'message': 'Successful Login'}
            status_code = 200

        json_response(self.response, result, status_code=status_code)


class LogoutHandler(SessionRequestHandler):
    def _logout(self):
        if 'user_key' in self.session:
            del self.session['user_key']
        if 'distributor' in self.session:
            del self.session['distributor']
        if 'state' in self.session:
            del self.session['state']
        if 'is_administrator' in self.session:
            del self.session['is_administrator']
        json_response(self.response, {'message': 'Successful Logout'}, status_code=200)

    def get(self):
        self._logout()

    def post(self):
        self._logout()