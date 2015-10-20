from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
from models import UnmanagedDevice

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestUnmanagedDeviceModel(BaseTest):
    TEST_GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
    MAC_ADDRESS = '54271e619346'
    CURRENT_CLASS_VERSION = 1
    IMPERSONATION_EMAIL = 'test@test.com'

    def setUp(self):
        super(TestUnmanagedDeviceModel, self).setUp()

    def test_create(self):
        unmanaged_device = UnmanagedDevice.create(
            gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
            mac_address=self.MAC_ADDRESS)
        self.assertIsNotNone(unmanaged_device)
        self.assertIsNotNone(unmanaged_device.api_key)
        self.assertIsNotNone(unmanaged_device.pairing_code)

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        unmanaged_device = UnmanagedDevice.create(
            gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
            mac_address=self.MAC_ADDRESS)
        unmanaged_device.class_version = 47
        unmanaged_device.put()
        self.assertEqual(unmanaged_device.class_version, self.CURRENT_CLASS_VERSION)

    def test_get_by_gcm_registration_id_returns_matching_unmanaged_device(self):
        unmanaged_device = UnmanagedDevice.create(
            gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
            mac_address=self.MAC_ADDRESS)
        unmanaged_device.put()
        actual = UnmanagedDevice.get_by_gcm_registration_id(self.TEST_GCM_REGISTRATION_ID)
        self.assertEqual(actual.mac_address, self.MAC_ADDRESS)

    def test_get_by_mac_address_returns_matching_unmanaged_device(self):
        unmanaged_device = UnmanagedDevice.create(
            gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
            mac_address=self.MAC_ADDRESS)
        unmanaged_device.put()
        actual = UnmanagedDevice.get_by_mac_address(self.MAC_ADDRESS)
        self.assertEqual(actual.gcm_registration_id, self.TEST_GCM_REGISTRATION_ID)

    def test_create_generates_pairing_code(self):
        unmanaged_device = UnmanagedDevice.create(
            gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
            mac_address=self.MAC_ADDRESS)
        self.assertIsNotNone(unmanaged_device.pairing_code)

    def test_create_generates_api_key(self):
        unmanaged_device = UnmanagedDevice.create(
            gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
            mac_address=self.MAC_ADDRESS)
        self.assertIsNotNone(unmanaged_device.api_key)
