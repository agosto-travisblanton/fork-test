from env_setup import setup_test_paths; setup_test_paths()

from time import sleep, gmtime, strftime

from agar.test import BaseTest
from chrome_os_devices_api import ChromeOsDevicesApi
from pprint import pprint


class TestChromeOsDevicesApi(BaseTest):
    SKYKIT_COM_CUSTOMER_ID = 'C04c2u0lg'
    ADMIN_ACCOUNT_TO_IMPERSONATE = 'administrator@skykit.com'
    TESTING_DEVICE_ID = '6daf712b-7a65-4450-abcd-45027a47a716'
    ORG_UNIT_DEPLOYED = '/SKD Automated Test/SKD Automated Deployed'
    ORG_UNIT_DISTRIBUTOR = '/SKD Automated Test/SKD Automated Distributor'

    def setUp(self):
        super(TestChromeOsDevicesApi, self).setUp()
        self.chrome_os_devices_api = ChromeOsDevicesApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)

    def testList(self):
        devices = self.chrome_os_devices_api.list(self.SKYKIT_COM_CUSTOMER_ID)
        pprint(devices)
        self.assertIsNotNone(devices)
        self.assertTrue(len(devices) > 0)

    def testGet(self):
        device = self.chrome_os_devices_api.get(self.SKYKIT_COM_CUSTOMER_ID, self.TESTING_DEVICE_ID)
        self.assertIsNotNone(device)
        pprint(device)

    def testUpdateOrgUnitPath(self):
        org_unit_path_changing_to = self.ORG_UNIT_DEPLOYED
        if self.findByDeviceIdAndOrgUnit(self.TESTING_DEVICE_ID, self.ORG_UNIT_DEPLOYED):
            org_unit_path_changing_to = self.ORG_UNIT_DISTRIBUTOR
        self.chrome_os_devices_api.update(self.SKYKIT_COM_CUSTOMER_ID,
                                          self.TESTING_DEVICE_ID,
                                          org_unit_path=org_unit_path_changing_to)
        sleep(1)
        device = self.chrome_os_devices_api.get(self.SKYKIT_COM_CUSTOMER_ID, self.TESTING_DEVICE_ID)
        self.assertEqual(org_unit_path_changing_to, device.get('orgUnitPath'))

    def testUpdateNotes(self):
        new_notes = 'Notes updated at {0} from unit test.'.format(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        self.chrome_os_devices_api.update(self.SKYKIT_COM_CUSTOMER_ID,
                                          self.TESTING_DEVICE_ID,
                                          notes=new_notes)
        sleep(1)
        device = self.chrome_os_devices_api.get(self.SKYKIT_COM_CUSTOMER_ID, self.TESTING_DEVICE_ID)
        self.assertEqual(new_notes, device.get('notes'))

    def testUpdateAnnotatedLocation(self):
        new_location = 'Location updated at {0} from unit test.'.format(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        self.chrome_os_devices_api.update(self.SKYKIT_COM_CUSTOMER_ID,
                                          self.TESTING_DEVICE_ID,
                                          annotated_location=new_location)
        sleep(1)
        device = self.chrome_os_devices_api.get(self.SKYKIT_COM_CUSTOMER_ID, self.TESTING_DEVICE_ID)
        self.assertEqual(new_location, device.get('annotatedLocation'))

    def testUpdateAnnotatedUser(self):
        new_user = 'administrator-{0}@skykit.com'.format(strftime("%m-%d-%Y-%H-%M-%S", gmtime()))
        self.chrome_os_devices_api.update(self.SKYKIT_COM_CUSTOMER_ID,
                                          self.TESTING_DEVICE_ID,
                                          annotated_user=new_user)
        sleep(1)
        device = self.chrome_os_devices_api.get(self.SKYKIT_COM_CUSTOMER_ID, self.TESTING_DEVICE_ID)
        self.assertEqual(new_user, device.get('annotatedUser'))

    def findByDeviceIdAndOrgUnit(self, device_id, org_unit):
        device = self.chrome_os_devices_api.get(self.SKYKIT_COM_CUSTOMER_ID, device_id)
        if device.get('orgUnitPath') == org_unit:
            return device
        else:
            return None
