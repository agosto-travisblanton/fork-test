import random

from app_config import config
from env_setup import setup_test_paths

setup_test_paths()
import datetime

from agar.test import BaseTest
from models import Tenant, Distributor, TENANT_ENTITY_GROUP_NAME, Domain, ChromeOsDevice, DeviceIssueLog

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

    def test_generate_enrollment_password_has_acceptable_random_characters(self):
        enrollment_password = Tenant.generate_enrollment_password(config.ACCEPTABLE_ENROLLMENT_USER_PASSWORD_SIZE)
        self.assertTrue(len(enrollment_password), config.ACCEPTABLE_ENROLLMENT_USER_PASSWORD_SIZE)
        for p in enrollment_password:
            self.assertTrue(p in config.ACCEPTABLE_ENROLLMENT_USER_PASSWORD_CHARS)

    def test_generate_enrollment_password_length_too_small_throws_value_error(self):
        with self.assertRaises(ValueError) as context:
            Tenant.generate_enrollment_password(config.ACCEPTABLE_ENROLLMENT_USER_PASSWORD_SIZE - 1)
        error_message = 'enrollment_password must be greater than {0} in length'.format(
            config.ACCEPTABLE_ENROLLMENT_USER_PASSWORD_SIZE - 1)
        self.assertTrue(error_message in context.exception.message)

    def test_create_sets_tenant_entity_group_as_parent(self):
        actual = Tenant.find_by_name(self.NAME)
        parent = actual.key.parent().get()
        self.assertEqual(parent.name, TENANT_ENTITY_GROUP_NAME)

    def test_find_by_name_returns_matching_tenant(self):
        actual = Tenant.find_by_name(self.NAME)
        self.assertEqual(actual.key, self.tenant_key)
        self.assertEqual(actual.name, self.NAME)

    def test_find_by_partial_name_returns_list_of_matching_tenants(self):
        actual = Tenant.find_by_partial_name(self.NAME, self.distributor.key.urlsafe())
        self.assertEqual(actual[0].key, self.tenant_key)
        self.assertEqual(actual[0].name, self.NAME)

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
        self.assertEqual(tenant_created.default_timezone, config.DEFAULT_TIMEZONE)
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

    def test_create_sets_organization_unit_path(self):
        expected_organization_unit_path = '/skykit/{0}'.format(self.TENANT_CODE)
        self.assertEqual(expected_organization_unit_path, self.tenant.organization_unit_path)

    def test_create_sets_organization_unit_path_with_prefix(self):
        organization_unit_path = '/abc/123/skykit'
        domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                               distributor_key=self.distributor_key,
                               impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                               active=True,
                               organization_path=organization_unit_path)
        domain_key = domain.put()
        tenant_with_prefix_on_domain = Tenant.create(tenant_code=self.TENANT_CODE,
                                                     name=self.NAME,
                                                     admin_email=self.ADMIN_EMAIL,
                                                     content_server_url=self.CONTENT_SERVER_URL,
                                                     content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                                     domain_key=domain_key,
                                                     active=False)
        tenant_with_prefix_on_domain.put()
        expected_organization_unit_path = '{0}/skykit/{1}'.format(organization_unit_path, self.TENANT_CODE)
        self.assertEqual(expected_organization_unit_path, tenant_with_prefix_on_domain.organization_unit_path)

    def test_create_sets_enrollment_password(self):
        self.assertIsNotNone(self.tenant.enrollment_password)

    def test_create_sets_expected_enrollment_email_format(self):
        expected_enrollment_email_format = '{0}.enrollment@{1}'.format(self.TENANT_CODE, self.domain_key.get().name)
        self.assertEqual(expected_enrollment_email_format, self.tenant.enrollment_email)

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

    def test_find_by_tenant_code_returns_none_for_active_false(self):
        actual = Tenant.find_by_tenant_code(self.TENANT_CODE)
        self.assertIsNotNone(actual)
        self.tenant.active = False
        self.tenant.put()
        actual = Tenant.find_by_tenant_code(self.TENANT_CODE)
        self.assertIsNone(actual)
        self.tenant.active = True
        self.tenant.put()

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


    ###############################################################
    # find devices by distributor
    ###############################################################
    def test_find_devices_with_partial_serial_of_distributor(self):
        serial_number = 'SN445-123-3434'
        partial_serial = 'SN445'
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               gcm_registration_id='BPA91bHyMJRcN7mj7b0aXGWE7Ae',
                                               mac_address='123123123')
        device.serial_number = serial_number
        device.put()
        devices = Tenant.find_devices_with_partial_serial_of_distributor(
            distributor_urlsafe_key=self.distributor.key.urlsafe(),
            unmanaged=False,
            partial_serial=partial_serial)
        self.assertLength(1, devices)

    def test_find_devices_with_partial_serial_archived_of_distributor(self):
        serial_number = 'SN445-123-3434'
        partial_serial = 'SN445'
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               gcm_registration_id='BPA91bHyMJRcN7mj7b0aXGWE7Ae',
                                               mac_address='123123123')
        device.serial_number = serial_number
        device.archived = True
        device.put()
        devices = Tenant.find_devices_with_partial_serial_of_distributor(
            distributor_urlsafe_key=self.distributor.key.urlsafe(),
            unmanaged=False,
            partial_serial=partial_serial)
        self.assertLength(0, devices)

    def test_find_devices_with_partial_mac_of_distributor(self):
        mac_address = '80324771123'
        partial_mac = '8032'
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               gcm_registration_id='BPA91bHyMJRcN7mj7b0aXGWE7Ae',
                                               mac_address=mac_address)
        device.put()
        devices = Tenant.find_devices_with_partial_mac_of_distributor(
            distributor_urlsafe_key=self.distributor.key.urlsafe(),
            unmanaged=False,
            partial_mac=partial_mac)
        self.assertLength(1, devices)

    def test_find_devices_with_partial_mac_archived_of_distributor(self):
        mac_address = '80324771123'
        partial_mac = '8032'
        device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                               gcm_registration_id='BPA91bHyMJRcN7mj7b0aXGWE7Ae',
                                               mac_address=mac_address)
        device.archived = True
        device.put()
        devices = Tenant.find_devices_with_partial_mac_of_distributor(
            distributor_urlsafe_key=self.distributor.key.urlsafe(),
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

        device_1 = ChromeOsDevice.create_managed(tenant_key=tenant_key,
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

    def test_find_issues_paginated(self):
        tenant = Tenant.create(tenant_code='foobar_inc',
                               name='Foobar, Inc.',
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                               domain_key=self.domain_key,
                               active=True)
        tenant_key = tenant.put()

        device_1 = ChromeOsDevice.create_managed(tenant_key=tenant_key,
                                                 gcm_registration_id='1PA91bHyMJRcN7mj7b0aXGWE7Ae', archived=False,
                                                 mac_address='1')
        device_1.put()
        start = datetime.datetime.utcnow()
        for i in range(1, 300):
            issue = DeviceIssueLog.create(device_key=device_1.key,
                                          category=config.DEVICE_ISSUE_PLAYER_DOWN,
                                          up=False,
                                          storage_utilization=random.randint(1, 100),
                                          memory_utilization=random.randint(1, 100),
                                          program=str(random.randint(1, 100)),
                                          program_id=device_1.program_id,
                                          last_error=device_1.last_error,
                                          )

            issue.put()
        end = datetime.datetime.utcnow()

        devices = Tenant.find_issues_paginated(start, end, device_1, prev_cursor_str=None,
                                               next_cursor_str=None)
        self.assertLength(25, devices["objects"])
        self.assertTrue(devices["next_cursor"])
        self.assertFalse(devices["prev_cursor"])

        next_devices = Tenant.find_issues_paginated(start, end, device_1, prev_cursor_str=None,
                                                    next_cursor_str=devices["next_cursor"])

        self.assertLength(25, next_devices["objects"])
        self.assertTrue(next_devices["next_cursor"])
        self.assertTrue(next_devices["prev_cursor"])

    ##################################################################################################################
    # toggle_proof_of_play_on_tenant_devices
    ##################################################################################################################

    def test_toggle_proof_of_play_on_tenant_devices_with_key_toggle_off(self):
        self.tenant.proof_of_play_logging = True
        self.tenant.put()
        self.assertTrue(self.tenant.proof_of_play_logging)
        devices = Tenant.find_devices(self.tenant_key, unmanaged=False)
        for device in devices:
            device.proof_of_play_logging = True
            device.proof_of_play_editable = True
            device.put()
        Tenant.toggle_proof_of_play_on_tenant_devices(
            should_be_enabled=False,
            tenant_code=self.TENANT_CODE,
            tenant_key=self.tenant_key)
        self.assertFalse(self.tenant.proof_of_play_logging)
        for device in devices:
            self.assertFalse(device.proof_of_play_logging)
            self.assertFalse(device.proof_of_play_editable)

    def test_toggle_proof_of_play_on_tenant_devices_without_key_toggle_off(self):
        self.tenant.proof_of_play_logging = True
        self.tenant.put()
        self.assertTrue(self.tenant.proof_of_play_logging)
        devices = Tenant.find_devices(self.tenant_key, unmanaged=False)
        for device in devices:
            device.proof_of_play_logging = True
            device.proof_of_play_editable = True
            device.put()
        Tenant.toggle_proof_of_play_on_tenant_devices(
            should_be_enabled=False,
            tenant_code=self.TENANT_CODE)
        self.assertFalse(self.tenant.proof_of_play_logging)
        for device in devices:
            self.assertFalse(device.proof_of_play_logging)
            self.assertFalse(device.proof_of_play_editable)

    def test_toggle_proof_of_play_on_tenant_devices_with_key_toggle_on(self):
        self.tenant.proof_of_play_logging = False
        self.tenant.put()
        self.assertFalse(self.tenant.proof_of_play_logging)
        devices = Tenant.find_devices(self.tenant_key, unmanaged=False)
        for device in devices:
            device.proof_of_play_logging = False
            device.proof_of_play_editable = False
            device.put()
        Tenant.toggle_proof_of_play_on_tenant_devices(
            should_be_enabled=True,
            tenant_code=self.TENANT_CODE,
            tenant_key=self.tenant_key)
        self.assertTrue(self.tenant.proof_of_play_logging)
        for device in devices:
            self.assertFalse(device.proof_of_play_logging)
            self.assertTrue(device.proof_of_play_editable)

    def test_toggle_proof_of_play_on_tenant_devices_without_key_toggle_on(self):
        self.tenant.proof_of_play_logging = False
        self.tenant.put()
        self.assertFalse(self.tenant.proof_of_play_logging)
        devices = Tenant.find_devices(self.tenant_key, unmanaged=False)
        for device in devices:
            device.proof_of_play_logging = False
            device.proof_of_play_editable = False
            device.put()
        Tenant.toggle_proof_of_play_on_tenant_devices(
            should_be_enabled=True,
            tenant_code=self.TENANT_CODE)
        self.assertTrue(self.tenant.proof_of_play_logging)
        for device in devices:
            self.assertFalse(device.proof_of_play_logging)
            self.assertTrue(device.proof_of_play_editable)

    ##################################################################################################################
    # set_proof_of_play_options
    ##################################################################################################################

    def set_proof_of_play_options(cls, tenant_code, proof_of_play_logging, proof_of_play_url, tenant_key=None):
        if tenant_key:
            tenant = tenant_key.get()
        else:
            tenant = Tenant.find_by_tenant_code(tenant_code)
        if proof_of_play_logging is not None:
            tenant.proof_of_play_logging = proof_of_play_logging
            Tenant.toggle_proof_of_play_on_tenant_devices(
                should_be_enabled=tenant.proof_of_play_logging,
                tenant_code=tenant.tenant_code,
                tenant_key=tenant_key)
        if proof_of_play_url is None or proof_of_play_url == '':
            tenant.proof_of_play_url = config.DEFAULT_PROOF_OF_PLAY_URL
        else:
            tenant.proof_of_play_url = proof_of_play_url.strip().lower()

    def test_set_proof_of_play_options_with_key_pop_on_url_none(self):
        self.tenant.proof_of_play_logging = True
        self.tenant.put()
        self.assertTrue(self.tenant.proof_of_play_logging)
        devices = Tenant.find_devices(self.tenant_key, unmanaged=False)
        for device in devices:
            device.proof_of_play_logging = False
            device.proof_of_play_editable = False
            device.put()
        Tenant.set_proof_of_play_options(
            tenant_code=self.TENANT_CODE,
            proof_of_play_logging=True,
            proof_of_play_url=None,
            tenant_key=self.tenant_key)
        self.assertEqual(self.tenant.proof_of_play_url, config.DEFAULT_PROOF_OF_PLAY_URL)
        for device in devices:
            self.assertFalse(device.proof_of_play_logging)
            self.assertTrue(device.proof_of_play_editable)

    def test_set_proof_of_play_options_with_key_pop_on_url_specified(self):
        self.tenant.proof_of_play_logging = True
        self.tenant.put()
        self.assertTrue(self.tenant.proof_of_play_logging)
        devices = Tenant.find_devices(self.tenant_key, unmanaged=False)
        for device in devices:
            device.proof_of_play_logging = False
            device.proof_of_play_editable = False
            device.put()
        Tenant.set_proof_of_play_options(
            tenant_code=self.TENANT_CODE,
            proof_of_play_logging=True,
            proof_of_play_url='http://www.FOO.com',
            tenant_key=self.tenant_key)
        self.assertEqual(self.tenant.proof_of_play_url, 'http://www.foo.com')
        for device in devices:
            self.assertFalse(device.proof_of_play_logging)
            self.assertTrue(device.proof_of_play_editable)

    def test_set_proof_of_play_options_with_key_pop_off_url_none(self):
        self.tenant.proof_of_play_logging = False
        self.tenant.put()
        self.assertFalse(self.tenant.proof_of_play_logging)
        devices = Tenant.find_devices(self.tenant_key, unmanaged=False)
        for device in devices:
            device.proof_of_play_logging = True
            device.proof_of_play_editable = True
            device.put()
        Tenant.set_proof_of_play_options(
            tenant_code=self.TENANT_CODE,
            proof_of_play_logging=False,
            proof_of_play_url=None,
            tenant_key=self.tenant_key)
        self.assertEqual(self.tenant.proof_of_play_url, config.DEFAULT_PROOF_OF_PLAY_URL)
        for device in devices:
            self.assertFalse(device.proof_of_play_logging)
            self.assertFalse(device.proof_of_play_editable)

    ##################################################################################################################
    # find_by_organization_unit_path
    ##################################################################################################################
    def test_find_by_organization_unit_path_when_stored_on_tenant_object(self):
        tenant = Tenant.find_by_organization_unit_path('/skykit/foobar')
        self.assertTrue(tenant.tenant_code, self.TENANT_CODE)

    def test_find_by_organization_unit_path_when_not_stored_on_tenant_object_with_leading_forward_slash(self):
        self.tenant.organization_unit_path = None
        self.tenant.put()
        tenant = Tenant.find_by_organization_unit_path('/something/Skykit/foobar/some_device_property')
        self.assertTrue(tenant.tenant_code, self.TENANT_CODE)
        tenant = Tenant.find_by_organization_unit_path('/something/skykit/foobar/some_device_property')
        self.assertTrue(tenant.tenant_code, self.TENANT_CODE)
        tenant = Tenant.find_by_organization_unit_path('/something/skykit/Foobar/some_device_property')
        self.assertTrue(tenant.tenant_code, self.TENANT_CODE)

    def test_find_by_organization_unit_path_when_not_stored_on_tenant_object_without_leading_forward_slash(self):
        self.tenant.organization_unit_path = None
        self.tenant.put()
        tenant = Tenant.find_by_organization_unit_path('something/Skykit/foobar/some_device_property')
        self.assertTrue(tenant.tenant_code, self.TENANT_CODE)
        tenant = Tenant.find_by_organization_unit_path('something/skykit/foobar/some_device_property')
        self.assertTrue(tenant.tenant_code, self.TENANT_CODE)
        tenant = Tenant.find_by_organization_unit_path('something/skykit/Foobar/some_device_property')
        self.assertTrue(tenant.tenant_code, self.TENANT_CODE)
