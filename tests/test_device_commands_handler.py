from env_setup import setup_test_paths
from handlers.device_commands_handler import DeviceCommandsHandler

setup_test_paths()

import json
from agar.test import BaseTest, WebTest
from app_config import config
from models import ChromeOsDevice, Tenant, Distributor, Domain
from routes import application
import device_message_processor
from mockito import when, any as any_matcher
from webtest import AppError


class TestDeviceCommandsHandler(BaseTest, WebTest):
    APPLICATION = application
    NAME = 'foobar tenant'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://skykit-contentmanager-int.appspot.com/content'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    TENANT_CODE = 'foobar'
    DEVICE_ID = '4f099e50-6028-422b-85d2-3a629a45bf38'
    GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
    MAC_ADDRESS = '54271e619346'
    DISTRIBUTOR_NAME = 'agosto'
    IMPERSONATION_EMAIL = 'test@test.com'
    DEVICE_URLSAFE_KEY = 'asdkalskdfjalksdj'

    def setUp(self):
        super(TestDeviceCommandsHandler, self).setUp()
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
                                              active=True)
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
        self.chrome_os_device = ChromeOsDevice.create_managed(tenant_key=self.tenant_key,
                                                      device_id=self.DEVICE_ID,
                                                      gcm_registration_id=self.GCM_REGISTRATION_ID,
                                                      mac_address=self.MAC_ADDRESS)
        self.chrome_os_device_key = self.chrome_os_device.put()
        self.valid_authorization_header = {
            'Authorization': config.API_TOKEN
        }
        self.bad_authorization_header = {}
        self.some_intent = 'https://skykit-display-int.appspot.com/40289e504f09422c85d23a629a45be3d'
        self.post_uri = application.router.build(None,
                                                 'device-commands',
                                                 None,
                                                 {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})

    ##################################################################################################################
    # post
    ##################################################################################################################

    def test_post_intent_returns_ok_status(self):
        request_body = {'intent': self.some_intent}
        when(device_message_processor).change_intent(any_matcher(str), any_matcher(str), any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        response = self.app.post(self.post_uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_post_no_authorization_header_returns_forbidden(self):
        request_body = {'intent': self.some_intent}
        with self.assertRaises(AppError) as context:
            self.app.post(self.post_uri, json.dumps(request_body), headers=self.bad_authorization_header)
        self.assertTrue('403 Forbidden' in context.exception.message)

    def test_post_none_intent_returns_bad_request(self):
        request_body = {}
        with self.assertRaises(AppError) as context:
            self.app.post(self.post_uri, json.dumps(request_body), headers=self.valid_authorization_header)
        message = '400 DeviceCommandsHandler.post: Invalid intent.'
        self.assertTrue(message in context.exception.message)

    def test_post_empty_string_intent_returns_bad_request(self):
        request_body = {'intent': ''}
        with self.assertRaises(AppError) as context:
            self.app.post(self.post_uri, json.dumps(request_body), headers=self.valid_authorization_header)
        message = '400 DeviceCommandsHandler.post: Invalid intent.'
        self.assertTrue(message in context.exception.message)

    def test_post_wrong_payload_returns_bad_request(self):
        request_body = {'wrong_intent': self.some_intent}
        with self.assertRaises(AppError) as context:
            self.app.post(self.post_uri, json.dumps(request_body), headers=self.valid_authorization_header)
        message = '400 DeviceCommandsHandler.post: Invalid intent.'
        self.assertTrue(message in context.exception.message)

    def test_post_bogus_key_returns_not_found(self):
        request_body = {'intent': self.some_intent}
        bogus_key = 'bogus key'
        uri = application.router.build(None,
                                       'device-commands',
                                       None,
                                       {'device_urlsafe_key': bogus_key})
        with self.assertRaises(AppError) as context:
            self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        message = 'Bad response: 404 post command not executed because device not found with key: {0}'.format(
            bogus_key
        )
        self.assertTrue(message in context.exception.message)

    ##################################################################################################################
    # reset
    ##################################################################################################################

    def test_reset_returns_ok_status(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_RESET_COMMAND, any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        uri = application.router.build(None,
                                       'device-reset-command',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {}
        response = self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_reset_with_bogus_device_key_returns_not_found_status(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_RESET_COMMAND, any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        bogus_key = '0AXC19Z0DE'
        uri = application.router.build(None,
                                       'device-reset-command',
                                       None,
                                       {'device_urlsafe_key': bogus_key})
        request_body = {}
        with self.assertRaises(AppError) as context:
            self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        message = 'Bad response: 404 reset command not executed because device not found with key: {0}'.format(
            bogus_key
        )
        self.assertTrue(message in context.exception.message)

    ##################################################################################################################
    # delete_content
    ##################################################################################################################

    def test_delete_content_returns_ok_status(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_DELETE_CONTENT_COMMAND, any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        uri = application.router.build(None,
                                       'device-delete-content-command',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {}
        response = self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_delete_content_with_bogus_device_key_returns_not_found_status(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_DELETE_CONTENT_COMMAND, any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        bogus_key = '0AXC19Z0DE'
        uri = application.router.build(None,
                                       'device-delete-content-command',
                                       None,
                                       {'device_urlsafe_key': bogus_key})
        request_body = {}
        with self.assertRaises(AppError) as context:
            self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)

        message = 'Bad response: 404 content_delete command not executed because device not found with key: {0}'.format(
            bogus_key
        )
        self.assertTrue(message in context.exception.message)


    ##################################################################################################################
    # content_update
    ##################################################################################################################

    def test_content_update_returns_ok_status(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_UPDATE_CONTENT_COMMAND, any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        uri = application.router.build(None,
                                       'device-update-content-command',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {}
        response = self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_content_update_with_bogus_device_key_returns_not_found_status(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_DELETE_CONTENT_COMMAND, any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        bogus_key = '0AXC19Z0DE'
        uri = application.router.build(None,
                                       'device-update-content-command',
                                       None,
                                       {'device_urlsafe_key': bogus_key})
        request_body = {}
        with self.assertRaises(AppError) as context:
            self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)

        message = 'Bad response: 404 content_update command not executed because device not found with key: {0}'.format(
            bogus_key
        )
        self.assertTrue(message in context.exception.message)

    ##################################################################################################################
    # volume
    ##################################################################################################################

    def test_volume_returns_ok_status(self):
        when(device_message_processor).change_intent(any_matcher(str), any_matcher(str), any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        uri = application.router.build(None,
                                       'device-volume-command',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {'volume': 5}
        response = self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertOK(response)
        request_body = {'volume': '5'}
        response = self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_volume_returns_bad_request_status_with_below_range_volume(self):
        when(device_message_processor).change_intent(any_matcher(str), any_matcher(str), any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        uri = application.router.build(None,
                                       'device-volume-command',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {'volume': 0}
        with self.assertRaises(AppError) as context:
            self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        message = 'DeviceCommandsHandler.volume: Invalid volume.'
        self.assertTrue(message in context.exception.message)

    def test_volume_returns_bad_request_status_with_above_range_volume(self):
        when(device_message_processor).change_intent(any_matcher(str), any_matcher(str), any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        uri = application.router.build(None,
                                       'device-volume-command',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {'volume': 101}
        with self.assertRaises(AppError) as context:
            self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        message = 'DeviceCommandsHandler.volume: Invalid volume.'
        self.assertTrue(message in context.exception.message)

    def test_volume_returns_bad_request_status_with_volume_none(self):
        when(device_message_processor).change_intent(any_matcher(str), any_matcher(str), any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        uri = application.router.build(None,
                                       'device-volume-command',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {'volume': None}
        with self.assertRaises(AppError) as context:
            self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        message = 'DeviceCommandsHandler.volume: Invalid volume.'
        self.assertTrue(message in context.exception.message)

    def test_volume_with_bogus_device_key_returns_not_found_status(self):
        when(device_message_processor).change_intent(any_matcher(str), any_matcher(str), any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        bogus_key = '0AXC19Z0DE'
        uri = application.router.build(None,
                                       'device-volume-command',
                                       None,
                                       {'device_urlsafe_key': bogus_key})
        request_body = {'volume': 5}
        with self.assertRaises(AppError) as context:
            self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        message = 'Bad response: 404 volume command not executed because device not found with key: {0}'.format(
            bogus_key
        )
        self.assertTrue(message in context.exception.message)

    ##################################################################################################################
    # device custom command
    ##################################################################################################################

    def test_custom_command_returns_ok_status(self):
        when(device_message_processor).change_intent(any_matcher(str), any_matcher(str), any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        uri = application.router.build(None,
                                       'device-custom-command',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {'command': 'skykit.com/skdchromeapp/update/content'}
        response = self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_custom_returns_bad_request_status_with_command_none(self):
        when(device_message_processor).change_intent(any_matcher(str), any_matcher(str), any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        uri = application.router.build(None,
                                       'device-custom-command',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {'command': None}
        with self.assertRaises(AppError) as context:
            self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertTrue('400 DeviceCommandsHandler: Invalid command.' in context.exception.message)

    def test_custom_command_with_bogus_device_key_returns_not_found_status(self):
        when(device_message_processor).change_intent(any_matcher(str), any_matcher(str), any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        bogus_key = '0AXC19Z0DE'
        uri = application.router.build(None,
                                       'device-custom-command',
                                       None,
                                       {'device_urlsafe_key': bogus_key})
        request_body = {'command': 'skykit.com/skdchromeapp/update/content'}
        with self.assertRaises(AppError) as context:
            self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        message = 'Bad response: 404 custom command not executed because device not found with key: {0}'.format(
            bogus_key
        )
        self.assertTrue(message in context.exception.message)

    ##################################################################################################################
    # power_on
    ##################################################################################################################

    def test_power_on_returns_ok_status(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_POWER_ON_COMMAND, any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        uri = application.router.build(None,
                                       'device-power-on-command',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {}
        response = self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_power_on_with_bogus_device_key_returns_not_found_status(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_POWER_ON_COMMAND, any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        bogus_key = '0AXC19Z0DE'
        uri = application.router.build(None,
                                       'device-power-on-command',
                                       None,
                                       {'device_urlsafe_key': bogus_key})
        request_body = {}
        with self.assertRaises(AppError) as context:
            self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        message = 'Bad response: 404 power_on command not executed because device not found with key: {0}'.format(
            bogus_key
        )
        self.assertTrue(message in context.exception.message)

    ##################################################################################################################
    # power_off
    ##################################################################################################################

    def test_power_off_returns_ok_status(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_POWER_OFF_COMMAND, any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        uri = application.router.build(None,
                                       'device-power-off-command',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {}
        response = self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_power_off_with_bogus_device_key_returns_not_found_status(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_POWER_OFF_COMMAND, any_matcher(str),
                                                     any_matcher(str)).thenReturn(None)
        bogus_key = '0AXC19Z0DE'
        uri = application.router.build(None,
                                       'device-power-off-command',
                                       None,
                                       {'device_urlsafe_key': bogus_key})
        request_body = {}
        with self.assertRaises(AppError) as context:
            self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        message = 'Bad response: 404 power_off command not executed because device not found with key: {0}'.format(
            bogus_key
        )
        self.assertTrue(message in context.exception.message)

    ##################################################################################################################
    # refresh_device_representation
    ##################################################################################################################

    def test_refresh_device_representation_returns_ok_status(self):
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                                                     any_matcher(str), any_matcher(str)).thenReturn(None)
        uri = application.router.build(None,
                                       'refresh-device-representation-command',
                                       None,
                                       {'device_urlsafe_key': self.chrome_os_device_key.urlsafe()})
        request_body = {}
        response = self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_refresh_device_representation_with_bogus_device_key_returns_not_found_status(self):
        command = 'refresh_device_representation'
        when(device_message_processor).change_intent(self.chrome_os_device.gcm_registration_id,
                                                     config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                                                     any_matcher(str), any_matcher(str)).thenReturn(None)
        bogus_key = '0AXC19Z0DE'
        uri = application.router.build(None,
                                       'refresh-device-representation-command',
                                       None,
                                       {'device_urlsafe_key': bogus_key})
        request_body = {}
        with self.assertRaises(AppError) as context:
            self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        message = 'Bad response: 404 {0} command not executed because device not found with key: {1}'.format(
            command, bogus_key
        )
        self.assertTrue(message in context.exception.message)

    ##################################################################################################################
    # resolve_device
    ##################################################################################################################

    def test_resolve_device_with_valid_device_key_returns_ok(self):
        status, message, device = DeviceCommandsHandler.resolve_device(self.chrome_os_device_key.urlsafe())
        self.assertEqual(status, 200)
        self.assertEqual(message, 'OK')
        self.assertEqual(device, self.chrome_os_device)

    def test_resolve_device_with_invalid_device_key_returns_not_found(self):
        bogus_key = 'ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyGwsSDkNocm9tZU9zRGV2aWNlGICAgIDepYUKDA'
        status, message, device = DeviceCommandsHandler.resolve_device(bogus_key)
        expected_error_message = 'test_resolve_device_with_invalid_device_key_returns_not_found ' \
                                 'command not executed because device not found with key: {0}'.format(bogus_key)
        self.assertEqual(status, 404)
        self.assertEqual(message, expected_error_message)
        self.assertIsNone(device)
