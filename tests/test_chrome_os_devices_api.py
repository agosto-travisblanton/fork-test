from agar.test import BaseTest
from chrome_os_devices_api import ChromeOsDevicesApi


class TestChromeOsDevicesApi(BaseTest):

    SKYKIT_COM_CUSTOMER_ID = 'C04c2u0lg'
    ADMIN_ACCOUNT_TO_IMPERSONATE = 'administrator@skykit.com'

    def setUp(self):
        super(TestChromeOsDevicesApi, self).setUp()
        self.chrome_os_devices_api = ChromeOsDevicesApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)

    def test_list(self):
        devices = self.chrome_os_devices_api.list(self.SKYKIT_COM_CUSTOMER_ID)
        self.assertIsNotNone(devices)

    def test_update(self):
        pass
