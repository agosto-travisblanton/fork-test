import json
import logging

from google.appengine.ext import ndb
from webapp2 import RequestHandler

from decorators import requires_api_token
from models import Distributor, DistributorEntityGroup, DistributorUser
from models import Distributor, DistributorEntityGroup, Domain
from restler.serializers import json_response
from decorators import has_admin_user_key, has_distributor_admin_user_key
from strategy import DISTRIBUTOR_STRATEGY, DOMAIN_STRATEGY

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>, Christopher Bartling <chris.bartling@agosto.com>'


class DistributorsHandler(RequestHandler):
    @requires_api_token
    def get_list_by_user(self, user_urlsafe_key):
        key = ndb.Key(urlsafe=user_urlsafe_key)
        distributor_user_associations = DistributorUser.query(DistributorUser.user_key == key).fetch(100)
        distributors = []
        for distributor_user_association in distributor_user_associations:
            distributors.append(distributor_user_association.distributor_key.get())
        json_response(self.response, distributors, strategy=DISTRIBUTOR_STRATEGY)

    @requires_api_token
    def get_list(self):
        distributor_name = self.request.get('distributorName')
        result = Distributor.query(ancestor=DistributorEntityGroup.singleton().key).fetch(100)
        if distributor_name:
            result = filter(lambda x: x.name == distributor_name, result)
        else:
            result = filter(lambda x: x.active is True, result)
        json_response(self.response, result, strategy=DISTRIBUTOR_STRATEGY)

    @requires_api_token
    def get(self, distributor_key):
        distributor_key = ndb.Key(urlsafe=distributor_key)
        result = distributor_key.get()
        json_response(self.response, result, strategy=DISTRIBUTOR_STRATEGY)

    @requires_api_token
    def get_domains(self, distributor_key):
        distributor_key = ndb.Key(urlsafe=distributor_key)
        result = Domain.query(Domain.distributor_key == distributor_key, True == Domain.active).fetch(100)
        json_response(self.response, result, strategy=DOMAIN_STRATEGY)

    @has_admin_user_key
    def post(self):
        incoming = json.loads(self.request.body)
        distributor_name = incoming["distributor"]
        admin_email = incoming["admin_email"]

        if Distributor.is_unique(distributor_name):
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

    @requires_api_token
    def put(self, distributor_key):
        key = ndb.Key(urlsafe=distributor_key)
        distributor = key.get()
        request_json = json.loads(self.request.body)
        distributor.name = request_json.get('name')
        distributor.active = request_json.get('active')
        distributor.put()
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)

    @requires_api_token
    def delete(self, distributor_key):
        key = ndb.Key(urlsafe=distributor_key)
        distributor = key.get()
        if distributor:
            distributor.active = False
            distributor.put()
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)