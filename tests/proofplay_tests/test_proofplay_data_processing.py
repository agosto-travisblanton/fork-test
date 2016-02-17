from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
import unittest
from collections import OrderedDict
import datetime

from proofplay.data_processing import (calculate_location_count, calculate_serial_count,
                                       reformat_program_record_by_location,
                                       generate_date_range_csv_by_date,
                                       format_program_record_data_with_array_of_resources,
                                       transform_resource_data_between_date_range_by_location,
                                       transform_resource_data_between_date_ranges_by_date)


def convert_datetime_to_string_of_day_at_midnight(date):
    return str(datetime.datetime.combine(date.date(), datetime.time()))


class TestDataProcessing(BaseTest):
    a_date_timestamp = datetime.datetime(2011, 4, 9, 10, 30)
    start_date = a_date_timestamp - datetime.timedelta(days=5)
    end_date = a_date_timestamp + datetime.timedelta(days=1)

    def test_calculate_location_count(self):
        example_input = [{"location_id": 5}, {"location_id": 6}, {"location_id": 6}]
        expected_result = 2
        self.assertEqual(calculate_location_count(example_input), expected_result)

    def test_calculate_serial_count(self):
        example_input = [{"device_id": 1}, {"device_id": 1}, {"device_id": 5}]
        expected_result = 2
        self.assertEqual(calculate_serial_count(example_input), expected_result)

    def test_transform_resource_data_between_date_range_by_location(self):
        example_input = [
            {"device_id": 1, "some_info": "123"},
            {"device_id": 1, "some_info": "abc"},
            {"device_id": 5, "some_info": "xyz"}
        ]

        expected_result = {
            1: [
                {"device_id": 1, "some_info": "123"},
                {"device_id": 1, "some_info": "abc"}
            ],
            5: [{"device_id": 5, "some_info": "xyz"}]
        }

        results = transform_resource_data_between_date_range_by_location(example_input)

        self.assertEqual(expected_result, results)

    def test_transform_resource_data_between_date_ranges_by_date(self):
        started_at_plus_one = self.start_date + datetime.timedelta(days=1)
        started_at_plus_two = self.start_date + datetime.timedelta(days=2)
        started_at_plus_three = self.start_date + datetime.timedelta(days=3)
        example_input = [
            {"device_id": 1, "started_at": started_at_plus_one},
            {"device_id": 1, "someinfo": "something", "started_at": started_at_plus_one},
            {"device_id": 1, "started_at": started_at_plus_two},
            {"device_id": 1, "started_at": started_at_plus_three},
        ]

        expected_result = {
            convert_datetime_to_string_of_day_at_midnight(started_at_plus_one): [
                {"device_id": 1, "started_at": started_at_plus_one},
                {"device_id": 1, "someinfo": "something", "started_at": started_at_plus_one},
            ],
            convert_datetime_to_string_of_day_at_midnight(started_at_plus_two): [
                {"device_id": 1, "started_at": started_at_plus_two},
            ],
            convert_datetime_to_string_of_day_at_midnight(started_at_plus_three): [
                {"device_id": 1, "started_at": started_at_plus_three}
            ]
        }

        self.assertEqual(expected_result, transform_resource_data_between_date_ranges_by_date(example_input))

    def test_reformat_program_record_by_location(self):
        example_input = {
            'resource': 'GSAD_2222',
            'raw_data': {
                'F5MSCX001002': [
                    {'resource_id': 'GSAD_2222', 'location_id': '6034',
                     'started_at': datetime.datetime(2016, 2, 1, 18, 54, 42),
                     'ended_at': datetime.datetime(2016, 2, 1, 19, 4, 42), 'device_id': 'F5MSCX001002'}],
                'F5MSCX001001': [
                    {'resource_id': 'GSAD_2222', 'location_id': '6034',
                     'started_at': datetime.datetime(2016, 2, 1, 18, 14, 42),
                     'ended_at': datetime.datetime(2016, 2, 1, 18, 24, 42), 'device_id': 'F5MSCX001001'},
                    {'resource_id': 'GSAD_2222', 'location_id': '6034',
                     'started_at': datetime.datetime(2016, 2, 1, 18, 59, 14),
                     'ended_at': datetime.datetime(2016, 2, 1, 19, 9, 14), 'device_id': 'F5MSCX001001'}],
                'F5MSCX001000': [
                    {'resource_id': 'GSAD_2222', 'location_id': '6034',
                     'started_at': datetime.datetime(2016, 2, 1, 19, 14, 42),
                     'ended_at': datetime.datetime(2016, 2, 1, 19, 24, 42), 'device_id': 'F5MSCX001000'},
                    {'resource_id': 'GSAD_2222', 'location_id': '6034',
                     'started_at': datetime.datetime(2016, 2, 2, 18, 44, 42),
                     'ended_at': datetime.datetime(2016, 2, 2, 18, 54, 42), 'device_id': 'F5MSCX001000'}]}
        }

        expected_output = {
            'F5MSCX001002': {'Play Count': 1, 'Content': 'GSAD_2222', 'Display': 'F5MSCX001002', 'Location': '6034'},
            'F5MSCX001001': {'Play Count': 2, 'Content': 'GSAD_2222', 'Display': 'F5MSCX001001', 'Location': '6034'},
            'F5MSCX001000': {'Play Count': 2, 'Content': 'GSAD_2222', 'Display': 'F5MSCX001000', 'Location': '6034'}}

        self.assertEqual(expected_output, reformat_program_record_by_location(example_input))

    def test_format_program_record_data_with_array_of_resources(self):
        example_input = [
            {
                'resource': 'GSAD_4334',
                'raw_data': {
                    '2016-01-01 00:00:00': [
                        {'started_at': datetime.datetime(2016, 1, 1, 18, 44, 28),
                         'ended_at': datetime.datetime(2016, 1, 1, 18, 54, 28), 'device_id': 'F5MSCX001000',
                         'location_id': '6034',
                         'resource_id': 'GSAD_4334'}, {'started_at': datetime.datetime(2016, 1, 1, 19, 4, 28),
                                                       'ended_at': datetime.datetime(2016, 1, 1, 19, 14, 28),
                                                       'device_id': 'F5MSCX001002', 'location_id': '6034',
                                                       'resource_id': 'GSAD_4334'},
                        {'started_at': datetime.datetime(2016, 1, 1, 18, 9, 13),
                         'ended_at': datetime.datetime(2016, 1, 1, 18, 19, 13), 'device_id': 'F5MSCX001000',
                         'location_id': '6034',
                         'resource_id': 'GSAD_4334'}, {'started_at': datetime.datetime(2016, 1, 1, 18, 59, 13),
                                                       'ended_at': datetime.datetime(2016, 1, 1, 19, 9, 13),
                                                       'device_id': 'F5MSCX001001', 'location_id': '6034',
                                                       'resource_id': 'GSAD_4334'}
                    ],
                    '2016-01-02 00:00:00': [
                        {'started_at': datetime.datetime(2016, 1, 2, 18, 29, 13),
                         'ended_at': datetime.datetime(2016, 1, 2, 18, 39, 13), 'device_id': 'F5MSCX001001',
                         'location_id': '6034',
                         'resource_id': 'GSAD_4334'}, {'started_at': datetime.datetime(2016, 1, 2, 19, 9, 13),
                                                       'ended_at': datetime.datetime(2016, 1, 2, 19, 19, 13),
                                                       'device_id': 'F5MSCX001001', 'location_id': '6034',
                                                       'resource_id': 'GSAD_4334'}
                    ]}
            },
            {
                'resource': 'GSAD_5553',
                'raw_data': {
                    '2016-01-01 00:00:00': [
                        {'started_at': datetime.datetime(2016, 1, 1, 18, 14, 28),
                         'ended_at': datetime.datetime(2016, 1, 1, 18, 24, 28),
                         'device_id': 'F5MSCX001002',
                         'location_id': '6034', 'resource_id': 'GSAD_5553'},
                        {'started_at': datetime.datetime(2016, 1, 1, 18, 24, 28),
                         'ended_at': datetime.datetime(2016, 1, 1, 18, 34, 28),
                         'device_id': 'F5MSCX001001',
                         'location_id': '6034', 'resource_id': 'GSAD_5553'},
                        {'started_at': datetime.datetime(2016, 1, 1, 18, 19, 13),
                         'ended_at': datetime.datetime(2016, 1, 1, 18, 29, 13),
                         'device_id': 'F5MSCX001000',
                         'location_id': '6034', 'resource_id': 'GSAD_5553'},
                        {'started_at': datetime.datetime(2016, 1, 1, 19, 19, 13),
                         'ended_at': datetime.datetime(2016, 1, 1, 19, 29, 13),
                         'device_id': 'F5MSCX001001',
                         'location_id': '6034', 'resource_id': 'GSAD_5553'}
                    ],
                    '2016-01-02 00:00:00': [
                        {'started_at': datetime.datetime(2016, 1, 2, 18, 14, 28),
                         'ended_at': datetime.datetime(2016, 1, 2, 18, 24, 28), 'device_id': 'F5MSCX001001',
                         'location_id': '6034', 'resource_id': 'GSAD_5553'},
                        {'started_at': datetime.datetime(2016, 1, 2, 18, 34, 28),
                         'ended_at': datetime.datetime(2016, 1, 2, 18, 44, 28), 'device_id': 'F5MSCX001000',
                         'location_id': '6034', 'resource_id': 'GSAD_5553'},
                        {'started_at': datetime.datetime(2016, 1, 2, 18, 19, 13),
                         'ended_at': datetime.datetime(2016, 1, 2, 18, 29, 13), 'device_id': 'F5MSCX001000',
                         'location_id': '6034', 'resource_id': 'GSAD_5553'},
                        {'started_at': datetime.datetime(2016, 1, 2, 18, 49, 13),
                         'ended_at': datetime.datetime(2016, 1, 2, 18, 59, 13), 'device_id': 'F5MSCX001000',
                         'location_id': '6034', 'resource_id': 'GSAD_5553'}
                    ]
                }}
        ]

        expected_output = {
            'GSAD_4334': OrderedDict(
                    [('2016-01-01 00:00:00', {'PlayCount': 4, 'PlayerCount': 3, 'LocationCount': 1}),
                     ('2016-01-02 00:00:00', {'PlayCount': 2, 'PlayerCount': 1, 'LocationCount': 1})]),
            'GSAD_5553': OrderedDict(
                    [('2016-01-01 00:00:00', {'PlayCount': 4, 'PlayerCount': 3, 'LocationCount': 1}),
                     ('2016-01-02 00:00:00', {'PlayCount': 4, 'PlayerCount': 2, 'LocationCount': 1})])}

        self.assertEqual(expected_output, format_program_record_data_with_array_of_resources(example_input))


if __name__ == '__main__':
    unittest.main()
