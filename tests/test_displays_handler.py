from google.appengine.ext import ndb

from env_setup import setup_test_paths

setup_test_paths()

from chrome_os_devices_api import (refresh_display,
                                   refresh_display_by_mac_address,
                                   update_chrome_os_device)
import json
from google.appengine.ext.deferred import deferred
from mockito import when, any as any_matcher

from agar.test import BaseTest, WebTest
from routes import application
from models import Display, Tenant
from app_config import config
from ae_test_data import build


class TestDisplaysHandler(BaseTest, WebTest):
    APPLICATION = application
    CUSTOMER_ID = 'my_customer'
    TENANT_NAME = 'Foobar, Inc,'
    TENANT_CODE = 'foobar_inc'
    ADMIN_EMAIL = 'foo@bar.com'
    ANOTHER_TENANT_NAME = 'Another, Inc,'
    ANOTHER_TENANT_CODE = 'another_inc'
    ANOTHER_ADMIN_EMAIL = 'foo@another.com'
    CONTENT_SERVER_URL = 'https://www.content.com'
    CONTENT_SERVER_API_KEY = 'API KEY'
    CHROME_DEVICE_DOMAIN = 'bar.com'
    DEVICE_ID = '132e235a-b346-4a37-a100-de49fa753a2a'
    GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
    MAC_ADDRESS = '54271e619346'

    def setUp(self):
        super(TestDisplaysHandler, self).setUp()
        self.tenant_key = self.__create_tenant(self.TENANT_CODE, self.TENANT_NAME, self.ADMIN_EMAIL)
        self.another_tenant_key = self.__create_tenant(self.ANOTHER_TENANT_CODE, self.ANOTHER_TENANT_NAME,
                                                       self.ANOTHER_ADMIN_EMAIL)
        self.managed_display_key = self.__create_display(self.tenant_key, is_managed_display=True)
        self.valid_authorization_header = {
            'Authorization': config.API_TOKEN
        }
        self.invalid_authorization_header = {}


    ##################################################################################################################
    ## get_list
    ##################################################################################################################
    def test_get_list_no_query_parameters_http_status_ok(self):
        displays = self.__build_list_displays(tenant_key=self.tenant_key, number_to_build=20)
        request_parameters = {}
        uri = application.router.build(None, 'displays-retrieval', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_get_list_no_query_parameters_entity_body_json(self):
        displays = self.__build_list_displays(tenant_key=self.tenant_key, number_to_build=20)
        request_parameters = {}
        uri = application.router.build(None, 'displays-retrieval', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json['objects']), 10)

    def test_get_list_mac_address_query_parameter_http_status_ok(self):
        displays = self.__build_list_displays(tenant_key=self.tenant_key, number_to_build=20)
        request_parameters = {'macAddress': displays[1].mac_address}
        uri = application.router.build(None, 'displays-retrieval', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_get_list_mac_address_query_parameter_entity_body_json(self):
        displays = self.__build_list_displays(tenant_key=self.tenant_key, number_to_build=20)
        request_parameters = {'macAddress': displays[1].mac_address}
        uri = application.router.build(None, 'displays-retrieval', None, {})
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json['objects']), 1)

    ##################################################################################################################
    ## get_displays_by_tenant
    ##################################################################################################################
    def test_get_displays_by_tenant_http_status_ok(self):
        displays = self.__build_list_displays(tenant_key=self.tenant_key, number_to_build=20)
        request_parameters = {}
        uri = application.router.build(None, 'displays-by-tenant', None,
                                       {'tenant_urlsafe_key': self.tenant_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_get_displays_by_tenant_entity_body_json(self):
        displays = self.__build_list_displays(tenant_key=self.tenant_key, number_to_build=20)
        request_parameters = {}
        uri = application.router.build(None, 'displays-by-tenant', None,
                                       {'tenant_urlsafe_key': self.tenant_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json['objects']), 10)

    ##################################################################################################################
    ## get
    ##################################################################################################################
    def test_get_display_by_key_http_status_ok(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'manage-display',
                                       None,
                                       {'display_urlsafe_key': self.managed_display_key.urlsafe()})
        when(deferred).defer(any_matcher(refresh_display),
                             any_matcher(self.managed_display_key.urlsafe())).thenReturn(None)
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        self.assertOK(response)

    def test_get_display_by_key_entity_body_json(self):
        request_parameters = {}
        uri = application.router.build(None,
                                       'manage-display',
                                       None,
                                       {'display_urlsafe_key': self.managed_display_key.urlsafe()})
        when(deferred).defer(any_matcher(refresh_display),
                             any_matcher(self.managed_display_key.urlsafe())).thenReturn(None)
        response = self.app.get(uri, params=request_parameters, headers=self.valid_authorization_header)
        response_json = json.loads(response.body)
        display = self.managed_display_key.get()
        tenant = display.tenant_key.get()
        self.assertEqual(response_json['annotated_user'], display.annotated_user)
        self.assertEqual(response_json['annotated_location'], display.annotated_location)
        self.assertEqual(response_json['api_key'], display.api_key)
        self.assertEqual(response_json['boot_mode'], display.boot_mode)
        self.assertEqual(response_json['created'], display.created.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response_json['device_id'], display.device_id)
        self.assertEqual(response_json['ethernet_mac_address'], display.ethernet_mac_address)
        self.assertEqual(response_json['firmware_version'], display.firmware_version)
        self.assertEqual(response_json['gcm_registration_id'], display.gcm_registration_id)
        self.assertEqual(response_json['key'], display.key.urlsafe())
        self.assertEqual(response_json['kind'], display.kind)
        self.assertEqual(response_json['last_enrollment_time'], display.last_enrollment_time)
        self.assertEqual(response_json['last_sync'], display.last_sync)
        self.assertEqual(response_json['mac_address'], display.mac_address)
        self.assertEqual(response_json['managed_display'], display.managed_display)
        self.assertEqual(response_json['model'], display.model)
        self.assertEqual(response_json['org_unit_path'], display.org_unit_path)
        self.assertEqual(response_json['os_version'], display.os_version)
        self.assertEqual(response_json['platform_version'], display.platform_version)
        self.assertEqual(response_json['serial_number'], display.serial_number)
        self.assertEqual(response_json['status'], display.status)
        self.assertEqual(response_json['updated'], display.updated.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response_json['tenant']['active'], tenant.active)
        self.assertEqual(response_json['tenant']['admin_email'], tenant.admin_email)
        self.assertEqual(response_json['tenant']['chrome_device_domain'], tenant.chrome_device_domain)
        self.assertEqual(response_json['tenant']['content_server_url'], tenant.content_server_url)
        self.assertEqual(response_json['tenant']['created'], tenant.created.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response_json['tenant']['name'], tenant.name)
        self.assertEqual(response_json['tenant']['tenant_code'], tenant.tenant_code)
        self.assertEqual(response_json['tenant']['updated'], tenant.updated.strftime('%Y-%m-%d %H:%M:%S'))

    ##################################################################################################################
    ## post
    ##################################################################################################################
    def test_post_http_status_created(self):
        tenant = self.tenant_key.get()
        mac_address = '7889BE879f'
        request_body = {'macAddress': mac_address,
                        'gcmRegistrationId': '123',
                        'tenantCode': tenant.tenant_code}
        when(deferred).defer(any_matcher(refresh_display_by_mac_address),
                             any_matcher(str),
                             any_matcher(mac_address)).thenReturn(None)
        response = self.app.post('/api/v1/displays', json.dumps(request_body), headers=self.valid_authorization_header)
        self.assertEqual('201 Created', response.status)

    def test_post_display_key_location_header(self):
        tenant = self.tenant_key.get()
        mac_address = '7889BE879f'
        request_body = {'macAddress': mac_address,
                        'gcmRegistrationId': '123',
                        'tenantCode': tenant.tenant_code}
        when(deferred).defer(any_matcher(refresh_display_by_mac_address),
                             any_matcher(str),
                             any_matcher(mac_address)).thenReturn(None)
        response = self.app.post('/api/v1/displays', json.dumps(request_body), headers=self.valid_authorization_header)
        location_uri_components = str(response.headers['Location']).split('/')
        self.assertEqual(location_uri_components[5], "displays")
        self.assertEqual(39, len(location_uri_components[6]))
        display = ndb.Key(urlsafe=location_uri_components[6]).get()
        self.assertIsNotNone(display)

    ##################################################################################################################
    ## put
    ##################################################################################################################
    def test_put_http_status_no_content(self):
        gcm_registration_id = 'd23784972038845ab3963412'
        request_body = {'gcmRegistrationId': gcm_registration_id, 'tenantKey': self.tenant_key.urlsafe()}
        when(deferred).defer(any_matcher(update_chrome_os_device),
                             any_matcher(self.managed_display_key.urlsafe())).thenReturn(None)
        response = self.app.put('/api/v1/displays/{0}'.format(self.managed_display_key.urlsafe()),
                                json.dumps(request_body),
                                headers=self.valid_authorization_header)
        self.assertEqual('204 No Content', response.status)

    def test_put_updates_display_entity_in_datastore(self):
        gcm_registration_id = 'd23784972038845ab3963412'
        request_body = {'gcmRegistrationId': gcm_registration_id, 'tenantKey': self.tenant_key.urlsafe()}
        when(deferred).defer(any_matcher(update_chrome_os_device),
                             any_matcher(self.managed_display_key.urlsafe())).thenReturn(None)
        self.app.put('/api/v1/displays/{0}'.format(self.managed_display_key.urlsafe()),
                     json.dumps(request_body),
                     headers=self.valid_authorization_header)
        updated_display = self.managed_display_key.get()
        self.assertEqual(gcm_registration_id, updated_display.gcm_registration_id)
        self.assertEqual(self.tenant_key, updated_display.tenant_key)

    def test_put_updates_display_entity_in_datastore_with_explicit_tenant_change(self):
        gcm_registration_id = 'd23784972038845ab3963412'
        request_body = {'gcmRegistrationId': gcm_registration_id, 'tenantKey': self.another_tenant_key.urlsafe()}
        when(deferred).defer(any_matcher(update_chrome_os_device),
                             any_matcher(self.managed_display_key.urlsafe())).thenReturn(None)
        self.app.put('/api/v1/displays/{0}'.format(self.managed_display_key.urlsafe()),
                     json.dumps(request_body),
                     headers=self.valid_authorization_header)
        updated_display = self.managed_display_key.get()
        self.assertEqual(self.another_tenant_key, updated_display.tenant_key)

    ##################################################################################################################
    ## delete
    ##################################################################################################################
    def test_delete_http_status_no_content(self):
        request_body = {}
        response = self.app.delete('/api/v1/displays/{0}'.format(self.managed_display_key.urlsafe()),
                                   json.dumps(request_body),
                                   headers=self.valid_authorization_header)
        self.assertEqual('204 No Content', response.status)

    def test_delete_removes_display_entity_from_datastore(self):
        request_body = {}
        response = self.app.delete('/api/v1/displays/{0}'.format(self.managed_display_key.urlsafe()),
                                   json.dumps(request_body),
                                   headers=self.valid_authorization_header)
        self.assertIsNone(self.managed_display_key.get())

    @staticmethod
    def __load_file_contents(file_name):
        with open(file_name, 'r') as json_file:
            data = json_file.read().replace('\n', '')
        return data

    def __create_tenant(self, code, name, email):
        tenant = Tenant.create(tenant_code=code,
                               name=name,
                               admin_email=email,
                               content_server_url=self.CONTENT_SERVER_URL,
                               chrome_device_domain=self.CHROME_DEVICE_DOMAIN,
                               active=True)
        return tenant.put()

    def __create_display(self, tenant_key, is_managed_display=True):
        display = Display.create(tenant_key=tenant_key,
                                 device_id=self.DEVICE_ID,
                                 gcm_registration_id=self.GCM_REGISTRATION_ID,
                                 mac_address=self.MAC_ADDRESS,
                                 managed_display=is_managed_display)
        return display.put()

    def __build_list_displays(self, tenant_key=None, number_to_build=10):
        results = []
        if tenant_key is None:
            tenant_key = self.__create_tenant()
        for i in range(number_to_build):
            results.append(build(Display, tenant_key=tenant_key))
        return results
