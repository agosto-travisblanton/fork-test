from app_config import config
from device_monitoring import sweep_devices_for_responsiveness, sweep_devices_for_exceeding_thresholds
from env_setup import setup_test_paths

setup_test_paths()

from models import Tenant, ChromeOsDevice, Distributor, Domain, DeviceIssueLog
from agar.test import BaseTest
from datetime import datetime, timedelta

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestDeviceMonitoring(BaseTest):
    ADMIN_EMAIL = 'foo@bar.com'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    CONTENT_SERVER_API_KEY = 'API KEY'
    CONTENT_SERVER_URL = 'https://skykit-contentmanager-int.appspot.com/content'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
    TENANT_CODE = 'foobar_inc'
    TENANT_NAME = 'Foobar, Inc,'
    DISTRIBUTOR_NAME = 'agosto'
    IMPERSONATION_EMAIL = 'test@test.com'
    STORAGE_UTILIZATION = 26
    MEMORY_UTILIZATION = 63

    def setUp(self):
        super(TestDeviceMonitoring, self).setUp()
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

    ##################################################################################################################
    ## sweep_devices_for_responsiveness
    ##################################################################################################################
    def test_sweep_devices_for_responsiveness_with_unresponsive_devices_creates_issues(self):
        number_of_devices = 3
        devices = self.__build_devices(tenant_key=self.tenant_key, number_to_build=number_of_devices, responsive=False,
                                       memory=self.MEMORY_UTILIZATION, storage=self.STORAGE_UTILIZATION)
        sweep_devices_for_responsiveness(devices, datetime.utcnow())
        issues = DeviceIssueLog.query().fetch()
        self.assertTrue(len(issues) == number_of_devices)
        for issue in issues:
            self.assertFalse(issue.up)
            self.assertEqual(issue.category, config.DEVICE_ISSUE_PLAYER_DOWN)
            self.assertEqual(issue.storage_utilization, self.STORAGE_UTILIZATION)
            self.assertEqual(issue.memory_utilization, self.MEMORY_UTILIZATION)

    def test_sweep_devices_for_responsiveness_with_responsive_devices_does_not_generate_issues(self):
        number_of_devices = 3
        devices = self.__build_devices(tenant_key=self.tenant_key, number_to_build=number_of_devices, responsive=False)
        sweep_devices_for_responsiveness(devices, datetime.utcnow())
        issues = DeviceIssueLog.query(DeviceIssueLog.up == True).fetch()
        self.assertTrue(len(issues) == 0)

    ##################################################################################################################
    ## sweep_devices_for_exceeding_thresholds
    ##################################################################################################################

    def test_sweep_devices_for_exceeding_thresholds_with_devices_exceeding_memory_threshold_creates_issues(self):
        number_of_devices = 3
        high_memory = config.MEMORY_UTILIZATION_THRESHOLD + 1
        normal_storage = config.STORAGE_UTILIZATION_THRESHOLD - 1
        devices = self.__build_devices(tenant_key=self.tenant_key, number_to_build=number_of_devices, responsive=True,
                                       memory=high_memory, storage=normal_storage)
        sweep_devices_for_exceeding_thresholds(devices, datetime.utcnow())
        issues = DeviceIssueLog.query().fetch()
        self.assertTrue(len(issues) == number_of_devices)
        for issue in issues:
            self.assertTrue(issue.up)
            self.assertEqual(issue.category, config.DEVICE_ISSUE_MEMORY_HIGH)
            self.assertEqual(issue.memory_utilization, high_memory)
            self.assertEqual(issue.storage_utilization, normal_storage)

    def test_sweep_devices_for_exceeding_thresholds_with_devices_exceeding_storage_threshold_creates_issues(self):
        number_of_devices = 3
        high_storage = config.STORAGE_UTILIZATION_THRESHOLD + 1
        normal_memory = config.MEMORY_UTILIZATION_THRESHOLD - 1
        devices = self.__build_devices(tenant_key=self.tenant_key, number_to_build=number_of_devices, responsive=True,
                                       memory=normal_memory, storage=high_storage)
        sweep_devices_for_exceeding_thresholds(devices, datetime.utcnow())
        issues = DeviceIssueLog.query().fetch()
        self.assertTrue(len(issues) == number_of_devices)
        for issue in issues:
            self.assertTrue(issue.up)
            self.assertEqual(issue.category, config.DEVICE_ISSUE_STORAGE_LOW)
            self.assertEqual(issue.storage_utilization, high_storage)
            self.assertEqual(issue.memory_utilization, normal_memory)

    def test_sweep_devices_for_exceeding_thresholds_with_devices_not_exceeding_thresholds_does_not_generate_issues(
            self):
        number_of_devices = 3
        normal_storage = config.STORAGE_UTILIZATION_THRESHOLD - 1
        normal_memory = config.MEMORY_UTILIZATION_THRESHOLD - 1
        devices = self.__build_devices(tenant_key=self.tenant_key, number_to_build=number_of_devices, responsive=True,
                                       memory=normal_memory, storage=normal_storage)
        sweep_devices_for_exceeding_thresholds(devices, datetime.utcnow())
        issues = DeviceIssueLog.query().fetch()
        self.assertTrue(len(issues) == 0)

    def __build_devices(self, tenant_key, number_to_build, responsive, memory=0, storage=0):
        results = []
        if responsive:
            elapsed_seconds = config.PLAYER_UNRESPONSIVE_SECONDS_THRESHOLD - 1
        else:
            elapsed_seconds = config.PLAYER_UNRESPONSIVE_SECONDS_THRESHOLD + 1
        for i in range(number_to_build):
            device = ChromeOsDevice.create_managed(tenant_key=tenant_key,
                                                   mac_address='mac{0}'.format(i),
                                                   gcm_registration_id='gcm{0}'.format(i),
                                                   device_id='d{0}'.format(i))
            device.storage_utilization = storage
            device.memory_utilization = memory
            device.heartbeat_updated = datetime.utcnow() - timedelta(seconds=elapsed_seconds)
            device.up = True
            device.put()
            results.append(device)
        return results
