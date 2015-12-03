# NOTE: These test can be used if deferred.defer is removed from device_heartbeat_status_sweep

# from app_config import config
# from device_monitoring import device_heartbeat_status_sweep
# from env_setup import setup_test_paths
#
# setup_test_paths()
#
# from models import Tenant, ChromeOsDevice, Distributor, Domain, DeviceIssueLog
# from agar.test import BaseTest
# from datetime import datetime, timedelta
#
# __author__ = 'Bob MacNeal <bob.macneal@agosto.com>'
#
#
# class TestDeviceMonitoring(BaseTest):
#     ADMIN_EMAIL = 'foo@bar.com'
#     CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
#     CONTENT_SERVER_API_KEY = 'API KEY'
#     CONTENT_SERVER_URL = 'https://skykit-contentmanager-int.appspot.com/content'
#     CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
#     DEVICE_ID = '132e235a-b346-4a37-a100-de49fa753a2a'
#     GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
#     MAC_ADDRESS = '54271e619346'
#     TENANT_CODE = 'foobar_inc'
#     TENANT_NAME = 'Foobar, Inc,'
#     DISTRIBUTOR_NAME = 'agosto'
#     IMPERSONATION_EMAIL = 'test@test.com'
#     DISK_UTILIZATION = 26
#     MEMORY_UTILIZATION = 63
#     PROGRAM = 'some program'
#
#     def setUp(self):
#         super(TestDeviceMonitoring, self).setUp()
#         self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
#                                               active=True)
#         self.distributor_key = self.distributor.put()
#         self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
#                                     distributor_key=self.distributor_key,
#                                     impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
#                                     active=True)
#         self.domain_key = self.domain.put()
#         self.tenant = Tenant.create(tenant_code=self.TENANT_CODE,
#                                     name=self.TENANT_NAME,
#                                     admin_email=self.ADMIN_EMAIL,
#                                     content_server_url=self.CONTENT_SERVER_URL,
#                                     content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
#                                     domain_key=self.domain_key,
#                                     active=True)
#         self.tenant_key = self.tenant.put()
#         self.device = ChromeOsDevice.create_managed(
#             tenant_key=self.tenant_key,
#             gcm_registration_id=self.GCM_REGISTRATION_ID,
#             device_id=self.DEVICE_ID,
#             mac_address=self.MAC_ADDRESS)
#         self.device.disk_utilization = self.DISK_UTILIZATION
#         self.device.memory_utilization = self.MEMORY_UTILIZATION
#         self.device.program = self.PROGRAM
#         self.device.heartbeat_updated = datetime.utcnow()
#
#     ##################################################################################################################
#     ## device_heartbeat_status_sweep
#     ##################################################################################################################
#
#     def test_device_heartbeat_status_sweep_adds_a_device_down_issue_for_unresponsive_device(self):
#         elapsed_seconds = config.PLAYER_UNRESPONSIVE_SECONDS_THRESHOLD + 1
#         self.device.heartbeat_updated = datetime.utcnow() - timedelta(seconds=elapsed_seconds)
#         device_key = self.device.put()
#         device_heartbeat_status_sweep()
#         issues = DeviceIssueLog.get_all_by_device_key(device_key)
#         self.assertLength(1, issues)
#         issue = issues[0]
#         self.assertFalse(issue.up)
#         self.assertEqual(issue.category, config.DEVICE_ISSUE_PLAYER_DOWN)
#         self.assertEqual(issue.device_key, device_key)
#         self.assertEqual(issue.disk_utilization, self.DISK_UTILIZATION)
#         self.assertEqual(issue.memory_utilization, self.MEMORY_UTILIZATION)
#         self.assertIsNone(issue.last_error)
#         self.assertEqual(issue.program, self.PROGRAM)
#         self.assertIsNone(issue.program_id)
#
#     ##################################################################################################################
#     ## chunking
#     ##################################################################################################################
#
#     def test_device_chunking_with_unresponsive_devices_creates_issues(self):
#         number_of_devices = 120
#         self.__build_unresponsive_devices(tenant_key=self.tenant_key, number_to_build=number_of_devices)
#         device_heartbeat_status_sweep()
#         issues = DeviceIssueLog.query().fetch()
#         self.assertTrue(len(issues) == number_of_devices)
#         for issue in issues:
#             self.assertFalse(issue.up)
#
#     def test_device_chunking_with_responsive_devices_does_not_create_issues(self):
#         number_of_devices = 120
#         self.__build_unresponsive_devices(tenant_key=self.tenant_key, number_to_build=number_of_devices)
#         device_heartbeat_status_sweep()
#         issues = DeviceIssueLog.query(DeviceIssueLog.up == True).fetch()
#         self.assertTrue(len(issues) == 0)
#
#     def __build_unresponsive_devices(self, tenant_key, number_to_build):
#         self.__build_devices(tenant_key=tenant_key, number_to_build=number_to_build, responsive=False)
#
#     def __build_responsive_devices(self, tenant_key, number_to_build):
#         self.__build_devices(self, tenant_key, number_to_build, responsive=True)
#
#     def __build_devices(self,tenant_key, number_to_build, responsive):
#         results = []
#         if responsive:
#             elapsed_seconds = config.PLAYER_UNRESPONSIVE_SECONDS_THRESHOLD - 1
#         else:
#             elapsed_seconds = config.PLAYER_UNRESPONSIVE_SECONDS_THRESHOLD + 1
#         for i in range(number_to_build):
#             device = ChromeOsDevice.create_managed(tenant_key=tenant_key,
#                                                    mac_address='mac{0}'.format(i),
#                                                    gcm_registration_id='gcm{0}'.format(i),
#                                                    device_id='d{0}'.format(i))
#             device.heartbeat_updated = datetime.utcnow() - timedelta(seconds=elapsed_seconds)
#             device.up = True
#             device.put()
#             results.append(device)
#         return results
#
