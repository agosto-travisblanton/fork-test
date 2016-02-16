from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
import unittest
import datetime

from proofplay.data_processing import (calculate_location_count, calculate_serial_count,
                                       get_total_play_count_of_resource_between_date_range_for_all_locations,
                                       generate_date_range_csv_by_date,
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


if __name__ == '__main__':
    unittest.main()
