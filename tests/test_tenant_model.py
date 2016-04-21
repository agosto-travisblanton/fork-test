from app_config import config
from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
from models import Tenant, Distributor, TENANT_ENTITY_GROUP_NAME, Domain, ChromeOsDevice

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TestTenantModel(BaseTest):
    NAME = 'foobar tenant'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://www.content.com'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    TENANT_CODE = 'foobar'
    ENTITY_GROUP_NAME = 'tenantEntityGroup'
    CURRENT_CLASS_VERSION = 1
    DISTRIBUTOR_NAME = 'Agosto'
    IMPERSONATION_EMAIL = 'test@test.com'

    def setUp(self):
        super(TestTenantModel, self).setUp()
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME, active=True)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.distributor_key,
                                    impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                    active=True)
        self.domain_key = self.domain.put()

        self.tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                                    name=self.NAME,
                                    admin_email=self.ADMIN_EMAIL,
                                    content_server_url=self.CONTENT_SERVER_URL,
                                    content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                    domain_key=self.domain_key,
                                    active=True)
        self.tenant_key = self.tenant.put()

        self.device_1 = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                              gcm_registration_id='APA91bHyMJRcN7mj7b0aXGWE7Ae',
                                              mac_address='54271ee81302')
        self.device_1_key = self.device_1.put()
        self.device_2 = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                              gcm_registration_id='c098d70a8d78a6dfa6df76dfas7',
                                              mac_address='48d2247f2132')
        self.device_2_key = self.device_2.put()
        self.device_to_be_archived = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                                                   gcm_registration_id='f090d7348d78b6cfa6df76dfa1b',
                                                                   mac_address='98d2247f2101')
        self.device_to_be_archived_key = self.device_to_be_archived.put()


    def test_create_sets_tenant_entity_group_as_parent(self):
        actual = Tenant.find_by_name(self.NAME)
        parent = actual.key.parent().get()
        self.assertEqual(parent.name, TENANT_ENTITY_GROUP_NAME)

    def test_find_by_name_returns_matching_tenant(self):
        actual = Tenant.find_by_name(self.NAME)
        self.assertEqual(actual.key, self.tenant_key)
        self.assertEqual(actual.name, self.NAME)

    def test_find_by_name_returns_none_when_no_matching_tenant_found(self):
        actual = Tenant.find_by_name('barfood tenant')
        self.assertIsNone(actual)

    def test_create_sets_an_inactive_tenant(self):
        name = 'Inactive Tenant'
        inactive_tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                                        name=name,
                                        admin_email=self.ADMIN_EMAIL,
                                        content_server_url=self.CONTENT_SERVER_URL,
                                        content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                        domain_key=self.domain_key,
                                        active=False)
        inactive_tenant.put()
        tenant_created = Tenant.find_by_name(name)
        self.assertEqual(tenant_created.name, name)
        self.assertFalse(tenant_created.active)

    def test_create_sets_proof_of_play_logging_to_false(self):
        tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                               name=self.NAME,
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                               domain_key=self.domain_key,
                               active=False)
        tenant.put()
        tenant_created = Tenant.find_by_name(self.NAME)
        self.assertFalse(tenant_created.proof_of_play_logging)

    def test_create_initialized_tenant_properties(self):
        tenant_created = Tenant.find_by_name(self.NAME)
        self.assertTrue(tenant_created.active)
        self.assertEqual(self.TENANT_CODE, tenant_created.tenant_code)
        self.assertEqual(self.ADMIN_EMAIL, tenant_created.admin_email)
        self.assertEqual(self.CONTENT_SERVER_URL, tenant_created.content_server_url)
        self.assertEqual(self.CONTENT_MANAGER_BASE_URL, tenant_created.content_manager_base_url)
        self.assertEqual(self.NAME, tenant_created.name)
        self.assertEqual(self.domain_key, tenant_created.domain_key)
        self.assertEqual(tenant_created.default_timezone, 'America/Chicago')
        self.assertLength(0, tenant_created.notification_emails)

    def test_create_gives_default_proof_of_play_url(self):
        tenant_created = Tenant.find_by_name(self.NAME)
        self.assertEqual(tenant_created.proof_of_play_url, config.DEFAULT_PROOF_OF_PLAY_URL)

    def test_create_can_override_default_proof_of_play_url(self):
        proof_of_play_url = 'https://skykit-provisioning-FOOBAR.appspot.com/proofplay/api/v1/post_new_program_play'
        tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                               name='FOOBAR_TENANT',
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                               domain_key=self.domain_key,
                               active=True,
                               proof_of_play_url=proof_of_play_url)
        tenant.put()
        tenant_created = Tenant.find_by_name('FOOBAR_TENANT')
        self.assertNotEqual(tenant_created.proof_of_play_url, config.DEFAULT_PROOF_OF_PLAY_URL)
        self.assertEqual(tenant_created.proof_of_play_url, proof_of_play_url)

    def test_is_tenant_code_unique_returns_false_when_code_found(self):
        uniqueness_check = Tenant.is_tenant_code_unique(self.TENANT_CODE)
        self.assertFalse(uniqueness_check)

    def test_is_unique_returns_true_when_code_not_found(self):
        uniqueness_check = Tenant.is_tenant_code_unique('foobar_inc')
        self.assertTrue(uniqueness_check)

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        self.tenant.class_version = 47
        self.tenant.put()
        self.assertEqual(self.tenant.class_version, self.CURRENT_CLASS_VERSION)

    def test_find_by_tenant_code_returns_entity_instance(self):
        actual = Tenant.find_by_tenant_code(self.tenant.tenant_code)
        self.assertEqual(actual.key, self.tenant.key)

    def test_find_by_tenant_code_returns_none(self):
        actual = Tenant.find_by_tenant_code('kdjfashdfjkah')
        self.assertIsNone(actual)

    def test_find_devices_returns_expected_device_count_for_tenant_key(self):
        self.device_to_be_archived.archived = True
        self.device_to_be_archived.put()
        devices = Tenant.find_devices(self.tenant_key, unmanaged=False)
        self.assertLength(2, devices)

    def test_find_devices_returns_expected_unmanaged_device_count_for_tenant_key(self):
        devices = Tenant.find_devices(self.tenant_key, unmanaged=True)
        self.assertLength(0, devices)

    def test_get_impersonation_email_for_tenant_key(self):
        urlsafe_tenant_key = self.tenant_key.urlsafe()
        impersonation_email = Tenant.get_impersonation_email(urlsafe_tenant_key=urlsafe_tenant_key)
        self.assertEqual(impersonation_email, self.IMPERSONATION_EMAIL)

    def test_get_domain_returns_domain_representation(self):
        domain = self.tenant.get_domain()
        self.assertEqual(domain, self.domain)

    def test_toggle_proof_of_play_off(self):
        self.tenant.proof_of_play_logging = True
        self.tenant.put()
        self.assertTrue(self.tenant.proof_of_play_logging)
        devices = Tenant.find_devices(self.tenant_key, unmanaged=False)
        for device in devices:
            device.proof_of_play_logging = True
            device.proof_of_play_editable = True
            device.put()
        Tenant.toggle_proof_of_play(tenant_code=self.TENANT_CODE, enable=False)
        self.assertFalse(self.tenant.proof_of_play_logging)
        for device in devices:
            self.assertFalse(device.proof_of_play_logging)
            self.assertFalse(device.proof_of_play_editable)

    def test_toggle_proof_of_play_on(self):
        self.tenant.proof_of_play_logging = False
        self.tenant.put()
        self.assertFalse(self.tenant.proof_of_play_logging)
        devices = Tenant.find_devices(self.tenant_key, unmanaged=False)
        for device in devices:
            device.proof_of_play_logging = False
            device.proof_of_play_editable = False
            device.put()
        Tenant.toggle_proof_of_play(tenant_code=self.TENANT_CODE, enable=True)
        self.assertTrue(self.tenant.proof_of_play_logging)
        for device in devices:
            self.assertFalse(device.proof_of_play_logging)
            self.assertTrue(device.proof_of_play_editable)

    def test_match_device_with_full_mac(self):
        mac_address = '1231233434'
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               gcm_registration_id='BPA91bHyMJRcN7mj7b0aXGWE7Ae',
                                               mac_address=mac_address)
        device.put()
        is_match = Tenant.match_device_with_full_mac(
            tenant_keys=[self.tenant_key],
            unmanaged=False,
            full_mac=mac_address)
        self.assertTrue(is_match)

    def test_match_device_with_full_mac_archived(self):
        mac_address = '1231233434'
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               gcm_registration_id='BPA91bHyMJRcN7mj7b0aXGWE7Ae',
                                               mac_address=mac_address)
        device.archived = True
        device.put()
        is_match = Tenant.match_device_with_full_mac(
            tenant_keys=[self.tenant_key],
            unmanaged=False,
            full_mac=mac_address)
        self.assertFalse(is_match)

    def test_match_device_with_full_serial(self):
        serial_number = 'SN123-123-3434'
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               gcm_registration_id='BPA91bHyMJRcN7mj7b0aXGWE7Ae',
                                               mac_address='123123123')
        device.serial_number = serial_number
        device.put()
        is_match = Tenant.match_device_with_full_serial(
            tenant_keys=[self.tenant_key],
            unmanaged=False,
            full_serial=serial_number)
        self.assertTrue(is_match)

    def test_match_device_with_full_serial_archived(self):
        serial_number = 'SN123-123-3434'
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               gcm_registration_id='BPA91bHyMJRcN7mj7b0aXGWE7Ae',
                                               mac_address='123123123')
        device.serial_number = serial_number
        device.archived = True
        device.put()
        is_match = Tenant.match_device_with_full_serial(
            tenant_keys=[self.tenant_key],
            unmanaged=False,
            full_serial=serial_number)
        self.assertFalse(is_match)

    def test_find_devices_with_partial_serial(self):
        serial_number = 'SN445-123-3434'
        partial_serial = 'SN445'
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               gcm_registration_id='BPA91bHyMJRcN7mj7b0aXGWE7Ae',
                                               mac_address='123123123')
        device.serial_number = serial_number
        device.put()
        devices = Tenant.find_devices_with_partial_serial(
            tenant_keys=[self.tenant_key],
            unmanaged=False,
            partial_serial=partial_serial)
        self.assertLength(1, devices)

    def test_find_devices_with_partial_serial_archived(self):
        serial_number = 'SN445-123-3434'
        partial_serial = 'SN445'
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               gcm_registration_id='BPA91bHyMJRcN7mj7b0aXGWE7Ae',
                                               mac_address='123123123')
        device.serial_number = serial_number
        device.archived = True
        device.put()
        devices = Tenant.find_devices_with_partial_serial(
            tenant_keys=[self.tenant_key],
            unmanaged=False,
            partial_serial=partial_serial)
        self.assertLength(0, devices)

    def test_find_devices_with_partial_mac(self):
        mac_address = '80324771123'
        partial_mac = '8032'
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               gcm_registration_id='BPA91bHyMJRcN7mj7b0aXGWE7Ae',
                                               mac_address=mac_address)
        device.put()
        devices = Tenant.find_devices_with_partial_mac(
            tenant_keys=[self.tenant_key],
            unmanaged=False,
            partial_mac=partial_mac)
        self.assertLength(1, devices)

    def test_find_devices_with_partial_mac_archived(self):
        mac_address = '80324771123'
        partial_mac = '8032'
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               gcm_registration_id='BPA91bHyMJRcN7mj7b0aXGWE7Ae',
                                               mac_address=mac_address)
        device.archived = True
        device.put()
        devices = Tenant.find_devices_with_partial_mac(
            tenant_keys=[self.tenant_key],
            unmanaged=False,
            partial_mac=partial_mac)
        self.assertLength(0, devices)

    def test_find_devices_paginated(self):
        tenant = Tenant.create(tenant_code='foobar_inc',
                               name='Foobar, Inc.',
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                               domain_key=self.domain_key,
                               active=True)
        tenant_key = tenant.put()

        device_1 = ChromeOsDevice.create_managed(tenant_key,
                                                 gcm_registration_id='1PA91bHyMJRcN7mj7b0aXGWE7Ae', archived=False,
                                                 mac_address='1')
        device_1.put()
        device_2 = ChromeOsDevice.create_managed(tenant_key=tenant_key,
                                                 gcm_registration_id='2PA91bHyMJRcN7mj7b0aXGWE7Ae', archived=False,
                                                 mac_address='2')
        device_2.put()
        device_3 = ChromeOsDevice.create_managed(tenant_key=tenant_key,
                                                 gcm_registration_id='3PA91bHyMJRcN7mj7b0aXGWE7Ae', archived=True,
                                                 mac_address='3')
        device_3.put()
        devices = Tenant.find_devices_paginated(tenant_keys=[tenant_key])
        self.assertLength(2, devices["objects"])
