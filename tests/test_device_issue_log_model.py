from app_config import config
from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
from models import Domain, Distributor, DeviceIssueLog, ChromeOsDevice, Tenant

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestDeviceIssueLogModel(BaseTest):
    ADMIN_EMAIL = 'foo@bar.com'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    CONTENT_SERVER_API_KEY = 'API KEY'
    CONTENT_SERVER_URL = 'https://skykit-contentmanager-int.appspot.com/content'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
    DEVICE_ID = '132e235a-b346-4a37-a100-de49fa753a2a'
    GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
    MAC_ADDRESS = '54271e619346'
    TENANT_CODE = 'foobar_inc'
    TENANT_NAME = 'Foobar, Inc,'
    DISTRIBUTOR_NAME = 'agosto'
    IMPERSONATION_EMAIL = 'test@test.com'
    DISK_UTILIZATION = 99
    MEMORY_UTILIZATION = 8
    PROGRAM = 'some program'
    CURRENT_CLASS_VERSION = 1

    def setUp(self):
        super(TestDeviceIssueLogModel, self).setUp()
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
        self.device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id=self.DEVICE_ID,
            mac_address=self.MAC_ADDRESS)
        self.device_key = self.device.put()

    def test_create_returns_expected_device_issue_representation(self):
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_PLAYER_DOWN,
                                      up=False,
                                      disk_utilization=self.DISK_UTILIZATION,
                                      memory_utilization=self.MEMORY_UTILIZATION,
                                      program=self.PROGRAM)
        self.assertEqual(issue.device_key, self.device_key)
        self.assertEqual(issue.category, 'Down')
        self.assertFalse(issue.up)
        self.assertEqual(issue.disk_utilization, self.DISK_UTILIZATION)
        self.assertEqual(issue.memory_utilization, self.MEMORY_UTILIZATION)
        self.assertEqual(issue.program, self.PROGRAM)
        self.assertIsNone(issue.program_id)
        self.assertIsNone(issue.last_error)
        self.assertIsNone(issue.created)
        self.assertIsNone(issue.updated)

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_PLAYER_DOWN,
                                      up=False)
        issue.class_version = 47
        issue.put()
        self.assertEqual(issue.class_version, self.CURRENT_CLASS_VERSION)

    def test_get_all_by_device_key(self):
        issue_down = DeviceIssueLog.create(device_key=self.device_key,
                                           category=config.DEVICE_ISSUE_PLAYER_DOWN,
                                           up=False)
        issue_down.put()
        issue_up = DeviceIssueLog.create(device_key=self.device_key,
                                         category=config.DEVICE_ISSUE_PLAYER_UP,
                                         up=True)
        issue_up.put()
        issues = DeviceIssueLog.get_all_by_device_key(self.device_key)
        self.assertLength(2, issues)

    def test_is_device_memory_high(self):
        pass

    def test_is_device_storage_low(self):
        pass
