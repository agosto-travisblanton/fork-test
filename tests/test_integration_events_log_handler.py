import json

from datetime import datetime, timedelta

from env_setup import setup_test_paths
from model_entities.integration_events_log_model import IntegrationEventLog
from routes import application
from tests.provisioning_base_test import ProvisioningBaseTest

setup_test_paths()

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestIntegrationEventsLogHandler(ProvisioningBaseTest):
    INTEGRATION_EVENTS_DEFAULT_EVENTS_CATEGORY = 'Device Registration'
    INTEGRATION_EVENTS_DEFAULT_COMPONENT_NAME = 'Player'
    INTEGRATION_EVENTS_REGISTRATION_WORKFLOW_STEP_1 = 'Request from Player for device creation'
    INTEGRATION_EVENTS_REGISTRATION_WORKFLOW_STEP_2 = 'Request to Directory API for device information'
    INTEGRATION_EVENTS_REGISTRATION_WORKFLOW_STEP_3 = 'Request to CM for device creation'
    INTEGRATION_EVENTS_REGISTRATION_WORKFLOW_STEP_4 = 'Response from CM for device creation'
    INTEGRATION_EVENTS_REGISTRATION_WORKFLOW_STEP_5 = 'Response from Directory API for device information'
    INTEGRATION_EVENTS_REGISTRATION_WORKFLOW_STEP_6 = 'Response to Player with resource URL in header'

    def setUp(self):
        super(TestIntegrationEventsLogHandler, self).setUp()
        self.distributor_admin = self.create_distributor_admin(email='distributor.admin@agosto.com',
                                                               distributor_name='Agosto')
        self.distributor_admin_header = {
            'X-Provisioning-User': self.distributor_admin.key.urlsafe()
        }
        self.platform_admin = self.create_platform_admin(email='platform.admin@agosto.com',
                                                         distributor_name='Agosto')
        self.platform_admin_header = {
            'X-Provisioning-User': self.platform_admin.key.urlsafe()
        }

        correlation_id = IntegrationEventLog.generate_correlation_id()
        timestamp = datetime.utcnow()
        self.registration_event_1 = IntegrationEventLog.create(
            event_category=self.INTEGRATION_EVENTS_DEFAULT_EVENTS_CATEGORY,
            component_name=self.INTEGRATION_EVENTS_DEFAULT_COMPONENT_NAME,
            workflow_step=self.INTEGRATION_EVENTS_REGISTRATION_WORKFLOW_STEP_1,
            utc_timestamp=timestamp + timedelta(seconds=1),
            correlation_identifier=correlation_id)
        self.registration_event_1.put()
        self.registration_event_2 = IntegrationEventLog.create(
            event_category=self.INTEGRATION_EVENTS_DEFAULT_EVENTS_CATEGORY,
            component_name=self.INTEGRATION_EVENTS_DEFAULT_COMPONENT_NAME,
            workflow_step=self.INTEGRATION_EVENTS_REGISTRATION_WORKFLOW_STEP_2,
            utc_timestamp=timestamp + timedelta(seconds=2),
            correlation_identifier=correlation_id)
        self.registration_event_2.put()
        self.registration_event_3 = IntegrationEventLog.create(
            event_category=self.INTEGRATION_EVENTS_DEFAULT_EVENTS_CATEGORY,
            component_name=self.INTEGRATION_EVENTS_DEFAULT_COMPONENT_NAME,
            workflow_step=self.INTEGRATION_EVENTS_REGISTRATION_WORKFLOW_STEP_3,
            utc_timestamp=timestamp + timedelta(seconds=3),
            correlation_identifier=correlation_id)
        self.registration_event_3.put()
        self.registration_event_4 = IntegrationEventLog.create(
            event_category=self.INTEGRATION_EVENTS_DEFAULT_EVENTS_CATEGORY,
            component_name=self.INTEGRATION_EVENTS_DEFAULT_COMPONENT_NAME,
            workflow_step=self.INTEGRATION_EVENTS_REGISTRATION_WORKFLOW_STEP_4,
            utc_timestamp=timestamp + timedelta(seconds=4),
            correlation_identifier=correlation_id)
        self.registration_event_4.put()
        self.registration_event_5 = IntegrationEventLog.create(
            event_category=self.INTEGRATION_EVENTS_DEFAULT_EVENTS_CATEGORY,
            component_name=self.INTEGRATION_EVENTS_DEFAULT_COMPONENT_NAME,
            workflow_step=self.INTEGRATION_EVENTS_REGISTRATION_WORKFLOW_STEP_5,
            utc_timestamp=timestamp + timedelta(seconds=5),
            correlation_identifier=correlation_id)
        self.registration_event_5.put()
        self.registration_event_6 = IntegrationEventLog.create(
            event_category=self.INTEGRATION_EVENTS_DEFAULT_EVENTS_CATEGORY,
            component_name=self.INTEGRATION_EVENTS_DEFAULT_COMPONENT_NAME,
            workflow_step=self.INTEGRATION_EVENTS_REGISTRATION_WORKFLOW_STEP_6,
            utc_timestamp=timestamp + timedelta(seconds=6),
            correlation_identifier=correlation_id)
        self.registration_event_6.put()

    def test_get_integration_events_list_with_platform_admin_access_returns_ok_http_status(self):
        request_parameters = {}
        uri = application.router.build(None, 'integration-events-list', None, {})
        response = self.get(uri, params=request_parameters, headers=self.platform_admin_header)
        self.assertOK(response)

    def test_get_integration_events_list_without_platform_admin_access_returns_forbidden_http_status(self):
        request_parameters = {}
        uri = application.router.build(None, 'integration-events-list', None, {})
        response = self.get(uri, params=request_parameters, headers=self.distributor_admin_header)
        self.assertForbidden(response)

    def test_get_integration_events_list_returns_expected_fetch_count_without_filter(self):
        request_parameters = {}
        uri = application.router.build(None, 'integration-events-list', None, {})
        response = self.get(uri, params=request_parameters, headers=self.platform_admin_header)
        response_json = json.loads(response.body)
        self.assertLength(6, response_json)

    def test_get_integration_events_list_returns_expected_page_size(self):
        request_parameters = {'pageSize': 3}
        uri = application.router.build(None, 'integration-events-list', None, {})
        response = self.get(uri, params=request_parameters, headers=self.platform_admin_header)
        response_json = json.loads(response.body)
        self.assertLength(3, response_json)

    def test_get_integration_events_returns_list_in_default_order_by_utc_timestamp(self):
        request_parameters = {}
        uri = application.router.build(None, 'integration-events-list', None, {})
        response = self.get(uri, params=request_parameters, headers=self.platform_admin_header)
        response_json = json.loads(response.body)
        item_1 = response_json[0]
        self.assertEqual(item_1['workflowStep'], self.INTEGRATION_EVENTS_REGISTRATION_WORKFLOW_STEP_1)
        item_6 = response_json[5]
        self.assertEqual(item_6['workflowStep'], self.INTEGRATION_EVENTS_REGISTRATION_WORKFLOW_STEP_6)
        self.assertLess(item_1['utcTimestamp'], item_6['utcTimestamp'])