from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
import unittest
import responses
import objects_for_testing
import datetime

from proofplay.data_processing import calculate_location_count, calculate_serial_count, \
    format_raw_program_record_data_for_single_resource_by_location, \
    get_total_play_count_of_resource_between_date_range_for_all_locations, generate_date_range_csv_by_date


class TestDataProcessing(BaseTest):
    current_timestamp = datetime.datetime(2011, 4, 9, 10, 30)
    start_date = current_timestamp - datetime.timedelta(days=5)
    end_date = current_timestamp + datetime.timedelta(days=1)
    device_serial_network_response = {
        u'entities': [
            {u'serial_number': u'F5MSCX001896', u'location_id': 6034, u'id': 5636026810761216,
             u'tenant_id': u'gamestop'},
            {u'serial_number': u'F5MSCX001736', u'location_id': 6023, u'id': 5638830484881408,
             u'tenant_id': u'gamestop'},
            {u'serial_number': u'F5MSCX001938', u'location_id': 6023, u'id': 5651124426113024,
             u'tenant_id': u'dev'},
            {u'serial_number': u'F5MSCX001891', u'location_id': 6023, u'id': 5652383656837120,
             u'tenant_id': u'dev'},
            {u'serial_number': u'F5MSCX001889', u'location_id': 6023, u'id': 5681034041491456,
             u'tenant_id': u'dev'},
            {u'serial_number': u'F5MSCX001835', u'location_id': 6034, u'id': 5710239819104256,
             u'tenant_id': u'dev'},
            {u'serial_number': u'F5MSCX001905', u'location_id': 6023, u'id': 5742796208078848,
             u'tenant_id': u'dev'},
            {u'serial_number': u'F5MSCX001939', u'location_id': 6023, u'id': 5767281011326976,
             u'tenant_id': u'dev'}
        ]
    }

    def test_calculate_location_count(self):
        example_input = [{"location_id": 5}, {"location_id": 6}, {"location_id": 6}]
        expected_result = 2
        self.assertEqual(calculate_location_count(example_input), expected_result)

    def test_calculate_serial_count(self):
        example_input = [{"device_id": 1}, {"device_id": 1}, {"device_id": 5}]
        expected_result = 2
        self.assertEqual(calculate_serial_count(example_input), expected_result)

    def test_format_raw_program_record_data_for_single_resource_by_location(self):
        example_input = {
            6023: [
                {"some_data": 6, "device_id": 2342423},
                {"some_data": 7, "device_id": 2342423},

            ],
            6034: [
                {"some_data": 6, "device_id": 3334},
                {"some_data": 7, "device_id": 3334},
                {"some_data": 8, "device_id": 3334}
            ]
        }
        expected_output = {
            6023: {
                "PlayCount": 2,
                "Player": 2342423
            },
            6034: {
                "PlayCount": 3,
                "Player": 3334
            }
        }

        self.assertEqual(format_raw_program_record_data_for_single_resource_by_location(example_input), expected_output)

    # def test_generate_date_range_csv_for_single_resource_by_location(self):
    #     dictionary = {
    #         u'6023': {'Player': u'F5MSCX001939', 'PlayCount': 16},
    #         u'6034': {'Player': u'F5MSCX001896', 'PlayCount': 11}
    #     }
    #     resource = "some_resource"
    #
    #     now = datetime.datetime.now()
    #
    #     generated_csv = generate_date_range_csv_for_single_resource_by_location(
    #             self.start_date,
    #             self.end_date,
    #             resource,
    #             dictionary,
    #             now
    #     )
    #
    #     expected_output_top_row = 'Creation_Date,Start_Date,End_Date,Start_Time,End_Time,Content'
    #
    #     expected_output = expected_output_top_row + '\r\n2016-01-27 12:41:27.273825,2011-04-04 10:30:00,2011-04-10 10:30:00,12:00 AM,11:59 PM,some_resource\r\nLocation,Player,PlayCount\r\n6023,F5MSCX001939,16\r\n6034,F5MSCX001896,11\r\n'
    #
    #     modified_output = expected_output.split("\r\n")
    #
    #     second_row = modified_output[1].split(",")
    #
    #     second_row[0] = str(now)
    #
    #     second_row_back_joined = ','.join(second_row)
    #
    #     modified_output[1] = second_row_back_joined
    #
    #     modified_output = '\r\n'.join(modified_output)
    #
    #     self.assertEqual(modified_output, generated_csv.read())

    # def test_generate_date_range_csv_for_a_single_resource(self):
    #     dictionary = {
    #         "some_resource": {
    #             '2016-01-23 00:00:00': {'LocationCount': 1, 'PlayerCount': 1, 'PlayCount': 2},
    #             '2016-01-09 00:00:00': {'LocationCount': 1, 'PlayerCount': 1, 'PlayCount': 2},
    #             '2016-01-17 00:00:00': {'LocationCount': 1, 'PlayerCount': 1, 'PlayCount': 1},
    #             '2016-01-10 00:00:00': {'LocationCount': 1, 'PlayerCount': 2, 'PlayCount': 2},
    #             '2016-01-13 00:00:00': {'LocationCount': 1, 'PlayerCount': 1, 'PlayCount': 2},
    #             '2016-01-19 00:00:00': {'LocationCount': 1, 'PlayerCount': 1, 'PlayCount': 1},
    #             '2016-01-12 00:00:00': {'LocationCount': 2, 'PlayerCount': 2, 'PlayCount': 2},
    #             '2016-01-15 00:00:00': {'LocationCount': 1, 'PlayerCount': 2, 'PlayCount': 2},
    #             '2016-01-08 00:00:00': {'LocationCount': 1, 'PlayerCount': 1, 'PlayCount': 1},
    #             '2016-01-21 00:00:00': {'LocationCount': 2, 'PlayerCount': 2, 'PlayCount': 2},
    #             '2016-01-24 00:00:00': {'LocationCount': 1, 'PlayerCount': 1, 'PlayCount': 1},
    #             '2016-01-11 00:00:00': {'LocationCount': 1, 'PlayerCount': 1, 'PlayCount': 1},
    #             '2016-01-25 00:00:00': {'LocationCount': 0, 'PlayerCount': 0, 'PlayCount': 0},
    #             '2016-01-16 00:00:00': {'LocationCount': 2, 'PlayerCount': 2, 'PlayCount': 2},
    #             '2016-01-26 00:00:00': {'LocationCount': 0, 'PlayerCount': 0, 'PlayCount': 0},
    #             '2016-01-27 00:00:00': {'LocationCount': 0, 'PlayerCount': 0, 'PlayCount': 0},
    #             '2016-01-14 00:00:00': {'LocationCount': 1, 'PlayerCount': 2, 'PlayCount': 2},
    #             '2016-01-20 00:00:00': {'LocationCount': 1, 'PlayerCount': 1, 'PlayCount': 1},
    #             '2016-01-22 00:00:00': {'LocationCount': 1, 'PlayerCount': 1, 'PlayCount': 1},
    #             '2016-01-18 00:00:00': {'LocationCount': 1, 'PlayerCount': 1, 'PlayCount': 2}
    #         }
    #     }
    #
    #     resource = "some_resource"
    #
    #     now = datetime.datetime.now()
    #
    #     generated_csv = generate_date_range_csv_for_a_single_resource(
    #             self.start_date,
    #             self.end_date,
    #             resource,
    #             dictionary,
    #             now
    #     )
    #
    #     expected_output_top_row = 'Creation_Date,Start_Date,End_Date,Start_Time,End_Time,Content'
    #
    #     expected_output = expected_output_top_row + '\r\n2016-01-27 13:52:55.106405,2011-04-04 10:30:00,2011-04-10 10:30:00,12:00 AM,11:59 PM,some_resource\r\nFile,Date,LocationCount,PlayerCount,ChannelCount,PlayCount\r\nsome_resource,2016-01-08 00:00:00,1,1, ,1\r\nsome_resource,2016-01-09 00:00:00,1,1, ,2\r\nsome_resource,2016-01-10 00:00:00,1,2, ,2\r\nsome_resource,2016-01-11 00:00:00,1,1, ,1\r\nsome_resource,2016-01-12 00:00:00,2,2, ,2\r\nsome_resource,2016-01-13 00:00:00,1,1, ,2\r\nsome_resource,2016-01-14 00:00:00,1,2, ,2\r\nsome_resource,2016-01-15 00:00:00,1,2, ,2\r\nsome_resource,2016-01-16 00:00:00,2,2, ,2\r\nsome_resource,2016-01-17 00:00:00,1,1, ,1\r\nsome_resource,2016-01-18 00:00:00,1,1, ,2\r\nsome_resource,2016-01-19 00:00:00,1,1, ,1\r\nsome_resource,2016-01-20 00:00:00,1,1, ,1\r\nsome_resource,2016-01-21 00:00:00,2,2, ,2\r\nsome_resource,2016-01-22 00:00:00,1,1, ,1\r\nsome_resource,2016-01-23 00:00:00,1,1, ,2\r\nsome_resource,2016-01-24 00:00:00,1,1, ,1\r\nsome_resource,2016-01-25 00:00:00,0,0, ,0\r\nsome_resource,2016-01-26 00:00:00,0,0, ,0\r\nsome_resource,2016-01-27 00:00:00,0,0, ,0\r\n'
    #
    #     modified_output = expected_output.split("\r\n")
    #
    #     second_row = modified_output[1].split(",")
    #
    #     second_row[0] = str(now)
    #
    #     second_row_back_joined = ','.join(second_row)
    #
    #     modified_output[1] = second_row_back_joined
    #
    #     modified_output = '\r\n'.join(modified_output)
    #
    #     self.assertEqual(modified_output, generated_csv.read())

    def test_generate_date_range_csv_for_a_multiple_resources(self):
        dictionary = objects_for_testing.date_range_multiple_resources_test_dictionary
        resources = [u'GSAD_5553', u'GSAD_5447']

        now = datetime.datetime.now()

        generated_csv = generate_date_range_csv_by_date(
                self.start_date,
                self.end_date,
                resources,
                dictionary,
                now
        )

        expected_output_top_row = 'Creation_Date,Start_Date,End_Date,Start_Time,End_Time,Content'

        expected_output = expected_output_top_row + objects_for_testing.date_range_multiple_resources_test_result

        modified_output = expected_output.split("\r\n")

        second_row = modified_output[1].split(",")

        second_row[0] = str(now)

        second_row_back_joined = ','.join(second_row)

        modified_output[1] = second_row_back_joined

        modified_output = '\r\n'.join(modified_output)

        self.assertEqual(modified_output, generated_csv.read())

    def test_get_total_play_count_of_resource_between_date_range_for_all_locations(self):
        raw_data = {
            '2014-12-02 00:00:00': [
                {'ended_at': datetime.datetime(2014, 12, 2, 9, 45, 34), 'resource_id': u'GSAD_5553',
                 'location_id': u'6023',
                 'started_at': datetime.datetime(2014, 12, 2, 9, 35, 34), 'device_id': u'F5MSCX001736'}],
            '2014-04-05 00:00:00': [],
            '2014-10-29 00:00:00': [
                {'ended_at': datetime.datetime(2014, 10, 29, 10, 45, 33), 'resource_id': u'GSAD_5553',
                 'location_id': u'6023', 'started_at': datetime.datetime(2014, 10, 29, 10, 35, 33),
                 'device_id': u'F5MSCX001736'}],
            '2015-01-18 00:00:00': [
                {'ended_at': datetime.datetime(2015, 1, 18, 11, 45, 35), 'resource_id': u'GSAD_5553',
                 'location_id': u'6023',
                 'started_at': datetime.datetime(2015, 1, 18, 11, 35, 35), 'device_id': u'F5MSCX001939'},
                {'ended_at': datetime.datetime(2015, 1, 18, 11, 45, 45), 'resource_id': u'GSAD_5553',
                 'location_id': u'6024',
                 'started_at': datetime.datetime(2015, 1, 18, 11, 35, 35), 'device_id': u'F5MSCX001559'}
            ],

        }

        resource = "some_resource"

        expected_output = {
            resource: {
                '2014-12-02 00:00:00': {
                    "LocationCount": 1,
                    "PlayerCount": 1,
                    "PlayCount": 1
                },
                '2014-04-05 00:00:00': {
                    "LocationCount": 0,
                    "PlayerCount": 0,
                    "PlayCount": 0
                },
                '2014-10-29 00:00:00': {
                    "LocationCount": 1,
                    "PlayerCount": 1,
                    "PlayCount": 1
                },
                '2015-01-18 00:00:00': {
                    "LocationCount": 2,
                    "PlayerCount": 2,
                    "PlayCount": 2
                }

            }
        }

        self.assertEqual(get_total_play_count_of_resource_between_date_range_for_all_locations(
                {"raw_data": raw_data, "resource": resource}),
                expected_output
        )


if __name__ == '__main__':
    unittest.main()
