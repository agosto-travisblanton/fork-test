from agar.test import BaseTest
from env_setup import setup_test_paths
from utils.timezone_util import TimezoneUtil

setup_test_paths()

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestTimezoneUtil(BaseTest):
    CHICAGO_OFFSET_CST = -6
    CHICAGO_OFFSET_CDT = -5
    NYC_OFFSET_EST = -5
    NYC_OFFSET_EDT = -4
    PHOENIX_OFFSET_MST = -7

    def setUp(self):
        super(TestTimezoneUtil, self).setUp()

    def test_get_timezone_offset_returns_expected_offset_for_chicago(self):
        timezone_offset = TimezoneUtil.get_timezone_offset('America/Chicago')
        self.assertGreaterEqual(timezone_offset, self.CHICAGO_OFFSET_CST)
        self.assertLessEqual(timezone_offset, self.CHICAGO_OFFSET_CDT)

    def test_get_timezone_offset_returns_expected_offset_for_nyc(self):
        timezone_offset = TimezoneUtil.get_timezone_offset('America/New_York')
        self.assertGreaterEqual(timezone_offset, self.NYC_OFFSET_EST)
        self.assertLessEqual(timezone_offset, self.NYC_OFFSET_EDT)

    def test_get_timezone_offset_returns_expected_offset_for_phoenix(self):
        timezone_offset = TimezoneUtil.get_timezone_offset('America/Phoenix')
        self.assertLessEqual(timezone_offset, self.PHOENIX_OFFSET_MST)

    def test_get_timezone_offset_returns_expected_offset_for_athens(self):
        timezone_offset = TimezoneUtil.get_timezone_offset('Europe/Athens')
        self.assertGreaterEqual(timezone_offset, 2)
        self.assertLessEqual(timezone_offset, 3)

    def test_get_us_timezones_returns_array(self):
        timezones = TimezoneUtil.get_us_timezones()
        self.assertGreaterEqual(30,len(timezones))

    def test_get_all_common_timezones_returns_array(self):
        timezones = TimezoneUtil.get_all_common_timezones()
        self.assertGreaterEqual(400,len(timezones))

    def test_get_custom_timezones_returns_array(self):
        timezones = TimezoneUtil.get_custom_timezones()
        self.assertEqual(394,len(timezones))

    def test_get_custom_timezones_return_an_offset(self):
        timezones = TimezoneUtil.get_custom_timezones()
        for timezone in timezones:
            timezone_offset = TimezoneUtil.get_timezone_offset(timezone)
            self.assertTrue(isinstance(timezone_offset, int))

