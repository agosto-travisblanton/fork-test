import httplib

from env_setup import setup_test_paths
from model_entities.chrome_os_device_model_and_overlays import Tenant, ChromeOsDevice
from model_entities.distributor_and_user_model import Distributor
from model_entities.domain_model import Domain
from tests.provisioning_distributor_user_base_test import ProvisioningDistributorUserBase
from utils.device_util import resolve_device

setup_test_paths()

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestDeviceUtil(ProvisioningDistributorUserBase):
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    DISTRIBUTOR_NAME = 'agosto'
    GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
    TENANT_NAME = 'foobar'

    def setUp(self):
        super(TestDeviceUtil, self).setUp()
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
                                              active=True)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.distributor_key,
                                    impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                    active=True)
        self.domain_key = self.domain.put()
        self.tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                                    name=self.TENANT_NAME,
                                    admin_email=self.ADMIN_EMAIL,
                                    content_server_url=self.CONTENT_SERVER_URL,
                                    content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                    domain_key=self.domain_key,
                                    active=True)
        self.tenant_key = self.tenant.put()
        self.chrome_os_device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                                              gcm_registration_id=self.GCM_REGISTRATION_ID,
                                                              mac_address=self.MAC_ADDRESS)

        self.chrome_os_device_key = self.chrome_os_device.put()

    ##################################################################################################################
    # resolve_device
    ##################################################################################################################

    def test_resolve_device_with_valid_device_key_returns_ok(self):
        status, message, device = resolve_device(self.chrome_os_device_key.urlsafe())
        self.assertEqual(status, httplib.OK)
        self.assertEqual(message, 'OK')
        self.assertEqual(device, self.chrome_os_device)

    def test_resolve_device_with_environmentally_invalid_device_key_returns_bad_request(self):
        environmentally_invalid_key = 'ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyGwsSDkNocm9tZU9zRGV2aWNlGICAgIDepYUKDA'
        status, message, device = resolve_device(environmentally_invalid_key)
        self.assertEqual(status, httplib.BAD_REQUEST)
        self.assertIsNone(device)

    def test_resolve_device_with_invalid_device_key_string_returns_bad_request(self):
        invalid_key = 'invalid key'
        status, message, device = resolve_device(invalid_key)
        expected_message = 'Invalid input (Type Error). Incorrect padding in urlsafe key'
        self.assertEqual(status, httplib.BAD_REQUEST)
        self.assertEqual(message, expected_message)
        self.assertIsNone(device)
