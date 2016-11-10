import uuid

from google.appengine.ext import ndb

from app_config import config
from env_setup import setup_test_paths
from utils.timezone_util import TimezoneUtil

setup_test_paths()

import json
from datetime import datetime
from restler.serializers import to_json
from strategy import CHROME_OS_DEVICE_STRATEGY
from agar.test import BaseTest
from models import ChromeOsDevice, Tenant, Domain, Distributor, Location

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>. Bob MacNeal <bob.macneal@agosto.com>'


class TestChromeOsDeviceModel(BaseTest):
    TESTING_DEVICE_ID = '132e235a-b346-5b77-a345-de49fa753a2a'
    TEST_GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
    NAME = 'foobar tenant'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://skykit-contentmanager-int.appspot.com/content'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
    CHROME_DEVICE_DOMAIN = 'bar.com'
    CONTENT_SERVER_API_KEY = 'API KEY'
    TENANT_CODE = 'foobar'
    MAC_ADDRESS = '54271e619346'
    SERIAL_NUMBER = 'E3MSCX004781'
    MODEL = 'ASUS Chromebox'
    DISTRIBUTOR_NAME = 'agosto'
    CURRENT_CLASS_VERSION = 3
    IMPERSONATION_EMAIL = 'test@test.com'
    DISPLAY_PANEL_MODEL = 'Sharp-PNE521'
    DISPLAY_PANEL_INPUT = 'sha6'
    TIME_ZONE = 'UTC-6'
    LATITUDE = 37.78
    LONGITUDE = -122.41
    CUSTOMER_DISPLAY_CODE = 'front_reception'
    REGISTRATION_CORRELATION_IDENTIFIER = 'correlation id'

    def setUp(self):
        super(TestChromeOsDeviceModel, self).setUp()
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
                                              active=True)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.distributor_key,
                                    impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                    active=True)
        self.domain_key = self.domain.put()
        self.tenant = Tenant.create(name=self.NAME,
                                    tenant_code=self.TENANT_CODE,
                                    admin_email=self.ADMIN_EMAIL,
                                    content_server_url=self.CONTENT_SERVER_URL,
                                    content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                    domain_key=self.domain_key,
                                    active=True)
        self.tenant_key = self.tenant.put()

    def test_get_by_device_id(self):
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS)
        expected_key = device.put()
        actual = ChromeOsDevice.get_by_device_id(self.TESTING_DEVICE_ID)
        self.assertEqual(actual.key, expected_key)

    def test_get_by_device_id_none_returned_when_device_id_invalid(self):
        actual = ChromeOsDevice.get_by_device_id(self.TESTING_DEVICE_ID)
        self.assertIsNone(actual)

    def test_create_managed(self):
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS)
        self.assertIsNotNone(device)
        self.assertIsNotNone(device.api_key)

    def test_create_managed_handles_proof_of_play_editable_when_tenant_allows(self):
        self.tenant.proof_of_play_logging = True
        self.tenant.put()
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS)
        self.assertTrue(device.proof_of_play_editable)

    def test_create_managed_handles_proof_of_play_editable_when_if_tenant_prohibits(self):
        self.tenant.proof_of_play_logging = False
        self.tenant.put()
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS)
        self.assertFalse(device.proof_of_play_editable)

    def test_create_managed_auto_sets_heartbeat_info(self):
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS)
        self.assertFalse(device.is_unmanaged_device)
        self.assertTrue(device.up)
        self.assertTrue(device.storage_utilization is 0)
        self.assertTrue(device.memory_utilization is 0)
        self.assertTrue(device.heartbeat_updated <= datetime.utcnow())
        self.assertEqual(device.program, '****initial****')
        self.assertEqual(device.program_id, '****initial****')
        self.assertTrue(device.heartbeat_interval_minutes is config.PLAYER_HEARTBEAT_INTERVAL_MINUTES)

    def test_create_managed_has_expected_default_check_for_content_interval(self):
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS)
        self.assertTrue(device.check_for_content_interval_minutes is config.CHECK_FOR_CONTENT_INTERVAL_MINUTES)

    def test_create_unmanaged_auto_sets_heartbeat_info(self):
        device = ChromeOsDevice.create_unmanaged(self.TEST_GCM_REGISTRATION_ID, self.MAC_ADDRESS)
        self.assertTrue(device.is_unmanaged_device)
        self.assertTrue(device.up)
        self.assertTrue(device.storage_utilization is 0)
        self.assertTrue(device.memory_utilization is 0)
        self.assertTrue(device.heartbeat_updated <= datetime.utcnow())
        self.assertEqual(device.program, '****initial****')
        self.assertEqual(device.program_id, '****initial****')
        self.assertTrue(device.heartbeat_interval_minutes is config.PLAYER_HEARTBEAT_INTERVAL_MINUTES)

    def test_json_serialization_strategy_with_default_timezone(self):
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS)
        device.panel_model = self.DISPLAY_PANEL_MODEL
        device.panel_input = self.DISPLAY_PANEL_INPUT
        customer_location_name = 'Store 445'
        customer_location_code = 'store_445'
        customer_display_name = 'Panel in Reception'
        customer_display_code = 'panel_in_reception'
        content_manager_display_name = 'Foo Panel'
        content_manager_location_description = 'Lobby'
        device.customer_display_name = customer_display_name
        device.customer_display_code = customer_display_code
        device.content_manager_display_name = content_manager_display_name
        device.content_manager_location_description = content_manager_location_description
        timezone = config.DEFAULT_TIMEZONE
        location = Location.create(tenant_key=self.tenant_key,
                                   customer_location_name=customer_location_name,
                                   customer_location_code=customer_location_code)
        location.geo_location = ndb.GeoPt(self.LATITUDE, self.LONGITUDE)
        device.registration_correlation_identifier = self.REGISTRATION_CORRELATION_IDENTIFIER
        device.location_key = location.put()
        device.put()
        json_representation = json.loads(to_json(device, CHROME_OS_DEVICE_STRATEGY))
        self.assertEqual(str(device.device_id), json_representation['deviceId'])
        self.assertEqual(str(device.gcm_registration_id), json_representation['gcmRegistrationId'])
        self.assertEqual(None, json_representation['serialNumber'])
        self.assertIsNotNone(json_representation['created'])
        self.assertIsNotNone(json_representation['updated'])
        self.assertEqual(str(device.api_key), json_representation['apiKey'])
        self.assertEqual(str(self.tenant.name), json_representation['tenantName'])
        self.assertEqual(str(self.tenant.content_server_url), json_representation['contentServerUrl'])
        self.assertEqual(str(device.mac_address), json_representation['macAddress'])
        self.assertEqual(str(device.panel_input), json_representation['panelInput'])
        self.assertEqual(str(device.panel_model), json_representation['panelModel'])
        self.assertEqual(str(device.location_key.urlsafe()), json_representation['locationKey'])
        self.assertEqual(customer_location_name, json_representation['customerLocationName'])
        self.assertEqual(customer_location_code, json_representation['customerLocationCode'])
        self.assertEqual(customer_display_name, json_representation['customerDisplayName'])
        self.assertEqual(customer_display_code, json_representation['customerDisplayCode'])
        self.assertEqual(content_manager_display_name, json_representation['contentManagerDisplayName'])
        self.assertEqual(content_manager_location_description, json_representation['contentManagerLocationDescription'])

        self.assertEqual(self.LATITUDE, json_representation['latitude'])
        self.assertEqual(self.LONGITUDE, json_representation['longitude'])
        self.assertEqual(timezone, json_representation['timezone'])
        self.assertEqual(TimezoneUtil.get_timezone_offset(json_representation['timezone']),
                         json_representation['timezoneOffset'])
        self.assertEqual(self.REGISTRATION_CORRELATION_IDENTIFIER,
                         json_representation['registrationCorrelationIdentifier'])

    def test_json_serialization_strategy_with_explicit_timezone(self):
        timezone = 'America/Denver'
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS,
                                               timezone=timezone)
        device.put()
        json_representation = json.loads(to_json(device, CHROME_OS_DEVICE_STRATEGY))
        self.assertEqual(timezone, json_representation['timezone'])
        self.assertEqual(TimezoneUtil.get_timezone_offset(json_representation['timezone']),
                         json_representation['timezoneOffset'])

    def test_json_serialization_strategy_with_default_geo_location(self):
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS)
        device.panel_model = self.DISPLAY_PANEL_MODEL
        device.panel_input = self.DISPLAY_PANEL_INPUT
        customer_location_name = 'Store 445'
        customer_location_code = 'store_445'
        timezone = config.DEFAULT_TIMEZONE
        location = Location.create(tenant_key=self.tenant_key,
                                   customer_location_name=customer_location_name,
                                   customer_location_code=customer_location_code)
        device.location_key = location.put()
        device.annotated_asset_id = 'test asset id'
        device.put()
        json_representation = json.loads(to_json(device, CHROME_OS_DEVICE_STRATEGY))
        self.assertEqual(str(device.annotated_asset_id), json_representation['annotatedAssetId'])
        self.assertEqual(str(device.device_id), json_representation['deviceId'])
        self.assertEqual(str(device.gcm_registration_id), json_representation['gcmRegistrationId'])
        self.assertEqual(None, json_representation['serialNumber'])
        self.assertIsNotNone(json_representation['created'])
        self.assertIsNotNone(json_representation['updated'])
        self.assertEqual(str(device.api_key), json_representation['apiKey'])
        self.assertEqual(str(self.tenant.name), json_representation['tenantName'])
        self.assertEqual(str(self.tenant.content_server_url), json_representation['contentServerUrl'])
        self.assertEqual(str(device.mac_address), json_representation['macAddress'])
        self.assertEqual(str(device.panel_input), json_representation['panelInput'])
        self.assertEqual(str(device.panel_model), json_representation['panelModel'])
        self.assertEqual(str(device.location_key.urlsafe()), json_representation['locationKey'])
        self.assertEqual(customer_location_name, json_representation['customerLocationName'])
        self.assertEqual(customer_location_code, json_representation['customerLocationCode'])
        geo_location_default = ndb.GeoPt(44.98, -93.27)
        self.assertEqual(geo_location_default.lat, json_representation['latitude'])
        self.assertEqual(geo_location_default.lon, json_representation['longitude'])
        self.assertEqual(timezone, json_representation['timezone'])
        self.assertEqual(TimezoneUtil.get_timezone_offset(json_representation['timezone']),
                         json_representation['timezoneOffset'])

    def test_json_serialization_strategy_with_optional_serial_number(self):
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS,
                                               serial_number=self.SERIAL_NUMBER,
                                               model=self.MODEL)
        device.put()
        json_representation = json.loads(to_json(device, CHROME_OS_DEVICE_STRATEGY))
        self.assertEqual(self.SERIAL_NUMBER, json_representation['serialNumber'])
        self.assertEqual(str(device.name), '{0} {1}'.format(self.SERIAL_NUMBER, self.MODEL))
        self.assertEqual(str(device.loggly_link),
                         'https://skykit.loggly.com/search?&terms=tag%3A"{0}"'.format(self.SERIAL_NUMBER))

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS,
                                               serial_number=self.SERIAL_NUMBER)
        device.class_version = 47
        device.put()
        self.assertEqual(device.class_version, self.CURRENT_CLASS_VERSION)

    def test_get_tenant_returns_tenant_representation(self):
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS)
        device.put()
        tenant = device.get_tenant()
        self.assertEqual(tenant, self.tenant)

    def test_mac_address_already_assigned(self):
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS)
        device.put()
        self.assertTrue(ChromeOsDevice.mac_address_already_assigned(self.MAC_ADDRESS, is_unmanaged_device=False))

    def test_ethernet_mac_address_already_assigned(self):
        ethernet_mac_address = '03271e619341'
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address='23271e61934d')
        device.ethernet_mac_address = ethernet_mac_address
        device.put()
        self.assertTrue(ChromeOsDevice.mac_address_already_assigned(ethernet_mac_address, is_unmanaged_device=False))

    def test_mac_address_already_assigned_for_case_where_it_has_not_yet_been_assigned(self):
        self.assertFalse(ChromeOsDevice.mac_address_already_assigned('0326f1e61930d', is_unmanaged_device=False))

    def test_get_unmanaged_device_by_mac_address(self):
        ChromeOsDevice.create_unmanaged(self.TEST_GCM_REGISTRATION_ID, self.MAC_ADDRESS).put()
        unmanaged_device = ChromeOsDevice.get_unmanaged_device_by_mac_address(self.MAC_ADDRESS)
        self.assertIsNotNone(unmanaged_device)

    def test_get_unmanaged_device_by_mac_address_with_bogus_mac_address(self):
        unmanaged_device = ChromeOsDevice.get_unmanaged_device_by_mac_address('bogus')
        self.assertIsNone(unmanaged_device)

    def test_get_unmanaged_device_by_gcm_registration_id(self):
        ChromeOsDevice.create_unmanaged(self.TEST_GCM_REGISTRATION_ID, self.MAC_ADDRESS).put()
        unmanaged_device = ChromeOsDevice.get_unmanaged_device_by_gcm_registration_id(self.TEST_GCM_REGISTRATION_ID)
        self.assertIsNotNone(unmanaged_device)

    def test_get_unmanaged_device_by_gcm_registration_id_with_bogus_gcm_registration_id(self):
        unmanaged_device = ChromeOsDevice.get_unmanaged_device_by_gcm_registration_id('bogus')
        self.assertIsNone(unmanaged_device)

    def test_gcm_registration_id_already_assigned_for_case_where_it_has_not_yet_been_assigned(self):
        self.assertFalse(ChromeOsDevice.gcm_registration_id_already_assigned('Foobar', is_unmanaged_device=False))

    def test_gcm_registration_id_already_assigned_for_managed_case_where_it_has_been_assigned(self):
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS)
        device.put()
        self.assertTrue(ChromeOsDevice.gcm_registration_id_already_assigned(self.TEST_GCM_REGISTRATION_ID,
                                                                            is_unmanaged_device=False))

    def test_gcm_registration_id_already_assigned_for_unmanaged_case_where_it_has_been_assigned(self):
        unmanaged_device = ChromeOsDevice.create_unmanaged(gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                                           mac_address=self.MAC_ADDRESS)
        unmanaged_device.put()
        self.assertTrue(ChromeOsDevice.gcm_registration_id_already_assigned(self.TEST_GCM_REGISTRATION_ID,
                                                                            is_unmanaged_device=True))

    def test_is_rogue_unmanaged_device_without_tenant_key_returns_true(self):
        device = ChromeOsDevice.create_unmanaged(self.TEST_GCM_REGISTRATION_ID, self.MAC_ADDRESS)
        device.put()
        self.assertTrue(ChromeOsDevice.is_rogue_unmanaged_device(self.MAC_ADDRESS))

    def test_is_rogue_unmanaged_device_check_with_tenant_key_returns_false(self):
        device = ChromeOsDevice.create_unmanaged(self.TEST_GCM_REGISTRATION_ID, self.MAC_ADDRESS)
        device.tenant_key = self.tenant_key
        device.put()
        self.assertFalse(ChromeOsDevice.is_rogue_unmanaged_device(self.MAC_ADDRESS))

    def test_create_sets_proof_of_play_logging_to_false(self):
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS,
                                               serial_number=self.SERIAL_NUMBER,
                                               model=self.MODEL)
        device.put()
        self.assertFalse(device.proof_of_play_logging)

    def test_create_sets_proof_of_play_editable_to_false(self):
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS,
                                               serial_number=self.SERIAL_NUMBER,
                                               model=self.MODEL)
        device.put()
        self.assertFalse(device.proof_of_play_editable)

    def test_json_serialization_strategy_of_proof_of_play_logging(self):
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS,
                                               serial_number=self.SERIAL_NUMBER,
                                               model=self.MODEL)
        device.proof_of_play_logging = True
        device.put()
        json_representation = json.loads(to_json(device, CHROME_OS_DEVICE_STRATEGY))
        self.assertTrue(json_representation['proofOfPlayLogging'])

    def test_is_customer_display_code_unique_returns_false_when_code_found(self):
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS,
                                               serial_number=self.SERIAL_NUMBER,
                                               model=self.MODEL)
        device.customer_display_code = self.CUSTOMER_DISPLAY_CODE
        device.put()
        uniqueness_check = ChromeOsDevice.is_customer_display_code_unique(
            customer_display_code=self.CUSTOMER_DISPLAY_CODE,
            tenant_key=self.tenant_key)
        self.assertFalse(uniqueness_check)

    def test_is_customer_display_code_unique_returns_true_when_code_not_found(self):
        display_code = str(uuid.uuid4().hex)
        uniqueness_check = ChromeOsDevice.is_customer_display_code_unique(customer_display_code=display_code,
                                                                          tenant_key=self.tenant_key)
        self.assertTrue(uniqueness_check)

    def test_get_by_gcm_registration_id(self):
        gcm_registration_id = 'foobar'
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=gcm_registration_id,
                                               mac_address=self.MAC_ADDRESS,
                                               serial_number=self.SERIAL_NUMBER,
                                               model=self.MODEL,
                                               archived=False)
        device.put()
        results = ChromeOsDevice.get_by_gcm_registration_id(gcm_registration_id)
        self.assertEqual(results[0].gcm_registration_id, gcm_registration_id)
        device.archived = True
        device.put()
        results = ChromeOsDevice.get_by_gcm_registration_id(gcm_registration_id)
        self.assertEmpty(results)

    def test_get_by_mac_address(self):
        mac_address = 'foobar'
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=mac_address,
                                               serial_number=self.SERIAL_NUMBER,
                                               model=self.MODEL,
                                               archived=False)
        device.put()
        results = ChromeOsDevice.get_by_mac_address(mac_address)
        self.assertEqual(results[0].mac_address, mac_address)
        device.archived = True
        device.put()
        results = ChromeOsDevice.get_by_mac_address(mac_address)
        self.assertEmpty(results)

    def test_get_by_pairing_code(self):
        pairing_code = 'foobar'
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS,
                                               serial_number=self.SERIAL_NUMBER,
                                               model=self.MODEL,
                                               archived=False)
        device.pairing_code = pairing_code
        device.put()
        results = ChromeOsDevice.get_by_pairing_code(pairing_code)
        self.assertEqual(results[0].pairing_code, pairing_code)
        device.archived = True
        device.put()
        results = ChromeOsDevice.get_by_pairing_code(pairing_code)
        self.assertEmpty(results)

    def test_get_impersonation_email(self):
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               device_id=self.TESTING_DEVICE_ID,
                                               gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                               mac_address=self.MAC_ADDRESS)
        impersonation_email = Tenant.get_impersonation_email(urlsafe_tenant_key=device.tenant_key.urlsafe())
        self.assertEqual(impersonation_email, self.IMPERSONATION_EMAIL)

