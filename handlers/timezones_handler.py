from webapp2 import RequestHandler

from decorators import requires_api_token
from restler.serializers import json_response
from utils.timezone_util import TimezoneUtil

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TimezonesHandler(RequestHandler):
    @requires_api_token
    def get_us_timezones(self):
        result = TimezoneUtil.get_us_timezones()
        json_response(self.response, result)

    @requires_api_token
    def get_all_common_timezones(self):
        result = TimezoneUtil.get_all_common_timezones()
        json_response(self.response, result)
