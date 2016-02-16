from env_setup import setup_test_paths
setup_test_paths()

from agar.test import BaseTest
import unittest
import datetime

from proofplay.data_processing import (calculate_location_count, calculate_serial_count,
                                       get_total_play_count_of_resource_between_date_range_for_all_locations,
                                       generate_date_range_csv_by_date)


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


if __name__ == '__main__':
    unittest.main()
