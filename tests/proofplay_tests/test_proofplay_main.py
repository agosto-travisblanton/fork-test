from env_setup import setup_test_paths

setup_test_paths()

from agar.test import WebTest
from base_sql_test_config import SQLBaseTest
from proofplay.proofplay_models import Resource, ProgramRecord, TenantCode, ProgramPlayEvent
from routes_proofplay import application
import json
from proofplay.dev.generate_mock_data import batch_up_one_day_without_changing_data
from utils.web_util import build_uri
import datetime
from models import Tenant, Distributor, Domain
from proofplay.database_calls import insert_new_location_or_get_existing, insert_new_device_or_get_existing
from app_config import config
import time


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
    one_device_customer_display_code = "my-device"
    location_code = "6025"

    def setUp(self):
        super(TestMain, self).setUp()

        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME, active=True)

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

        self.load_tenant()

    def test_multi_device_by_date_api(self):
        self.load_tenants()
        self.load_resources()
        self.load_one_device()

        start_date = datetime.datetime.now()
        end_date = start_date - datetime.timedelta(days=5)
        start_unix = int(time.mktime(start_date.timetuple()))
        end_unix = int(time.mktime(end_date.timetuple()))
        devices = [self.one_device_customer_display_code]

        all_devices = ''
        for item in devices:
            all_devices = "," + item

        uri = build_uri('MultiDeviceByDate', module='proofplay', params_dict={
            'tenant': self.tenant_code,
            'distributor_key': self.distributor_key.urlsafe(),
            'devices': all_devices,
            'start_date': start_unix,
            'end_date': end_unix
        })

        response = self.app.get(uri, headers=self.headers)
        self.assertEqual(200, response.status_int)

    def test_multi_location_summarized(self):
        self.load_tenants()
        self.load_resources()
        self.load_one_device()

        start_date = datetime.datetime.now()
        end_date = start_date - datetime.timedelta(days=5)
        start_unix = int(time.mktime(start_date.timetuple()))
        end_unix = int(time.mktime(end_date.timetuple()))
        locations = [self.location_code]

        all_locations = ''
        for item in locations:
            all_locations = "," + item

        uri = build_uri('MultiLocationSummarized', module='proofplay', params_dict={
            'tenant': self.tenant_code,
            'distributor_key': self.distributor_key.urlsafe(),
            'locations': all_locations,
            'start_date': start_unix,
            'end_date': end_unix
        })

        response = self.app.get(uri, headers=self.headers)
        self.assertEqual(200, response.status_int)

    def test_multi_location_by_device(self):
        self.load_tenants()
        self.load_resources()
        self.load_one_device()

        start_date = datetime.datetime.now()
        end_date = start_date - datetime.timedelta(days=5)
        start_unix = int(time.mktime(start_date.timetuple()))
        end_unix = int(time.mktime(end_date.timetuple()))
        locations = [self.location_code]

        all_locations = ''
        for item in locations:
            all_locations = "," + item

        uri = build_uri('MultiLocationByDevice', module='proofplay', params_dict={
            'tenant': self.tenant_code,
            'distributor_key': self.distributor_key.urlsafe(),
            'locations': all_locations,
            'start_date': start_unix,
            'end_date': end_unix
        })

        response = self.app.get(uri, headers=self.headers)
        self.assertEqual(200, response.status_int)

    def test_multi_device_summarized_api(self):
        self.load_tenants()
        self.load_resources()
        self.load_one_device()

        start_date = datetime.datetime.now()
        end_date = start_date - datetime.timedelta(days=5)
        start_unix = int(time.mktime(start_date.timetuple()))
        end_unix = int(time.mktime(end_date.timetuple()))
        devices = [self.one_device_customer_display_code]

        all_devices = ''
        for item in devices:
            all_devices = "," + item

        uri = build_uri('MultiDeviceSummarized', module='proofplay', params_dict={
            'tenant': self.tenant_code,
            'distributor_key': self.distributor_key.urlsafe(),
            'devices': all_devices,
            'start_date': start_unix,
            'end_date': end_unix
        })

        response = self.app.get(uri, headers=self.headers)
        self.assertEqual(200, response.status_int)

    def test_multi_resource_by_device_api(self):
        self.load_tenants()
        self.load_resources()
        self.load_one_device()

        start_date = datetime.datetime.now()
        end_date = start_date - datetime.timedelta(days=5)
        start_unix = int(time.mktime(start_date.timetuple()))
        end_unix = int(time.mktime(end_date.timetuple()))
        resource_identifiers = ["1234", "5678"]

        all_resources = ''
        for item in resource_identifiers:
            all_resources = "-" + item

        uri = build_uri('MultiResourceByDevice', module='proofplay', params_dict={
            'tenant': self.tenant_code,
            'distributor_key': self.distributor_key.urlsafe(),
            'resource_identifiers': all_resources,
            'start_date': start_unix,
            'end_date': end_unix
        })

        response = self.app.get(uri, headers=self.headers)
        self.assertEqual(200, response.status_int)

    def test_multi_resource_by_date_api(self):
        self.load_tenants()
        self.load_resources()
        self.load_one_device()

        start_date = datetime.datetime.now()
        end_date = start_date - datetime.timedelta(days=5)
        start_unix = int(time.mktime(start_date.timetuple()))
        end_unix = int(time.mktime(end_date.timetuple()))
        resources = ["1234", "5678"]

        all_resources = ''
        for item in resources:
            all_resources = "-" + item

        uri = build_uri('MultiResourceByDate', module='proofplay', params_dict={
            'tenant': self.tenant_code,
            'distributor_key': self.distributor_key.urlsafe(),
            'resource_identifiers': all_resources,
            'start_date': start_unix,
            'end_date': end_unix
        })
        response = self.app.get(uri, headers=self.headers)
        self.assertEqual(200, response.status_int)

    def test_get_all_tenants(self):
        self.load_tenants()

        uri = build_uri('GetTenants', module='proofplay')

        response = self.app.get(uri, headers=self.headers)
        self.assertEqual(json.loads(response.body), {u'tenants': [u'gamestop']})

    def test_get_all_locations_of_tenant(self):
        self.load_tenants()
        self.load_one_device()

        uri = build_uri('RetrieveAllLocationsOfTenant', module='proofplay', params_dict={'tenant': self.tenant_code})
        response = self.app.get(uri, headers=self.headers)

        self.assertEqual(json.loads(response.body), {u'locations': [unicode(self.location_code)]})

    def test_get_all_resources(self):
        self.load_tenants()
        self.load_resources()

        uri = build_uri('RetrieveAllResources', module='proofplay', params_dict={'tenant': self.tenant_code})
        response = self.app.get(uri, headers=self.headers)

        self.assertEqual(json.loads(response.body),
                         {u'resources': [{u'resource_identifier': u'1234', u'resource_name': u'test'},
                                         {u'resource_identifier': u'5678', u'resource_name': u'test2'}]
                          })

    def test_get_all_devices(self):
        self.load_tenants()
        self.load_one_device()
        uri = build_uri('RetrieveAllDevicesOfTenant', module='proofplay', params_dict={'tenant': 'gamestop'})
        response = self.app.get(uri, headers=self.headers)

        self.assertEqual(json.loads(response.body), {u'devices': [self.one_device_customer_display_code]})

    def test_post_new_program_play(self):
        uri = build_uri('PostNewProgramPlay', module='proofplay')
        self.app.post(uri, params=json.dumps(batch_up_one_day_without_changing_data(
            started_at=datetime.datetime.now(),
            amount_a_day=10,
            tenant="acme_inc"
        )),
                      headers={"Authorization": config.API_TOKEN})

        self.assertRunAndClearTasksInQueue(1, queue_names="proof-of-play")
        self.assertTrue(len(self.db_session.query(ProgramRecord).all()), 10)

    def load_one_device(self):
        device_serial = "1234"
        device_key = "5443"
        location_id = insert_new_location_or_get_existing(self.location_code, self.tenant_code)
        insert_new_device_or_get_existing(location_id, device_serial, device_key, self.one_device_customer_display_code,
                                          self.tenant_code)

    def load_tenant(self):
        new_tenant = TenantCode(
            tenant_code=self.tenant_code
        )

        self.db_session.add(new_tenant)
        self.db_session.commit()
        self.tenant_id = new_tenant.id

    def load_resources(self):
        new_resource = Resource(
            resource_name="test",
            resource_identifier="1234",
            tenant_id=self.tenant_id
        )
        self.db_session.add(new_resource)
        another_new_resource = Resource(
            resource_name="test2",
            resource_identifier="5678",
            tenant_id=self.tenant_id

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
        tenant = Tenant.create(tenant_code=self.tenant_code,
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

    def test_delete_raw_event_entries_older_than_thirty_days(self):
        uri = build_uri('PostNewProgramPlay', module='proofplay')

        for each in reversed(xrange(1, 36)):
            started_at = datetime.datetime.now() - datetime.timedelta(days=each)
            self.app.post(uri, params=json.dumps(
                batch_up_one_day_without_changing_data(
                    started_at=started_at,
                    amount_a_day=10,
                    tenant="acme_inc"
                )
            ), headers={"Authorization": config.API_TOKEN})

        self.assertRunAndClearTasksInQueue(35, queue_names="proof-of-play")

        all_events = self.db_session.query(ProgramPlayEvent).all()

        self.assertEqual(len(all_events), 350)

        delete_uri = build_uri('ManageRawPayloadTable', module='proofplay')

        self.app.get(delete_uri)

        all_events_now = self.db_session.query(ProgramPlayEvent).all()

        self.assertEqual(len(all_events_now), 300)
