import json

from google.appengine.ext import ndb

from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest, WebTest
from models import Distributor, Domain, Tenant, Location
from routes import application
from app_config import config
from webtest import AppError


class TestLocationsHandler(BaseTest, WebTest):
    APPLICATION = application
    DISTRIBUTOR_NAME = 'agosto'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    IMPERSONATION_EMAIL = 'test@test.com'
    TENANT_CODE = 'foobar_inc'
    TENANT_NAME = 'Foobar, Inc,'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://skykit-contentmanager-int.appspot.com/content'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
    CUSTOMER_LOCATION_NAME = 'Store 4532'
    CUSTOMER_LOCATION_CODE = 'store_4532'

    def setUp(self):
        super(TestLocationsHandler, self).setUp()
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
                                              active=True)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.distributor_key,
                                    impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                    active=True)
        self.domain_key = self.domain.put()
        self.tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                                    name=self.TENANT_NAME,
                                    admin_email=self.ADMIN_EMAIL,
                                    content_server_url=self.CONTENT_SERVER_URL,
                                    content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                    domain_key=self.domain_key,
                                    active=True)
        self.tenant_key = self.tenant.put()
        self.location = Location.create(tenant_key=self.tenant_key,
                                        customer_location_name=self.CUSTOMER_LOCATION_NAME,
                                        customer_location_code=self.CUSTOMER_LOCATION_CODE)
        self.location_key = self.location.put()
        self.headers = {
            'Authorization': config.API_TOKEN,
        }

    ##################################################################################################################
    ## get_locations_by_tenant
    ##################################################################################################################
    def test_get_locations_by_tenant_returns_location_list(self):
        tenant = Tenant.create(tenant_code='acme_inc',
                               name='Acme, Inc.',
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                               domain_key=self.domain_key,
                               active=True)
        tenant_key = tenant.put()
        number_of_locations = 3
        self.load_tenant_locations(number_of_locations, tenant_key)
        request_parameters = {}
        uri = application.router.build(None, 'locations-list-retrieval', None,
                                       {'tenant_urlsafe_key': tenant_key.urlsafe()})
        response = self.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), number_of_locations)
        for x in range(number_of_locations):
            self.assertEqual(response_json[x].get('customerLocationName'), 'Store #{0}'.format(x))
            self.assertEqual(response_json[x].get('customerLocationCode'), 'store_{0}'.format(x))
            self.assertTrue(response_json[x].get('active'))

    ##################################################################################################################
    ## post
    ##################################################################################################################
    def test_post_returns_created_status(self):
        request_parameters = {'tenantKey': self.tenant_key.urlsafe(),
                              'customerLocationName': 'Store 4532',
                              'customerLocationCode': 'store_4532B',
                              'timezone': 'America/Phoenix',
                              'active': True,
                              'address': '123 Main St.',
                              'city': 'Minneapolis',
                              'state': 'MN',
                              'postalCode': '55401',
                              'latitude': 44.986656,
                              'longitude': -93.258133,
                              'dma': 'some dma code'
                              }
        uri = application.router.build(None, 'location-create', None, {})
        response = self.app.post_json(uri, params=request_parameters, headers=self.headers)
        self.assertEqual(201, response.status_int)

    def test_post_returns_bad_response_for_missing_tenant_key(self):
        request_parameters = {'tenantKey': '',
                              'customerLocationName': 'Store 4532',
                              'customerLocationCode': 'store_4532',
                              'timezone': 'America/Phoenix',
                              'active': True,
                              'address': '123 Main St.',
                              'city': 'Minneapolis',
                              'state': 'MN',
                              'postalCode': '55401',
                              'latitude': 44.986656,
                              'longitude': -93.258133,
                              'dma': 'some dma code'
                              }
        uri = application.router.build(None, 'location-create', None, {})
        with self.assertRaises(AppError) as context:
            self.app.post_json(uri, params=request_parameters, headers=self.headers)
        self.assertTrue('Bad response: 400 The tenant key parameter is invalid.'
                        in context.exception.message)

    def test_post_returns_bad_response_for_missing_customer_location_name(self):
        request_parameters = {'tenantKey': self.tenant_key.urlsafe(),
                              'customerLocationCode': 'store_4532',
                              'timezone': 'America/Phoenix',
                              'active': True,
                              'address': '123 Main St.',
                              'city': 'Minneapolis',
                              'state': 'MN',
                              'postalCode': '55401',
                              'latitude': 44.986656,
                              'longitude': -93.258133,
                              'dma': 'some dma code'
                              }
        uri = application.router.build(None, 'location-create', None, {})
        with self.assertRaises(AppError) as context:
            self.app.post_json(uri, params=request_parameters, headers=self.headers)
        self.assertTrue('Bad response: 400 The customer location name parameter is invalid.'
                        in context.exception.message)

    def test_post_returns_bad_response_for_missing_customer_location_code(self):
        request_parameters = {'tenantKey': self.tenant_key.urlsafe(),
                              'customerLocationName': 'Store 4532',
                              'timezone': 'America/Phoenix',
                              'active': True,
                              'address': '123 Main St.',
                              'city': 'Minneapolis',
                              'state': 'MN',
                              'postalCode': '55401',
                              'latitude': 44.986656,
                              'longitude': -93.258133,
                              'dma': 'some dma code'
                              }
        uri = application.router.build(None, 'location-create', None, {})
        with self.assertRaises(AppError) as context:
            self.app.post_json(uri, params=request_parameters, headers=self.headers)
        self.assertTrue('Bad response: 400 The customer location code parameter is invalid.'
                        in context.exception.message)

    def test_post_returns_bad_response_for_missing_active(self):
        request_parameters = {'tenantKey': self.tenant_key.urlsafe(),
                              'customerLocationName': 'Store 4532',
                              'customerLocationCode': 'store_4532',
                              'timezone': 'America/Phoenix',
                              'address': '123 Main St.',
                              'city': 'Minneapolis',
                              'state': 'MN',
                              'postalCode': '55401',
                              'latitude': 44.986656,
                              'longitude': -93.258133,
                              'dma': 'some dma code'
                              }
        uri = application.router.build(None, 'location-create', None, {})
        with self.assertRaises(AppError) as context:
            self.app.post_json(uri, params=request_parameters, headers=self.headers)
        self.assertTrue('Bad response: 400 The active parameter is invalid.'
                        in context.exception.message)

    def test_post_returns_conflict_when_encountering_an_existing_customer_location_code(self):
        location = Location.create(tenant_key=self.tenant_key,
                                   customer_location_name=self.CUSTOMER_LOCATION_NAME,
                                   customer_location_code=self.CUSTOMER_LOCATION_CODE)
        location.put()
        request_parameters = {'tenantKey': self.tenant_key.urlsafe(),
                              'customerLocationName': 'Store 4532',
                              'customerLocationCode': self.CUSTOMER_LOCATION_CODE,
                              'active': True,
                              'address': '123 Main St.',
                              'city': 'Minneapolis',
                              'state': 'MN',
                              'postalCode': '55401',
                              'latitude': 44.986656,
                              'longitude': -93.258133,
                              'dma': 'some dma code'
                              }
        uri = application.router.build(None, 'location-create', None, {})
        with self.assertRaises(AppError) as context:
            self.app.post_json(uri, params=request_parameters, headers=self.headers)
        error_message = "Bad response: 409 Conflict. Customer location code \"{0}\" is already assigned for tenant.".format(
            self.CUSTOMER_LOCATION_CODE)
        self.assertTrue(error_message in context.exception.message)

    ##################################################################################################################
    ## get
    ##################################################################################################################
    def test_get_location_representation(self):
        request_parameters = {}
        uri = application.router.build(None, 'manage-location', None,
                                       {'location_urlsafe_key': self.location_key.urlsafe()})
        response = self.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertEqual(response_json.get('customerLocationName'), self.CUSTOMER_LOCATION_NAME)
        self.assertEqual(response_json.get('customerLocationCode'), self.CUSTOMER_LOCATION_CODE)
        self.assertTrue(response_json.get('active'))

    ##################################################################################################################
    ## put
    ##################################################################################################################
    def test_put_returns_no_content_status(self):
        uri = application.router.build(None, 'manage-location', None,
                                       {'location_urlsafe_key': self.location_key.urlsafe()})
        customer_location_name = 'Acme, Inc.'
        entity_body = {
            'customerLocationName': customer_location_name,
            'active': True,
            'latitude':44.98,
            'longitude': -93.27
        }
        response = self.app.put_json(uri, entity_body, headers=self.headers)
        self.assertEqual(204, response.status_int)

    def test_put_updates_selected_properties(self):
        uri = application.router.build(None, 'manage-location', None,
                                       {'location_urlsafe_key': self.location_key.urlsafe()})
        customer_location_name = 'Acme, Inc.'
        entity_body = {
            'customerLocationName': customer_location_name,
            'active': False
        }
        self.app.put_json(uri, entity_body, headers=self.headers)
        expected = self.location_key.get()
        self.assertEqual(expected.customer_location_name, customer_location_name)
        self.assertEqual(expected.customer_location_code, self.CUSTOMER_LOCATION_CODE)
        geo_location_default = ndb.GeoPt(44.98, -93.27)  # Home plate Target Field
        self.assertEqual(expected.geo_location.lat, geo_location_default.lat)
        self.assertEqual(expected.geo_location.lon, geo_location_default.lon)
        self.assertFalse(expected.active)

    def load_tenant_locations(self, number_of_locations, tenant_key):
        for x in range(number_of_locations):
            customer_location_name = 'Store #{0}'.format(x)
            customer_location_code = 'store_{0}'.format(x)
            location = Location.create(tenant_key=tenant_key,
                                       customer_location_name=customer_location_name,
                                       customer_location_code=customer_location_code)
            location.put()
