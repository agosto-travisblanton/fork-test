import datetime

import pytz.reference
import pytz.tzfile
import pytz.tzinfo

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TimezoneUtil(object):

    @staticmethod
    def get_timezone_offset(timezone):
        offset = datetime.datetime.now(pytz.timezone(timezone)).strftime('%z').replace('0', '')
        timezone_offset = int(offset)
        return timezone_offset

    @staticmethod
    def get_us_timezones():
        timezones = pytz.country_timezones['us']
        return timezones

    @staticmethod
    def get_all_common_timezones():
        timezones = pytz.common_timezones
        return timezones
