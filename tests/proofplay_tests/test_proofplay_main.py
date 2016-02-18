from env_setup import setup_test_paths

setup_test_paths()

from agar.test import WebTest
from base_sql_test_config import SQLBaseTest
from proofplay.proofplay_models import Resource, ProgramRecord
from routes_proofplay import application
import json
from proofplay.dev.make_mock_data import make_one_days_worth_of_data
from utils.web_util import build_uri
import datetime
from models import Tenant, TENANT_ENTITY_GROUP_NAME, Distributor, Domain, ChromeOsDevice
from proofplay.database_calls import insert_new_location_or_get_existing, insert_new_device_or_get_existing
from app_config import config


class TestMain(SQLBaseTest, WebTest):
    APPLICATION = application
    ADMIN_EMAIL = "foo{0}@bar.com"
    API_KEY = "SOME_KEY_{0}"
    CONTENT_SERVER_URL = 'https://skykit-contentmanager-int.appspot.com/content'
    CONTENT_MANAGER_BASE_URL = 'https://skykit-contentmanager-int.appspot.com'
    CHROME_DEVICE_DOMAIN = 'dev.agosto.com'
    DISTRIBUTOR_NAME = 'agosto'
    IMPERSONATION_EMAIL = 'test@test.com'
    ORIGINAL_NOTIFICATION_EMAILS = ['test@skykit.com', 'admin@skykit.com']
    tenant_code = "gamestop"

    def setUp(self):
        super(TestMain, self).setUp()
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
                                              active=True)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.distributor_key,
                                    impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                    active=True)
        self.domain_key = self.domain.put()
        self.headers = {
            'Authorization': config.API_TOKEN,
            'X-Provisioning-Distributor': self.distributor_key.urlsafe()
        }

    def test_get_all_tenants(self):
        self.load_tenants()

        uri = build_uri('GetTenants', module='proofplay')
        response = self.app.get(uri, headers=self.headers)

        self.assertEqual(json.loads(response.body), {u'tenants': [u'gamestop']})

    def test_get_all_resources(self):
        self.load_tenants()
        self.load_resources()

        uri = build_uri('RetrieveAllResources', module='proofplay', params_dict={'tenant': 'gamestop'})
        response = self.app.get(uri, headers=self.headers)

        self.assertEqual(json.loads(response.body), {u'resources': [u'test', u'test2']})

    def test_get_all_devices(self):
        self.load_tenants()
        device_serial = "1234"
        device_key = "5443"
        customer_display_code = "my-device"
        location_id = insert_new_location_or_get_existing("6025")
        insert_new_device_or_get_existing(location_id, device_serial, device_key, customer_display_code,
                                          self.tenant_code)

        uri = build_uri('RetrieveAllDevicesOfTenant', module='proofplay', params_dict={'tenant': 'gamestop'})
        response = self.app.get(uri, headers=self.headers)

        self.assertEqual(json.loads(response.body), {u'devices': [customer_display_code]})

    def test_post_new_program_play(self):
        uri = build_uri('PostNewProgramPlay', module='proofplay')
        self.app.post(uri, params=json.dumps(make_one_days_worth_of_data(10, datetime.datetime.now())))
        self.assertRunAndClearTasksInQueue(1, queue_names="default")
        self.assertTrue(self.db_session.query(ProgramRecord).first())

    def load_resources(self):
        new_resource = Resource(
                resource_name="test",
                resource_identifier="1234",
                tenant_code=self.tenant_code
        )
        self.db_session.add(new_resource)
        another_new_resource = Resource(
                resource_name="test2",
                resource_identifier="5678",
                tenant_code=self.tenant_code

        )
        self.db_session.add(another_new_resource)
        self.db_session.commit()

    def load_tenants(self):
        tenant_keys = []
        domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                               distributor_key=self.distributor_key,
                               impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                               active=True)
        domain_key = domain.put()
        tenant = Tenant.create(tenant_code='gamestop',
                               name=self.tenant_code,
                               admin_email=self.ADMIN_EMAIL,
                               content_server_url=self.CONTENT_SERVER_URL,
                               content_manager_base_url=self.CONTENT_MANAGER_BASE_URL,
                               domain_key=domain_key,
                               active=True)
        tenant.notification_emails = self.ORIGINAL_NOTIFICATION_EMAILS
        tenant_key = tenant.put()
        tenant_keys.append(tenant_key)
        return tenant_keys
