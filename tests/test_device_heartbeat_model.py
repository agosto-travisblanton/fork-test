from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
from models import Tenant, Distributor, Domain, ChromeOsDevice, DeviceHeartbeat

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestDeviceHeartbeatModel(BaseTest):
    DISK_UTILIZATION = 26
    MEMORY_UTILIZATION = 63
    PROGRAM = 'some program'
    CURRENT_CLASS_VERSION = 1

    def setUp(self):
        super(TestDeviceHeartbeatModel, self).setUp()
        self.distributor = Distributor.create(name='Agosto', active=True)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name='dev.agosto.com',
                                    distributor_key=self.distributor_key,
                                    impersonation_admin_email_address='test@test.com',
                                    active=True)
        self.domain_key = self.domain.put()
        self.tenant = Tenant.create(tenant_code='foobar_inc',
                                    name='Foobar, Inc.',
                                    admin_email='foo@bar.com',
                                    content_server_url='https://skykit-contentmanager-int.appspot.com/content',
                                    content_manager_base_url='https://skykit-contentmanager-int.appspot.com',
                                    domain_key=self.domain_key,
                                    active=True)
        self.tenant_key = self.tenant.put()
        self.device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                                    gcm_registration_id='APA91bHyMJRcN7mj7b0aXGWE7Ae',
                                                    mac_address='54271ee81302')
        self.device_key = self.device.put()
        self.heartbeat = DeviceHeartbeat.create(device_key=self.device_key,
                                                disk_utilization=self.DISK_UTILIZATION,
                                                memory_utilization=self.MEMORY_UTILIZATION,
                                                currently_playing=self.PROGRAM)
        self.heartbeat.put()

    def test_find_by_device_key_returns_expected_heartbeat_representation(self):
        heartbeat = DeviceHeartbeat.find_by_device_key(self.heartbeat.device_key)
        self.assertIsNotNone(heartbeat)
        self.assertEqual(heartbeat.disk_utilization, self.DISK_UTILIZATION)
        self.assertEqual(heartbeat.memory_utilization, self.MEMORY_UTILIZATION)
        self.assertEqual(heartbeat.program, self.PROGRAM)
        self.assertTrue(heartbeat.up)

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        self.heartbeat.class_version = 47
        self.heartbeat.put()
        self.assertEqual(self.heartbeat.class_version, self.CURRENT_CLASS_VERSION)
