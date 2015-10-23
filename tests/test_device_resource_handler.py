from google.appengine.ext import ndb

from env_setup import setup_test_paths
from utils.web_util import build_uri

setup_test_paths()

import json
from webtest import AppError
from google.appengine.ext.deferred import deferred
from chrome_os_devices_api import (refresh_device, refresh_device_by_mac_address, update_chrome_os_device)
from agar.test import BaseTest, WebTest
from chrome_os_devices_api import ChromeOsDevicesApi
from mockito import when, any as any_matcher
from routes import application
from models import ChromeOsDevice, Tenant, Distributor, Domain, UnmanagedDevice
from app_config import config
from ae_test_data import build


class TestDeviceResourceHandler(BaseTest, WebTest):
    ADMIN_EMAIL = 'foo@bar.com'
    ANOTHER_TENANT_NAME = 'Another, Inc,'
    ANOTHER_TENANT_CODE = 'another_inc'
    ANOTHER_ADMIN_EMAIL = 'foo@another.com'
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
    DEVICE_NOTES = 'This is a device note'

    def setUp(self):
        super(TestDeviceResourceHandler, self).setUp()
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
        self.another_tenant = Tenant.create(tenant_code=self.ANOTHER_TENANT_CODE,
                                            name=self.ANOTHER_TENANT_NAME,
                                            admin_email=self.ANOTHER_ADMIN_EMAIL,
                                            content_server_url=self.CONTENT_SERVER_URL,
                                            content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                            domain_key=self.domain_key,
                                            active=True)
        self.another_tenant_key = self.another_tenant.put()
        self.unmanaged_device = UnmanagedDevice.create(self.GCM_REGISTRATION_ID, self.MAC_ADDRESS)
        self.unmanaged_device_key = self.unmanaged_device.put()
        self.device_key = build(ChromeOsDevice,
                                tenant_key=self.tenant_key,
                                gcm_registration_id=self.GCM_REGISTRATION_ID,
                                device_id=self.DEVICE_ID,
                                mac_address=self.MAC_ADDRESS).key
        self.valid_authorization_header = {
            'Authorization': config.API_TOKEN
        }
        self.valid_unmanaged_device_authorization_header = {
            'Authorization': config.LIMITED_UNMANAGED_DEVICE_REGISTRATION_API_TOKEN
        }

        self.invalid_authorization_header = {}

    #################################################################################################################
    # get_list
    #################################################################################################################

    def test_get_list_no_query_parameters_http_status_ok(self):
        request_parameters = {}
        uri = build_uri('devices-retrieval')
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_get_list_no_query_parameters_entity_body_json(self):
        self.__build_list_devices(tenant_key=self.tenant_key, number_to_build=20)
        request_parameters = {}
        uri = build_uri('devices-retrieval')
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        response_json = json.loads(response.body)
        # When pagination comes back from the dead...
        # self.assertLength(10, response_json['objects'])
        self.assertLength(21, response_json)

    def test_get_list_mac_address_query_parameters_http_status_ok(self):
        request_parameters = {'macAddress': self.MAC_ADDRESS}
        uri = build_uri('devices-retrieval')
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_get_list_mac_address_query_parameters_payload_single_resource(self):
        request_parameters = {'macAddress': self.MAC_ADDRESS}
        uri = build_uri('devices-retrieval')
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        response_json = json.loads(response.body)
        self.assertEqual(response_json['macAddress'], self.MAC_ADDRESS)
        device = self.device_key.get()
        self.assertEqual(response_json['gcmRegistrationId'], device.gcm_registration_id)
        self.assertEqual(response_json['deviceId'], device.device_id)

    ##################################################################################################################
    ## get_devices_by_tenant
    ##################################################################################################################

    def test_get_devices_by_tenant_http_status_ok(self):
        self.__build_list_devices(tenant_key=self.tenant_key, number_to_build=20)
        request_parameters = {}
        uri = application.router.build(None, 'devices-by-tenant', None,
                                       {'tenant_urlsafe_key': self.tenant_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_get_devices_by_tenant_entity_body_json(self):
        self.__build_list_devices(tenant_key=self.tenant_key, number_to_build=20)
        request_parameters = {}
        uri = application.router.build(None, 'devices-by-tenant', None,
                                       {'tenant_urlsafe_key': self.tenant_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        response_json = json.loads(response.body)
        self.assertLength(10, response_json['objects'])

    #################################################################################################################
    # get_devices_by_distributor
    #################################################################################################################

    def test_get_devices_by_distributor_http_status_ok(self):
        distributor = Distributor.create(name='Acme Brothers',
                                         active=True)
        distributor_key = distributor.put()
        self.__setup_distributor_with_two_tenants_with_n_devices(distributor_key,
                                                                 tenant_1_device_count=1,
                                                                 tenant_2_device_count=1)
        request_parameters = {}
        uri = application.router.build(None, 'devices-by-distributor', None,
                                       {'distributor_urlsafe_key': distributor_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_get_devices_by_distributor_returns_expected_device_count(self):
        distributor = Distributor.create(name='Acme Brothers',
                                         active=True)
        distributor_key = distributor.put()
        self.__setup_distributor_with_two_tenants_with_n_devices(distributor_key,
                                                                 tenant_1_device_count=13,
                                                                 tenant_2_device_count=6)
        request_parameters = {}
        uri = application.router.build(None, 'devices-by-distributor', None,
                                       {'distributor_urlsafe_key': distributor_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        response_json = json.loads(response.body)
        self.assertLength(19, response_json)

    ##################################################################################################################
    ## get ChromeOsDevice
    ##################################################################################################################
    def test_get_device_by_key_no_authorization_header_returns_forbidden(self):
        uri = build_uri('device', params_dict={'device_urlsafe_key': self.device_key.urlsafe()})
        response = self.get(uri, headers=self.invalid_authorization_header)
        self.assertForbidden(response)

    def test_get_device_by_key_http_status_ok(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': self.device_key.urlsafe()})
        when(deferred).defer(any_matcher(refresh_device),
                             any_matcher(self.device_key.urlsafe())).thenReturn(None)
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_get_device_by_key_returns_not_found_status_with_a_valid_key_not_found(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': self.device_key.urlsafe()})
        self.app.delete('/api/v1/devices/{0}'.format(self.device_key.urlsafe()),
                        json.dumps({}),
                        headers=self.valid_authorization_header)
        when(deferred).defer(any_matcher(refresh_device),
                             any_matcher(self.device_key.urlsafe())).thenReturn(None)
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        self.assertTrue('404 Not Found' in context.exception.message)

    def test_get_device_by_key_returns_bad_request_status_with_invalid_key(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': '0000ZXN0YmVkLXRlc3RyFAsSDkNocm9tZU9zRGV2aWNl0000'})
        when(deferred).defer(any_matcher(refresh_device),
                             any_matcher(self.device_key.urlsafe())).thenReturn(None)
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        self.assertTrue('400 Bad Request' in context.exception.message)

    def test_get_device_by_key_entity_body_json(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': self.device_key.urlsafe()})
        when(deferred).defer(any_matcher(refresh_device),
                             any_matcher(self.device_key.urlsafe())).thenReturn(None)
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        response_json = json.loads(response.body)
        device = self.device_key.get()
        tenant = device.tenant_key.get()
        self.assertEqual(response_json['annotatedUser'], device.annotated_user)
        self.assertEqual(response_json['annotatedLocation'], device.annotated_location)
        self.assertEqual(response_json['apiKey'], device.api_key)
        self.assertEqual(response_json['bootMode'], device.boot_mode)
        self.assertEqual(response_json['created'], device.created.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response_json['deviceId'], device.device_id)
        self.assertEqual(response_json['ethernetMacAddress'], device.ethernet_mac_address)
        self.assertEqual(response_json['firmwareVersion'], device.firmware_version)
        self.assertEqual(response_json['gcmRegistrationId'], device.gcm_registration_id)
        self.assertEqual(response_json['key'], device.key.urlsafe())
        self.assertEqual(response_json['kind'], device.kind)
        self.assertEqual(response_json['lastEnrollmentTime'], device.last_enrollment_time)
        self.assertEqual(response_json['lastSync'], device.last_sync)
        self.assertEqual(response_json['macAddress'], device.mac_address)
        self.assertEqual(response_json['model'], device.model)
        self.assertEqual(response_json['orgUnitPath'], device.org_unit_path)
        self.assertEqual(response_json['osVersion'], device.os_version)
        self.assertEqual(response_json['platformVersion'], device.platform_version)
        self.assertEqual(response_json['serialNumber'], device.serial_number)
        self.assertEqual(response_json['status'], device.status)
        self.assertEqual(response_json['updated'], device.updated.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response_json['tenantKey'], tenant.key.urlsafe())
        self.assertEqual(response_json['chromeDeviceDomain'], self.CHROME_DEVICE_DOMAIN)
        self.assertEqual(response_json['logglyLink'], 'https://skykit.loggly.com/search?&terms=tag%3A"{0}"'.format(
        device.serial_number))

    ##################################################################################################################
    ## get UnmanagedDevice
    ##################################################################################################################

    def test_get_unmanaged_device_by_key_http_status_ok(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.valid_unmanaged_device_authorization_header)
        self.assertOK(response)

    def test_get_unmanaged_device_by_key_returns_not_found_status_with_a_key_for_a_deleted_device(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': self.unmanaged_device_key.urlsafe()})
        self.app.delete('/api/v1/devices/{0}'.format(self.unmanaged_device_key.urlsafe()),
                        json.dumps({}),
                        headers=self.valid_unmanaged_device_authorization_header)
        with self.assertRaises(AppError) as context:
            self.app.get(uri, params=request_parameters, headers=self.valid_unmanaged_device_authorization_header)
        self.assertTrue('404 Not Found' in context.exception.message)



    ##################################################################################################################
    # post ChromeOsDevice
    ##################################################################################################################

    def test_device_resource_handler_post_no_authorization_header_returns_forbidden(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.TENANT_CODE}
        uri = build_uri('device-creator')
        response = self.post(uri, params=request_body, headers=self.invalid_authorization_header)
        self.assertForbidden(response)

    def test_device_resource_handler_post_no_returns_bad_response_if_mac_address_already_assigned_to_device(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.TENANT_CODE}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertTrue('Bad response: 400 Cannot create because macAddress has already been assigned to this device.'
                        in context.exception.message)

    def test_device_resource_handler_post_no_returns_bad_response_for_empty_tenant_code(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': None}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertTrue('Bad response: 400 Invalid or inactive tenant for device.'
                        in context.exception.message)

    def test_device_resource_handler_post_no_returns_bad_response_for_empty_gcm(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': None,
                        'tenantCode': self.TENANT_CODE}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertTrue('Bad response: 400 The gcmRegistrationId parameter is invalid.'
                        in context.exception.message)

    def test_device_resource_handler_post_no_returns_bad_response_for_empty_mac_address(self):
        request_body = {'macAddress': None,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.TENANT_CODE}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertTrue('Bad response: 400 The macAddress parameter is invalid.'
                        in context.exception.message)

    def test_post_http_status_created(self):
        tenant = self.tenant_key.get()
        mac_address = '7889BE879f'
        request_body = {'macAddress': mac_address,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': tenant.tenant_code}
        when(deferred).defer(any_matcher(refresh_device_by_mac_address),
                             any_matcher(str),
                             any_matcher(mac_address)).thenReturn(None)
        response = self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertEqual('201 Created', response.status)

    def test_post_device_key_location_header(self):
        tenant = self.tenant_key.get()
        mac_address = '7889BE879f'
        request_body = {'macAddress': mac_address,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': tenant.tenant_code}
        when(deferred).defer(any_matcher(refresh_device_by_mac_address),
                             any_matcher(str),
                             any_matcher(mac_address)).thenReturn(None)
        response = self.app.post('/api/v1/devices', json.dumps(request_body), headers=self.valid_authorization_header)
        location_uri_components = str(response.headers['Location']).split('/')
        self.assertEqual(location_uri_components[5], "devices")
        device = ndb.Key(urlsafe=location_uri_components[6]).get()
        self.assertIsNotNone(device)

    ##################################################################################################################
    # post UnmanagedDevice
    ##################################################################################################################

    def test_device_resource_handler_unmanaged_post_returns_bad_response_for_empty_gcm(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': None}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body),
                          headers=self.valid_unmanaged_device_authorization_header)
        self.assertTrue('Bad response: 400 The gcmRegistrationId parameter is invalid.'
                        in context.exception.message)

    def test_device_resource_handler_unmanaged_post_returns_bad_response_for_mac_address(self):
        request_body = {'macAddress': None,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID}
        with self.assertRaises(AppError) as context:
            self.app.post('/api/v1/devices', json.dumps(request_body),
                          headers=self.valid_unmanaged_device_authorization_header)
        self.assertTrue('Bad response: 400 The macAddress parameter is invalid.'
                        in context.exception.message)

    def test_device_resource_handler_unmanaged_post_returns_created_status_code(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID}
        response = self.app.post('/api/v1/devices', json.dumps(request_body),
                                 headers=self.valid_unmanaged_device_authorization_header)
        self.assertEqual(201, response.status_code)

    def test_device_resource_handler_unmanaged_post_device_key_location_header(self):
        request_body = {'macAddress': self.MAC_ADDRESS,
                        'gcmRegistrationId': self.GCM_REGISTRATION_ID}
        response = self.app.post('/api/v1/devices', json.dumps(request_body),
                                 headers=self.valid_unmanaged_device_authorization_header)
        location_uri_components = str(response.headers['Location']).split('/')
        self.assertEqual(location_uri_components[5], "devices")
        device = ndb.Key(urlsafe=location_uri_components[6]).get()
        self.assertIsNotNone(device)


    ##################################################################################################################
    ## put
    ##################################################################################################################

    def test_device_resource_put_no_authorization_header_returns_forbidden(self):
        request_body = {'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.TENANT_CODE,
                        'notes': self.DEVICE_NOTES}
        when(ChromeOsDevicesApi).get(any_matcher(), any_matcher()).thenReturn(self.device_key.get())
        uri = build_uri('device', params_dict={'device_urlsafe_key': self.device_key.urlsafe()})
        response = self.put(uri, params=request_body, headers=self.invalid_authorization_header)
        self.assertForbidden(response)

    def test_put_http_status_no_content(self):
        request_body = {'gcmRegistrationId': self.GCM_REGISTRATION_ID,
                        'tenantCode': self.tenant_key.get().tenant_code,
                        'notes': self.DEVICE_NOTES
                        }
        when(deferred).defer(any_matcher(update_chrome_os_device),
                             any_matcher(self.device_key.urlsafe())).thenReturn(None)
        response = self.app.put('/api/v1/devices/{0}'.format(self.device_key.urlsafe()),
                                json.dumps(request_body),
                                headers=self.valid_authorization_header)
        self.assertEqual('204 No Content', response.status)

    def test_put_updates_device_entity(self):
        gcm_registration_id = 'd23784972038845ab3963412'
        request_body = {
            'gcmRegistrationId': gcm_registration_id,
            'tenantCode': self.tenant_key.get().tenant_code,
            'notes': self.DEVICE_NOTES
        }
        when(deferred).defer(any_matcher(update_chrome_os_device),
                             any_matcher(self.device_key.urlsafe())).thenReturn(None)
        self.app.put('/api/v1/devices/{0}'.format(self.device_key.urlsafe()),
                     json.dumps(request_body),
                     headers=self.valid_authorization_header)
        updated_display = self.device_key.get()
        self.assertEqual(gcm_registration_id, updated_display.gcm_registration_id)
        self.assertEqual(self.tenant_key, updated_display.tenant_key)
        self.assertEqual(self.DEVICE_NOTES, updated_display.notes)

    def test_put_updates_device_entity_with_explicit_tenant_change(self):
        new_tenant = self.another_tenant_key.get()
        request_body = {
            'gcmRegistrationId': self.GCM_REGISTRATION_ID,
            'tenantCode': new_tenant.tenant_code
        }
        when(deferred).defer(any_matcher(update_chrome_os_device),
                             any_matcher(self.device_key.urlsafe())).thenReturn(None)
        self.app.put('/api/v1/devices/{0}'.format(self.device_key.urlsafe()),
                     json.dumps(request_body),
                     headers=self.valid_authorization_header)
        updated_display = self.device_key.get()
        self.assertEqual(self.another_tenant_key, updated_display.tenant_key)

    ##################################################################################################################
    ## delete
    ##################################################################################################################

    def test_delete_no_authorization_header_returns_forbidden(self):
        uri = build_uri('device', params_dict={'device_urlsafe_key': self.device_key.urlsafe()})
        response = self.delete(uri, headers=self.invalid_authorization_header)
        self.assertForbidden(response)

    def test_delete_http_status_no_content(self):
        request_body = {}
        response = self.app.delete('/api/v1/devices/{0}'.format(self.device_key.urlsafe()),
                                   json.dumps(request_body),
                                   headers=self.valid_authorization_header)
        self.assertEqual('204 No Content', response.status)

    def test_delete_removes_device_entity(self):
        request_body = {}
        self.app.delete('/api/v1/devices/{0}'.format(self.device_key.urlsafe()),
                        json.dumps(request_body),
                        headers=self.valid_authorization_header)
        self.assertIsNone(self.device_key.get())

    def __create_tenant(self, code, name, email):
        tenant = Tenant.create(tenant_code=code,
                               name=name,
                               admin_email=email,
                               content_server_url=self.CONTENT_SERVER_URL,
                               content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                               chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                               domain_key=self.domain_key,
                               active=True)
        return tenant.put()

    def __build_list_devices(self, tenant_key=None, number_to_build=10):
        results = []
        if tenant_key is None:
            tenant_key = self.__create_tenant()
        for i in range(number_to_build):
            results.append(build(ChromeOsDevice,
                                 tenant_key=tenant_key,
                                 gcm_registration_id=self.GCM_REGISTRATION_ID,
                                 device_id=self.DEVICE_ID))
        return results

    def __setup_distributor_with_two_tenants_with_n_devices(self, distributor_key, tenant_1_device_count,
                                                            tenant_2_device_count):
        domain_1 = Domain.create(name='dev.acme.com',
                                 distributor_key=distributor_key,
                                 impersonation_admin_email_address='fred@acme.com',
                                 active=True)
        domain_key_1 = domain_1.put()
        domain_2 = Domain.create(name='test.acme.com',
                                 distributor_key=distributor_key,
                                 impersonation_admin_email_address='fred@acme.com',
                                 active=True)
        domain_key_2 = domain_2.put()
        tenant_1 = Tenant.create(tenant_code='foobar_inc',
                                 name='Foobar, Inc',
                                 admin_email='bill@foobar.com',
                                 content_server_url=self.CONTENT_SERVER_URL,
                                 content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                 domain_key=domain_key_1,
                                 active=True)
        tenant_key_1 = tenant_1.put()
        self.__build_list_devices(tenant_key=tenant_key_1, number_to_build=tenant_1_device_count)
        tenant_2 = Tenant.create(tenant_code='goober_inc',
                                 name='Goober, Inc',
                                 admin_email='bill@goober.com',
                                 content_server_url=self.CONTENT_SERVER_URL,
                                 content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                 domain_key=domain_key_2,
                                 active=True)
        tenant_key_2 = tenant_2.put()
        self.__build_list_devices(tenant_key=tenant_key_2, number_to_build=tenant_2_device_count)
