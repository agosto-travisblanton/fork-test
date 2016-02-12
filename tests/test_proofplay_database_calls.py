from env_setup import setup_test_paths

setup_test_paths()

from base_sql_test_config import SQLBaseTest

from proofplay.database_calls import insert_new_resource_or_get_existing, insert_new_program_record, \
    insert_new_location_or_get_existing, \
    insert_new_device_or_get_existing, get_gamestop_store_location_from_serial_via_db, \
    get_raw_program_record_data_for_resource_between_date_ranges_by_date, \
    get_raw_program_record_data_for_resource_between_date_ranges_by_location, insert_new_gamestop_store_location
import datetime

from proofplay.models import Resource, ProgramRecord, Device, Location, GamestopStoreLocation


class TestDatabase(SQLBaseTest):
    resource_name = "some_resource"
    resource_id = "1234"
    location_identifier = "6025"
    device_serial = "62525"
    device_key = "5678"
    tenant_code = "SOME_TENANT"
    started_at = datetime.datetime(2016, 2, 2, 15, 31, 43, 683139)
    ended_at = datetime.datetime(2016, 2, 2, 16, 31, 43, 683139)

    def test_insert_new_resource(self):
        insert_new_resource_or_get_existing(self.resource_name, self.resource_id)
        resource = self.db_session.query(Resource).filter_by(resource_name=self.resource_name).first()
        self.assertEqual(resource.resource_name, self.resource_name)

    def test_insert_new_location(self):
        insert_new_location_or_get_existing(self.location_identifier)
        resource = self.db_session.query(Location).filter_by(location_identifier=self.location_identifier).first()
        self.assertEqual(resource.location_identifier, self.location_identifier)

    def test_insert_new_device(self):
        self.test_insert_new_location()
        device_id = insert_new_device_or_get_existing(
                1,
                self.device_serial,
                self.device_key,
                self.tenant_code
        )

        device = self.db_session.query(Device).filter_by(serial_number=self.device_serial).first()
        self.assertEqual(device.serial_number, self.device_serial)
        self.assertEqual(device.device_key, self.device_key)
        self.assertEqual(device.tenant_code, self.tenant_code)
        self.assertEqual(device.full_location.location_identifier, self.location_identifier)

    def test_insert_new_program_record(self):
        resource_id = insert_new_resource_or_get_existing(self.resource_name, self.resource_id)
        location_id = insert_new_location_or_get_existing(self.location_identifier)
        device_id = insert_new_device_or_get_existing(self.location_identifier, self.device_serial, self.device_key,
                                                      self.tenant_code)

        insert_new_program_record(
                location_id,
                device_id,
                resource_id,
                self.started_at,
                self.ended_at
        )
        program_record = self.db_session.query(ProgramRecord).filter_by(started_at=self.started_at).first()
        self.assertEqual(program_record.full_device.serial_number, self.device_serial)
        self.assertEqual(program_record.full_location.location_identifier, self.location_identifier)
        self.assertEqual(program_record.started_at, self.started_at)
        self.assertEqual(program_record.ended_at, self.ended_at)

    def test_insert_new_gamestop_store_location(self):
        insert_new_gamestop_store_location(self.location_identifier, self.device_serial)
        pair = self.db_session.query(GamestopStoreLocation).filter_by(location_name=self.location_identifier).first()
        self.assertEqual(pair.location_name, self.location_identifier)

    def test_get_gamestop_store_location_from_serial_via_db(self):
        self.assertFalse(get_gamestop_store_location_from_serial_via_db(self.device_serial))
        self.test_insert_new_gamestop_store_location()
        self.assertEqual(get_gamestop_store_location_from_serial_via_db(self.device_serial), self.location_identifier)

    def test_get_raw_program_record_data_for_resource_between_date_ranges_by_location(self):
        self.test_insert_new_program_record()
        expected_output = {
            u'6025': [
                {
                    'started_at': datetime.datetime(2016, 2, 2, 15, 31, 43, 683139),
                    'ended_at': datetime.datetime(2016, 2, 2, 16, 31, 43, 683139),
                    'resource_id': u'some_resource', 'location_id': u'6025', 'device_id': u'62525'
                }
            ]
        }

        self.assertEqual(get_raw_program_record_data_for_resource_between_date_ranges_by_location(
                self.started_at,
                self.ended_at,
                self.resource_name
        ), expected_output)

    def test_get_raw_program_record_data_for_resource_between_date_ranges_by_date(self):
        self.test_insert_new_program_record()
        expected_output = {
            '2016-02-02 00:00:00': [
                {
                    'started_at': datetime.datetime(2016, 2, 2, 15, 31, 43, 683139),
                    'ended_at': datetime.datetime(2016, 2, 2, 16, 31, 43, 683139), 'resource_id': u'some_resource',
                    'location_id': u'6025', 'device_id': u'62525'
                }
            ]
        }

        self.assertEqual(get_raw_program_record_data_for_resource_between_date_ranges_by_date(
                self.started_at,
                self.ended_at,
                self.resource_name
        ), expected_output)

