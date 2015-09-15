import json
import logging

from google.appengine.ext import ndb
from webapp2 import RequestHandler

from decorators import api_token_required
from models import Distributor, DistributorEntityGroup, DistributorUser
from restler.serializers import json_response
from strategy import DISTRIBUTOR_STRATEGY

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>, Christopher Bartling <chris.bartling@agosto.com>'


class DistributorsHandler(RequestHandler):
    @api_token_required
    def get_list_by_user(self, user_urlsafe_key):
        key = ndb.Key(urlsafe=user_urlsafe_key)
        distributor_user_associations = DistributorUser.query(DistributorUser.user_key == key).fetch(100)
        distributors = []
        for distributor_user_association in distributor_user_associations:
            distributors.append(distributor_user_association.distributor_key.get())
        json_response(self.response, distributors, strategy=DISTRIBUTOR_STRATEGY)

    @api_token_required
    def get_list(self):
        distributor_name = self.request.get('distributorName')
        result = Distributor.query(ancestor=DistributorEntityGroup.singleton().key).fetch(100)
        if distributor_name:
            result = filter(lambda x: x.name == distributor_name, result)
        else:
            result = filter(lambda x: x.active is True, result)
        json_response(self.response, result, strategy=DISTRIBUTOR_STRATEGY)

    @api_token_required
    def get(self, distributor_key):
        distributor_key = ndb.Key(urlsafe=distributor_key)
        result = distributor_key.get()
        json_response(self.response, result, strategy=DISTRIBUTOR_STRATEGY)

    @api_token_required
    def post(self):
        if self.request.body is not str('') and self.request.body is not None:
            status = 201
            error_message = None
            request_json = json.loads(self.request.body)
            name = request_json.get('name')
            if name is None or name == '':
                status = 400
                error_message = 'The name parameter is invalid.'
            active = request_json.get('active')
            if active is None or active == '' or (str(active).lower() != 'true' and str(active).lower() != 'false'):
                status = 400
                error_message = 'The active parameter is invalid.'
            else:
                active = bool(active)
            if status == 201:
                distributor = Distributor.create(name=name,
                                                 active=active)
                distributor_key = distributor.put()
                distributor_uri = self.request.app.router.build(None,
                                                                'manage-distributor',
                                                                None,
                                                                {'distributor_key': distributor_key.urlsafe()})
                self.response.headers['Location'] = distributor_uri
                self.response.headers.pop('Content-Type', None)
                self.response.set_status(status)
            else:
                self.response.set_status(status, error_message)
        else:
            logging.info("Problem creating Distributor. No request body.")
            self.response.set_status(400, 'Did not receive request body.')

    @api_token_required
    def put(self, distributor_key):
        key = ndb.Key(urlsafe=distributor_key)
        distributor = key.get()
        request_json = json.loads(self.request.body)
        distributor.name = request_json.get('name')
        distributor.active = request_json.get('active')
        distributor.put()
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)

    @api_token_required
    def delete(self, distributor_key):
        key = ndb.Key(urlsafe=distributor_key)
        distributor = key.get()
        if distributor:
            distributor.active = False
            distributor.put()
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)
