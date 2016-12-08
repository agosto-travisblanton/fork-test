import json

from datetime import datetime, timedelta

from app_config import config
from env_setup import setup_test_paths
from model_entities.integration_events_log_model import IntegrationEventLog
from provisioning_distributor_user_base_test import ProvisioningDistributorUserBase
from utils.web_util import build_uri
from utils.auth_util import generate_token

setup_test_paths()

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestIntegrationEventsLogHandler(ProvisioningDistributorUserBase):
    REGISTRATION = 'Registration'
    PLAYER = 'Player'
    PROVISIONING = 'Provisioning'
    DIRECTORY_API = 'Chrome Directory API'
    CONTENT_MANAGER = 'Content Manager'
    CORRELATION_IDENTIFIER = '0779aec7ae3040dcb8a3a572c356df66'
    GCM_REGISTRATION_ID = 'APA91bGl7nxmJ9JXF0_9e8zEuXIMBxX0S0o9bmmMMkqxZTjjN4hoPsweooggycp1rJonDbszrTIioEI'
    DEVICE_KEY = 'ahVzfnNreWtpdC1wcm92aXNpb25pbmdyIAsSE0ludGVncmF0aW9uRXZlbnRMb2cYgICA4JmV2wkM'
    REGISTRATION_WORKFLOW_STEP_1 = 'Request from Player to create a managed device'
    REGISTRATION_WORKFLOW_STEP_2 = 'Response to Player after creating a managed device'
    REGISTRATION_WORKFLOW_STEP_3_REQUEST = 'Request for device information'
    REGISTRATION_WORKFLOW_STEP_3_RESPONSE = 'Response for device information request'
    REGISTRATION_WORKFLOW_NO_DEVICE_INFO = 'Requested device not found'
    REGISTRATION_WORKFLOW_STEP_4_REQUEST = 'Request for device information'
    REGISTRATION_WORKFLOW_STEP_4_RESPONSE = 'Response for device information request'
    REGISTRATION_WORKFLOW_STEP_5_REQUEST = 'Request to Content Manager for a create_device'
    REGISTRATION_WORKFLOW_STEP_5_RESPONSE = 'Response from Content Manager for a create_device'

    def setUp(self):
        super(TestIntegrationEventsLogHandler, self).setUp()
        self.distributor_admin = self.create_distributor_admin(email='distributor.admin@agosto.com',
                                                               distributor_name='Agosto')
        self.distributor_admin_header = {
            'X-Provisioning-User': self.distributor_admin.key.urlsafe(),
            'JWT': str(generate_token(self.distributor_admin))
        }
        self.platform_admin = self.create_platform_admin(email='platform.admin@agosto.com',
                                                         distributor_name='Agosto')
        self.platform_admin_header = {
            'X-Provisioning-User': self.platform_admin.key.urlsafe(),
            'JWT': str(generate_token(self.platform_admin))

        }
        timestamp = datetime.utcnow()

        self.registration_event_1 = IntegrationEventLog.create(
            event_category=self.REGISTRATION,
            component_name=self.PLAYER,
            workflow_step=self.REGISTRATION_WORKFLOW_STEP_1,
            correlation_identifier=self.CORRELATION_IDENTIFIER,
            utc_timestamp=timestamp + timedelta(seconds=1),
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_urlsafe_key=self.DEVICE_KEY,
            details=
            'register_device with device key ahVzfnNreWtpdC1wcm92aXNpb25pbmdyGwsSDkNocm9tZU9zRGV2aWNlGICAgOCZsP0JDA.'
        )
        self.registration_event_1.put()

        self.registration_event_2 = IntegrationEventLog.create(
            event_category=self.REGISTRATION,
            component_name=self.PROVISIONING,
            workflow_step=self.REGISTRATION_WORKFLOW_STEP_2,
            correlation_identifier=self.CORRELATION_IDENTIFIER,
            utc_timestamp=timestamp + timedelta(seconds=2),
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_urlsafe_key=self.DEVICE_KEY,
            details=
            'Device resource uri '
            '/internal/v1/devices/ahVzfnNreWtpdC1wcm92aXNpb25pbmdyGwsSDkNocm9tZU9zRGV2aWNlGICAgOCZsP0JDA returned '
            'in response Location header.'
        )
        self.registration_event_2.put()

        self.registration_event_3 = IntegrationEventLog.create(
            event_category=self.REGISTRATION,
            component_name=self.DIRECTORY_API,
            workflow_step=self.REGISTRATION_WORKFLOW_STEP_3_REQUEST,
            correlation_identifier=self.CORRELATION_IDENTIFIER,
            utc_timestamp=timestamp + timedelta(seconds=3),
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_urlsafe_key=self.DEVICE_KEY,
        )
        self.registration_event_3.put()

        self.registration_event_4 = IntegrationEventLog.create(
            event_category=self.REGISTRATION,
            component_name=self.DIRECTORY_API,
            workflow_step=self.REGISTRATION_WORKFLOW_STEP_3_RESPONSE,
            correlation_identifier=self.CORRELATION_IDENTIFIER,
            utc_timestamp=timestamp + timedelta(seconds=4),
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_urlsafe_key=self.DEVICE_KEY,
        )
        self.registration_event_4.put()

        self.registration_event_5 = IntegrationEventLog.create(
            event_category=self.REGISTRATION,
            component_name=self.DIRECTORY_API,
            workflow_step=self.REGISTRATION_WORKFLOW_NO_DEVICE_INFO,
            correlation_identifier=self.CORRELATION_IDENTIFIER,
            utc_timestamp=timestamp + timedelta(seconds=5),
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_urlsafe_key=self.DEVICE_KEY,
        )
        self.registration_event_5.put()

        self.registration_event_6 = IntegrationEventLog.create(
            event_category=self.REGISTRATION,
            component_name=self.DIRECTORY_API,
            workflow_step=self.REGISTRATION_WORKFLOW_STEP_4_REQUEST,
            correlation_identifier=self.CORRELATION_IDENTIFIER,
            utc_timestamp=timestamp + timedelta(seconds=6),
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_urlsafe_key=self.DEVICE_KEY,
        )
        self.registration_event_6.put()

        self.registration_event_7 = IntegrationEventLog.create(
            event_category=self.REGISTRATION,
            component_name=self.DIRECTORY_API,
            workflow_step=self.REGISTRATION_WORKFLOW_STEP_4_RESPONSE,
            correlation_identifier=self.CORRELATION_IDENTIFIER,
            utc_timestamp=timestamp + timedelta(seconds=7),
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_urlsafe_key=self.DEVICE_KEY,
            details='Chrome Directory API call success! Notifying Content Manager.'
        )
        self.registration_event_7.put()

        self.registration_event_8 = IntegrationEventLog.create(
            event_category=self.REGISTRATION,
            component_name=self.CONTENT_MANAGER,
            workflow_step=self.REGISTRATION_WORKFLOW_STEP_5_REQUEST,
            correlation_identifier=self.CORRELATION_IDENTIFIER,
            utc_timestamp=timestamp + timedelta(seconds=8),
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_urlsafe_key=self.DEVICE_KEY,
            details=
            'Request url: https://skykit-contentmanager.appspot.com/provisioning/v1/displays for call to CM.'
        )
        self.registration_event_8.put()

        self.registration_event_9 = IntegrationEventLog.create(
            event_category=self.REGISTRATION,
            component_name=self.CONTENT_MANAGER,
            workflow_step=self.REGISTRATION_WORKFLOW_STEP_5_RESPONSE,
            correlation_identifier=self.CORRELATION_IDENTIFIER,
            utc_timestamp=timestamp + timedelta(seconds=9),
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_urlsafe_key=self.DEVICE_KEY,
            details=
            'ContentManagerApi.create_device: http_status=201, '
            'url=https://skykit-contentmanager.appspot.com/provisioning/v1/displays, '
            'device_key=ahVzfnNreWtpdC1wcm92aXNpb25pbmdyGwsSDkNocm9tZU9zRGV2aWNlGICAgOCZsP0JDA, '
            'api_key=6c522ae93b7b481c9f0485a419194ad4, tenant_code=agosto, SN=FBMACX001373. Success!'
        )
        self.registration_event_9.put()

        self.registration_event_10 = IntegrationEventLog.create(
            event_category='Other',
            component_name='Foobar1',
            workflow_step='Nothing',
            gcm_registration_id='jdalskdjfa'
        )
        self.registration_event_10.put()

        self.registration_event_11 = IntegrationEventLog.create(
            event_category='Other',
            component_name='Foobar2',
            workflow_step='Nothing'
        )
        self.registration_event_11.put()

        self.registration_event_12 = IntegrationEventLog.create(
            event_category='Other',
            component_name='Foobar3',
            workflow_step='Nothing'
        )
        self.registration_event_12.put()

    # **************************************************************************************************
    # get_by_event_category
    # **************************************************************************************************
    def test_get_integration_events_list_with_platform_admin_access_returns_ok_http_status(self):
        request_parameters = {}
        uri = build_uri('integration-events-list')
        response = self.get(uri, params=request_parameters, headers=self.platform_admin_header)
        self.assertOK(response)

    def test_get_integration_events_list_without_platform_admin_access_returns_forbidden_http_status(self):
        request_parameters = {}
        uri = build_uri('integration-events-list')
        response = self.get(uri, params=request_parameters, headers=self.distributor_admin_header)
        self.assertForbidden(response)

    def test_get_integration_events_list_returns_expected_fetch_count_without_filter(self):
        request_parameters = {}
        uri = build_uri('integration-events-list')
        response = self.get(uri, params=request_parameters, headers=self.platform_admin_header)
        response_json = json.loads(response.body)
        self.assertLength(9, response_json)

    def test_get_integration_events_list_returns_expected_page_size(self):
        request_parameters = {'pageSize': 1, 'eventCategory': 'Other'}
        uri = build_uri('integration-events-list')
        response = self.get(uri, params=request_parameters, headers=self.platform_admin_header)
        response_json = json.loads(response.body)
        self.assertLength(1, response_json)

    def test_get_integration_events_list_returns_expected_category_count(self):
        request_parameters = {'pageSize': 10, 'eventCategory': 'Other'}
        uri = build_uri('integration-events-list')
        response = self.get(uri, params=request_parameters, headers=self.platform_admin_header)
        response_json = json.loads(response.body)
        self.assertLength(3, response_json)

    # **************************************************************************************************
    # get_enrollment_events
    # **************************************************************************************************
    def test_get_enrollment_events_returns_expected_enrollment_events_count_with_gcm_id(self):
        request_parameters = {'deviceKey': self.DEVICE_KEY}
        uri = build_uri('enrollment-events-list')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertLength(9, response_json)

    def test_get_enrollment_events_returns_expected_enrollment_events_count_without_gcm_id(self):
        request_parameters = {}
        uri = build_uri('enrollment-events-list')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        self.assertLength(9, response_json)

    def test_get_enrollment_events_returns_list_in_default_order_by_utc_timestamp(self):
        request_parameters = {'deviceKey': self.DEVICE_KEY}
        uri = build_uri('enrollment-events-list')
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        item_1 = response_json[0]
        self.assertEqual(item_1['workflowStep'], self.REGISTRATION_WORKFLOW_STEP_1)
        item_9 = response_json[8]
        self.assertEqual(item_9['workflowStep'], self.REGISTRATION_WORKFLOW_STEP_5_RESPONSE)
        self.assertLess(item_1['utcTimestamp'], item_9['utcTimestamp'])
