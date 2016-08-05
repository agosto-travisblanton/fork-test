from time import sleep, strftime, gmtime

from env_setup import setup_test_paths

setup_test_paths()

from models import Tenant, ChromeOsDevice, Distributor, Domain
from agar.test import BaseTest
from integrations.directory_api.chrome_os_devices_api import ChromeOsDevicesApi


class TestChromeOsDevicesApi(BaseTest):
    SKYKIT_COM_CUSTOMER_ID = 'C04c2u0lg'
    ADMIN_ACCOUNT_TO_IMPERSONATE = 'administrator@skykit.com'
    TESTING_DEVICE_ID = '6daf712b-7a65-4450-abcd-45027a47a716'
    ORG_UNIT_DEPLOYED = '/SKD Automated Test/SKD Automated Deployed'
    ORG_UNIT_DISTRIBUTOR = '/SKD Automated Test/SKD Automated Distributor'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    DISTRIBUTOR_NAME = 'agosto'
    IMPERSONATION_EMAIL = 'administrator@skykit.com'

    def setUp(self):
        super(TestChromeOsDevicesApi, self).setUp()
        self.chrome_os_devices_api = ChromeOsDevicesApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
                                              active=True)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.distributor_key,
                                    impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                    active=True)
        self.domain_key = self.domain.put()
        self.tenant = Tenant.create(name='Foobar, Inc',
                                    tenant_code='foobar_inc',
                                    admin_email='admin@foobar.com',
                                    content_server_url='https://skykit-contentmanager-int.appspot.com/content',
                                    content_manager_base_url='https://skykit-contentmanager-int.appspot.com',
                                    domain_key=self.domain_key,
                                    active=True)
        self.tenant_key = self.tenant.put()
        self.mac_address = '54271e4af1e7'
        self.device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                                    gcm_registration_id='8d70a8d78a6dfa6df76dfasd',
                                                    mac_address=self.mac_address)
        self.device_key = self.device.put()

    def test_list(self):
        devices = self.chrome_os_devices_api.list(self.SKYKIT_COM_CUSTOMER_ID)
        self.assertIsNotNone(devices)
        self.assertTrue(len(devices) > 0)

    def test_get(self):
        device = self.chrome_os_devices_api.get(self.SKYKIT_COM_CUSTOMER_ID, self.TESTING_DEVICE_ID)
        self.assertIsNotNone(device)

    def test_update_org_unit_path_no_device_id(self):
        self.chrome_os_devices_api.update(self.SKYKIT_COM_CUSTOMER_ID,
                                          None,
                                          org_unit_path='/Not/used')

    def test_update_org_unit_path(self):
        org_unit_path_changing_to = self.ORG_UNIT_DEPLOYED
        if self._find_by_device_id_and_org_unit(self.TESTING_DEVICE_ID, self.ORG_UNIT_DEPLOYED):
            org_unit_path_changing_to = self.ORG_UNIT_DISTRIBUTOR
        self.chrome_os_devices_api.update(self.SKYKIT_COM_CUSTOMER_ID,
                                          self.TESTING_DEVICE_ID,
                                          org_unit_path=org_unit_path_changing_to)
        sleep(1)
        device = self.chrome_os_devices_api.get(self.SKYKIT_COM_CUSTOMER_ID, self.TESTING_DEVICE_ID)
        self.assertEqual(org_unit_path_changing_to, device.get('orgUnitPath'))

    def test_update_notes(self):
        new_notes = 'Notes updated at {0} from unit test.'.format(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        self.chrome_os_devices_api.update(self.SKYKIT_COM_CUSTOMER_ID,
                                          self.TESTING_DEVICE_ID,
                                          notes=new_notes)
        sleep(1)
        device = self.chrome_os_devices_api.get(self.SKYKIT_COM_CUSTOMER_ID, self.TESTING_DEVICE_ID)
        self.assertEqual(new_notes, device.get('notes'))

    def test_update_annotated_location(self):
        new_location = 'Location updated at {0} from unit test.'.format(
            strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        self.chrome_os_devices_api.update(self.SKYKIT_COM_CUSTOMER_ID,
                                          self.TESTING_DEVICE_ID,
                                          annotated_location=new_location)
        sleep(1)
        device = self.chrome_os_devices_api.get(self.SKYKIT_COM_CUSTOMER_ID, self.TESTING_DEVICE_ID)
        self.assertEqual(new_location, device.get('annotatedLocation'))

    def test_update_annotated_user(self):
        new_user = 'administrator-{0}@skykit.com'.format(strftime("%m-%d-%Y-%H-%M-%S", gmtime()))
        self.chrome_os_devices_api.update(self.SKYKIT_COM_CUSTOMER_ID,
                                          self.TESTING_DEVICE_ID,
                                          annotated_user=new_user)
        sleep(1)
        device = self.chrome_os_devices_api.get(self.SKYKIT_COM_CUSTOMER_ID, self.TESTING_DEVICE_ID)
        self.assertEqual(new_user, device.get('annotatedUser'))

    def test_update_annotated_asset_id(self):
        device_key_urlsafe = self.device_key.urlsafe()
        self.chrome_os_devices_api.update(self.SKYKIT_COM_CUSTOMER_ID,
                                          self.TESTING_DEVICE_ID,
                                          annotated_asset_id=device_key_urlsafe)
        sleep(1)
        device = self.chrome_os_devices_api.get(self.SKYKIT_COM_CUSTOMER_ID, self.TESTING_DEVICE_ID)
        self.assertEqual(device_key_urlsafe, device.get('annotatedAssetId'))

    def _find_by_device_id_and_org_unit(self, device_id, org_unit):
        device = self.chrome_os_devices_api.get(self.SKYKIT_COM_CUSTOMER_ID, device_id)
        if device.get('orgUnitPath') == org_unit:
            return device
        else:
            return None

    def _find_by_device_id(self, device_id, org_unit):
        device = self.chrome_os_devices_api.get(self.SKYKIT_COM_CUSTOMER_ID, device_id)
        if device.get('orgUnitPath') == org_unit:
            return device
        else:
            return None
