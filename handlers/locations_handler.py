import json
import logging
import re

from google.appengine.ext import ndb
from webapp2 import RequestHandler

from decorators import requires_auth
from models import Location, Tenant
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response
from strategy import LOCATION_STRATEGY

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class LocationsHandler(RequestHandler, KeyValidatorMixin):
    LATITUDE_PATTERN = '^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)'
    LONGITUDE_PATTERN = '\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'

    @requires_auth
    def get(self, location_urlsafe_key):
        result = self.validate_and_get(location_urlsafe_key, Location, abort_on_not_found=True)
        json_response(self.response, result, strategy=LOCATION_STRATEGY)

    @requires_auth
    def get_locations_by_tenant(self, tenant_urlsafe_key):
        tenant_key = ndb.Key(urlsafe=tenant_urlsafe_key)

        customer_location_name = self.request.get("customer_location_name")
        if customer_location_name:
            query_results = Location.find_by_partial_location_name(customer_location_name, tenant_key)
        else:
            query_results = Location.query(Location.tenant_key == tenant_key).order(Location.customer_location_code).fetch()

        json_response(self.response, query_results, strategy=LOCATION_STRATEGY)

    @requires_auth
    def get_locations_by_tenant_paginated(self, tenant_urlsafe_key, prev_cursor, next_cursor):
        tenant_key = ndb.Key(urlsafe=tenant_urlsafe_key)
        next_cursor = next_cursor if next_cursor != "null" else None
        prev_cursor = prev_cursor if prev_cursor != "null" else None

        query_results = Tenant.find_locations_of_tenant_paginated(
            tenant_key=tenant_key,
            next_cursor_str=next_cursor,
            prev_cursor_str=prev_cursor
        )

        json_response(
            self.response,
            {
                "locations": query_results["objects"],
                "next_cursor": query_results["next_cursor"],
                "prev_cursor": query_results["prev_cursor"]
            },
            strategy=LOCATION_STRATEGY
        )

    @requires_auth
    def post(self):
        if self.request.body is not '' and self.request.body is not None:
            status = 201
            error_message = None
            request_json = json.loads(self.request.body)
            tenant_urlsafe_key = request_json.get('tenantKey')
            if tenant_urlsafe_key is None or tenant_urlsafe_key == '':
                status = 400
                error_message = 'The tenant key parameter is invalid.'
                self.response.set_status(status, error_message)
                return
            else:
                tenant_key = ndb.Key(urlsafe=tenant_urlsafe_key)
            customer_location_code = request_json.get('customerLocationCode')
            if customer_location_code is None or customer_location_code == '':
                status = 400
                error_message = 'The customer location code parameter is invalid.'
                self.response.set_status(status, error_message)
                return
            customer_location_name = request_json.get('customerLocationName')
            if customer_location_name is None or customer_location_name == '':
                status = 400
                error_message = 'The customer location name parameter is invalid.'
                self.response.set_status(status, error_message)
                return
            active = request_json.get('active')
            if active is None or active == '' or (str(active).lower() != 'true' and str(active).lower() != 'false'):
                status = 400
                error_message = 'The active parameter is invalid.'
            else:
                active = bool(active)
            address = request_json.get('address')
            city = request_json.get('city')
            state = request_json.get('state')
            postal_code = request_json.get('postalCode')
            latitude = request_json.get('latitude')
            longitude = request_json.get('longitude')
            if latitude is None or longitude is None:
                geo_location = None
            else:
                if re.match(self.LATITUDE_PATTERN, str(latitude)) is None or re.match(self.LONGITUDE_PATTERN,
                                                                                      str(longitude)) is None:
                    logging.warning(
                        'Invalid latitude {0} or longitude {1} detected.'.format(str(latitude), str(longitude)))
                    geo_location = None
                else:
                    geo_location = ndb.GeoPt(latitude, longitude)
            dma = request_json.get('dma')
            if status == 201:
                if Location.is_customer_location_code_unique(customer_location_code, tenant_key):
                    location = Location.create(tenant_key=tenant_key,
                                               customer_location_name=customer_location_name,
                                               customer_location_code=customer_location_code)
                    if address:
                        location.address = address
                    if city:
                        location.city = city
                    if state:
                        location.state = state
                    if postal_code:
                        location.postal_code = postal_code
                    if geo_location:
                        location.geo_location = geo_location
                    if dma:
                        location.dma = dma
                    if active:
                        location.active = active
                    location.put()
                    self.response.headers.pop('Content-Type', None)
                    self.response.set_status(201)
                else:
                    error_message = "Conflict. Customer location code \"{0}\" is already assigned for tenant.".format(
                        customer_location_code)
                    self.response.set_status(409, error_message)
            else:
                self.response.set_status(status, error_message)
        else:
            logging.info("Problem creating Location. No request body.")
            self.response.set_status(400, 'Did not receive request body.')

    @requires_auth
    def put(self, location_urlsafe_key):
        key = ndb.Key(urlsafe=location_urlsafe_key)
        location = key.get()
        request_json = json.loads(self.request.body)
        location.customer_location_name = request_json.get('customerLocationName')
        address = request_json.get('address')
        if address:
            location.address = address
        city = request_json.get('city')
        if city:
            location.city = city
        state = request_json.get('state')
        if state:
            location.state = state
        postal_code = request_json.get('postalCode')
        if postal_code:
            location.postal_code = postal_code
        dma = request_json.get('dma')
        if dma:
            location.dma = dma
        latitude = request_json.get('latitude')
        longitude = request_json.get('longitude')
        if latitude and longitude:
            if re.match(self.LATITUDE_PATTERN, str(latitude)) is None or re.match(self.LONGITUDE_PATTERN,
                                                                                  str(longitude)) is None:
                logging.warning(
                    'Invalid latitude {0} or longitude {1} detected.'.format(str(latitude), str(longitude)))
            else:
                location.geo_location = ndb.GeoPt(latitude, longitude)
        location.active = request_json.get('active')
        location.put()
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)
