import json

from google.appengine.ext import ndb
from decorators import requires_api_token, has_distributor_admin_user_key
from strategy import DISTRIBUTOR_STRATEGY
from agar.sessions import SessionRequestHandler
from models import User, Distributor, DistributorUser
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response


class UsersHandler(SessionRequestHandler, KeyValidatorMixin):
    @requires_api_token
    def get_list_by_user(self, user_urlsafe_key):
        user = ndb.Key(urlsafe=user_urlsafe_key).get()
        distributors = user.distributors
        json_response(self.response, distributors, strategy=DISTRIBUTOR_STRATEGY)

    @has_distributor_admin_user_key
    def post(self, **kwargs):
        incoming = json.loads(self.request.body)
        user_email = incoming["user_email"].lower()
        user = User.get_or_insert_by_email(email=user_email)
        user_distributors = [each_distro.name for each_distro in user.distributors]
        distributor_name = incoming["distributor"]
        distributor_admin_role = incoming["distributor_admin"]
        distributor = Distributor.find_by_name(name=distributor_name)
        current_user = kwargs["current_user"]

        if not distributor:
            return json_response(self.response, {'message': 'Not a valid distributor'}, status_code=403)

        else:
            distro_admin_of_distributor = current_user.is_distributor_administrator_of_distributor(distributor_name)
            if not distro_admin_of_distributor and not current_user.is_administrator:

                return json_response(
                    self.response,
                    {
                        'message': 'User not allowed to modify this distributor.'
                    },
                    status_code=403
                )

            if distributor.name not in user_distributors:

                if distributor_admin_role:
                    distributor_admin_role = 1

                else:
                    distributor_admin_role = 0

                user.add_distributor(distributor.key, role=distributor_admin_role)

                json_response(self.response, {
                    "success": True,
                    "message": 'SUCCESS! {0} is linked to {1}'.format(user.email, distributor.name)
                })

            else:
                json_response(self.response, {
                    "success": False,
                    "message": distributor.name + " is already linked to " + user_email
                }, status_code=409)
