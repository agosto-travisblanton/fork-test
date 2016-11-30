from datetime import datetime

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
    STORAGE_UTILIZATION = 99
    MEMORY_UTILIZATION = 8
    PROGRAM = 'some program'
    PLAYLIST = 'some playlist'
    CONTENT_KIND = 'Video'
    CONTENT_NAME = 'Video 101'
    CONTENT_ID = 'V101'
    CURRENT_CLASS_VERSION = 1
    NORMAL_LEVEL = 0
    NORMAL_LEVEL_DESCRIPTION = 'Normal'
    WARNING_LEVEL = 1
    WARNING_LEVEL_DESCRIPTION = 'Warning'
    DANGER_LEVEL = 2
    DANGER_LEVEL_DESCRIPTION = 'Danger'


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

    def test_create_returns_expected_device_issue_representation_for_down_device(self):
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_PLAYER_DOWN,
                                      up=False,
                                      storage_utilization=self.STORAGE_UTILIZATION,
                                      memory_utilization=self.MEMORY_UTILIZATION,
                                      program=self.PROGRAM,
                                      playlist=self.PLAYLIST,
                                      content_kind=self.CONTENT_KIND,
                                      content_name=self.CONTENT_NAME,
                                      content_id=self.CONTENT_ID)
        self.assertEqual(issue.device_key, self.device_key)
        self.assertEqual(issue.category, config.DEVICE_ISSUE_PLAYER_DOWN)
        self.assertEqual(issue.level, self.DANGER_LEVEL)
        self.assertEqual(issue.level_descriptor,self.DANGER_LEVEL_DESCRIPTION)
        self.assertFalse(issue.up)
        self.assertFalse(issue.resolved)
        self.assertIsNone(issue.resolved_datetime)
        self.assertEqual(issue.storage_utilization, self.STORAGE_UTILIZATION)
        self.assertEqual(issue.memory_utilization, self.MEMORY_UTILIZATION)
        self.assertEqual(issue.program, self.PROGRAM)
        self.assertEqual(issue.playlist, self.PLAYLIST)
        self.assertEqual(issue.content_kind, self.CONTENT_KIND)
        self.assertEqual(issue.content_name, self.CONTENT_NAME)
        self.assertEqual(issue.content_id, self.CONTENT_ID)
        self.assertIsNone(issue.program_id)
        self.assertIsNone(issue.last_error)
        self.assertIsNone(issue.created)
        self.assertIsNone(issue.updated)

    def test_create_returns_expected_device_issue_representation_for_up_device(self):
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_PLAYER_UP,
                                      up=True,
                                      storage_utilization=self.STORAGE_UTILIZATION,
                                      memory_utilization=self.MEMORY_UTILIZATION,
                                      program=self.PROGRAM)
        self.assertEqual(issue.device_key, self.device_key)
        self.assertEqual(issue.category, config.DEVICE_ISSUE_PLAYER_UP)
        self.assertEqual(issue.level, self.NORMAL_LEVEL)
        self.assertEqual(issue.level_descriptor, self.NORMAL_LEVEL_DESCRIPTION)
        self.assertTrue(issue.up)

    def test_create_with_float_memory_input_converts_to_int(self):
        memory = 31.920000000000002
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_PLAYER_UP,
                                      up=True,
                                      storage_utilization=self.STORAGE_UTILIZATION,
                                      memory_utilization=memory,
                                      program=self.PROGRAM)
        self.assertEqual(issue.memory_utilization, int(memory))

    def test_create_with_float_storage_input_converts_to_int(self):
        storage = 89.910000000000001
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_PLAYER_UP,
                                      up=True,
                                      storage_utilization=storage,
                                      memory_utilization=self.MEMORY_UTILIZATION,
                                      program=self.PROGRAM)
        self.assertEqual(issue.storage_utilization, int(storage))

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

    def test_device_has_unresolved_memory_issue_returns_true_when_unresolved(self):
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_MEMORY_HIGH,
                                      up=True)
        issue.put()
        self.assertFalse(issue.resolved)
        self.assertEqual(issue.category, config.DEVICE_ISSUE_MEMORY_HIGH)
        self.assertIsNone(issue.resolved_datetime)
        self.assertTrue(DeviceIssueLog.device_has_unresolved_memory_issues(self.device_key))

    def test_device_has_unresolved_memory_issue_returns_false_when_none(self):
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_MEMORY_HIGH,
                                      up=True)
        issue.resolved = True
        issue.resolved_datetime = datetime.utcnow()
        issue.put()
        self.assertTrue(issue.resolved)
        self.assertIsNotNone(issue.resolved_datetime)
        self.assertFalse(DeviceIssueLog.device_has_unresolved_memory_issues(self.device_key))

    def test_device_has_unresolved_storage_issue_returns_true_when_unresolved(self):
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_STORAGE_LOW,
                                      up=True)
        issue.put()
        self.assertFalse(issue.resolved)
        self.assertEqual(issue.category, 'Storage available low')
        self.assertIsNone(issue.resolved_datetime)
        self.assertTrue(DeviceIssueLog.device_has_unresolved_storage_issues(self.device_key))

    def test_device_has_unresolved_storage_issue_returns_false_when_none(self):
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_STORAGE_LOW,
                                      up=True)
        issue.resolved = True
        issue.resolved_datetime = datetime.utcnow()
        issue.put()
        self.assertTrue(issue.resolved)
        self.assertIsNotNone(issue.resolved_datetime)
        self.assertFalse(DeviceIssueLog.device_has_unresolved_storage_issues(self.device_key))

    def test_resolve_device_storage_issues(self):
        issue_1 = DeviceIssueLog.create(device_key=self.device_key,
                                        category=config.DEVICE_ISSUE_STORAGE_LOW,
                                        up=True)
        issue_1.put()
        self.assertFalse(issue_1.resolved)
        self.assertIsNone(issue_1.resolved_datetime)
        issue_2 = DeviceIssueLog.create(device_key=self.device_key,
                                        category=config.DEVICE_ISSUE_STORAGE_LOW,
                                        up=True)
        issue_2.put()
        self.assertFalse(issue_2.resolved)
        self.assertIsNone(issue_2.resolved_datetime)
        resolved_datetime = datetime.utcnow()
        DeviceIssueLog.resolve_device_storage_issues(self.device_key, resolved_datetime)
        self.assertTrue(issue_1.resolved)
        self.assertEqual(issue_1.resolved_datetime, resolved_datetime)
        self.assertEqual(issue_1.level, self.WARNING_LEVEL)
        self.assertEqual(issue_1.level_descriptor, self.WARNING_LEVEL_DESCRIPTION)
        self.assertTrue(issue_2.resolved)
        self.assertEqual(issue_2.resolved_datetime, resolved_datetime)
        self.assertEqual(issue_2.level, self.WARNING_LEVEL)
        self.assertEqual(issue_2.level_descriptor, self.WARNING_LEVEL_DESCRIPTION)

    def test_resolve_device_memory_issues(self):
        issue_1 = DeviceIssueLog.create(device_key=self.device_key,
                                        category=config.DEVICE_ISSUE_MEMORY_HIGH,
                                        up=True)
        issue_1.put()
        self.assertFalse(issue_1.resolved)
        self.assertIsNone(issue_1.resolved_datetime)
        issue_2 = DeviceIssueLog.create(device_key=self.device_key,
                                        category=config.DEVICE_ISSUE_MEMORY_HIGH,
                                        up=True)
        issue_2.put()
        self.assertFalse(issue_2.resolved)
        self.assertIsNone(issue_2.resolved_datetime)
        resolved_datetime = datetime.utcnow()
        DeviceIssueLog.resolve_device_memory_issues(self.device_key, resolved_datetime)
        self.assertTrue(issue_1.resolved)
        self.assertEqual(issue_1.resolved_datetime, resolved_datetime)
        self.assertEqual(issue_1.level, self.WARNING_LEVEL)
        self.assertEqual(issue_1.level_descriptor, self.WARNING_LEVEL_DESCRIPTION)
        self.assertTrue(issue_2.resolved)
        self.assertEqual(issue_2.resolved_datetime, resolved_datetime)
        self.assertEqual(issue_2.level, self.WARNING_LEVEL)
        self.assertEqual(issue_2.level_descriptor, self.WARNING_LEVEL_DESCRIPTION)

    def test_resolve_device_down_issues(self):
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_PLAYER_DOWN,
                                      up=False,
                                      storage_utilization=self.STORAGE_UTILIZATION,
                                      memory_utilization=self.MEMORY_UTILIZATION,
                                      program=self.PROGRAM,
                                      resolved=False)
        issue.put()
        self.assertFalse(issue.up)
        self.assertFalse(issue.resolved)
        self.assertIsNone(issue.resolved_datetime)
        self.assertEqual(issue.level, self.DANGER_LEVEL)
        self.assertEqual(issue.level_descriptor, self.DANGER_LEVEL_DESCRIPTION)
        resolved_datetime = datetime.utcnow()
        DeviceIssueLog.resolve_device_down_issues(self.device_key, resolved_datetime)
        self.assertTrue(issue.up)
        self.assertEqual(issue.level, self.DANGER_LEVEL)
        self.assertEqual(issue.level_descriptor, self.DANGER_LEVEL_DESCRIPTION)
        self.assertTrue(issue.resolved)
        self.assertEqual(issue.resolved_datetime, resolved_datetime)

    def test_no_matching_issues_returns_true_when_no_matching_issue_exists(self):
        self.assertTrue(DeviceIssueLog.no_matching_issues(device_key=self.device_key,
                                                          category=config.DEVICE_ISSUE_MEMORY_HIGH,
                                                          up=True,
                                                          storage_utilization=self.STORAGE_UTILIZATION,
                                                          memory_utilization=self.MEMORY_UTILIZATION))

    def test_no_matching_issues_returns_false_when_matching_issue_exists(self):
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_MEMORY_HIGH,
                                      up=True,
                                      storage_utilization=self.STORAGE_UTILIZATION,
                                      memory_utilization=self.MEMORY_UTILIZATION,
                                      program=self.PROGRAM)
        issue.put()
        self.assertFalse(DeviceIssueLog.no_matching_issues(device_key=self.device_key,
                                                           category=config.DEVICE_ISSUE_MEMORY_HIGH,
                                                           up=True,
                                                           storage_utilization=self.STORAGE_UTILIZATION,
                                                           memory_utilization=self.MEMORY_UTILIZATION,
                                                           program=self.PROGRAM))

    def test_no_matching_issues_returns_true_when_similar_but_not_matching_issue_exists(self):
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_MEMORY_HIGH,
                                      up=True,
                                      storage_utilization=self.STORAGE_UTILIZATION + 5,
                                      memory_utilization=self.MEMORY_UTILIZATION)
        issue.put()
        self.assertTrue(DeviceIssueLog.no_matching_issues(device_key=self.device_key,
                                                          category=config.DEVICE_ISSUE_MEMORY_HIGH,
                                                          up=True,
                                                          storage_utilization=self.STORAGE_UTILIZATION,
                                                          memory_utilization=self.MEMORY_UTILIZATION))

    def test_first_heartbeat_has_issue_level_normal(self):
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_FIRST_HEARTBEAT,
                                      up=True)
        issue.put()
        self.assertEqual(issue.level, self.NORMAL_LEVEL)
        self.assertEqual(issue.level_descriptor, self.NORMAL_LEVEL_DESCRIPTION)

    def test_player_version_change_has_issue_level_normal(self):
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_PLAYER_VERSION_CHANGE,
                                      up=True)
        issue.put()
        self.assertEqual(issue.level, self.NORMAL_LEVEL)
        self.assertEqual(issue.level_descriptor, self.NORMAL_LEVEL_DESCRIPTION)

    def test_os_change_has_issue_level_normal(self):
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_OS_CHANGE,
                                      up=True)
        issue.put()
        self.assertEqual(issue.level, self.NORMAL_LEVEL)
        self.assertEqual(issue.level_descriptor, self.NORMAL_LEVEL_DESCRIPTION)

    def test_os_version_change_has_issue_level_normal(self):
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_OS_VERSION_CHANGE,
                                      up=True)
        issue.put()
        self.assertEqual(issue.level, self.NORMAL_LEVEL)
        self.assertEqual(issue.level_descriptor, self.NORMAL_LEVEL_DESCRIPTION)

    def test_timezone_change_has_issue_level_normal(self):
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_TIMEZONE_CHANGE,
                                      up=True)
        issue.put()
        self.assertEqual(issue.level, self.NORMAL_LEVEL)
        self.assertEqual(issue.level_descriptor, self.NORMAL_LEVEL_DESCRIPTION)

    def test_device_not_reported_yet_method_when_no_records_retrieved(self):
        mac_address='i3234i03554350'
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id=self.DEVICE_ID,
            mac_address=mac_address)
        device_key = device.put()
        device_not_reported = DeviceIssueLog.device_not_reported_yet(device_key=device_key)
        self.assertTrue(device_not_reported)

    def test_device_not_reported_method_when_records_retrieved(self):
        issue = DeviceIssueLog.create(device_key=self.device_key,
                                      category=config.DEVICE_ISSUE_TIMEZONE_CHANGE,
                                      up=True)
        issue.put()
        device_not_reported = DeviceIssueLog.device_not_reported_yet(device_key=self.device_key)
        self.assertFalse(device_not_reported)
