import random
import string
import os

from agar.sessions import SessionRequestHandler
from app_config import config
from models import User, Distributor
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response
from decorators import has_admin_user_key, has_distributor_admin_user_key
import json


def is_distributor_admin_associated_with_this_distributor(current_user, distributor):
    current_user_distributors = [each_distributor.name for each_distributor in current_user.distributors]
    return_value = False
    if distributor:
        if current_user.is_distributor_administrator:
            if distributor.name in current_user_distributors:
                return_value = True

    return return_value


class IdentityHandler(SessionRequestHandler, KeyValidatorMixin):
    def get(self):
        app_version = os.environ['CURRENT_VERSION_ID']

        state = self.session.get('state')

        if not state:
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

            if not session_distributor and len(distributors) == 1:
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

    @staticmethod
    def add_user_to_distributor_as_distributor_admin(distributor_name, user, current_user):
        distributor = Distributor.find_by_name(distributor_name)
        if distributor:
            if is_distributor_admin_associated_with_this_distributor(
                    current_user=current_user,
                    distributor=distributor):
                user.add_distributor(distributor.key, is_distributor_administrator=True)

            else:
                print current_user.name + "IS NOT ALLOWED TO MAKE " + user.email + " A DISTRIBUTOR ADMIN OF " + \
                      distributor_name
        else:
            print "NO DISTRIBUTOR BY THIS NAME"


    @has_distributor_admin_user_key
    def add_user_to_distributor(self, **kwargs):
        incoming = json.loads(self.request.body)
        user_email = incoming["user_email"]
        user = User.get_or_insert_by_email(email=user_email)
        user_distributors = [each_distro.name for each_distro in user.distributors]
        distributor_name = incoming["distributor"]
        distributor_admin = incoming["distributor_admin"]
        distributor = Distributor.find_by_name(name=distributor_name)
        current_user = kwargs["current_user"]

        if not distributor:
            return json_response(self.response, {'error': 'Not a valid distributor'}, status_code=403)

        else:
            if not is_distributor_admin_associated_with_this_distributor(
                    current_user,
                    distributor
            ) and not current_user.is_administrator:
                return json_response(
                    self.response,
                    {
                        'error': 'User not allowed to modify this distributor.'
                    },
                    status_code=403
                )

            if not distributor.name in user_distributors:
                user.add_distributor(distributor.key, is_distributor_administrator=distributor_admin)

                json_response(self.response, {
                    "success": True,
                    "message": 'SUCCESS! ' + user.email + ' is linked to ' + distributor.name
                })

            else:
                json_response(self.response, {
                    "success": False,
                    "message": distributor.name + " is already linked to " + current_user.email
                }, status_code=409)

    @has_admin_user_key
    def make_distributor(self):
        incoming = json.loads(self.request.body)
        distributor_name = incoming["distributor"]
        admin_email = incoming["admin_email"]
        distributor_name_unique = Distributor.is_unique(distributor_name)

        if distributor_name_unique:
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
            json_response(self.response, {
                "success": False,
                "message": "Distributor already exists"
            }, status_code=409)
