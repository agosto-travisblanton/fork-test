import json

from datetime import datetime, timedelta

from env_setup import setup_test_paths
from model_entities.integration_events_log_model import IntegrationEventLog
from routes import application
from tests.provisioning_base_test import ProvisioningBaseTest

setup_test_paths()

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestIntegrationEventsLogHandler(ProvisioningBaseTest):
    EVENT_CATEGORY = 'Device Registration'
    COMPONENT_NAME = 'Player'
    WORKFLOW_STEP_1 = 'request to provisioning to create device'
    WORKFLOW_STEP_2 = 'request for device info'
    WORKFLOW_STEP_3 = 'request to create device'
    WORKFLOW_STEP_4 = 'resposne to create device'
    WORKFLOW_STEP_5 = 'response for device info'
    WORKFLOW_STEP_6 = 'response from provisioning to player'

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
        timestamp = datetime.utcnow()
        self.registration_event_1 = IntegrationEventLog.create(
            event_category=self.EVENT_CATEGORY,
            component_name=self.COMPONENT_NAME,
            workflow_step=self.WORKFLOW_STEP_1,
            utc_timestamp=timestamp + timedelta(seconds=1))
        self.registration_event_1.put()
        self.registration_event_2 = IntegrationEventLog.create(
            event_category=self.EVENT_CATEGORY,
            component_name=self.COMPONENT_NAME,
            workflow_step=self.WORKFLOW_STEP_2,
            utc_timestamp=timestamp + timedelta(seconds=2))
        self.registration_event_2.put()
        self.registration_event_3 = IntegrationEventLog.create(
            event_category=self.EVENT_CATEGORY,
            component_name=self.COMPONENT_NAME,
            workflow_step=self.WORKFLOW_STEP_3,
            utc_timestamp=timestamp + timedelta(seconds=3))
        self.registration_event_3.put()
        self.registration_event_4 = IntegrationEventLog.create(
            event_category=self.EVENT_CATEGORY,
            component_name=self.COMPONENT_NAME,
            workflow_step=self.WORKFLOW_STEP_4,
            utc_timestamp=timestamp + timedelta(seconds=4))
        self.registration_event_4.put()
        self.registration_event_5 = IntegrationEventLog.create(
            event_category=self.EVENT_CATEGORY,
            component_name=self.COMPONENT_NAME,
            workflow_step=self.WORKFLOW_STEP_5,
            utc_timestamp=timestamp + timedelta(seconds=5))
        self.registration_event_5.put()
        self.registration_event_6 = IntegrationEventLog.create(
            event_category=self.EVENT_CATEGORY,
            component_name=self.COMPONENT_NAME,
            workflow_step=self.WORKFLOW_STEP_6,
            utc_timestamp=timestamp + timedelta(seconds=6))
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
        self.assertEqual(item_1['workflowStep'], self.WORKFLOW_STEP_1)
        item_6 = response_json[5]
        self.assertEqual(item_6['workflowStep'], self.WORKFLOW_STEP_6)
        self.assertLess(item_1['utcTimestamp'], item_6['utcTimestamp'])
