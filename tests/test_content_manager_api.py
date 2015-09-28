import logging

from env_setup import setup_test_paths

setup_test_paths()

from http_client import HttpClient, HttpClientRequest, HttpClientResponse
from models import Tenant, ChromeOsDevice, Distributor, Domain
from agar.test import BaseTest
from content_manager_api import ContentManagerApi

from mockito import when, any as any_matcher

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>, Christopher Bartling <chris.bartling@agosto.com>'


class TestContentManagerApi(BaseTest):
    NAME = 'foobar tenant'
    ADMIN_EMAIL = 'foo@bar.com'
    CONTENT_SERVER_URL = 'https://skykit-contentmanager-int.appspot.com/content'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
    CONTENT_SERVER_API_KEY = 'API KEY'
    CHROME_DEVICE_DOMAIN = 'bar.com'
    TENANT_CODE = 'foobar'
    DISTRIBUTOR_NAME = 'agosto'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    IMPERSONATION_EMAIL = 'test@test.com'

    def setUp(self):
        super(TestContentManagerApi, self).setUp()
        self.content_manager_api = ContentManagerApi()
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
        self.device = ChromeOsDevice.create(tenant_key=self.tenant_key,
                                            device_id='f7ds8970dfasd8f70ad987',
                                            gcm_registration_id='fad7f890ad7f8ad0s7fa8s',
                                            mac_address='54271e619346')
        self.device_key = self.device.put()

    ##################################################################################################################
    ## create_tenant
    ##################################################################################################################

    def test_create_tenant_success(self):
        when(HttpClient).post(any_matcher(HttpClientRequest)).thenReturn(HttpClientResponse(status_code=201))
        result = self.content_manager_api.create_tenant(tenant=self.tenant)
        self.assertTrue(result)

    def test_unsuccessful_create_tenant_raises_error(self):
        error_code = 400
        when(HttpClient).post(any_matcher(HttpClientRequest)).thenReturn(HttpClientResponse(status_code=error_code))
        with self.assertRaises(RuntimeError) as context:
            self.content_manager_api.create_tenant(tenant=self.tenant)
        error_message = 'Unable to create tenant {0} in Content Manager. Status code: {1}'.format(
            self.NAME, error_code)
        self.assertEqual(error_message, str(context.exception))

    ##################################################################################################################
    ## create_device
    ##################################################################################################################

    def test_create_device_success(self):
        when(HttpClient).post(any_matcher(HttpClientRequest)).thenReturn(HttpClientResponse(status_code=201))
        result = self.content_manager_api.create_device(device_urlsafe_key=self.device_key.urlsafe())
        self.assertTrue(result)

    def test_unsuccessful_create_device_raises_error(self):
        error_code = 400
        when(HttpClient).post(any_matcher(HttpClientRequest)).thenReturn(HttpClientResponse(status_code=error_code))
        with self.assertRaises(RuntimeError) as context:
            self.content_manager_api.create_device(device_urlsafe_key=self.device_key.urlsafe())
        error_message = 'Unable to create device in Content Manager with tenant code {0}. Status code: {1}, ' \
                        'url={2}/provisioning/v1/displays'.format(self.TENANT_CODE, error_code,
                                                                  self.CONTENT_MANAGER_BASE_URL)
        self.assertEqual(error_message, str(context.exception))

    def test_create_device_without_tenant_key_raises_error(self):
        when(logging).error(any_matcher()).thenReturn('')
        tenant_less_device = ChromeOsDevice.create(tenant_key=None,
                                                   device_id='f7ds8970dfasd8f70ad987',
                                                   gcm_registration_id='fad7f890ad7f8ad0s7fa8s',
                                                   mac_address='54271e619346')
        tenant_less_device_key = tenant_less_device.put()
        with self.assertRaises(RuntimeError) as context:
            self.content_manager_api.create_device(device_urlsafe_key=tenant_less_device_key.urlsafe())
        error_message = 'No tenant_key for device'
        self.assertEqual(error_message, str(context.exception))

    ##################################################################################################################
    ## update_device
    ##################################################################################################################
    def test_update_device_success(self):
        when(self.content_manager_api).delete_device(any_matcher()).thenReturn(True)
        when(HttpClient).post(any_matcher(HttpClientRequest)).thenReturn(HttpClientResponse(status_code=201))
        result = self.content_manager_api.update_device(device_urlsafe_key=self.device_key.urlsafe())
        self.assertTrue(result)

    def test_update_device_throws_error_when_delete_fails(self):
        when(self.content_manager_api).delete_device(any_matcher()).thenReturn(False)
        when(logging).error(any_matcher()).thenReturn('')
        with self.assertRaises(RuntimeError) as context:
            self.content_manager_api.update_device(device_urlsafe_key=self.device_key.urlsafe())
        error_message = 'update_device failed deleting device in Content Manager. device_key={0}'.format(
            self.device.key.urlsafe())
        self.assertTrue(error_message in context.exception.message)

    ##################################################################################################################
    ## delete_device
    ##################################################################################################################
    def test_delete_device_success(self):
        when(HttpClient).delete(any_matcher(HttpClientRequest)).thenReturn(HttpClientResponse(status_code=204))
        result = self.content_manager_api.delete_device(device_urlsafe_key=self.device_key.urlsafe())
        self.assertTrue(result)

    def test_delete_device_failure(self):
        when(HttpClient).delete(any_matcher(HttpClientRequest)).thenReturn(HttpClientResponse(status_code=400))
        when(logging).error(any_matcher()).thenReturn('')
        result = self.content_manager_api.delete_device(device_urlsafe_key=self.device_key.urlsafe())
        self.assertFalse(result)
