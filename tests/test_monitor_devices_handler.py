from datetime import datetime, timedelta

from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest, WebTest
from models import Distributor, Domain, Tenant, ChromeOsDevice
from routes import application
from utils.web_util import build_uri
from app_config import config


class TestMonitorDevicesHandler(BaseTest, WebTest):
    ADMIN_EMAIL = 'foo@bar.com'
    APPLICATION = application
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
    DISK_UTILIZATION = 26
    MEMORY_UTILIZATION = 63
    PROGRAM = 'some program'

    def setUp(self):
        super(TestMonitorDevicesHandler, self).setUp()
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
        self.managed_device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id=self.DEVICE_ID,
            mac_address=self.MAC_ADDRESS)
        self.managed_device.disk_utilization = self.DISK_UTILIZATION
        self.managed_device.memory_utilization = self.MEMORY_UTILIZATION
        self.managed_device.program = self.PROGRAM
        self.managed_device.heartbeat_updated = datetime.utcnow()
        self.managed_device_key = self.managed_device.put()
        self.api_token_authorization_header = {
            'Authorization': config.API_TOKEN
        }

        self.empty_header = {}

    ##################################################################################################################
    ## last_contact_check
    ##################################################################################################################
    def test_get_last_contact_check_returns_accepted_status(self):
        request_parameters = {}
        uri = build_uri('monitor-devices')
        response = self.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertEqual(response.status, '202 Accepted')
        self.assertEqual(response.status_int, 202)

    def test_get_last_contact_check_with_no_authorization_header_returns_forbidden(self):
        request_parameters = {}
        uri = build_uri('monitor-devices')
        response = self.get(uri, params=request_parameters, headers=self.empty_header)
        self.assertForbidden(response)

    # NOTE: This test can be used if deferred.defer is removed from device_heartbeat_status_sweep
    # def test_get_last_contact_check_toggles_up_to_false_when_threshold_met(self):
    #     request_parameters = {}
    #     uri = build_uri('monitor-devices')
    #     self.assertTrue(self.managed_device.up)
    #     elapsed_seconds = config.PLAYER_UNRESPONSIVE_SECONDS_THRESHOLD + 1
    #     self.managed_device.heartbeat_updated = datetime.utcnow() - timedelta(seconds=elapsed_seconds)
    #     self.managed_device.put()
    #     self.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
    #     self.assertFalse(self.managed_device.up)

    def test_get_last_contact_check_does_not_toggle_up_when_threshold_not_met(self):
        request_parameters = {}
        uri = build_uri('monitor-devices')
        self.assertTrue(self.managed_device.up)
        elapsed_seconds = config.PLAYER_UNRESPONSIVE_SECONDS_THRESHOLD - 1
        self.managed_device.heartbeat_updated = datetime.utcnow() - timedelta(seconds=elapsed_seconds)
        self.managed_device.put()
        self.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        self.assertTrue(self.managed_device.up)
