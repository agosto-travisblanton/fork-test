from uuid import uuid4

from google.appengine.ext.deferred import deferred

from env_setup import setup_test_paths
from mock import patch, Mock, ANY
from model_entities.integration_events_log_model import IntegrationEventLog
from workflow.register_device import register_device

setup_test_paths()

from models import Tenant, ChromeOsDevice, Distributor, Domain
from agar.test import BaseTest


class TestRegisterDevice(BaseTest):
    SKYKIT_COM_CUSTOMER_ID = 'C04c2u0lg'
    ADMIN_ACCOUNT_TO_IMPERSONATE = 'administrator@skykit.com'
    TESTING_DEVICE_ID = '6daf712b-7a65-4450-abcd-45027a47a716'
    ORG_UNIT_DEPLOYED = '/SKD Automated Test/SKD Automated Deployed'
    ORG_UNIT_DISTRIBUTOR = '/SKD Automated Test/SKD Automated Distributor'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    DISTRIBUTOR_NAME = 'agosto'
    IMPERSONATION_EMAIL = 'administrator@skykit.com'

    def setUp(self):
        super(TestRegisterDevice, self).setUp()
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

    @patch('workflow.register_device.ContentManagerApi')
    @patch('workflow.register_device.ChromeOsDevicesApi')
    def test_register_device_creates_integration_event_log_entities(self,
                                                                    chrome_os_devices_api_class_mock,
                                                                    content_manager_api_class_mock):
        self._build_cursor_list_mock(chrome_os_devices_api_class_mock)
        self._build_create_device_mock(content_manager_api_class_mock)
        register_device(self.device_key.urlsafe(),
                        device_mac_address=self.mac_address,
                        gcm_registration_id=self.expected_gcm_registration_id,
                        correlation_id=self.expected_correlation_id)
        integration_event_logs = IntegrationEventLog.query(
            IntegrationEventLog.correlation_identifier == self.expected_correlation_id).fetch(25)
        self.assertEqual(2, len(integration_event_logs))

    @patch('workflow.register_device.ContentManagerApi')
    @patch('workflow.register_device.ChromeOsDevicesApi')
    def test_register_device_fails_device_key_urlsafe_is_none(self,
                                                              chrome_os_devices_api_class_mock,
                                                              content_manager_api_class_mock):
        with self.assertRaises(deferred.PermanentTaskFailure):
            register_device(None,
                            device_mac_address=self.mac_address,
                            gcm_registration_id=self.expected_gcm_registration_id,
                            correlation_id=self.expected_correlation_id)

    @patch('workflow.register_device.ContentManagerApi')
    @patch('workflow.register_device.ChromeOsDevicesApi')
    def test_register_device_fails_device_mac_address_is_none(self,
                                                              chrome_os_devices_api_class_mock,
                                                              content_manager_api_class_mock):
        with self.assertRaises(deferred.PermanentTaskFailure):
            register_device(self.device_key.urlsafe(),
                            device_mac_address=None,
                            gcm_registration_id=self.expected_gcm_registration_id,
                            correlation_id=self.expected_correlation_id)

    @patch('workflow.register_device.ContentManagerApi')
    @patch('workflow.register_device.ChromeOsDevicesApi')
    def test_register_device_invokes_cursor_list(self,
                                                 chrome_os_devices_api_class_mock,
                                                 content_manager_api_class_mock):
        chrome_os_devices_api_instance_mock = self._build_cursor_list_mock(chrome_os_devices_api_class_mock)
        self._build_create_device_mock(content_manager_api_class_mock)
        register_device(self.device_key.urlsafe(),
                        device_mac_address=self.mac_address,
                        gcm_registration_id=self.expected_gcm_registration_id,
                        correlation_id=self.expected_correlation_id)
        chrome_os_devices_api_instance_mock.cursor_list.assert_called_with(next_page_token=None,
                                                                           customer_id=ANY)

    @patch('workflow.register_device.ContentManagerApi')
    @patch('workflow.register_device.ChromeOsDevicesApi')
    def test_register_copy_values_from_chrome_os_device(self,
                                                        chrome_os_devices_api_class_mock,
                                                        content_manager_api_class_mock):
        matching_chrome_os_device_dict = self._build_chrome_os_device_resource_representation()
        self._build_cursor_list_mock(chrome_os_devices_api_class_mock, [matching_chrome_os_device_dict])
        self._build_create_device_mock(content_manager_api_class_mock)
        register_device(self.device_key.urlsafe(),
                        device_mac_address=self.mac_address,
                        gcm_registration_id=self.expected_gcm_registration_id,
                        correlation_id=self.expected_correlation_id)
        actual = self.device_key.get()
        self.assertEqual(actual.device_id, str(matching_chrome_os_device_dict.get('deviceId')))
        self.assertEqual(actual.mac_address, str(matching_chrome_os_device_dict.get('macAddress')))
        self.assertEqual(actual.serial_number, str(matching_chrome_os_device_dict.get('serialNumber')))
        self.assertEqual(actual.status, str(matching_chrome_os_device_dict.get('status')))
        self.assertEqual(actual.last_sync, str(matching_chrome_os_device_dict.get('lastSync')))
        self.assertEqual(actual.kind, str(matching_chrome_os_device_dict.get('kind')))
        self.assertEqual(actual.ethernet_mac_address, str(matching_chrome_os_device_dict.get('ethernetMacAddress')))
        self.assertEqual(actual.org_unit_path, str(matching_chrome_os_device_dict.get('orgUnitPath')))
        self.assertEqual(actual.annotated_user, str(matching_chrome_os_device_dict.get('annotatedUser')))
        self.assertEqual(actual.annotated_location, str(matching_chrome_os_device_dict.get('annotatedLocation')))
        self.assertEqual(actual.notes, str(matching_chrome_os_device_dict.get('notes')))
        self.assertEqual(actual.boot_mode, str(matching_chrome_os_device_dict.get('bootMode')))
        self.assertEqual(actual.last_enrollment_time, str(matching_chrome_os_device_dict.get('lastEnrollmentTime')))
        self.assertEqual(actual.platform_version, str(matching_chrome_os_device_dict.get('platformVersion')))
        self.assertEqual(actual.model, str(matching_chrome_os_device_dict.get('model')))
        self.assertEqual(actual.os_version, str(matching_chrome_os_device_dict.get('osVersion')))
        self.assertEqual(actual.firmware_version, str(matching_chrome_os_device_dict.get('firmwareVersion')))
        self.assertEqual(actual.etag, str(matching_chrome_os_device_dict.get('etag')))
        self.assertEqual(actual.customer_display_name, str(matching_chrome_os_device_dict.get('annotatedAssetId')))

    @patch('workflow.register_device.ContentManagerApi')
    @patch('workflow.register_device.ChromeOsDevicesApi')
    def test_register_device_sets_device_key_to_entity_annotated_asset_id(self,
                                                                          chrome_os_devices_api_class_mock,
                                                                          content_manager_api_class_mock):
        matching_chrome_os_device_dict = self._build_chrome_os_device_resource_representation()
        self._build_cursor_list_mock(chrome_os_devices_api_class_mock, [matching_chrome_os_device_dict])
        self._build_create_device_mock(content_manager_api_class_mock)
        register_device(self.device_key.urlsafe(),
                        device_mac_address=self.mac_address,
                        gcm_registration_id=self.expected_gcm_registration_id,
                        correlation_id=self.expected_correlation_id)
        actual = self.device_key.get()
        self.assertEqual(actual.annotated_asset_id, self.device_key.urlsafe())

    @patch('workflow.register_device.ContentManagerApi')
    @patch('workflow.register_device.ChromeOsDevicesApi')
    def test_register_device_sets_api_response_event_attributes(self,
                                                                chrome_os_devices_api_class_mock,
                                                                content_manager_api_class_mock):
        matching_chrome_os_device_dict = self._build_chrome_os_device_resource_representation()
        self._build_cursor_list_mock(chrome_os_devices_api_class_mock, [matching_chrome_os_device_dict])
        self._build_create_device_mock(content_manager_api_class_mock)
        register_device(self.device_key.urlsafe(),
                        device_mac_address=self.mac_address,
                        gcm_registration_id=self.expected_gcm_registration_id,
                        correlation_id=self.expected_correlation_id)
        actual = IntegrationEventLog.query(
            IntegrationEventLog.correlation_identifier == self.expected_correlation_id,
            IntegrationEventLog.serial_number == matching_chrome_os_device_dict.get('serialNumber')).fetch(1)
        self.assertIsNotNone(actual)
        self.assertIsNotNone(actual[0])
        self.assertEqual('Chrome Directory API call success! Notifying Content Manager.', actual[0].details)

    @patch('workflow.register_device.ContentManagerApi')
    @patch('workflow.register_device.ChromeOsDevicesApi')
    def test_register_device_creates_update_directory_api_integration_event_log(self,
                                                                                chrome_os_devices_api_class_mock,
                                                                                content_manager_api_class_mock):
        matching_chrome_os_device_dict = self._build_chrome_os_device_resource_representation()
        self._build_cursor_list_mock(chrome_os_devices_api_class_mock, [matching_chrome_os_device_dict])
        self._build_create_device_mock(content_manager_api_class_mock)
        register_device(self.device_key.urlsafe(),
                        device_mac_address=self.mac_address,
                        gcm_registration_id=self.expected_gcm_registration_id,
                        correlation_id=self.expected_correlation_id)
        actual = IntegrationEventLog.query(
            IntegrationEventLog.correlation_identifier == self.expected_correlation_id,
            IntegrationEventLog.workflow_step == 'Update Directory API with device key in annotatedAssetId field.').fetch(
            1)
        self.assertIsNotNone(actual)
        self.assertEqual(1, len(actual))

    @patch('workflow.register_device.ContentManagerApi')
    @patch('workflow.register_device.ChromeOsDevicesApi')
    def test_register_device_invokes_create_device(self,
                                                   chrome_os_devices_api_class_mock,
                                                   content_manager_api_class_mock):
        self._build_cursor_list_mock(chrome_os_devices_api_class_mock)
        content_manager_api_instance_mock = self._build_create_device_mock(content_manager_api_class_mock)
        register_device(self.device_key.urlsafe(),
                        device_mac_address=self.mac_address,
                        gcm_registration_id=self.expected_gcm_registration_id,
                        correlation_id=self.expected_correlation_id)
        content_manager_api_instance_mock.create_device.assert_called()

    ################################################################################################################
    ## Private helper methods
    ################################################################################################################
    def _build_cursor_list_mock(self, chrome_os_devices_api_class_mock, chrome_os_devices_list=None):
        if chrome_os_devices_list is None:
            chrome_os_devices_list = []
        chrome_os_devices_api_instance_mock = Mock()
        chrome_os_devices_api_class_mock.return_value = chrome_os_devices_api_instance_mock
        chrome_os_devices_api_instance_mock.cursor_list.return_value = chrome_os_devices_list, None
        return chrome_os_devices_api_instance_mock

    def _build_create_device_mock(self, content_manager_api_class_mock, expected_result=True):
        content_manager_api_instance_mock = Mock()
        content_manager_api_class_mock.return_value = content_manager_api_instance_mock
        content_manager_api_instance_mock.create_device.return_value = expected_result
        return content_manager_api_instance_mock

    def _build_chrome_os_device_resource_representation(self):
        return {
            'macAddress': self.mac_address,
            'serialNumber': 'df78a6d78fasd97asdgd7f6s98d76s9df',
            'status': 'ACTIVE',
            'lastSync': '20160101T00:00:00.000',
            'kind': 'ChromeBit',
            'ethernetMacAddress': 'test-ethernetMacAddress',
            'orgUnitPath': 'testing-org-unit-path',
            'annotatedUser': 'Joe Smith',
            'annotatedLocation': 'A location',
            'notes': 'Just some notes',
            'bootMode': 'NETWORK',
            'lastEnrollmentTime': '78879898879980909877545644',
            'platformVersion': '23.4.67',
            'model': 'Jaguar 7888',
            'osVersion': 'Linux kernel 3.6.11',
            'firmwareVersion': '67.9888',
            'etag': 'd8f7s8d7f0a8s97df89fas7d098f7asd089f7asd89f7as89d7f0a9s87d8f9s',
            'annotatedAssetId': 'My company display name',
            'deviceId': 'd7f9s8d79879'
        }
