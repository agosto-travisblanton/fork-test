from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
import responses
import datetime
from proofplay.utils import join_array_of_strings, create_merged_dictionary, order_dictionary_with_datetimes_as_keys


class TestUtils(BaseTest):
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

    def test_join_array_of_string(self):
        example_array = ["test", "test2", "test3"]
        expected_result = "test;test2;test3;"
        self.assertEqual(expected_result, join_array_of_strings(example_array))

    def test_create_merged_dictionary(self):
        one_dict = {"one": "one_value"}
        two_dict = {"two": "two_value"}
        combined = create_merged_dictionary([one_dict, two_dict])

        expected_output = {
            "one": "one_value",
            "two": "two_value"
        }

        self.assertEqual(combined, expected_output)

    def test_order_dictionary_with_datetimes_as_keys(self):
        input = {
            '2016-01-08 00:00:00': {'LocationCount': 1, 'PlayCount': 1, 'PlayerCount': 1},
            '2016-01-23 00:00:00': {'LocationCount': 1, 'PlayCount': 2, 'PlayerCount': 1},
            '2016-01-21 00:00:00': {'LocationCount': 2, 'PlayCount': 2, 'PlayerCount': 2},
            '2016-01-16 00:00:00': {'LocationCount': 2, 'PlayCount': 2, 'PlayerCount': 2},
            '2016-01-24 00:00:00': {'LocationCount': 1, 'PlayCount': 1, 'PlayerCount': 1},
            '2016-01-12 00:00:00': {'LocationCount': 2, 'PlayCount': 2, 'PlayerCount': 2},
            '2016-01-20 00:00:00': {'LocationCount': 1, 'PlayCount': 1, 'PlayerCount': 1},
            '2016-01-10 00:00:00': {'LocationCount': 1, 'PlayCount': 2, 'PlayerCount': 2},
            '2016-01-26 00:00:00': {'LocationCount': 0, 'PlayCount': 0, 'PlayerCount': 0},
            '2016-01-15 00:00:00': {'LocationCount': 1, 'PlayCount': 2, 'PlayerCount': 2},
            '2016-01-25 00:00:00': {'LocationCount': 0, 'PlayCount': 0, 'PlayerCount': 0},
            '2016-01-22 00:00:00': {'LocationCount': 1, 'PlayCount': 1, 'PlayerCount': 1},
            '2016-01-09 00:00:00': {'LocationCount': 1, 'PlayCount': 2, 'PlayerCount': 1},
            '2016-01-11 00:00:00': {'LocationCount': 1, 'PlayCount': 1, 'PlayerCount': 1},
            '2016-01-18 00:00:00': {'LocationCount': 1, 'PlayCount': 2, 'PlayerCount': 1},
            '2016-01-17 00:00:00': {'LocationCount': 1, 'PlayCount': 1, 'PlayerCount': 1},
            '2016-01-14 00:00:00': {'LocationCount': 1, 'PlayCount': 2, 'PlayerCount': 2},
            '2016-01-13 00:00:00': {'LocationCount': 1, 'PlayCount': 2, 'PlayerCount': 1},
            '2016-01-19 00:00:00': {'LocationCount': 1, 'PlayCount': 1, 'PlayerCount': 1},
            '2016-01-27 00:00:00': {'LocationCount': 0, 'PlayCount': 0, 'PlayerCount': 0}
        }

        expected_output = [
            '2016-01-08 00:00:00', '2016-01-09 00:00:00', '2016-01-10 00:00:00', '2016-01-11 00:00:00',
            '2016-01-12 00:00:00', '2016-01-13 00:00:00', '2016-01-14 00:00:00', '2016-01-15 00:00:00',
            '2016-01-16 00:00:00', '2016-01-17 00:00:00', '2016-01-18 00:00:00', '2016-01-19 00:00:00',
            '2016-01-20 00:00:00', '2016-01-21 00:00:00', '2016-01-22 00:00:00', '2016-01-23 00:00:00',
            '2016-01-24 00:00:00', '2016-01-25 00:00:00', '2016-01-26 00:00:00', '2016-01-27 00:00:00'
        ]

        result = order_dictionary_with_datetimes_as_keys(input)
        self.assertEqual(expected_output, result)
