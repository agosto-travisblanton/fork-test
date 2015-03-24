from agar.test import BaseTest
from chrome_os_devices_api import ChromeOsDevicesApi


class TestChromeOsDevicesApi(BaseTest):
    def setUp(self):
        super(TestChromeOsDevicesApi, self).setUp()
        self.chrome_os_devices_api = ChromeOsDevicesApi()

    def test_list(self):
        pass

    def test_update(self):
        pass
