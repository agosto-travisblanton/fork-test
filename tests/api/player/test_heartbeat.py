import httplib
import json

from google.appengine.ext import ndb

import device_message_processor
from env_setup import setup_test_paths
from mockito import when, any as any_matcher
from model_entities.chrome_os_device_model_and_overlays import DeviceIssueLog
from utils.timezone_util import TimezoneUtil

setup_test_paths()

from agar.test import BaseTest, WebTest
from app_config import config
from models import ChromeOsDevice, Tenant, Distributor, Domain
from routes import application
from utils.web_util import build_uri


class TestHeartbeat(BaseTest, WebTest):
    APPLICATION = application
    ADMIN_EMAIL = 'foo@bar.com'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    CONTENT_SERVER_URL = 'https://skykit-contentmanager-int.appspot.com/content'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
    GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
    MAC_ADDRESS = '54271e619346'
    ETHERNET_MAC_ADDRESS = '8e271e619346'
    TENANT_CODE = 'foobar_inc'
    TENANT_NAME = 'Foobar, Inc,'
    DISTRIBUTOR_NAME = 'agosto'
    IMPERSONATION_EMAIL = 'test@test.com'
    STORAGE_UTILIZATION = 26
    MEMORY_UTILIZATION = 63
    PROGRAM = 'some program'
    PROGRAM_ID = 'ID-512341234'
    PLAYLIST = 'some playlist'
    PLAYLIST_ID = 'Playlist Id'
    CONTENT_KIND = 'Video'
    CONTENT_NAME = 'Video 101'
    CONTENT_ID = 'V101'
    PLAYLIST_ID = 'Playlist Id'
    LAST_ERROR = 'Some error'

    def setUp(self):
        super(TestHeartbeat, self).setUp()
        self.valid_authorization_header = {
            'Authorization': config.API_TOKEN
        }
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
            mac_address=self.MAC_ADDRESS)
        self.managed_device_key = self.managed_device.put()
        self.api_token_authorization_header = {
            'Authorization': config.API_TOKEN
        }
        self.unmanaged_api_token_authorization_header = {
            'Authorization': config.UNMANAGED_API_TOKEN
        }
        self.empty_header = {}
        self.uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': self.managed_device_key.urlsafe()})

    ##################################################################################################################
    # PUT /api/v1/devices/<device_urlsafe_key>/heartbeat
    ##################################################################################################################

    def test_heartbeat_no_api_token_returns_forbidden_status(self):
        request_body = {'storage': self.STORAGE_UTILIZATION, 'memory': self.MEMORY_UTILIZATION}
        response = self.put(self.uri, params=request_body, headers=self.empty_header)
        self.assertForbidden(response)
        response_body = json.loads(response.body)
        self.assertEqual(response_body['error'], 'No API token supplied in the HTTP request.')

    def test_heartbeat_returns_no_content_status(self):
        request_body = {'storage': self.STORAGE_UTILIZATION, 'memory': self.MEMORY_UTILIZATION}
        response = self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        self.assertEqual(httplib.NO_CONTENT, response.status_int)

    def test_heartbeat_returns_not_found_status_for_archived_device(self):
        self.__initialize_heartbeat_info()
        self.managed_device.archived = True
        self.managed_device.put()
        request_body = {}
        response = self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        self.assertEqual('404 Device with key: {0} archived.'.format(self.managed_device_key.urlsafe()),
                         response.status)

    def test_heartbeat_updates_storage_utilization(self):
        self.__initialize_heartbeat_info()
        reduced_storage = self.STORAGE_UTILIZATION - 5
        request_body = {'storage': reduced_storage}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        updated_heartbeat = self.managed_device_key.get()
        self.assertNotEqual(updated_heartbeat.storage_utilization, self.STORAGE_UTILIZATION)

    def test_heartbeat_updates_memory_utilization(self):
        self.__initialize_heartbeat_info()
        reduced_memory = self.MEMORY_UTILIZATION - 5
        request_body = {'memory': reduced_memory}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        updated_heartbeat = self.managed_device_key.get()
        self.assertNotEqual(updated_heartbeat.memory_utilization, self.MEMORY_UTILIZATION)

    def test_heartbeat_updates_content(self):
        self.__initialize_heartbeat_info()
        request_body = {'contentKind': 'animated gif', 'contentName': 'spinner', 'contentId': 'SP1'}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        updated_heartbeat = self.managed_device_key.get()
        self.assertNotEqual(updated_heartbeat.content_kind, self.CONTENT_KIND)
        self.assertNotEqual(updated_heartbeat.content_name, self.CONTENT_NAME)
        self.assertNotEqual(updated_heartbeat.content_id, self.CONTENT_ID)

    def test_heartbeat_updates_last_error(self):
        self.__initialize_heartbeat_info()
        request_body = {'lastError': 'Houston, we have a problem'}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        updated_heartbeat = self.managed_device_key.get()
        self.assertNotEqual(updated_heartbeat.last_error, self.LAST_ERROR)

    def test_heartbeat_cannot_update_up_status(self):
        self.__initialize_heartbeat_info()
        request_body = {'storage': self.STORAGE_UTILIZATION, 'memory': self.MEMORY_UTILIZATION}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        updated_heartbeat = self.managed_device_key.get()
        self.assertEqual(updated_heartbeat.up, updated_heartbeat.up)

    def test_heartbeat_updates_heartbeat_timestamp(self):
        self.__initialize_heartbeat_info()
        original_heartbeat_timestamp = self.managed_device.heartbeat_updated
        self.assertIsNotNone(original_heartbeat_timestamp)
        request_body = {'storage': self.STORAGE_UTILIZATION, 'memory': self.MEMORY_UTILIZATION}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        device = self.managed_device_key.get()
        self.assertGreater(device.heartbeat_updated, original_heartbeat_timestamp)

    def test_heartbeat_populates_device_connection_type_for_ethernet_mac_address(self):
        self.managed_device.ethernet_mac_address = self.ETHERNET_MAC_ADDRESS
        self.managed_device.put()
        request_body = {'macAddress': self.ETHERNET_MAC_ADDRESS}
        self.assertIsNone(self.managed_device.connection_type)
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        self.assertIsNotNone(self.managed_device.connection_type)
        self.assertEqual(self.managed_device.connection_type, config.ETHERNET_CONNECTION)

    def test_heartbeat_populates_device_connection_type_for_wifi_mac_address(self):
        self.managed_device.mac_address = self.MAC_ADDRESS
        self.managed_device.put()
        request_body = {'macAddress': self.MAC_ADDRESS}
        self.assertIsNone(self.managed_device.connection_type)
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        self.assertIsNotNone(self.managed_device.connection_type)
        self.assertEqual(self.managed_device.connection_type, config.WIFI_CONNECTION)

    def test_heartbeat_does_not_populate_device_connection_type_for_unrecognized_mac_address(self):
        request_body = {'macAddress': '22234234234'}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        self.assertIsNone(self.managed_device.connection_type)

    ##################################################################################################################
    # Changes recorded to DeviceIssueLog
    ##################################################################################################################

    def test_heartbeat_timezone_change_creates_timezone_change_event(self):
        self.__initialize_heartbeat_info()
        self.managed_device.timezone = 'America/Denver'
        self.managed_device.put()
        request_body = {'timezone': 'America/Boise'}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        log_entry = DeviceIssueLog.query(DeviceIssueLog.device_key == self.managed_device_key,
                                         ndb.AND(
                                             DeviceIssueLog.category ==
                                             config.DEVICE_ISSUE_TIMEZONE_CHANGE)).get()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.category, config.DEVICE_ISSUE_TIMEZONE_CHANGE)

    def test_heartbeat_timezone_offset_change_creates_timezone_offset_change_event(self):
        self.__initialize_heartbeat_info()
        self.managed_device.timezone = config.DEFAULT_TIMEZONE
        self.managed_device.put()
        request_body = {'timezone': config.DEFAULT_TIMEZONE,
                        'timezoneOffset': TimezoneUtil.get_timezone_offset(config.DEFAULT_TIMEZONE) + 3}
        when(device_message_processor).change_intent(
            any_matcher(), config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND).thenReturn(None)
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        log_entry = DeviceIssueLog.query(DeviceIssueLog.device_key == self.managed_device_key,
                                         ndb.AND(
                                             DeviceIssueLog.category ==
                                             config.DEVICE_ISSUE_TIMEZONE_OFFSET_CHANGE)).get()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.category, config.DEVICE_ISSUE_TIMEZONE_OFFSET_CHANGE)

    def test_heartbeat_playlist_change_creates_playlist_change_event(self):
        self.__initialize_heartbeat_info()
        request_body = {'playlist': 'Tuesday Playlist'}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        issues = DeviceIssueLog.get_all_by_device_key(self.managed_device.key)
        self.assertEqual(issues[1].category, config.DEVICE_ISSUE_PLAYLIST_CHANGE)

    def test_heartbeat_program_change_creates_program_change_event(self):
        self.__initialize_heartbeat_info()
        request_body = {'program': 'Tuesday Program'}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        issues = DeviceIssueLog.get_all_by_device_key(self.managed_device.key)
        self.assertEqual(issues[1].category, config.DEVICE_ISSUE_PROGRAM_CHANGE)

    def test_heartbeat_content_change_creates_content_change_event(self):
        self.__initialize_heartbeat_info()
        request_body = {'contentKind': 'Video', 'contentName': 'Programming 101', 'contentId': 'Pro-101'}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        issues = DeviceIssueLog.get_all_by_device_key(self.managed_device.key)
        self.assertEqual(issues[1].category, config.DEVICE_ISSUE_CONTENT_CHANGE)
        self.assertEqual(issues[1].content_kind, 'Video')
        self.assertEqual(issues[1].content_name, 'Programming 101')
        self.assertEqual(issues[1].content_id, 'Pro-101')

    def test_heartbeat_invokes_a_device_issue_log_up_toggle_if_device_was_previously_down(self):
        self.__initialize_heartbeat_info(up=False)
        issues = DeviceIssueLog.get_all_by_device_key(self.managed_device.key)
        self.assertLength(0, issues)
        request_body = {'storage': self.STORAGE_UTILIZATION, 'memory': self.MEMORY_UTILIZATION}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        issues = DeviceIssueLog.get_all_by_device_key(self.managed_device.key)
        self.assertLength(2, issues)
        self.assertEqual(issues[0].category, config.DEVICE_ISSUE_FIRST_HEARTBEAT)
        self.assertTrue(issues[1].up)
        self.assertEqual(issues[1].category, config.DEVICE_ISSUE_PLAYER_UP)

    def test_heartbeat_invokes_a_device_issue_log_up_toggle_if_device_was_previously_down(self):
        self.__initialize_heartbeat_info(up=False)
        issues = DeviceIssueLog.get_all_by_device_key(self.managed_device.key)
        self.assertLength(0, issues)
        request_body = {'storage': self.STORAGE_UTILIZATION, 'memory': self.MEMORY_UTILIZATION}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        issues = DeviceIssueLog.get_all_by_device_key(self.managed_device.key)
        self.assertLength(2, issues)
        self.assertEqual(issues[0].category, config.DEVICE_ISSUE_FIRST_HEARTBEAT)
        self.assertTrue(issues[1].up)
        self.assertEqual(issues[1].category, config.DEVICE_ISSUE_PLAYER_UP)
        self.assertEqual(issues[1].storage_utilization, self.STORAGE_UTILIZATION)
        self.assertEqual(issues[1].memory_utilization, self.MEMORY_UTILIZATION)

    def test_heartbeat_resolves_previously_down_issue(self):
        self.managed_device.up = False
        self.managed_device.put()
        issue = DeviceIssueLog.create(device_key=self.managed_device_key,
                                      category=config.DEVICE_ISSUE_PLAYER_DOWN,
                                      up=False,
                                      storage_utilization=self.STORAGE_UTILIZATION,
                                      memory_utilization=self.MEMORY_UTILIZATION,
                                      resolved=False)
        issue.put()
        request_body = {'storage': self.STORAGE_UTILIZATION, 'memory': self.MEMORY_UTILIZATION}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        issues = DeviceIssueLog.get_all_by_device_key(self.managed_device_key)
        self.assertLength(2, issues)
        self.assertEqual(issues[0].category, config.DEVICE_ISSUE_PLAYER_DOWN)
        self.assertEqual(issues[1].category, config.DEVICE_ISSUE_PLAYER_UP)
        self.assertTrue(issues[0].resolved)
        self.assertTrue(issues[1].resolved)
        self.assertIsNotNone(issues[0].resolved_datetime)
        self.assertIsNotNone(issues[1].resolved_datetime)

    def test_heartbeat_can_resolve_previous_memory_issues(self):
        issue = DeviceIssueLog.create(device_key=self.managed_device_key,
                                      category=config.DEVICE_ISSUE_MEMORY_HIGH,
                                      up=True,
                                      storage_utilization=self.STORAGE_UTILIZATION,
                                      memory_utilization=config.MEMORY_UTILIZATION_THRESHOLD + 1,
                                      resolved=False)
        issue.put()
        request_body = {'storage': self.STORAGE_UTILIZATION, 'memory': self.MEMORY_UTILIZATION}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        issues = DeviceIssueLog.get_all_by_device_key(self.managed_device_key)
        self.assertLength(2, issues)
        self.assertEqual(issues[0].category, config.DEVICE_ISSUE_MEMORY_HIGH)
        self.assertEqual(issues[1].category, config.DEVICE_ISSUE_MEMORY_NORMAL)
        self.assertTrue(issues[0].resolved)
        self.assertTrue(issues[1].resolved)
        self.assertIsNotNone(issues[0].resolved_datetime)
        self.assertIsNotNone(issues[1].resolved_datetime)

    def test_heartbeat_can_resolve_previous_storage_issues(self):
        issue = DeviceIssueLog.create(device_key=self.managed_device_key,
                                      category=config.DEVICE_ISSUE_STORAGE_LOW,
                                      up=True,
                                      storage_utilization=config.STORAGE_UTILIZATION_THRESHOLD + 1,
                                      memory_utilization=self.MEMORY_UTILIZATION,
                                      resolved=False)
        issue.put()
        request_body = {'storage': self.STORAGE_UTILIZATION, 'memory': self.MEMORY_UTILIZATION}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        issues = DeviceIssueLog.get_all_by_device_key(self.managed_device_key)
        self.assertLength(2, issues)
        self.assertEqual(issues[0].category, config.DEVICE_ISSUE_STORAGE_LOW)
        self.assertEqual(issues[1].category, config.DEVICE_ISSUE_STORAGE_NORMAL)
        self.assertTrue(issues[0].resolved)
        self.assertTrue(issues[1].resolved)
        self.assertIsNotNone(issues[0].resolved_datetime)
        self.assertIsNotNone(issues[1].resolved_datetime)

    def test_heartbeat_records_first_heartbeat_for_new_device(self):
        device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            mac_address='2313412341230')
        device_key = device.put()
        request_body = {'storage': self.STORAGE_UTILIZATION, 'memory': self.MEMORY_UTILIZATION}
        uri = build_uri('device-heartbeat', params_dict={'device_urlsafe_key': device_key.urlsafe()})
        self.put(uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        log_entry = DeviceIssueLog.query(DeviceIssueLog.device_key == device_key,
                                         ndb.AND(DeviceIssueLog.category == config.DEVICE_ISSUE_FIRST_HEARTBEAT),
                                         ndb.AND(DeviceIssueLog.storage_utilization == self.STORAGE_UTILIZATION),
                                         ndb.AND(DeviceIssueLog.memory_utilization == self.MEMORY_UTILIZATION),
                                         ndb.AND(DeviceIssueLog.up == True),
                                         ndb.AND(DeviceIssueLog.resolved == True)).get()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.category, config.DEVICE_ISSUE_FIRST_HEARTBEAT)

    def test_heartbeat_records_os_change(self):
        self.__initialize_heartbeat_info()
        self.managed_device.os = 'Windows 10'
        self.managed_device.put()
        request_body = {'os': 'Linux'}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        log_entry = DeviceIssueLog.query(DeviceIssueLog.device_key == self.managed_device_key,
                                         ndb.AND(DeviceIssueLog.category == config.DEVICE_ISSUE_OS_CHANGE)).get()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.category, config.DEVICE_ISSUE_OS_CHANGE)

    def test_heartbeat_records_os_version_change(self):
        self.__initialize_heartbeat_info()
        self.managed_device.os_version = '8.3'
        self.managed_device.put()
        request_body = {'osVersion': '10.0'}
        self.put(self.uri, params=json.dumps(request_body), headers=self.api_token_authorization_header)
        log_entry = DeviceIssueLog.query(DeviceIssueLog.device_key == self.managed_device_key,
                                         ndb.AND(
                                             DeviceIssueLog.category == config.DEVICE_ISSUE_OS_VERSION_CHANGE)).get()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.category, config.DEVICE_ISSUE_OS_VERSION_CHANGE)

    def __initialize_heartbeat_info(self, up=True):
        self.managed_device.storage_utilization = self.STORAGE_UTILIZATION
        self.managed_device.memory_utilization = self.MEMORY_UTILIZATION
        self.managed_device.program = self.PROGRAM
        self.managed_device.program_id = self.PROGRAM_ID
        self.managed_device.last_error = self.LAST_ERROR
        self.managed_device.playlist = self.PLAYLIST
        self.managed_device.playlist_id = self.PLAYLIST_ID
        self.managed_device.content_kind = self.CONTENT_KIND
        self.managed_device.content_name = self.CONTENT_NAME
        self.managed_device.content_id = self.CONTENT_ID
        self.managed_device.up = up
        self.managed_device.put()
