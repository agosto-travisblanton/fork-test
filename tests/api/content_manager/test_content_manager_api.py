import httplib

from google.appengine.ext import ndb

from env_setup import setup_test_paths
from model_entities.integration_events_log_model import IntegrationEventLog

setup_test_paths()
from http_client import HttpClient, HttpClientRequest, HttpClientResponse
from models import Tenant, ChromeOsDevice, Distributor, Domain
from agar.test import BaseTest
from integrations.content_manager.content_manager_api import ContentManagerApi

from mockito import when, any as any_matcher

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>, Christopher Bartling <chris.bartling@agosto.com>'


class TestContentManagerApi(BaseTest):
    NAME = 'foobar tenant'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://skykit-contentmanager-int.appspot.com/content'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
    CONTENT_SERVER_API_KEY = 'API KEY'
    TENANT_CODE = 'foobar'
    DISTRIBUTOR_NAME = 'agosto'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    IMPERSONATION_EMAIL = 'test@test.com'
    CONTENT_MANAGER_DISPLAY_NAME = 'Agosto No. 1'
    CONTENT_MANAGER_LOCATION_DESCRIPTION = 'Front Reception'
    CORRELATION_ID = 'adsfsd132'

    def setUp(self):
        super(TestContentManagerApi, self).setUp()
        self.content_manager_api = ContentManagerApi()
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.distributor_key,
                                    impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                    active=True)
        self.domain_key = self.domain.put()

        self.tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                                    name=self.NAME,
                                    admin_email=self.ADMIN_EMAIL,
                                    content_server_url=self.CONTENT_SERVER_URL,
                                    content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                    domain_key=self.domain_key,
                                    active=True)
        self.tenant_key = self.tenant.put()
        self.device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                                    device_id='f7ds8970dfasd8f70ad987',
                                                    gcm_registration_id='fad7f890ad7f8ad0s7fa8s',
                                                    mac_address='54271e619346',
                                                    serial_number='SN000123')
        self.device.content_manager_location_description = self.CONTENT_MANAGER_LOCATION_DESCRIPTION
        self.device.content_manager_display_name = self.CONTENT_MANAGER_DISPLAY_NAME
        self.device_key = self.device.put()

    ##################################################################################################################
    # create_tenant
    ##################################################################################################################

    def test_create_tenant_success(self):
        when(HttpClient).post(any_matcher(HttpClientRequest)).thenReturn(
            HttpClientResponse(status_code=httplib.CREATED))
        result = self.content_manager_api.create_tenant(tenant=self.tenant, correlation_id=self.CORRELATION_ID)
        self.assertTrue(result)
        events = IntegrationEventLog.query(
            ndb.AND(IntegrationEventLog.event_category == 'Tenant Creation',
                    IntegrationEventLog.correlation_identifier == self.CORRELATION_ID)).fetch()
        self.assertEqual(events[0].workflow_step,
                         'Response from Content Manager for create_tenant request (201 Created)')

    def test_create_tenant_failure(self):
        when(HttpClient).post(any_matcher(HttpClientRequest)).thenReturn(
            HttpClientResponse(status_code=httplib.BAD_REQUEST))
        result = self.content_manager_api.create_tenant(tenant=self.tenant, correlation_id=self.CORRELATION_ID)
        self.assertFalse(result)
        events = IntegrationEventLog.query(
            ndb.AND(IntegrationEventLog.event_category == 'Tenant Creation',
                    IntegrationEventLog.correlation_identifier == self.CORRELATION_ID)).fetch()
        self.assertEqual(events[0].workflow_step, 'Response from Content Manager for create_tenant request (Failed)')

    ##################################################################################################################
    # create_device
    ##################################################################################################################

    def test_create_device_success_creates_expected_event_logging(self):
        when(HttpClient).post(any_matcher(HttpClientRequest)).thenReturn(HttpClientResponse(
            status_code=httplib.CREATED))
        self.content_manager_api.create_device(device_urlsafe_key=self.device_key.urlsafe(),
                                               correlation_id=self.CORRELATION_ID)
        events = IntegrationEventLog.query(
            ndb.AND(IntegrationEventLog.event_category == 'Registration',
                    IntegrationEventLog.correlation_identifier == self.CORRELATION_ID)).fetch()
        self.assertEqual(events[0].workflow_step, 'Request to Content Manager for a create_device')
        self.assertEqual(events[1].workflow_step,
                         'Response from Content Manager for create_device request (201 Created)')

    def test_create_device_failure_creates_expected_retry_event_logging(self):
        when(HttpClient).post(any_matcher(HttpClientRequest)).thenReturn(HttpClientResponse(
            status_code=httplib.BAD_REQUEST))
        self.content_manager_api.create_device(device_urlsafe_key=self.device_key.urlsafe(),
                                               correlation_id=self.CORRELATION_ID)
        events = IntegrationEventLog.query(
            ndb.AND(IntegrationEventLog.event_category == 'Registration',
                    IntegrationEventLog.correlation_identifier == self.CORRELATION_ID)).fetch()
        self.assertEqual(events[0].workflow_step, 'Request to Content Manager for a create_device')
        self.assertEqual(events[1].workflow_step, 'Response from Content Manager for create_device request (Failed)')
        self.assertEqual(events[2].workflow_step, 'Retry 1: Request to Content Manager for a create_device')
        self.assertEqual(events[3].workflow_step,
                         'Retry 1: Response from Content Manager for create_device request (Failed)')
        self.assertEqual(events[4].workflow_step, 'Retry 2: Request to Content Manager for a create_device')
        self.assertEqual(events[5].workflow_step,
                         'Retry 2: Response from Content Manager for create_device request (Failed)')
        self.assertEqual(events[6].workflow_step,
                         'Retry 3: Request to Content Manager for a create_device')
        self.assertEqual(events[7].workflow_step,
                         'Retry 3: Response from Content Manager for create_device request (Failed)')
        self.assertEqual(events[8].workflow_step, 'Retry 4: Request to Content Manager for a create_device')
        self.assertEqual(events[9].workflow_step,
                         'Retry 4: Response from Content Manager for create_device request (Failed)')
        self.assertEqual(events[10].workflow_step, 'Ending Retry')

