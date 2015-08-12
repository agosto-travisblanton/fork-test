from env_setup import setup_test_paths

setup_test_paths()

import json
from restler.serializers import to_json
from strategy import CHROME_OS_DEVICE_STRATEGY
from agar.test import BaseTest
from models import ChromeOsDevice, Tenant

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>. Bob MacNeal <bob.macneal@agosto.com>'


class TestChromeOsDeviceModel(BaseTest):
    TESTING_DEVICE_ID = '132e235a-b346-5b77-a345-de49fa753a2a'
    TEST_GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
    NAME = 'foobar tenant'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://www.content.com'
    CHROME_DEVICE_DOMAIN = 'bar.com'
    CONTENT_SERVER_API_KEY = 'API KEY'
    TENANT_CODE = 'foobar'
    MAC_ADDRESS = '54271e619346'
    SERIAL_NUMBER = 'E3MSCX004781'
    MODEL = 'ASUS Chromebox'
    CURRENT_CLASS_VERSION = 2

    def setUp(self):
        super(TestChromeOsDeviceModel, self).setUp()
        self.tenant = Tenant.create(name=self.NAME,
                                    tenant_code=self.TENANT_CODE,
                                    admin_email=self.ADMIN_EMAIL,
                                    content_server_url=self.CONTENT_SERVER_URL,
                                    chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                                    active=True)
        self.tenant_key = self.tenant.put()

    def test_get_by_device_id(self):
        chrome_os_device = ChromeOsDevice.create(tenant_key=self.tenant_key,
                                                 device_id=self.TESTING_DEVICE_ID,
                                                 gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                                 mac_address=self.MAC_ADDRESS)
        expected_key = chrome_os_device.put()
        actual = ChromeOsDevice.get_by_device_id(self.TESTING_DEVICE_ID)
        self.assertEqual(actual.key, expected_key)

    def test_get_by_device_id_none_returned_when_device_id_invalid(self):
        actual = ChromeOsDevice.get_by_device_id(self.TESTING_DEVICE_ID)
        self.assertIsNone(actual)

    def test_create(self):
        chrome_os_device = ChromeOsDevice.create(tenant_key=self.tenant_key,
                                                 device_id=self.TESTING_DEVICE_ID,
                                                 gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                                 mac_address=self.MAC_ADDRESS)
        self.assertIsNotNone(chrome_os_device)
        self.assertIsNotNone(chrome_os_device.api_key)

    def test_json_serialization_strategy(self):
        chrome_os_device = ChromeOsDevice.create(tenant_key=self.tenant_key,
                                                 device_id=self.TESTING_DEVICE_ID,
                                                 gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                                 mac_address=self.MAC_ADDRESS)
        chrome_os_device.put()
        json_representation = json.loads(to_json(chrome_os_device, CHROME_OS_DEVICE_STRATEGY))
        self.assertEqual(self.TESTING_DEVICE_ID, json_representation['device_id'])
        self.assertEqual(self.TEST_GCM_REGISTRATION_ID, json_representation['gcm_registration_id'])
        self.assertEqual(None, json_representation['serial_number'])
        self.assertIsNotNone(json_representation['created'])
        self.assertIsNotNone(json_representation['updated'])
        self.assertEqual(str(chrome_os_device.api_key), json_representation['api_key'])
        self.assertEqual(str(self.tenant.name), json_representation['tenant_name'])
        self.assertEqual(str(self.tenant.content_server_url), json_representation['content_server_url'])
        self.assertEqual(str(self.tenant.chrome_device_domain), json_representation['chrome_device_domain'])

    def test_json_serialization_strategy_with_optional_serial_number(self):
        chrome_os_device = ChromeOsDevice.create(tenant_key=self.tenant_key,
                                                 device_id=self.TESTING_DEVICE_ID,
                                                 gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                                 mac_address=self.MAC_ADDRESS,
                                                 serial_number=self.SERIAL_NUMBER,
                                                 model=self.MODEL)
        chrome_os_device.put()
        json_representation = json.loads(to_json(chrome_os_device, CHROME_OS_DEVICE_STRATEGY))
        self.assertEqual(self.TESTING_DEVICE_ID, json_representation['device_id'])
        self.assertEqual(self.TEST_GCM_REGISTRATION_ID, json_representation['gcm_registration_id'])
        self.assertEqual(self.SERIAL_NUMBER, json_representation['serial_number'])
        self.assertIsNotNone(json_representation['created'])
        self.assertIsNotNone(json_representation['updated'])
        self.assertEqual(str(chrome_os_device.api_key), json_representation['api_key'])
        self.assertEqual(str(chrome_os_device.name), '{0} {1}'.format(self.SERIAL_NUMBER, self.MODEL))

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        chrome_os_device = ChromeOsDevice.create(tenant_key=self.tenant_key,
                                                 device_id=self.TESTING_DEVICE_ID,
                                                 gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                                 mac_address=self.MAC_ADDRESS,
                                                 serial_number=self.SERIAL_NUMBER)
        chrome_os_device.class_version = 47
        chrome_os_device.put()
        self.assertEqual(chrome_os_device.class_version, self.CURRENT_CLASS_VERSION)
