import json

from agar.test import BaseTest, WebTest
from app_config import config
from env_setup import setup_test_paths
from routes import application
from models import ChromeOsDevice, Tenant, Distributor, Domain

setup_test_paths()


class TestDeviceResourceSearchHandlers(BaseTest, WebTest):
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
    ETHERNET_MAC_ADDRESS = '8e271e619346'
    TENANT_CODE = 'foobar_inc'
    TENANT_NAME = 'Foobar, Inc,'
    DISTRIBUTOR_NAME = 'agosto'
    IMPERSONATION_EMAIL = 'test@test.com'
    DEVICE_NOTES = 'This is a device note'
    PAIRING_CODE = '0e8f-fc4e-d632-09dc'
    STORAGE_UTILIZATION = 26
    MEMORY_UTILIZATION = 63
    PROGRAM = 'some program'
    PROGRAM_ID = 'ID-512341234'
    LAST_ERROR = 'some error'

    def setUp(self):
        super(TestDeviceResourceSearchHandlers, self).setUp()
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
        self.unmanaged_device = ChromeOsDevice.create_unmanaged(self.GCM_REGISTRATION_ID, self.MAC_ADDRESS)
        self.unmanaged_device_key = self.unmanaged_device.put()
        self.managed_device = ChromeOsDevice.create_managed(
            tenant_key=self.tenant_key,
            gcm_registration_id=self.GCM_REGISTRATION_ID,
            device_id=self.DEVICE_ID,
            mac_address=self.MAC_ADDRESS)
        self.managed_device_key = self.managed_device.put()
        self.unmanaged_registration_token_authorization_header = {
            'Authorization': config.UNMANAGED_REGISTRATION_TOKEN
        }
        self.api_token_authorization_header = {
            'Authorization': config.API_TOKEN
        }
        self.unmanaged_api_token_authorization_header = {
            'Authorization': config.UNMANAGED_API_TOKEN
        }

        self.empty_header = {}

    ############################################################
    # TENANT SEARCH AND MAC
    ############################################################
    def test_search_for_device_by_serial_by_tenant(self):
        managed_number_build = 20
        self.__build_list_devices_with_serials(tenant_key=self.tenant_key, managed_number_to_build=managed_number_build,
                                               unmanaged_number_to_build=0)

        uri = application.router.build(
            None,
            'search_for_device_by_tenant',
            None,
            {
                'tenant_urlsafe_key': self.tenant_key.urlsafe(),

            }
        )

        response = self.app.get(uri, headers=self.api_token_authorization_header, params={'partial_serial': 'm-',
                                                                                          'unmanaged': 'false'})

        response_json = json.loads(response.body)
        self.assertTrue(len(response_json["matches"]) == managed_number_build)

    def test_search_for_device_by_mac_by_tenant(self):
        managed_number_build = 20
        self.__build_list_devices_with_serials(tenant_key=self.tenant_key, managed_number_to_build=managed_number_build,
                                               unmanaged_number_to_build=0)

        uri = application.router.build(
            None,
            'search_for_device_by_tenant',
            None,
            {
                'tenant_urlsafe_key': self.tenant_key.urlsafe(),

            }
        )

        response = self.app.get(uri, headers=self.api_token_authorization_header, params={'partial_mac': 'm-mac',
                                                                                          'unmanaged': 'false'})

        response_json = json.loads(response.body)
        self.assertTrue(len(response_json["matches"]) == managed_number_build)


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
        request_parameters = {'unmanaged': 'false', 'cur_prev_cursor': 'null',
                              'cur_next_cursor': 'null'}

        uri = application.router.build(None, 'devices-by-distributor', None,
                                       {'distributor_urlsafe_key': distributor_key.urlsafe()})

        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)

        self.assertOK(response)

    def test_get_devices_by_distributor_returns_expected_device_count(self):
        distributor = Distributor.create(name='Acme Brothers',
                                         active=True)
        distributor_key = distributor.put()
        self.__setup_distributor_with_two_tenants_with_n_devices(distributor_key,
                                                                 tenant_1_device_count=13,
                                                                 tenant_2_device_count=6)
        request_parameters = {'unmanaged': 'false', 'cur_prev_cursor': 'null',
                              'cur_next_cursor': 'null'}

        uri = application.router.build(
            None,
            'devices-by-distributor',
            None,
            {
                'distributor_urlsafe_key': distributor_key.urlsafe(),

            }
        )
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)

        response_json = json.loads(response.body)

        self.assertTrue(len(response_json["devices"]) < 200)
        self.assertFalse(response_json["prev_cursor"])

    def test_search_for_device_by_serial(self):
        distributor = Distributor.create(name='Acme Brothers',
                                         active=True)
        distributor_key = distributor.put()
        tenant_one_amount = 13
        tenant_two_amount = 6
        self.__setup_distributor_with_two_tenants_with_n_devices_with_serials(distributor_key,
                                                                              tenant_1_device_count=tenant_one_amount,
                                                                              tenant_2_device_count=tenant_two_amount)
        uri = application.router.build(
            None,
            'search_for_device_by_serial',
            None,
            {
                'distributor_urlsafe_key': distributor_key.urlsafe(),
                'partial_serial': 'm-',
                'unmanaged': 'false'
            }
        )

        response = self.app.get(uri, headers=self.api_token_authorization_header)

        response_json = json.loads(response.body)
        self.assertTrue(len(response_json["matches"]) == tenant_one_amount + tenant_two_amount)

    def test_search_for_device_by_serial(self):
        distributor = Distributor.create(name='Acme Brothers',
                                         active=True)
        distributor_key = distributor.put()
        tenant_one_amount = 13
        tenant_two_amount = 6
        self.__setup_distributor_with_two_tenants_with_n_devices_with_serials(distributor_key,
                                                                              tenant_1_device_count=tenant_one_amount,
                                                                              tenant_2_device_count=tenant_two_amount)
        uri = application.router.build(
            None,
            'search_for_device',
            None,
            {
                'distributor_urlsafe_key': distributor_key.urlsafe(),

            }
        )

        response = self.app.get(uri, headers=self.api_token_authorization_header, params={'partial_serial': 'm-',
                                                                                          'unmanaged': 'false'})
        response_json = json.loads(response.body)
        self.assertTrue(len(response_json["matches"]) == tenant_one_amount + tenant_two_amount)

    def test_search_for_device_by_gcmid(self):
        distributor = Distributor.create(name='Acme Brothers', active=True)
        distributor_key = distributor.put()
        tenant_one_amount = 13
        tenant_two_amount = 6
        self.__setup_distributor_with_two_tenants_with_n_devices_with_serials(
            distributor_key,
            tenant_1_device_count=tenant_one_amount,
            tenant_2_device_count=tenant_two_amount
        )

        uri = application.router.build(
            None,
            'search_for_device',
            None,
            {
                'distributor_urlsafe_key': distributor_key.urlsafe()
            }
        )
        response = self.app.get(uri, headers=self.api_token_authorization_header,
                                params={'partial_gcmid': 'm-gcm',
                                        'unmanaged': 'false'})

        response_json = json.loads(response.body)
        self.assertTrue(len(response_json["matches"]) == tenant_one_amount + tenant_two_amount)

    def test_search_for_device_by_mac(self):
        distributor = Distributor.create(name='Acme Brothers',
                                         active=True)
        distributor_key = distributor.put()
        tenant_one_amount = 13
        tenant_two_amount = 6
        self.__setup_distributor_with_two_tenants_with_n_devices_with_serials(distributor_key,
                                                                              tenant_1_device_count=tenant_one_amount,
                                                                              tenant_2_device_count=tenant_two_amount)
        uri = application.router.build(
            None,
            'search_for_device',
            None,
            {
                'distributor_urlsafe_key': distributor_key.urlsafe(),
            }
        )

        response = self.app.get(uri, headers=self.api_token_authorization_header, params={'partial_mac': 'm-mac',
                                                                                          'unmanaged': 'false'})

        response_json = json.loads(response.body)
        self.assertTrue(len(response_json["matches"]) == tenant_one_amount + tenant_two_amount)

    def test_search_for_device_by_mac(self):
        distributor = Distributor.create(name='Acme Brothers',
                                         active=True)
        distributor_key = distributor.put()
        tenant_one_amount = 13
        tenant_two_amount = 6
        self.__setup_distributor_with_two_tenants_with_n_devices_with_serials(distributor_key,
                                                                              tenant_1_device_count=tenant_one_amount,
                                                                              tenant_2_device_count=tenant_two_amount)
        uri = application.router.build(
            None,
            'search_for_device',
            None,
            {
                'distributor_urlsafe_key': distributor_key.urlsafe(),

            }
        )

        response = self.app.get(uri, headers=self.api_token_authorization_header, params={'partial_mac': 'm-mac',
                                                                                          'unmanaged': 'false'})

        response_json = json.loads(response.body)
        self.assertTrue(len(response_json["matches"]) == tenant_one_amount + tenant_two_amount)



    ############################################################
    # HELPER FUNCTIONS
    ############################################################


    def __initialize_heartbeat_info(self, up=True):
        self.managed_device.storage_utilization = self.STORAGE_UTILIZATION
        self.managed_device.memory_utilization = self.MEMORY_UTILIZATION
        self.managed_device.program = self.PROGRAM
        self.managed_device.program_id = self.PROGRAM_ID
        self.managed_device.last_error = self.LAST_ERROR
        self.managed_device.up = up
        self.managed_device.put()

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

    def __build_list_devices_with_serials(self, tenant_key=None, managed_number_to_build=5,
                                          unmanaged_number_to_build=5):
        results = []
        if tenant_key is None:
            tenant_key = self.__create_tenant()
        for i in range(managed_number_to_build):
            mac_address = 'm-mac{0}'.format(i)
            gcm_registration_id = 'm-gcm{0}'.format(i)
            device_id = 'd{0}'.format(i)
            serial_number = 'm-serial{0}'.format(i)
            device = ChromeOsDevice.create_managed(tenant_key=tenant_key,
                                                   mac_address=mac_address,
                                                   gcm_registration_id=gcm_registration_id,
                                                   device_id=device_id,
                                                   serial_number=serial_number)
            device.put()
            results.append(device)

        for i in range(unmanaged_number_to_build):
            mac_address = 'u-mac{0}'.format(i)
            gcm_registration_id = 'u-gcm{0}'.format(i)
            serial_number = 'u-serial{0}'.format(i)
            device = ChromeOsDevice.create_unmanaged(gcm_registration_id=gcm_registration_id,
                                                     mac_address=mac_address,
                                                     serial_number=serial_number)
            device.put()
            results.append(device)

        return results

    def __build_list_devices(self, tenant_key=None, managed_number_to_build=5, unmanaged_number_to_build=5):

        results = []

        if tenant_key is None:
            tenant_key = self.__create_tenant()

        for i in range(managed_number_to_build):
            mac_address = 'm-mac{0}'.format(i)
            gcm_registration_id = 'm-gcm{0}'.format(i)
            device_id = 'd{0}'.format(i)
            device = ChromeOsDevice.create_managed(tenant_key=tenant_key,
                                                   mac_address=mac_address,
                                                   gcm_registration_id=gcm_registration_id,
                                                   device_id=device_id)
            device.archived = False
            device.put()
            results.append(device)

        for i in range(unmanaged_number_to_build):
            mac_address = 'u-mac{0}'.format(i)
            gcm_registration_id = 'u-gcm{0}'.format(i)
            device = ChromeOsDevice.create_unmanaged(gcm_registration_id=gcm_registration_id,
                                                     mac_address=mac_address)
            device.put()
            results.append(device)

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
        self.__build_list_devices(tenant_key=tenant_key_1, managed_number_to_build=tenant_1_device_count,
                                  unmanaged_number_to_build=0)
        tenant_2 = Tenant.create(tenant_code='goober_inc',
                                 name='Goober, Inc',
                                 admin_email='bill@goober.com',
                                 content_server_url=self.CONTENT_SERVER_URL,
                                 content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                 domain_key=domain_key_2,
                                 active=True)
        tenant_key_2 = tenant_2.put()
        self.__build_list_devices(tenant_key=tenant_key_2, managed_number_to_build=tenant_2_device_count,
                                  unmanaged_number_to_build=0)

    def __setup_distributor_with_two_tenants_with_n_devices_with_serials(self, distributor_key, tenant_1_device_count,
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

        self.__build_list_devices_with_serials(tenant_key=tenant_key_1, managed_number_to_build=tenant_1_device_count,
                                               unmanaged_number_to_build=0)
        tenant_2 = Tenant.create(tenant_code='goober_inc',
                                 name='Goober, Inc',
                                 admin_email='bill@goober.com',
                                 content_server_url=self.CONTENT_SERVER_URL,
                                 content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                                 domain_key=domain_key_2,
                                 active=True)
        tenant_key_2 = tenant_2.put()
        self.__build_list_devices_with_serials(tenant_key=tenant_key_2, managed_number_to_build=tenant_2_device_count,
                                               unmanaged_number_to_build=0)
