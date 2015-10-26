from env_setup import setup_test_paths

setup_test_paths()

import json
from restler.serializers import to_json
from strategy import DEVICE_STRATEGY
from agar.test import BaseTest
from models import Device, Tenant, Domain, Distributor

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class DeviceModel(BaseTest):
    TESTING_DEVICE_ID = '132e235a-b346-5b77-a345-de49fa753a2a'
    TEST_GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
    NAME = 'foobar tenant'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://skykit-contentmanager-int.appspot.com/content'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
    CHROME_DEVICE_DOMAIN = 'bar.com'
    CONTENT_SERVER_API_KEY = 'API KEY'
    TENANT_CODE = 'foobar'
    MAC_ADDRESS = '54271e619346'
    SERIAL_NUMBER = 'E3MSCX004781'
    MODEL = 'ASUS Chromebox'
    DISTRIBUTOR_NAME = 'agosto'
    CURRENT_CLASS_VERSION = 1
    IMPERSONATION_EMAIL = 'test@test.com'
    DISPLAY_PANEL_MODEL = 'Sharp-PNE521'
    DISPLAY_PANEL_INPUT = 'sha6'

    def setUp(self):
        super(DeviceModel, self).setUp()
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
                                              active=True)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.distributor_key,
                                    impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                    active=True)
        self.domain_key = self.domain.put()
        self.tenant = Tenant.create(name=self.NAME,
                                    tenant_code=self.TENANT_CODE,
                                    admin_email=self.ADMIN_EMAIL,
                                    content_server_url=self.CONTENT_SERVER_URL,
                                    content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                    domain_key=self.domain_key,
                                    active=True)
        self.tenant_key = self.tenant.put()

    ##################################################################################################################
    ## get_by_device_id (unmanaged devices only)
    ##################################################################################################################

    def test_get_by_device_id(self):
        device = Device.create_managed(tenant_key=self.tenant_key,
                                                 device_id=self.TESTING_DEVICE_ID,
                                                 gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                                 mac_address=self.MAC_ADDRESS)
        expected_key = device.put()
        actual = Device.get_by_device_id(self.TESTING_DEVICE_ID)
        self.assertEqual(actual.key, expected_key)

    def test_get_by_device_id_none_returned_when_device_id_invalid(self):
        actual = Device.get_by_device_id(self.TESTING_DEVICE_ID)
        self.assertIsNone(actual)

    ##################################################################################################################
    ## create_unmanaged
    ##################################################################################################################

    def test_create_unmanaged_device(self):
        device = Device.create_unmanaged(
            gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
            mac_address=self.MAC_ADDRESS)
        self.assertIsNotNone(device)
        self.assertIsNotNone(device.api_key)
        self.assertIsNotNone(device.pairing_code)
        self.assertFalse(device.is_managed_device)

    ##################################################################################################################
    ## create_managed
    ##################################################################################################################
    def test_create_managed_device(self):
        device = Device.create_managed(tenant_key=self.tenant_key,
                                       device_id=self.TESTING_DEVICE_ID,
                                       gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                       mac_address=self.MAC_ADDRESS)
        self.assertIsNotNone(device)
        self.assertIsNotNone(device.api_key)
        self.assertIsNone(device.pairing_code)
        self.assertTrue(device.is_managed_device)

    def test_json_serialization_strategy(self):
        device = Device.create_managed(tenant_key=self.tenant_key,
                                       device_id=self.TESTING_DEVICE_ID,
                                       gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                       mac_address=self.MAC_ADDRESS)
        device.panel_model = self.DISPLAY_PANEL_MODEL
        device.panel_input = self.DISPLAY_PANEL_INPUT
        device.put()
        json_representation = json.loads(to_json(device, DEVICE_STRATEGY))
        self.assertEqual(str(device.device_id), json_representation['deviceId'])
        self.assertEqual(str(device.gcm_registration_id), json_representation['gcmRegistrationId'])
        self.assertEqual(None, json_representation['serialNumber'])
        self.assertIsNotNone(json_representation['created'])
        self.assertIsNotNone(json_representation['updated'])
        self.assertEqual(str(device.api_key), json_representation['apiKey'])
        self.assertEqual(str(self.tenant.name), json_representation['tenantName'])
        self.assertEqual(str(self.tenant.content_server_url), json_representation['contentServerUrl'])
        self.assertEqual(str(device.mac_address), json_representation['macAddress'])
        self.assertEqual(str(device.panel_input), json_representation['panelInput'])
        self.assertEqual(str(device.panel_model), json_representation['panelModel'])
        self.assertEqual(device.is_managed_device, json_representation['isManagedDevice'])
        self.assertEqual(str(device.loggly_link),
                         'https://skykit.loggly.com/search?&terms=tag%3A"{0}"'.format(None))

    def test_json_serialization_strategy_with_optional_serial_number(self):
        device = Device.create_managed(tenant_key=self.tenant_key,
                                       device_id=self.TESTING_DEVICE_ID,
                                       gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                       mac_address=self.MAC_ADDRESS,
                                       serial_number=self.SERIAL_NUMBER,
                                       model=self.MODEL)
        device.put()
        json_representation = json.loads(to_json(device, DEVICE_STRATEGY))
        self.assertEqual(self.SERIAL_NUMBER, json_representation['serialNumber'])
        self.assertEqual(str(device.name), '{0} {1}'.format(self.SERIAL_NUMBER, self.MODEL))
        self.assertEqual(str(device.loggly_link),
                         'https://skykit.loggly.com/search?&terms=tag%3A"{0}"'.format(self.SERIAL_NUMBER))

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        device = Device.create_managed(tenant_key=self.tenant_key,
                                       device_id=self.TESTING_DEVICE_ID,
                                       gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
                                       mac_address=self.MAC_ADDRESS,
                                       serial_number=self.SERIAL_NUMBER)
        device.class_version = 47
        device.put()
        self.assertEqual(device.class_version, self.CURRENT_CLASS_VERSION)

        # def test_get_tenant_returns_tenant_representation(self):
        #     managed_device = ChromeOsDevice.create(tenant_key=self.tenant_key,
        #                                              device_id=self.TESTING_DEVICE_ID,
        #                                              gcm_registration_id=self.TEST_GCM_REGISTRATION_ID,
        #                                              mac_address=self.MAC_ADDRESS)
        #     managed_device.put()
        #     tenant = managed_device.get_tenant()
        #     self.assertEqual(tenant, self.tenant)
