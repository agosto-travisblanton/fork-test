from env_setup import setup_test_paths

setup_test_paths()

import json
from restler.serializers import to_json
from strategy import DISPLAY_STRATEGY
from agar.test import BaseTest
from models import Display, Tenant

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestDisplayModel(BaseTest):
    TENANT_NAME = 'Foobar, Inc'
    TENANT_CODE = 'foobar_inc'
    ADMIN_EMAIL = 'admin@foobar.com'
    DEVICE_ID = '132e235a-b346-5b77-a345-de49fa753a2a'
    GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
    CONTENT_SERVER_URL = 'https://www.content.com'
    CHROME_DEVICE_DOMAIN = 'foobar.com'
    CONTENT_SERVER_API_KEY = 'API KEY'
    MAC_ADDRESS = '54271e619346'
    SERIAL_NUMBER = 'SN0MZCX005783'
    CURRENT_CLASS_VERSION = 1

    def setUp(self):
        super(TestDisplayModel, self).setUp()
        self.tenant = Tenant.create(name=self.TENANT_NAME,
                                    tenant_code=self.TENANT_CODE,
                                    admin_email=self.ADMIN_EMAIL,
                                    content_server_url=self.CONTENT_SERVER_URL,
                                    chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                                    active=True)
        self.tenant_key = self.tenant.put()

    def test_get_by_device_id(self):
        display = Display.create(tenant_key=self.tenant_key,
                                 gcm_registration_id=self.GCM_REGISTRATION_ID,
                                 mac_address=self.MAC_ADDRESS,
                                 device_id=self.DEVICE_ID)
        expected_key = display.put()
        actual = Display.get_by_device_id(self.DEVICE_ID)
        self.assertEqual(actual.key, expected_key)

    def test_get_by_device_id_none_returned_when_device_id_invalid(self):
        actual = Display.get_by_device_id(self.DEVICE_ID)
        self.assertIsNone(actual)

    def test_create(self):
        display = Display.create(tenant_key=self.tenant_key,
                                 gcm_registration_id=self.GCM_REGISTRATION_ID,
                                 mac_address=self.MAC_ADDRESS,
                                 device_id=self.DEVICE_ID)
        self.assertIsNotNone(display)
        self.assertIsNotNone(display.api_key)

    def test_json_serialization_strategy(self):
        display = Display.create(tenant_key=self.tenant_key,
                                 gcm_registration_id=self.GCM_REGISTRATION_ID,
                                 mac_address=self.MAC_ADDRESS,
                                 device_id=self.DEVICE_ID)
        display.put()
        json_representation = json.loads(to_json(display, DISPLAY_STRATEGY))
        self.assertEqual(self.DEVICE_ID, json_representation['device_id'])
        self.assertEqual(self.GCM_REGISTRATION_ID, json_representation['gcm_registration_id'])
        self.assertEqual(None, json_representation['serial_number'])
        self.assertTrue(json_representation['managed_display'])
        self.assertIsNotNone(json_representation['created'])
        self.assertIsNotNone(json_representation['updated'])
        self.assertEqual(str(display.api_key), json_representation['api_key'])
        self.assertEqual(str(self.tenant.name), json_representation['tenant']['name'])
        self.assertEqual(str(self.tenant.tenant_code), json_representation['tenant']['tenant_code'])
        self.assertEqual(str(self.tenant.admin_email), json_representation['tenant']['admin_email'])
        self.assertEqual(str(self.tenant.content_server_url), json_representation['tenant']['content_server_url'])
        self.assertEqual(str(self.tenant.chrome_device_domain), json_representation['tenant']['chrome_device_domain'])
        self.assertEqual(self.tenant.active, json_representation['tenant']['active'])

    def test_json_serialization_strategy_for_optional_chrome_os_device_properties(self):
        display = Display.create(tenant_key=self.tenant_key,
                                 gcm_registration_id=self.GCM_REGISTRATION_ID,
                                 mac_address=self.MAC_ADDRESS,
                                 device_id=self.DEVICE_ID)
        display.put()
        json_representation = json.loads(to_json(display, DISPLAY_STRATEGY))
        self.assertIsNone(json_representation['status'])
        self.assertIsNone(json_representation['last_sync'])
        self.assertIsNone(json_representation['kind'])
        self.assertIsNone(json_representation['ethernet_mac_address'])
        self.assertIsNone(json_representation['org_unit_path'])
        self.assertIsNone(json_representation['annotated_user'])
        self.assertIsNone(json_representation['boot_mode'])
        self.assertIsNone(json_representation['last_enrollment_time'])
        self.assertIsNone(json_representation['platform_version'])
        self.assertIsNone(json_representation['model'])
        self.assertIsNone(json_representation['os_version'])
        self.assertIsNone(json_representation['firmware_version'])

    def test_serialization_with_optional_serial_number(self):
        display = Display.create(tenant_key=self.tenant_key,
                                 gcm_registration_id=self.GCM_REGISTRATION_ID,
                                 mac_address=self.MAC_ADDRESS,
                                 serial_number=self.SERIAL_NUMBER
                                 )
        display.put()
        json_representation = json.loads(to_json(display, DISPLAY_STRATEGY))
        self.assertEqual(self.SERIAL_NUMBER, json_representation['serial_number'])

    def test_serialization_without_optional_serial_number(self):
        display = Display.create(tenant_key=self.tenant_key,
                                 gcm_registration_id=self.GCM_REGISTRATION_ID,
                                 mac_address=self.MAC_ADDRESS
                                 )
        display.put()
        json_representation = json.loads(to_json(display, DISPLAY_STRATEGY))
        self.assertEqual(None, json_representation['serial_number'])

    def test_serialization_with_optional_device_id(self):
        display = Display.create(tenant_key=self.tenant_key,
                                 gcm_registration_id=self.GCM_REGISTRATION_ID,
                                 mac_address=self.MAC_ADDRESS,
                                 device_id=self.DEVICE_ID
                                 )
        display.put()
        json_representation = json.loads(to_json(display, DISPLAY_STRATEGY))
        self.assertEqual(self.DEVICE_ID, json_representation['device_id'])

    def test_serialization_without_optional_device_id(self):
        display = Display.create(tenant_key=self.tenant_key,
                                 gcm_registration_id=self.GCM_REGISTRATION_ID,
                                 mac_address=self.MAC_ADDRESS
                                 )
        display.put()
        json_representation = json.loads(to_json(display, DISPLAY_STRATEGY))
        self.assertEqual(None, json_representation['device_id'])

    def test_serialization_for_un_managed_display(self):
        managed_display = False
        display = Display.create(tenant_key=self.tenant_key,
                                 gcm_registration_id=self.GCM_REGISTRATION_ID,
                                 mac_address=self.MAC_ADDRESS,
                                 device_id=self.DEVICE_ID,
                                 managed_display=managed_display
                                 )
        display.put()
        json_representation = json.loads(to_json(display, DISPLAY_STRATEGY))
        self.assertEqual(managed_display, json_representation['managed_display'])

    def test_serialization_without_optional_returns_managed_true_by_default(self):
        display = Display.create(tenant_key=self.tenant_key,
                                 gcm_registration_id=self.GCM_REGISTRATION_ID,
                                 mac_address=self.MAC_ADDRESS
                                 )
        display.put()
        json_representation = json.loads(to_json(display, DISPLAY_STRATEGY))
        self.assertEqual(True, json_representation['managed_display'])

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        display = Display.create(tenant_key=self.tenant_key,
                                 gcm_registration_id=self.GCM_REGISTRATION_ID,
                                 mac_address=self.MAC_ADDRESS
                                 )
        display.class_version = 47
        display.put()
        self.assertEqual(display.class_version, self.CURRENT_CLASS_VERSION)
