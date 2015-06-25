from env_setup import setup_test_paths;

setup_test_paths()

from agar.test import BaseTest
from models import ChromeOsDevice, Tenant

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TestChromeOsDeviceModel(BaseTest):
    TESTING_DEVICE_ID = '132e235a-b346-5b77-a345-de49fa753a2a'
    TEST_GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
    NAME = 'foobar tenant'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://www.content.com'
    CHROME_DEVICE_DOMAIN = 'bar.com'

    def setUp(self):
        super(TestChromeOsDeviceModel, self).setUp()
        self.tenant = Tenant.create(name=self.NAME,
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               content_server_api_key='',
                               chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                               active=True)
        self.tenant_key = self.tenant.put()

    def test_get_by_device_id(self):
        chrome_os_device = ChromeOsDevice(device_id=self.TESTING_DEVICE_ID,
                                          gcm_registration_id=self.TEST_GCM_REGISTRATION_ID, tenant_code='Acme')
        expected_key = chrome_os_device.put()
        actual = ChromeOsDevice.get_by_device_id(self.TESTING_DEVICE_ID)
        self.assertEqual(actual.key, expected_key)

    def test_get_by_device_id_none_returned_when_device_id_invalid(self):
        actual = ChromeOsDevice.get_by_device_id(self.TESTING_DEVICE_ID)
        self.assertIsNone(actual)

    def test_create(self):
        chrome_os_device = ChromeOsDevice.create(tenant_key=self.tenant_key,
                                                 device_id=self.TESTING_DEVICE_ID,
                                                 gcm_registration_id=self.TEST_GCM_REGISTRATION_ID)
        self.assertIsNotNone(chrome_os_device)