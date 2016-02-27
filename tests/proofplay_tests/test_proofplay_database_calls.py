from env_setup import setup_test_paths
setup_test_paths()

from base_sql_test_config import SQLBaseTest
import datetime
from proofplay.proofplay_models import Resource, ProgramRecord, Device, Location
from collections import OrderedDict

from proofplay.database_calls import (
    insert_new_resource_or_get_existing,
    insert_new_program_record,
    insert_new_location_or_get_existing,
    insert_new_device_or_get_existing,
    program_record_for_resource_by_date,
    program_record_for_resource_by_location,
    retrieve_all_resources_of_tenant,
    retrieve_all_resources,
    get_raw_program_record_data_by_device,
    program_record_for_device_by_date,
    program_record_for_device_summarized,
    retrieve_all_locations_of_tenant,
    get_raw_program_record_data_by_location,
    program_record_for_location_summarized
)


class TestDatabase(SQLBaseTest):
    resource_name = "some_resource"
    resource_id = "1234"
    customer_location_code = "6025"
    device_serial = "62525"
    device_key = "5678"
    tenant_code = "SOME_TENANT"
    customer_display_code = "some_display_code"
    started_at = datetime.datetime(2016, 2, 2, 15, 31, 43, 683139)
    ended_at = datetime.datetime(2016, 2, 2, 16, 31, 43, 683139)

    def test_insert_new_resource(self):
        insert_new_resource_or_get_existing(self.resource_name, self.resource_id, self.tenant_code)
        resource = self.db_session.query(Resource).filter_by(resource_name=self.resource_name).first()
        self.assertEqual(resource.resource_name, self.resource_name)

    def test_retrieve_all_resources_of_tenant(self):
        self.test_insert_new_resource()
        resources = retrieve_all_resources_of_tenant(self.tenant_code)
        self.assertEqual(resources, [
            {'resource_identifier': unicode(self.resource_id), 'resource_name': unicode(self.resource_name)}])

    def test_retrieve_all_resources(self):
        self.test_insert_new_resource()
        insert_new_resource_or_get_existing("new_resource", "12345", self.tenant_code)
        resources = retrieve_all_resources()
        self.assertEqual(resources, [self.resource_name, "new_resource"])

    def test_insert_new_location(self):
        insert_new_location_or_get_existing(self.customer_location_code)
        resource = self.db_session.query(Location).filter_by(customer_location_code=self.customer_location_code).first()
        self.assertEqual(resource.customer_location_code, self.customer_location_code)

    def test_insert_new_device(self):
        self.test_insert_new_location()
        insert_new_device_or_get_existing(
                1,
                self.device_serial,
                self.device_key,
                self.customer_display_code,
                self.tenant_code
        )

        device = self.db_session.query(Device).filter_by(serial_number=self.device_serial).first()
        self.assertEqual(device.serial_number, self.device_serial)
        self.assertEqual(device.device_key, self.device_key)
        self.assertEqual(device.tenant_code, self.tenant_code)
        self.assertEqual(device.full_location.customer_location_code, self.customer_location_code)

    def test_insert_new_program_record(self):
        resource_id = insert_new_resource_or_get_existing(self.resource_name, self.resource_id, self.tenant_code)
        location_id = insert_new_location_or_get_existing(self.customer_location_code)

        device_id = insert_new_device_or_get_existing(
                1,
                self.device_serial,
                self.device_key,
                self.customer_display_code,
                self.tenant_code
        )

        insert_new_program_record(
                location_id,
                device_id,
                resource_id,
                self.started_at,
                self.ended_at
        )

        program_record = self.db_session.query(ProgramRecord).filter_by(started_at=self.started_at).first()

        self.assertEqual(program_record.full_device.serial_number, self.device_serial)
        self.assertEqual(program_record.full_location.customer_location_code, self.customer_location_code)
        self.assertEqual(program_record.started_at, self.started_at)
        self.assertEqual(program_record.ended_at, self.ended_at)

    def test_program_record_for_device_summarized(self):
        self.test_insert_new_program_record()
        expected_result = {
            u'some_display_code': [
                {
                    'started_at': datetime.datetime(2016, 2, 2, 15, 31, 43, 683139),
                    'ended_at': datetime.datetime(2016, 2, 2, 16, 31, 43, 683139),
                    'resource_id': u'some_resource', 'location_id': u'6025',
                    'device_id': unicode(self.customer_display_code)}
            ]
        }

        start_search = self.started_at - datetime.timedelta(days=1)
        end_search = self.started_at + datetime.timedelta(days=1)

        result = program_record_for_device_summarized(start_search,
                                                      end_search,
                                                      self.customer_display_code,
                                                      self.tenant_code)

        self.assertEqual(expected_result, result)

    def test_program_record_for_device_by_date(self):
        self.test_insert_new_program_record()
        expected_result = {
            str(datetime.datetime(2016, 2, 2, 0, 0, 0, 0)): [
                {
                    'started_at': datetime.datetime(2016, 2, 2, 15, 31, 43, 683139),
                    'ended_at': datetime.datetime(2016, 2, 2, 16, 31, 43, 683139),
                    'resource_id': u'some_resource',
                    'location_id': u'6025',
                    'device_id': unicode(self.customer_display_code)
                }
            ]
        }

        start_search = self.started_at - datetime.timedelta(days=1)
        end_search = self.started_at + datetime.timedelta(days=1)

        result = program_record_for_device_by_date(start_search,
                                                   end_search,
                                                   self.customer_display_code,
                                                   self.tenant_code)

        self.assertEqual(expected_result, result)

    def test_get_raw_program_record_data_by_device(self):
        self.test_insert_new_program_record()

        start_search = self.started_at - datetime.timedelta(days=1)
        end_search = self.started_at + datetime.timedelta(days=1)

        result = get_raw_program_record_data_by_device(start_search,
                                                       end_search,
                                                       self.customer_display_code,
                                                       self.tenant_code)

        expected_output = [
            {
                "location_id": self.customer_location_code,
                "device_id": self.customer_display_code,
                "resource_id": self.resource_name,
                "started_at": self.started_at,
                "ended_at": self.ended_at
            }
        ]

        self.assertEqual(result, expected_output)

    def test_get_raw_program_record_data_for_resource_between_date_ranges_by_location(self):
        self.test_insert_new_program_record()
        expected_output = {
            unicode(self.customer_display_code): [
                {
                    'started_at': datetime.datetime(2016, 2, 2, 15, 31, 43, 683139),
                    'ended_at': datetime.datetime(2016, 2, 2, 16, 31, 43, 683139),
                    'resource_id': u'some_resource', 'location_id': u'6025',
                    'device_id': unicode(self.customer_display_code)
                }
            ]
        }

        self.assertEqual(program_record_for_resource_by_location(
                self.started_at,
                self.ended_at,
                self.resource_id,
                self.tenant_code
        ), expected_output)

    def test_get_raw_program_record_data_by_location(self):
        self.test_insert_new_program_record()

        start_search = self.started_at - datetime.timedelta(days=1)
        end_search = self.started_at + datetime.timedelta(days=1)

        result = get_raw_program_record_data_by_location(start_search,
                                                         end_search,
                                                         self.customer_location_code,
                                                         self.tenant_code)

        expected_output = [
            {
                "location_id": self.customer_location_code,
                "device_id": self.customer_display_code,
                "resource_id": self.resource_name,
                "started_at": self.started_at,
                "ended_at": self.ended_at
            }
        ]

        self.assertEqual(result, expected_output)

    def test_program_record_for_location_summarized(self):
        self.test_insert_new_program_record()

        start_search = self.started_at - datetime.timedelta(days=1)
        end_search = self.started_at + datetime.timedelta(days=1)

        result = program_record_for_location_summarized(start_search,
                                                        end_search,
                                                        self.customer_location_code,
                                                        self.tenant_code)
        self.maxDiff = None

        expected_output = {u'6025': OrderedDict([(u'some_resource', [
            {'started_at': datetime.datetime(2016, 2, 2, 15, 31, 43, 683139),
             'ended_at': datetime.datetime(2016, 2, 2, 16, 31, 43, 683139), 'resource_id': u'some_resource',
             'location_id': u'6025', 'device_id': u'some_display_code'}])])}

        self.assertEqual(result, expected_output)

    def test_get_raw_program_record_data_for_resource_between_date_ranges_by_date(self):
        self.test_insert_new_program_record()
        expected_output = {
            '2016-02-02 00:00:00': [
                {
                    'started_at': datetime.datetime(2016, 2, 2, 15, 31, 43, 683139),
                    'ended_at': datetime.datetime(2016, 2, 2, 16, 31, 43, 683139),
                    'resource_id': u'some_resource',
                    'location_id': u'6025', 'device_id': unicode(self.customer_display_code)
                }
            ]
        }

        self.assertEqual(program_record_for_resource_by_date(
                self.started_at,
                self.ended_at,
                self.resource_id,
                self.tenant_code

        ), expected_output)

    def test_retrieve_all_locations_of_tenant(self):
        self.test_insert_new_device()
        self.assertEqual([self.customer_location_code], retrieve_all_locations_of_tenant(self.tenant_code))
