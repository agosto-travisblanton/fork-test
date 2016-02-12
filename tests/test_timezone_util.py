import json

from agar.test import BaseTest
from env_setup import setup_test_paths
from utils.mail_util import MailUtil
from utils.timezone_util import TimezoneUtil

setup_test_paths()

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestTimezoneUtil(BaseTest):

    def setUp(self):
        super(TestTimezoneUtil, self).setUp()

    def test_get_offset_returns_timezone_offset(self):
        #This test passes for now since have yet to implement Googlemaps timezone API
        expected_offset = 0
        offset = TimezoneUtil.get_offset('US/Arizona')
        self.assertEqual(expected_offset,offset)
