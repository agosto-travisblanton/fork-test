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

    def test_get_get_timezone_offset_returns_expected_offset_for_chicago(self):
        timezone_offset = TimezoneUtil.get_timezone_offset('America/Chicago')
        self.assertGreaterEqual(timezone_offset, self.CHICAGO_OFFSET_CST)
        self.assertLessEqual(timezone_offset, self.CHICAGO_OFFSET_CDT)

    def test_get_get_timezone_offset_returns_expected_offset_for_nyc(self):
        timezone_offset = TimezoneUtil.get_timezone_offset('America/New_York')
        self.assertGreaterEqual(timezone_offset, self.NYC_OFFSET_EST)
        self.assertLessEqual(timezone_offset, self.NYC_OFFSET_EDT)

    def test_get_get_timezone_offset_returns_expected_offset_for_phoenix(self):
        timezone_offset = TimezoneUtil.get_timezone_offset('America/Phoenix')
        self.assertLessEqual(timezone_offset, self.PHOENIX_OFFSET_MST)
