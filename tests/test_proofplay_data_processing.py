from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
import unittest
import responses
import objects_for_testing
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

    # def test_get_total_play_count_of_resource_between_date_range_for_all_locations(self):
    #     raw_data = {
    #         '2014-12-02 00:00:00': [
    #             {'ended_at': datetime.datetime(2014, 12, 2, 9, 45, 34), 'resource_id': u'GSAD_5553',
    #              'location_id': u'6023',
    #              'started_at': datetime.datetime(2014, 12, 2, 9, 35, 34), 'device_id': u'F5MSCX001736'}],
    #         '2014-04-05 00:00:00': [],
    #         '2014-10-29 00:00:00': [
    #             {'ended_at': datetime.datetime(2014, 10, 29, 10, 45, 33), 'resource_id': u'GSAD_5553',
    #              'location_id': u'6023', 'started_at': datetime.datetime(2014, 10, 29, 10, 35, 33),
    #              'device_id': u'F5MSCX001736'}],
    #         '2015-01-18 00:00:00': [
    #             {'ended_at': datetime.datetime(2015, 1, 18, 11, 45, 35), 'resource_id': u'GSAD_5553',
    #              'location_id': u'6023',
    #              'started_at': datetime.datetime(2015, 1, 18, 11, 35, 35), 'device_id': u'F5MSCX001939'},
    #             {'ended_at': datetime.datetime(2015, 1, 18, 11, 45, 45), 'resource_id': u'GSAD_5553',
    #              'location_id': u'6024',
    #              'started_at': datetime.datetime(2015, 1, 18, 11, 35, 35), 'device_id': u'F5MSCX001559'}
    #         ],
    #
    #     }
    #
    #     resource = "some_resource"
    #
    #     expected_output = {
    #         resource: {
    #             '2014-12-02 00:00:00': {
    #                 "LocationCount": 1,
    #                 "PlayerCount": 1,
    #                 "PlayCount": 1
    #             },
    #             '2014-04-05 00:00:00': {
    #                 "LocationCount": 0,
    #                 "PlayerCount": 0,
    #                 "PlayCount": 0
    #             },
    #             '2014-10-29 00:00:00': {
    #                 "LocationCount": 1,
    #                 "PlayerCount": 1,
    #                 "PlayCount": 1
    #             },
    #             '2015-01-18 00:00:00': {
    #                 "LocationCount": 2,
    #                 "PlayerCount": 2,
    #                 "PlayCount": 2
    #             }
    #
    #         }
    #     }
    #
    #     self.assertEqual(get_total_play_count_of_resource_between_date_range_for_all_locations(
    #             {"raw_data": raw_data, "resource": resource}),
    #             expected_output
    #     )


if __name__ == '__main__':
    unittest.main()
