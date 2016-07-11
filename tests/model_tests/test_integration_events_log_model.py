from datetime import datetime

from env_setup import setup_test_paths
from tests.provisioning_distributor_user_base_test import ProvisioningDistributorUserBase

setup_test_paths()

from models import IntegrationEventLog

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestIntegrationEventLogModel(ProvisioningDistributorUserBase):
    EVENT_CATEGORY = 'Registration'
    COMPONENT_NAME = 'Player'
    WORKFLOW_STEP = 'request to provisioning to create device'
    CURRENT_CLASS_VERSION = 1

    def setUp(self):
        super(TestIntegrationEventLogModel, self).setUp()

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

    def test_get_correlation_identifier_for_registration_event(self):
        device_urlsafe_key = 'ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyGwsSDkNocm9tZU9zRGV2aWNlGICAgKC2uokJDA'
        event_log = IntegrationEventLog.create(
            event_category=self.EVENT_CATEGORY,
            component_name=self.COMPONENT_NAME,
            workflow_step='First heartbeat',
            device_urlsafe_key=device_urlsafe_key)
        event_log.put()
        correlation_identifier = IntegrationEventLog.get_correlation_identifier_for_registration(
            device_urlsafe_key)
        self.assertEqual(event_log.correlation_identifier, correlation_identifier)

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        event_log = IntegrationEventLog.create(
            event_category=self.EVENT_CATEGORY,
            component_name=self.COMPONENT_NAME,
            workflow_step=self.WORKFLOW_STEP)
        event_log.class_version = 47
        event_log.put()
        self.assertEqual(event_log.class_version, self.CURRENT_CLASS_VERSION)
