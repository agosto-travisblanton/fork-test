from env_setup import setup_test_paths

setup_test_paths()

from uuid import uuid4

from mock import patch, Mock
from workflow.update_chrome_os_device import update_chrome_os_device
from app_config import config

from models import Tenant, ChromeOsDevice, Distributor, Domain
from agar.test import BaseTest


class TestUpdateChromeOsDevice(BaseTest):
    SKYKIT_COM_CUSTOMER_ID = 'C04c2u0lg'
    ADMIN_ACCOUNT_TO_IMPERSONATE = 'administrator@skykit.com'
    TESTING_DEVICE_ID = '6daf712b-7a65-4450-abcd-45027a47a716'
    ORG_UNIT_DEPLOYED = '/SKD Automated Test/SKD Automated Deployed'
    ORG_UNIT_DISTRIBUTOR = '/SKD Automated Test/SKD Automated Distributor'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    DISTRIBUTOR_NAME = 'agosto'
    IMPERSONATION_EMAIL = 'administrator@skykit.com'

    def setUp(self):
        super(TestUpdateChromeOsDevice, self).setUp()
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
        self.expected_gcm_registration_id = '8d70a8d78a6dfa6df76dfasd'
        self.expected_correlation_id = str(uuid4())
        self.device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                                    gcm_registration_id=self.expected_gcm_registration_id,
                                                    mac_address=self.mac_address,
                                                    device_id='a8sd7f8df9sd7')
        self.device_key = self.device.put()
        self.device.annotated_user = 'Joe Smoe'
        self.device.annotated_location = 'Accounting'
        self.device.notes = 'Some notes about this device.'
        self.device.org_unit_path = '/AgostoDev/Accounting'
        self.device.annotated_asset_id = self.device_key.urlsafe()
        self.device.put()

    @patch('workflow.update_chrome_os_device.ChromeOsDevicesApi')
    def test_register_device_invokes_chrome_os_devices_api_update(self, chrome_os_devices_api_class_mock):
        chrome_os_devices_api_instance_mock = self._build_update_mock(chrome_os_devices_api_class_mock)
        update_chrome_os_device(self.device_key.urlsafe())
        chrome_os_devices_api_instance_mock.update.assert_called_with(config.GOOGLE_CUSTOMER_ID,
                                                                      self.device.device_id,
                                                                      annotated_user=self.device.annotated_user,
                                                                      annotated_location=self.device.annotated_location,
                                                                      notes=self.device.notes,
                                                                      org_unit_path=self.device.org_unit_path,
                                                                      annotated_asset_id=self.device.annotated_asset_id)

    ################################################################################################################
    ## Private helper methods
    ################################################################################################################
    def _build_update_mock(self, chrome_os_devices_api_class_mock):
        chrome_os_devices_api_instance_mock = Mock()
        chrome_os_devices_api_class_mock.return_value = chrome_os_devices_api_instance_mock
        chrome_os_devices_api_instance_mock.update.return_value = None
        return chrome_os_devices_api_instance_mock
