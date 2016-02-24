import datetime

import pytz.reference
import pytz.tzfile
import pytz.tzinfo

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TimezoneUtil(object):

    @staticmethod
    def get_timezone_offset(timezone):
        zone = pytz.timezone(timezone)
        now = datetime.datetime.utcnow()
        timezone_offset = int(zone.utcoffset(now).total_seconds()/3600)
        return timezone_offset

    @staticmethod
    def get_us_timezones():
        timezones = pytz.country_timezones['us']
        return timezones
