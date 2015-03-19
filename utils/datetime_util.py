from datetime import datetime, timedelta
from random import choice
from dateutil import tz
from dateutil.tz import tzutc

CENTRAL_TZ = tz.gettz('US/Central')
UTC_TZ = tzutc()

US_DATETIME_FORMAT = "%m/%d/%Y %H:%M:%S"  # sanity lost
US_DATE_FORMAT = "%m/%d/%Y"

EU_DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"  # sanity restored
EU_DATE_FORMAT = "%d/%m/%Y"

MONDAY = "Monday"
TUESDAY = "Tuesday"
WEDNESDAY = "Wednesday"
THURSDAY = "Thursday"
FRIDAY = "Friday"
SATURDAY = "Saturday"
SUNDAY = "Sunday"

WEEKDAYS = [
    MONDAY,
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
    SATURDAY,
    SUNDAY
]

def convert_timezone(dt, to_zone):
    """
    Makes a datetime tz-aware, then converts it to the given timezone
    to_zone may be either a string (e.g. 'US/Central') or a tzinfo object
    If to_zone is not valid, date-time is converted to US/Central
    """
    if dt:
        if isinstance(to_zone, basestring) is True:
            to_zone = tz.gettz(to_zone)

        if to_zone is None:
            to_zone = CENTRAL_TZ

        if dt.tzinfo is None:
            tz_aware_time = dt.replace(tzinfo=UTC_TZ)
        else:
            tz_aware_time = dt

        converted_time = tz_aware_time.astimezone(tz=to_zone)

        return converted_time

    return None


def unix_time(dt):
    """
    Convert a datetime to seconds since 1/1/1970
    """
    if dt is None:
        return None

    epoch = datetime.utcfromtimestamp(0)
    if dt.tzinfo is not None:
        epoch = epoch.replace(tzinfo=UTC_TZ)

    delta = dt - epoch
    return int(delta.total_seconds())


def timedelta_in_days(time1, time2):
    """
    Calculates the duration delta between two datetime objects
    :returns duration: the calculated timedelta in days
    """
    duration = None

    if time1 is not None and time2 is not None:
        delta = time1 - time2  # create a datetime.timedelta object
        duration = delta.days

    return duration


def nullsafe_formatted_date(dt, date_format, default=''):
    if dt and date_format:
        return dt.strftime(date_format)
    return default


def is_us_timezone(timezone):
    return timezone and timezone.startswith('US/')


def unix_time_millis(dt):
    if dt:
        return unix_time(dt) * 1000
    return dt


def datetime_from_millis(millis):
    return datetime.utcfromtimestamp(long(millis) / 1000) if millis else None


def date_format_for_timezone(timezone):
    return US_DATE_FORMAT if is_us_timezone(timezone) else EU_DATE_FORMAT


def datetime_format_for_timezone(timezone):
    return US_DATETIME_FORMAT if is_us_timezone(timezone) else EU_DATETIME_FORMAT


def date_for_weekday(the_date, daynum):
    """
    Find the date for a particular day in the same week as the given date
    :param the_date: A date or datetie object
    :param daynum: day number (0=Monday, 6=Sunday)
    :return: The date adjusted to the particular day of that same week.
    """
    assert 0 <= daynum <= 6
    diff = daynum - the_date.weekday()
    return the_date + timedelta(days=diff)


def is_same_week(first, second):
    """
    Determime if the two dates/datetimes occur in the same calendar week (Monday-Sunday
    :param first:
    :param second:
    :return:
    """
    date1 = first.date() if type(first) is datetime else first
    date2 = second.date() if type(second) is datetime else second
    return date1.isocalendar()[1] == date2.isocalendar()[1]


