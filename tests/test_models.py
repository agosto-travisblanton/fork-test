from agar.test import BaseTest
from models import ChromeOsDevice

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TestChromeOsDeviceModel(BaseTest):
    TESTING_DEVICE_ID = '132e235a-b346-5b77-a345-de49fa753a2a'

    def setUp(self):
        super(TestChromeOsDeviceModel, self).setUp()

    def testGetByDeviceId(self):
        chrome_os_device = ChromeOsDevice(device_id=self.TESTING_DEVICE_ID,
                                          gcm_registration_id='8d70a8d78a6dfa6df76dfasd')
        expected_key = chrome_os_device.put()
        actual = ChromeOsDevice.get_by_device_id(self.TESTING_DEVICE_ID)
        self.assertEqual(actual.key, expected_key)

    def testGetByDeviceId_NoneReturnedWhenDeviceIdInvalid(self):
        actual = ChromeOsDevice.get_by_device_id('566e235a-b346-5b77-a345-de49fa753a2a')
        self.assertIsNone(actual)