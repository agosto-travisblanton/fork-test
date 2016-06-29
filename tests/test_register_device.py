from uuid import uuid4

from google.appengine.ext.deferred import deferred

from env_setup import setup_test_paths
from mock import patch, Mock, ANY
from model_entities.integration_events_log_model import IntegrationEventLog
from workflow.register_device import register_device

setup_test_paths()

from models import Tenant, ChromeOsDevice, Distributor, Domain
from agar.test import BaseTest


class TestRegsiterDevice(BaseTest):
    SKYKIT_COM_CUSTOMER_ID = 'C04c2u0lg'
    ADMIN_ACCOUNT_TO_IMPERSONATE = 'administrator@skykit.com'
    TESTING_DEVICE_ID = '6daf712b-7a65-4450-abcd-45027a47a716'
    ORG_UNIT_DEPLOYED = '/SKD Automated Test/SKD Automated Deployed'
    ORG_UNIT_DISTRIBUTOR = '/SKD Automated Test/SKD Automated Distributor'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    DISTRIBUTOR_NAME = 'agosto'
    IMPERSONATION_EMAIL = 'administrator@skykit.com'

    def setUp(self):
        super(TestRegsiterDevice, self).setUp()
        # self.chrome_os_devices_api = ChromeOsDevicesApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)
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
                                                    mac_address=self.mac_address)
        self.device_key = self.device.put()

    @patch('workflow.register_device.ChromeOsDevicesApi')
    def test_register_device_creates_integration_event_log_entities(self, chrome_os_devices_api_class_mock):
        self._build_cursor_list_mock(chrome_os_devices_api_class_mock)
        register_device(self.device_key.urlsafe(),
                        device_mac_address=self.mac_address,
                        gcm_registration_id=self.expected_gcm_registration_id,
                        correlation_id=self.expected_correlation_id)
        integration_event_logs = IntegrationEventLog.query(
            IntegrationEventLog.correlation_identifier == self.expected_correlation_id).fetch(25)
        self.assertEqual(2, len(integration_event_logs))

    @patch('workflow.register_device.ChromeOsDevicesApi')
    def test_register_device_fails_device_key_urlsafe_is_none(self, chrome_os_devices_api_class_mock):
        with self.assertRaises(deferred.PermanentTaskFailure):
            register_device(None,
                            device_mac_address=self.mac_address,
                            gcm_registration_id=self.expected_gcm_registration_id,
                            correlation_id=self.expected_correlation_id)

    @patch('workflow.register_device.ChromeOsDevicesApi')
    def test_register_device_fails_device_mac_address_is_none(self, chrome_os_devices_api_class_mock):
        with self.assertRaises(deferred.PermanentTaskFailure):
            register_device(self.device_key.urlsafe(),
                            device_mac_address=None,
                            gcm_registration_id=self.expected_gcm_registration_id,
                            correlation_id=self.expected_correlation_id)

    @patch('workflow.register_device.ChromeOsDevicesApi')
    def test_register_device_invokes_(self, chrome_os_devices_api_class_mock):
        chrome_os_devices_api_instance_mock = self._build_cursor_list_mock(chrome_os_devices_api_class_mock)
        register_device(self.device_key.urlsafe(),
                        device_mac_address=self.mac_address,
                        gcm_registration_id=self.expected_gcm_registration_id,
                        correlation_id=self.expected_correlation_id)
        chrome_os_devices_api_instance_mock.cursor_list.assert_called_with(next_page_token=None,
                                                                           customer_id=ANY)

    ################################################################################################################
    ## Private helper methods
    ################################################################################################################
    def _build_cursor_list_mock(self, chrome_os_devices_api_class_mock):
        chrome_os_devices_api_instance_mock = Mock()
        chrome_os_devices_api_class_mock.return_value = chrome_os_devices_api_instance_mock
        chrome_os_devices_api_instance_mock.cursor_list.return_value = [], None
        return chrome_os_devices_api_instance_mock
