from datetime import datetime

from app_config import config
from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
from models import Domain, Distributor, DeviceIssueLog, ChromeOsDevice, Tenant, IssueLevel, IntegrationEventLog

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestIntegrationEventLogModel(BaseTest):
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
    EVENT_CATEGORY = 'Device Registration'
    COMPONENT_NAME = 'Player'
    WORKFLOW_STEP = 'request to provisioning to create device'
    CURRENT_CLASS_VERSION = 1

    def setUp(self):
        super(TestIntegrationEventLogModel, self).setUp()
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

    def test_create_returns_expected_event_log(self):
        event_log = IntegrationEventLog.create(
            event_category=self.EVENT_CATEGORY,
            component_name=self.COMPONENT_NAME,
            workflow_step=self.WORKFLOW_STEP)
        event_log.put()
        self.assertEqual(event_log.event_category, self.EVENT_CATEGORY)
        self.assertEqual(event_log.component_name, self.COMPONENT_NAME)
        self.assertEqual(event_log.workflow_step, self.WORKFLOW_STEP)
        self.assertIsNotNone(event_log.correlation_identifier)
        self.assertLessEqual(event_log.utc_timestamp, datetime.utcnow())

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        event_log = IntegrationEventLog.create(
            event_category=self.EVENT_CATEGORY,
            component_name=self.COMPONENT_NAME,
            workflow_step=self.WORKFLOW_STEP)
        event_log.class_version = 47
        event_log.put()
        self.assertEqual(event_log.class_version, self.CURRENT_CLASS_VERSION)
