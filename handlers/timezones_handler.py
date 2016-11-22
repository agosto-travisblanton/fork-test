from webapp2 import RequestHandler

from utils.auth_util import requires_auth
from restler.serializers import json_response
from utils.timezone_util import TimezoneUtil
from extended_session_request_handler import ExtendedSessionRequestHandler

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TimezonesHandler(ExtendedSessionRequestHandler):

    @requires_auth
    def get_us_timezones(self):
        result = TimezoneUtil.get_us_timezones()
        json_response(self.response, result)

    @requires_auth
    def get_all_common_timezones(self):
        result = TimezoneUtil.get_all_common_timezones()
        json_response(self.response, result)

    @requires_auth
    def get_custom_timezones(self):
        result = TimezoneUtil.get_custom_timezones()
        json_response(self.response, result)
