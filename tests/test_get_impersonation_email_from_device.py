from env_setup import setup_test_paths
from workflow.get_impersonation_email_from_device import get_impersonation_email_from_device

setup_test_paths()

from models import Tenant, ChromeOsDevice, Distributor, Domain
from agar.test import BaseTest
from integrations.directory_api.chrome_os_devices_api import ChromeOsDevicesApi


class TestGetImpersonationEmailFromDevice(BaseTest):
    SKYKIT_COM_CUSTOMER_ID = 'C04c2u0lg'
    ADMIN_ACCOUNT_TO_IMPERSONATE = 'administrator@skykit.com'
    TESTING_DEVICE_ID = '6daf712b-7a65-4450-abcd-45027a47a716'
    ORG_UNIT_DEPLOYED = '/SKD Automated Test/SKD Automated Deployed'
    ORG_UNIT_DISTRIBUTOR = '/SKD Automated Test/SKD Automated Distributor'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    DISTRIBUTOR_NAME = 'agosto'
    IMPERSONATION_EMAIL = 'administrator@skykit.com'

    def setUp(self):
        super(TestGetImpersonationEmailFromDevice, self).setUp()
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

    def test_get_impersonation_email_from_device(self):
        result = get_impersonation_email_from_device(self.device)
        self.assertEqual(result, self.IMPERSONATION_EMAIL)
