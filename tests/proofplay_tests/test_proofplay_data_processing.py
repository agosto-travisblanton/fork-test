from env_setup import setup_test_paths

setup_test_paths()

import unittest
from collections import OrderedDict
import datetime
from base_sql_test_config import SQLBaseTest

from proofplay.data_processing import (
    calculate_location_count, calculate_serial_count,
    reformat_program_record_array_by_location,
    generate_resource_csv_by_date,
    format_program_record_data_with_array_of_resources_by_date,
    transform_db_data_to_by_device,
    transform_db_data_to_by_date,
    generate_resource_csv_by_device,
    create_merged_dictionary,
    count_resource_plays_from_dict_by_device,
    format_transformed_program_data_by_device,
    prepare_transformed_query_by_device_to_csv_by_date,
    generate_device_csv_summarized,
    generate_device_csv_by_date,
    transform_db_data_to_by_location_then_resource,
    format_multi_location_by_device,
    format_multi_location_summarized,
    generate_location_csv_summarized,
    generate_location_csv_by_device
)

import mock


def convert_datetime_to_string_of_day_at_midnight(date):
    return str(datetime.datetime.combine(date.date(), datetime.time()))


def retrieve_resource_name_from_resource_identifier_as_expected(dontmatter):
    return "GSAD_4334"


class TestDataProcessing(SQLBaseTest):
    a_date_timestamp = datetime.datetime(2011, 4, 9, 10, 30)
    start_date = a_date_timestamp - datetime.timedelta(days=5)
    end_date = a_date_timestamp + datetime.timedelta(days=1)

    def test_create_merged_dictionary(self):
        array_of_dicts = [
            {
                "one_dict": {
                    "somestuff": 1,
                    "some_other_stuff": 2
                }
            },
            {
                "two_dict": {
                    "somestuff": 1,
                    "some_other_stuff": 2
                }
            },

        ]

        expected_result = {
            "one_dict": {
                "somestuff": 1,
                "some_other_stuff": 2
            },
            "two_dict": {
                "somestuff": 1,
                "some_other_stuff": 2
            }
        }

        self.assertEqual(create_merged_dictionary(array_of_dicts), expected_result)

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

        results = transform_db_data_to_by_device(example_input)

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

        self.assertEqual(expected_result, transform_db_data_to_by_date(example_input))

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

        self.assertEqual(expected_output, reformat_program_record_array_by_location(example_input))

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

        start = datetime.datetime(2016, 1, 1, 0, 0, 0)

        end = datetime.datetime(2016, 1, 2, 0, 0, 0)

        self.assertEqual(expected_output,
                         format_program_record_data_with_array_of_resources_by_date(start, end, example_input))

    @mock.patch('proofplay.database_calls.retrieve_resource_name_from_resource_identifier',
                side_effect=retrieve_resource_name_from_resource_identifier_as_expected)
    def test_generate_date_range_csv_by_location(self, retrieve_function):
        now = datetime.datetime.now()
        resources = ["GSAD_4334"]
        expected_output = """Creation Date,Start Date,End Date,Content\r\n{},2016-02-01,2016-02-02,GSAD_4334\r\nContent,Display,Location,Play Count\r\nGSAD_4334,F5MSCX001001,6034,3\r\nGSAD_4334,F5MSCX001000,6034,4\r\nGSAD_4334,F5MSCX001002,6034,5\r\n""".format(
            str(now)[:10])

        start_time = datetime.datetime.strptime("Feb 1 2016", '%b %d %Y')
        end_time = datetime.datetime.strptime("Feb 2 2016", '%b %d %Y')

        example_input = [
            {
                'F5MSCX001002': {'Location': '6034', 'Play Count': 5, 'Display': 'F5MSCX001002',
                                 'Content': 'GSAD_4334'},
                'F5MSCX001000': {'Location': '6034', 'Play Count': 4, 'Display': 'F5MSCX001000',
                                 'Content': 'GSAD_4334'},
                'F5MSCX001001': {'Location': '6034', 'Play Count': 3, 'Display': 'F5MSCX001001',
                                 'Content': 'GSAD_4334'}}
        ]

        result = generate_resource_csv_by_device(
            start_date=start_time,
            end_date=end_time,
            resources=resources,
            array_of_data=example_input,
            created_time=now
        ).read()

        self.assertEqual(expected_output, result)

    @mock.patch('proofplay.database_calls.retrieve_resource_name_from_resource_identifier',
                side_effect=retrieve_resource_name_from_resource_identifier_as_expected)
    def test_generate_date_range_csv_by_date(self, retrieve_function):
        now = datetime.datetime.now()
        resources = ["GSAD_4334"]
        expected_output = """Creation Date,Start Date,End Date,Start Time,End Time,All Content\r\n{},2016-02-01,2016-02-02,12:00 AM,11:59 PM,GSAD_4334\r\nContent,Date,Location Count,Display Count,Play Count\r\nGSAD_4334,2016-02-01,1,2,6\r\nGSAD_4334,2016-02-02,1,3,6\r\n""".format(
            str(now)[:10])

        start_time = datetime.datetime.strptime("Feb 1 2016", '%b %d %Y')
        end_time = datetime.datetime.strptime("Feb 2 2016", '%b %d %Y')

        example_input = {
            'GSAD_4334': OrderedDict(
                [
                    ('2016-02-01', {'PlayCount': 6, 'LocationCount': 1, 'PlayerCount': 2}),
                    ('2016-02-02', {'PlayCount': 6, 'LocationCount': 1, 'PlayerCount': 3})]
            )
        }

        result = generate_resource_csv_by_date(
            start_date=start_time,
            end_date=end_time,
            resources=resources,
            dictionary=example_input,
            now=now
        ).read()

        self.assertEqual(expected_output, result)

    def test_count_resource_plays_from_dict_by_device(self):
        expected_output = {
            "my-device": {
                "location": "3443",
                "resource_55442": 2,
                "resource_3342": 3,
            }
        }

        the_input = {
            "raw_data": {
                "my-device": [
                    {"resource_id": "resource_55442", "location_id": "3443"},
                    {"resource_id": "resource_55442", "location_id": "3443"},
                    {"resource_id": "resource_3342", "location_id": "3443"},
                    {"resource_id": "resource_3342", "location_id": "3443"},
                    {"resource_id": "resource_3342", "location_id": "3443"},

                ]
            }
        }

        self.assertEqual(count_resource_plays_from_dict_by_device(the_input), expected_output)

    def test_format_transformed_program_data_by_device(self):
        example_input = [
            {
                'device': 'my-device-3',
                'raw_data': {
                    'my-device-3': [
                        {'started_at': datetime.datetime(2016, 2, 2, 15, 3, 12), 'location_id': '1001',
                         'device_id': 'my-device-3',
                         'ended_at': datetime.datetime(2016, 2, 2, 15, 13, 12), 'resource_id': 'GSAD_4334'}]}},
            {
                'device': 'my-device-7',
                'raw_data': {
                    'my-device-7': [
                        {'started_at': datetime.datetime(2016, 2, 1, 15, 3, 12), 'location_id': '3001',
                         'device_id': 'my-device-7', 'ended_at': datetime.datetime(2016, 2, 1, 15, 13, 12),
                         'resource_id': 'GSAD_2222'},
                        {'started_at': datetime.datetime(2016, 2, 1, 15, 23, 12), 'location_id': '3001',
                         'device_id': 'my-device-7', 'ended_at': datetime.datetime(2016, 2, 1, 15, 33, 12),
                         'resource_id': 'GSAD_5447'},
                        {'started_at': datetime.datetime(2016, 2, 1, 16, 3, 12), 'location_id': '3001',
                         'device_id': 'my-device-7', 'ended_at': datetime.datetime(2016, 2, 1, 16, 13, 12),
                         'resource_id': 'GSAD_4334'},
                        {'started_at': datetime.datetime(2016, 2, 1, 16, 13, 12), 'location_id': '3001',
                         'device_id': 'my-device-7', 'ended_at': datetime.datetime(2016, 2, 1, 16, 23, 12),
                         'resource_id': 'GSAD_4334'},
                        {'started_at': datetime.datetime(2016, 2, 2, 15, 53, 12), 'location_id': '3001',
                         'device_id': 'my-device-7', 'ended_at': datetime.datetime(2016, 2, 2, 16, 3, 12),
                         'resource_id': 'GSAD_2222'},
                        {'started_at': datetime.datetime(2016, 2, 3, 15, 43, 13), 'location_id': '3001',
                         'device_id': 'my-device-7', 'ended_at': datetime.datetime(2016, 2, 3, 15, 53, 13),
                         'resource_id': 'GSAD_4334'},
                        {'started_at': datetime.datetime(2016, 2, 3, 16, 3, 13), 'location_id': '3001',
                         'device_id': 'my-device-7', 'ended_at': datetime.datetime(2016, 2, 3, 16, 13, 13),
                         'resource_id': 'GSAD_5447'},
                        {'started_at': datetime.datetime(2016, 2, 3, 16, 13, 13), 'location_id': '3001',
                         'device_id': 'my-device-7', 'ended_at': datetime.datetime(2016, 2, 3, 16, 23, 13),
                         'resource_id': 'GSAD_2222'}]
                }}
        ]

        expected_output = [
            {'content': 'GSAD_4334', 'playcount': 1, 'display': 'my-device-3', 'location': '1001'},
            {'content': 'GSAD_2222', 'playcount': 3, 'display': 'my-device-7', 'location': '3001'},
            {'content': 'GSAD_4334', 'playcount': 3, 'display': 'my-device-7', 'location': '3001'},
            {'content': 'GSAD_5447', 'playcount': 2, 'display': 'my-device-7', 'location': '3001'}
        ]

        self.assertEqual(format_transformed_program_data_by_device(example_input), expected_output)

    def test_prepare_transformed_query_by_device_to_csv_by_date(self):
        example_input = [
            {
                'raw_data': {
                    '2016-02-02': [
                        {'device_id': 'my-device-3', 'resource_id': 'GSAD_4334', 'location_id': '1001',
                         'started_at': datetime.datetime(2016, 2, 2, 15, 3, 12),
                         'ended_at': datetime.datetime(2016, 2, 2, 15, 13, 12)}]
                },
                'device': 'my-device-3'
            },
            {
                'raw_data': {
                    '2016-02-03': [
                        {'device_id': 'my-device-7', 'resource_id': 'GSAD_4334', 'location_id': '3001',
                         'started_at': datetime.datetime(2016, 2, 3, 15, 43, 13),
                         'ended_at': datetime.datetime(2016, 2, 3, 15, 53, 13)},
                        {'device_id': 'my-device-7', 'resource_id': 'GSAD_5447', 'location_id': '3001',
                         'started_at': datetime.datetime(2016, 2, 3, 16, 3, 13),
                         'ended_at': datetime.datetime(2016, 2, 3, 16, 13, 13)},
                        {'device_id': 'my-device-7', 'resource_id': 'GSAD_2222', 'location_id': '3001',
                         'started_at': datetime.datetime(2016, 2, 3, 16, 13, 13),
                         'ended_at': datetime.datetime(2016, 2, 3, 16, 23, 13)}],
                    '2016-02-02': [
                        {'device_id': 'my-device-7', 'resource_id': 'GSAD_2222', 'location_id': '3001',
                         'started_at': datetime.datetime(2016, 2, 2, 15, 53, 12),
                         'ended_at': datetime.datetime(2016, 2, 2, 16, 3, 12)}],
                    '2016-02-01': [
                        {'device_id': 'my-device-7', 'resource_id': 'GSAD_2222', 'location_id': '3001',
                         'started_at': datetime.datetime(2016, 2, 1, 15, 3, 12),
                         'ended_at': datetime.datetime(2016, 2, 1, 15, 13, 12)},
                        {'device_id': 'my-device-7', 'resource_id': 'GSAD_5447', 'location_id': '3001',
                         'started_at': datetime.datetime(2016, 2, 1, 15, 23, 12),
                         'ended_at': datetime.datetime(2016, 2, 1, 15, 33, 12)},
                        {'device_id': 'my-device-7', 'resource_id': 'GSAD_4334', 'location_id': '3001',
                         'started_at': datetime.datetime(2016, 2, 1, 16, 3, 12),
                         'ended_at': datetime.datetime(2016, 2, 1, 16, 13, 12)},
                        {'device_id': 'my-device-7', 'resource_id': 'GSAD_4334', 'location_id': '3001',
                         'started_at': datetime.datetime(2016, 2, 1, 16, 13, 12),
                         'ended_at': datetime.datetime(2016, 2, 1, 16, 23, 12)}]
                },
                'device': 'my-device-7'
            }
        ]

        expected_result = OrderedDict([
            (
                'my-device-3',
                OrderedDict(
                    [
                        (
                            '2016-02-02', {
                                'GSAD_4334': {
                                    'playcount': 1, 'location': '1001'}}
                        )
                    ]
                )),
            (
                'my-device-7',
                OrderedDict(
                    [
                        (
                            '2016-02-01', {
                                'GSAD_4334': {
                                    'playcount': 2,
                                    'location': '3001'
                                },
                                'GSAD_2222': {
                                    'playcount': 1,
                                    'location': '3001'
                                },
                                'GSAD_5447': {
                                    'playcount': 1,
                                    'location': '3001'
                                }
                            }
                        ),
                        (
                            '2016-02-02', {
                                'GSAD_2222': {
                                    'playcount': 1,
                                    'location': '3001'
                                }
                            }
                        ),
                        (
                            '2016-02-03', {
                                'GSAD_4334': {
                                    'playcount': 1,
                                    'location': '3001'
                                },
                                'GSAD_2222': {
                                    'playcount': 1,
                                    'location': '3001'
                                },
                                'GSAD_5447': {
                                    'playcount': 1,
                                    'location': '3001'
                                }
                            }
                        )
                    ]
                )
            )
        ])

        result = prepare_transformed_query_by_device_to_csv_by_date(self.start_date, self.end_date, example_input)

        self.assertEqual(result, expected_result)

    def test_generate_device_csv_summarized(self):
        example_input = [
            {'content': 'GSAD_4334', 'display': 'my-device-3', 'location': '1001', 'playcount': 1},
            {'content': 'GSAD_2222', 'display': 'my-device-7', 'location': '3001', 'playcount': 3},
            {'content': 'GSAD_4334', 'display': 'my-device-7', 'location': '3001', 'playcount': 3},
            {'content': 'GSAD_5447', 'display': 'my-device-7', 'location': '3001', 'playcount': 2}
        ]
        now = str(datetime.datetime.now())

        expected_output = """Creation Date,Start Date,End Date,Displays\r\n{},2016-02-01,2016-02-03,"my-device-3, my-device-7"\r\nDisplay,Location,Content,Play Count\r\nmy-device-3,1001,GSAD_4334,1\r\nmy-device-7,3001,GSAD_2222,3\r\nmy-device-7,3001,GSAD_4334,3\r\nmy-device-7,3001,GSAD_5447,2\r\n""".format(
            now[:10])

        start_time = datetime.datetime.strptime("Feb 1 2016", '%b %d %Y')
        end_time = datetime.datetime.strptime("Feb 3 2016", '%b %d %Y')

        displays = ["my-device-3", "my-device-7"]
        self.assertEqual(generate_device_csv_summarized(start_time, end_time, displays, example_input, now).read(),
                         expected_output)

    def test_generate_device_csv_by_date(self):
        example_input = OrderedDict(
            [
                ('my-device-3',
                 OrderedDict(
                     [('2016-02-02', {'GSAD_4334': {'location': '1001', 'playcount': 1}})])),
                ('my-device-7',
                 OrderedDict(
                     [(
                         '2016-02-01',
                         {
                             'GSAD_5447': {
                                 'location': '3001',
                                 'playcount': 1},
                             'GSAD_4334': {
                                 'location': '3001',
                                 'playcount': 2},
                             'GSAD_2222': {
                                 'location': '3001',
                                 'playcount': 1}}),
                         (
                             '2016-02-02',
                             {
                                 'GSAD_2222': {
                                     'location': '3001',
                                     'playcount': 1}}),
                         (
                             '2016-02-03',
                             {
                                 'GSAD_5447': {
                                     'location': '3001',
                                     'playcount': 1},
                                 'GSAD_4334': {
                                     'location': '3001',
                                     'playcount': 1},
                                 'GSAD_2222': {
                                     'location': '3001',
                                     'playcount': 1}})]))]
        )

        now = str(datetime.datetime.now())
        devices = ["my-device-3", "my-device-7"]

        expected_result = 'Creation Date,Start Date,End Date,Displays\r\n{},2016-02-01,2016-02-03,"my-device-3, my-device-7"\r\nDisplay,Location,Date,Content,Play Count\r\nmy-device-3,1001,2016-02-02,GSAD_4334,1\r\nmy-device-7,3001,2016-02-01,GSAD_5447,1\r\nmy-device-7,3001,2016-02-01,GSAD_2222,1\r\nmy-device-7,3001,2016-02-01,GSAD_4334,2\r\nmy-device-7,3001,2016-02-02,GSAD_2222,1\r\nmy-device-7,3001,2016-02-03,GSAD_5447,1\r\nmy-device-7,3001,2016-02-03,GSAD_2222,1\r\nmy-device-7,3001,2016-02-03,GSAD_4334,1\r\n'.format(
            now[:10])

        start_time = datetime.datetime.strptime("Feb 1 2016", '%b %d %Y')
        end_time = datetime.datetime.strptime("Feb 3 2016", '%b %d %Y')

        self.assertEqual(generate_device_csv_by_date(now, start_time, end_time, devices, example_input).read(),
                         expected_result)

    def test_transform_db_data_to_by_location_then_resource(self):
        example_input = [
            {'resource_id': 'GSAD_2222', 'started_at': datetime.datetime(2016, 1, 1, 15, 53, 11), 'location_id': '3001',
             'device_id': 'my-device-9', 'ended_at': datetime.datetime(2016, 1, 1, 16, 3, 11)},
            {'resource_id': 'GSAD_2222', 'started_at': datetime.datetime(2016, 1, 2, 14, 53, 11), 'location_id': '3001',
             'device_id': 'my-device-8', 'ended_at': datetime.datetime(2016, 1, 2, 15, 3, 11)},
            {'resource_id': 'GSAD_5533', 'started_at': datetime.datetime(2016, 1, 2, 15, 13, 11), 'location_id': '3001',
             'device_id': 'my-device-7', 'ended_at': datetime.datetime(2016, 1, 2, 15, 23, 11)},
            {'resource_id': 'GSAD_2222', 'started_at': datetime.datetime(2016, 1, 2, 16, 3, 11), 'location_id': '3001',
             'device_id': 'my-device-9', 'ended_at': datetime.datetime(2016, 1, 2, 16, 13, 11)},
            {'resource_id': 'GSAD_5533', 'started_at': datetime.datetime(2016, 1, 3, 14, 53, 11), 'location_id': '3001',
             'device_id': 'my-device-8', 'ended_at': datetime.datetime(2016, 1, 3, 15, 3, 11)},
            {'resource_id': 'GSAD_5533', 'started_at': datetime.datetime(2016, 1, 3, 15, 33, 11), 'location_id': '3001',
             'device_id': 'my-device-8', 'ended_at': datetime.datetime(2016, 1, 3, 15, 43, 11)},
            {'resource_id': 'GSAD_4334', 'started_at': datetime.datetime(2016, 1, 3, 15, 43, 11), 'location_id': '3001',
             'device_id': 'my-device-8', 'ended_at': datetime.datetime(2016, 1, 3, 15, 53, 11)},
            {'resource_id': 'GSAD_4334', 'started_at': datetime.datetime(2016, 1, 3, 16, 3, 11), 'location_id': '3001',
             'device_id': 'my-device-7', 'ended_at': datetime.datetime(2016, 1, 3, 16, 13, 11)},
            {'resource_id': 'GSAD_4334', 'started_at': datetime.datetime(2016, 1, 3, 16, 13, 11), 'location_id': '3001',
             'device_id': 'my-device-9', 'ended_at': datetime.datetime(2016, 1, 3, 16, 23, 11)}
        ]

        expected_output = {'3001': OrderedDict([('GSAD_2222', [{'resource_id': 'GSAD_2222', 'device_id': 'my-device-9',
                                                                'ended_at': datetime.datetime(2016, 1, 1, 16, 3, 11),
                                                                'started_at': datetime.datetime(2016, 1, 1, 15, 53, 11),
                                                                'location_id': '3001'},
                                                               {'resource_id': 'GSAD_2222', 'device_id': 'my-device-8',
                                                                'ended_at': datetime.datetime(2016, 1, 2, 15, 3, 11),
                                                                'started_at': datetime.datetime(2016, 1, 2, 14, 53, 11),
                                                                'location_id': '3001'},
                                                               {'resource_id': 'GSAD_2222', 'device_id': 'my-device-9',
                                                                'ended_at': datetime.datetime(2016, 1, 2, 16, 13, 11),
                                                                'started_at': datetime.datetime(2016, 1, 2, 16, 3, 11),
                                                                'location_id': '3001'}]), ('GSAD_5533', [
            {'resource_id': 'GSAD_5533', 'device_id': 'my-device-7',
             'ended_at': datetime.datetime(2016, 1, 2, 15, 23, 11),
             'started_at': datetime.datetime(2016, 1, 2, 15, 13, 11), 'location_id': '3001'},
            {'resource_id': 'GSAD_5533', 'device_id': 'my-device-8',
             'ended_at': datetime.datetime(2016, 1, 3, 15, 3, 11),
             'started_at': datetime.datetime(2016, 1, 3, 14, 53, 11), 'location_id': '3001'},
            {'resource_id': 'GSAD_5533', 'device_id': 'my-device-8',
             'ended_at': datetime.datetime(2016, 1, 3, 15, 43, 11),
             'started_at': datetime.datetime(2016, 1, 3, 15, 33, 11), 'location_id': '3001'}]), ('GSAD_4334', [
            {'resource_id': 'GSAD_4334', 'device_id': 'my-device-8',
             'ended_at': datetime.datetime(2016, 1, 3, 15, 53, 11),
             'started_at': datetime.datetime(2016, 1, 3, 15, 43, 11), 'location_id': '3001'},
            {'resource_id': 'GSAD_4334', 'device_id': 'my-device-7',
             'ended_at': datetime.datetime(2016, 1, 3, 16, 13, 11),
             'started_at': datetime.datetime(2016, 1, 3, 16, 3, 11), 'location_id': '3001'},
            {'resource_id': 'GSAD_4334', 'device_id': 'my-device-9',
             'ended_at': datetime.datetime(2016, 1, 3, 16, 23, 11),
             'started_at': datetime.datetime(2016, 1, 3, 16, 13, 11), 'location_id': '3001'}])])}

        self.assertEqual(transform_db_data_to_by_location_then_resource(example_input), expected_output)

    def test_format_multi_location_by_device(self):
        example_input = {
            "raw_data": {
                "location-1": {
                    "resource-one": [{
                        "location_id": "my-customer-location-code",
                        "device_id": "my-customer-display-code",
                        "resource_id": "my-resource-name",
                        "started_at": datetime.datetime(2016, 1, 3, 16, 3, 11),
                        "ended_at": datetime.datetime(2016, 1, 3, 15, 53, 11)
                    }]
                }
            }
        }

        expected_output = {
            'location-1': OrderedDict([('resource-one', OrderedDict([('my-customer-display-code', 1)]))])}

        self.assertEqual(format_multi_location_by_device(example_input), expected_output)

    def test_format_multi_location_summarized(self):
        example_input = {
            "raw_data": {
                "location-1": {
                    "resource-one": [{
                        "location_id": "my-customer-location-code",
                        "device_id": "my-customer-display-code",
                        "resource_id": "my-resource-name",
                        "started_at": datetime.datetime(2016, 1, 3, 16, 3, 11),
                        "ended_at": datetime.datetime(2016, 1, 3, 15, 53, 11)
                    }]
                }
            }
        }

        expected_result = {'location-1': OrderedDict([('resource-one', 1)])}

        self.assertEqual(format_multi_location_summarized(example_input), expected_result)

    def test_generate_location_csv_summarized(self):
        example_input = {
            '3001': OrderedDict(
                [('GSAD_2222', 3), ('GSAD_5533', 3), ('GSAD_4334', 3)]),
            '1001': OrderedDict(
                [('GSAD_5447', 3), ('GSAD_2222', 4), ('GSAD_5533', 1), ('GSAD_5553', 2), ('GSAD_4334', 1)])}

        now = str(datetime.datetime.now())

        start_time = datetime.datetime.strptime("Feb 1 2016", '%b %d %Y')
        end_time = datetime.datetime.strptime("Feb 3 2016", '%b %d %Y')
        locations = ["1001", "3001"]

        expected_result = 'Creation Date,Start Date,End Date,Locations\r\n{},2016-02-01,2016-02-03,"1001, 3001"\r\nLocation,Content,Play Count\r\n3001,GSAD_2222,3\r\n3001,GSAD_5533,3\r\n3001,GSAD_4334,3\r\n1001,GSAD_5447,3\r\n1001,GSAD_2222,4\r\n1001,GSAD_5533,1\r\n1001,GSAD_5553,2\r\n1001,GSAD_4334,1\r\n'.format(
            now[:10])

        self.assertEqual(generate_location_csv_summarized(now, start_time, end_time, locations, example_input).read(),
                         expected_result)

    def test_generate_location_csv_by_device(self):
        example_input = {
            '3001': OrderedDict([('GSAD_2222', OrderedDict([('my-device-9', 2), ('my-device-8', 1)])),
                                 ('GSAD_5533', OrderedDict([('my-device-7', 1), ('my-device-8', 2)])), (
                                     'GSAD_4334', OrderedDict(
                                         [('my-device-8', 1), ('my-device-7', 1), ('my-device-9', 1)]))]),
            '1001': OrderedDict([('GSAD_5447', OrderedDict([('my-device-1', 1), ('my-device-3', 2)])), (
                'GSAD_2222', OrderedDict([('my-device-1', 2), ('my-device-2', 1), ('my-device-3', 1)])),
                                 ('GSAD_5533', OrderedDict([('my-device-2', 1)])),
                                 ('GSAD_5553', OrderedDict([('my-device-2', 1), ('my-device-3', 1)])),
                                 ('GSAD_4334', OrderedDict([('my-device-3', 1)]))])}

        now = str(datetime.datetime.now())

        start_time = datetime.datetime.strptime("Feb 1 2016", '%b %d %Y')
        end_time = datetime.datetime.strptime("Feb 3 2016", '%b %d %Y')
        locations = ["1001", "3001"]

        expected_result = 'Creation Date,Start Date,End Date,Locations\r\n{},2016-02-01,2016-02-03,"1001, 3001"\r\nLocation,Device,Content,Play Count\r\n3001,my-device-9,GSAD_2222,2\r\n3001,my-device-8,GSAD_2222,1\r\n3001,my-device-7,GSAD_5533,1\r\n3001,my-device-8,GSAD_5533,2\r\n3001,my-device-8,GSAD_4334,1\r\n3001,my-device-7,GSAD_4334,1\r\n3001,my-device-9,GSAD_4334,1\r\n1001,my-device-1,GSAD_5447,1\r\n1001,my-device-3,GSAD_5447,2\r\n1001,my-device-1,GSAD_2222,2\r\n1001,my-device-2,GSAD_2222,1\r\n1001,my-device-3,GSAD_2222,1\r\n1001,my-device-2,GSAD_5533,1\r\n1001,my-device-2,GSAD_5553,1\r\n1001,my-device-3,GSAD_5553,1\r\n1001,my-device-3,GSAD_4334,1\r\n'.format(
            now[:10])

        self.assertEqual(generate_location_csv_by_device(now, start_time, end_time, locations, example_input).read(),
                         expected_result)


if __name__ == '__main__':
    unittest.main()
