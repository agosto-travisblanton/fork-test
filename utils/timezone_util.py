import pytz.tzfile
import pytz.reference
import pytz.tzinfo
import datetime

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TimezoneUtil(object):

    @staticmethod
    def get_offset(timezone):

        tz = pytz.timezone(timezone)

        #Implement The Google Maps Time Zone API
        #https://developers.google.com/maps/documentation/timezone/intro
        #Google maps API Key AIzaSyBcZQf7qcJibJmBKHDaqgdRwf2XQ3MZFiY for Prod
        #Google maps API Key AIzaSyB0mE3DWNt8iFFvZ60TQyTgl3NpKK6-BQA for Stage
        #Google maps API Key AIzaSyAzS-hwl5dV-Wn4g5opG_34gGYplgJT1Fc for INT
        now = datetime.datetime.utcnow()

        tz_offset = tz.utcoffset(now)

        return 0

