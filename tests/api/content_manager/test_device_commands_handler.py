from env_setup import setup_test_paths

setup_test_paths()

import json
from models import ChromeOsDevice, Tenant, Distributor, Domain
from routes import application
import device_message_processor
from mockito import when, any as any_matcher
from webtest import AppError
from tests.provisioning_distributor_user_base_test import ProvisioningDistributorUserBase


class TestDeviceCommandsHandler(ProvisioningDistributorUserBase):
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
        self.valid_authorization_header = self.JWT_DEFAULT_HEADER
        self.bad_authorization_header = {}
        self.some_intent = 'skykit.com/skdchromeapp/play/program/87c57d6bea0240fd8dee4d806059a92f'
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

    def test_post_corrupted_key_returns_invalid_urlsafe_string_error(self):
        request_body = {'intent': self.some_intent}
        corrupted_key = 'corrupted key'
        uri = application.router.build(None,
                                       'device-commands',
                                       None,
                                       {'device_urlsafe_key': corrupted_key})
        with self.assertRaises(AppError) as context:
            self.app.post(uri, json.dumps(request_body), headers=self.valid_authorization_header)
        message = 'Bad response: 400 Invalid urlsafe string (Protocol Buffer Decode Error): corrupted'
        self.assertTrue(message in context.exception.message)
