from random import choice
import sys
import logging
from datetime import timedelta, datetime
from collections import namedtuple
from operator import attrgetter
import itertools
import uuid

from google.appengine.ext import ndb
from google.appengine.ext.deferred import deferred

import cloudstorage as gcs
from dateutil.relativedelta import relativedelta
from restler.decorators import ae_ndb_serializer
from utils.datetime_util import CENTRAL_TZ, UTC_TZ, is_same_week, date_for_weekday, WEEKDAYS, TUESDAY
from utils.image_util import PORTRAIT, create_wheel_schematic
from app_config import config
from i18n_util import SUPPORTED_LANGUAGES
from utils.conversion_util import CELSIUS_UNIT, FAHRENHEIT_UNIT, PSI_UNIT, BAR_UNIT
from utils.iterable_util import flatten, index_of
from utils.url_sign import sign_cloud_storage_url
from agar.env import on_development_server, on_server
from utils.web_util import build_uri
import models_db
import numpy
from utils.domain_conversion_util import normalize_pressures_metric, haversine


TEMPERATURE_UNITS = [CELSIUS_UNIT, FAHRENHEIT_UNIT]
PRESSURE_UNITS = [BAR_UNIT, PSI_UNIT]

NTS_REPORT_TYPE = "nts"
NTV_REPORT_TYPE = "ntv"
INFLATION_REPORT_TYPE = "ir"
CSV_REPORT_TYPE = "csv"

REPORT_TYPES = [NTS_REPORT_TYPE, NTV_REPORT_TYPE, INFLATION_REPORT_TYPE, CSV_REPORT_TYPE]
SCHEDULED_REPORT_TYPES = [NTS_REPORT_TYPE, NTV_REPORT_TYPE, INFLATION_REPORT_TYPE]

DAILY = 'daily'
WEEKLY = 'weekly'
MONTHLY = 'monthly'
REPORT_FREQUENCIES = [DAILY, WEEKLY, MONTHLY]

# defaults for scheduled reports
DEFAULT_WEEKDAY = WEEKDAYS.index(TUESDAY)  # 0=Monday, 1=Tuesday
DEFAULT_MONTHDAY = 1  # first of the month

VEHICLE_TRAILER = 'trailer'
VEHICLE_TRACTOR = 'tractor'
VEHICLE_OTHER = 'other'
VEHICLE_TYPES = [VEHICLE_TRAILER, VEHICLE_TRACTOR, VEHICLE_OTHER]

RED = 'red'
YELLOW = 'yellow'
GREEN = 'green'

COLOR_LEVELS = {
    GREEN: 0,
    YELLOW: 1,
    RED: 2
}

THRESHOLD_COLORS = [GREEN, YELLOW, RED]

PRESSURE_NATURE = 'pressure'
TEMPERATURE_NATURE = 'temperature'
LEAK_NATURE = 'leak'

NATURES = [PRESSURE_NATURE, TEMPERATURE_NATURE, LEAK_NATURE]

INFLATION_HISTORY_DAYS = 30


# ############## "State" types for content download ###############

STATE_IN_PROGRESS = "loading"
STATE_SUCCESS = "created"
STATE_SUCCESS_NO_REPORT = "no_report"
STATE_ERROR = "error"

REPORT_STATES = [STATE_SUCCESS, STATE_IN_PROGRESS, STATE_ERROR, STATE_SUCCESS_NO_REPORT]

ReportMetadata = namedtuple('ReportMetadata', 'content_type file_extension')
REPORT_METADATA = {
    NTV_REPORT_TYPE: ReportMetadata("application/pdf", 'pdf'),
    NTS_REPORT_TYPE: ReportMetadata("application/pdf", 'pdf'),
    INFLATION_REPORT_TYPE: ReportMetadata("application/pdf", 'pdf'),
    CSV_REPORT_TYPE: ReportMetadata("text/csv", 'csv'),
}

@ae_ndb_serializer
class TelemetryProvider(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    name = ndb.StringProperty(required=True)
    name_lower = ndb.ComputedProperty(lambda self: self.name.lower())

    @classmethod
    def get_by_name(cls, name):
        if name:
            provider_key = TelemetryProvider.query(TelemetryProvider.name_lower == name.lower()).get(keys_only=True)
            if None is not provider_key:
                return provider_key.get()


@ae_ndb_serializer
class Tenant(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    name = ndb.StringProperty(required=True)
    name_lower = ndb.ComputedProperty(lambda self: self.name.lower())

    @classmethod
    def get_by_name(cls, name):
        if name:
            t_key = Tenant.query(Tenant.name_lower == name.lower()).get(keys_only=True)
            if None is not t_key:
                return t_key.get()

    @property
    def customers(self):
        query = Customer.query(Customer.tenant_key == self.key)
        keys = query.fetch(keys_only=True)
        return ndb.get_multi(keys)


@ae_ndb_serializer
class Address(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    street1 = ndb.StringProperty()
    street2 = ndb.StringProperty()
    city = ndb.StringProperty()
    state_region = ndb.StringProperty()
    country = ndb.StringProperty()
    postal_code = ndb.StringProperty()

    @classmethod
    def create_or_update_from_json(cls, address_json, address=None):
        if address is None:
            address = Address()
        address.street1 = address_json.get('street1')
        address.street2 = address_json.get('street2')
        address.city = address_json.get('city')
        address.state_region = address_json.get('state_region')
        address.country = address_json.get('country')
        address.postal_code = address_json.get('postal_code')
        address.put()
        return address


@ae_ndb_serializer
class Customer(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    name = ndb.StringProperty(required=True)
    name_lower = ndb.ComputedProperty(lambda self: self.name.lower())
    tenant_key = ndb.KeyProperty(kind=Tenant, required=True)
    address_key = ndb.KeyProperty(kind=Address)
    contact_person = ndb.StringProperty(required=True)
    contact_email = ndb.StringProperty(required=True)
    phone_number = ndb.StringProperty(required=True)
    pkey = ndb.StringProperty()  # for FleetHQ
    class_version = ndb.IntegerProperty()

    def _pre_put_hook(self):
        self.class_version = 1

    @classmethod
    def get_by_name(cls, tenant_key, name):
        if tenant_key and name:
            query = Customer.query(Customer.tenant_key == tenant_key)
            query = query.filter(Customer.name_lower == name.lower())
            customer_key = query.get(keys_only=True)
            if None is not customer_key:
                return customer_key.get()

    @classmethod
    def get_by_customer_id(cls, telemetry_provider_key, customer_id):
        query = TelemetryCustomer.query(TelemetryCustomer.telemetry_provider_key == telemetry_provider_key)
        query = query.filter(TelemetryCustomer.customer_id == customer_id)
        telemetry_customer_key = query.get(keys_only=True)
        if None is not telemetry_customer_key:
            telemetry_customer = telemetry_customer_key.get()
            if None is not telemetry_customer:
                return telemetry_customer.customer_key.get()

    def is_duplicate_name(self, name):
        if name == self.name:
            return False

        existing_customer = Customer.get_by_name(self.tenant_key, name)
        return existing_customer is not None

    def get_threshold_set(self, vehicle_template_key):
        return ThresholdSet.get_by_owner_and_template(self.key, vehicle_template_key)

    @property
    def telemetry_customers(self):
        query = TelemetryCustomer.query(TelemetryCustomer.customer_key == self.key)
        keys = query.fetch(keys_only=True)
        return ndb.get_multi(keys)

    @property
    def tenant(self):
        return self.tenant_key.get()

    @property
    def entity_owner_key(self):
        """ Gets this entity's parent; i.e. its Tenant """
        return self.tenant_key

    @property
    def address(self):
        return self.address_key.get() if self.address_key else None


@ae_ndb_serializer
class TelemetryCustomer(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    telemetry_provider_key = ndb.KeyProperty(kind=TelemetryProvider, required=True)
    customer_key = ndb.KeyProperty(kind=Customer, required=True)
    customer_id = ndb.StringProperty(required=True)

    @classmethod
    def get_by_customer_id(cls, telemetry_provider_key, customer_id):
        query = TelemetryCustomer.query(TelemetryCustomer.telemetry_provider_key == telemetry_provider_key)
        query = query.filter(TelemetryCustomer.customer_id == customer_id)
        t_customer_key = query.get(keys_only=True)
        if None is not t_customer_key:
            return t_customer_key.get()


@ae_ndb_serializer
class VehicleTemplate(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    telemetry_provider_key = ndb.KeyProperty(kind=TelemetryProvider, required=True)
    name = ndb.StringProperty(required=True)
    name_lower = ndb.ComputedProperty(lambda self: self.name.lower())
    type = ndb.StringProperty(choices=VEHICLE_TYPES, required=True)

    @classmethod
    def get_by_name(cls, telemetry_provider_key, name):
        query = VehicleTemplate.query(VehicleTemplate.telemetry_provider_key == telemetry_provider_key)
        query = query.filter(VehicleTemplate.name_lower == name.lower())
        template_key = query.get(keys_only=True)
        if None is not template_key:
            return template_key.get()

    @property
    def telemetry_provider(self):
        return self.telemetry_provider_key.get()

    @property
    def axle_positions(self):
        ns = self.key.namespace()
        query = AxlePosition.query(AxlePosition.vehicle_template_key == self.key, namespace=ns).order(AxlePosition.sequence)
        axle_keys = query.fetch(keys_only=True)
        return ndb.get_multi(axle_keys)

    def get_axle(self, sequence):
        ns = self.key.namespace()
        query = AxlePosition.query(AxlePosition.vehicle_template_key == self.key, namespace=ns).filter(
            AxlePosition.sequence == sequence)
        axle_position_key = query.get(keys_only=True)
        return axle_position_key.get() if axle_position_key else None

    @property
    def wheel_positions(self):
        '''
        :return:all wheel_positions on the vehicle
        '''
        positions = []
        for axle_position in self.axle_positions:
            positions.extend(axle_position.wheel_positions)
        return positions


@ae_ndb_serializer
class AxlePosition(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    vehicle_template_key = ndb.KeyProperty(kind=VehicleTemplate, required=True)
    sequence = ndb.IntegerProperty(required=True)  # sequence from front of vehicle.  e.g. 1 = front axle

    # tire info (applies to tires on the axle), used by Fleet HQ
    width = ndb.IntegerProperty()  # in mm
    diameter = ndb.FloatProperty() # in inches (way to be consistent!)
    aspect_ratio = ndb.IntegerProperty()
    radial_bias_flag = ndb.StringProperty()  # R=Radial

    @property
    def wheel_positions(self):
        ns = self.key.namespace()
        query = WheelPosition.query(WheelPosition.axle_position_key == self.key, namespace=ns)
        query = query.order(WheelPosition.sequence)
        wheel_position_keys = query.fetch(keys_only=True)
        return sorted(ndb.get_multi(wheel_position_keys), key=lambda wheel_position: wheel_position.sequence)

    def get_wheel_position(self, sequence):
        ns = self.key.namespace()
        query = WheelPosition.query(WheelPosition.axle_position_key == self.key, namespace=ns)
        query = query.filter(WheelPosition.sequence == sequence)
        wheel_position_key = query.get(keys_only=True)
        return wheel_position_key.get() if wheel_position_key is not None else None


@ae_ndb_serializer
class WheelPosition(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    axle_position_key = ndb.KeyProperty(kind=AxlePosition)  # TODO: make required after migrations
    sequence = ndb.IntegerProperty(required=True)  # sequence from left to right, starts at 1
    temperature_label = ndb.StringProperty(required=True)
    pressure_label = ndb.StringProperty(required=True)
    position_label = ndb.StringProperty(required=True)

    vehicle_template_key = ndb.ComputedProperty(
        lambda self: self.axle_position.vehicle_template_key if self.axle_position is not None else None)

    @property
    def axle_position(self):
        return self.axle_position_key.get() if self.axle_position_key else None  # once required, shouldn't need this if

    def threshold_set_for(self, owner_key):
        return ThresholdSet.find_by_owner_and_template(owner_key, self.vehicle_template_key,
            wheel_position_key=self.key)

    def threshold_range_set_for(self, nature, owner_key):
        return ThresholdRangeSet.find_by_owner_and_template(nature, owner_key, self.vehicle_template_key,
            wheel_position_key=self.key)


@ae_ndb_serializer
class PersonLanguage(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    email = ndb.StringProperty(required=True)
    language = ndb.StringProperty(required=True, choices=SUPPORTED_LANGUAGES)

    @classmethod
    def get_by_email_and_language(cls, email, language):
        return cls.query().filter(cls.email == email).filter(cls.language == language).get()


@ae_ndb_serializer
class VehicleGroup(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    customer_key = ndb.KeyProperty(kind=Customer, required=True)
    name = ndb.StringProperty(required=True)
    name_lower = ndb.ComputedProperty(lambda self: self.name.lower())
    address_key = ndb.KeyProperty(kind=Address)
    contact_keys = ndb.KeyProperty(kind=PersonLanguage, repeated=True, indexed=False)
    group_type_description = ndb.StringProperty(required=True)
    timezone = ndb.StringProperty(required=True)
    temperature_unit = ndb.StringProperty(required=True, choices=TEMPERATURE_UNITS)
    pressure_unit = ndb.StringProperty(required=True, choices=PRESSURE_UNITS)

    @classmethod
    def get_by_name(cls, customer_key, name):
        if customer_key and name:
            query = VehicleGroup.query(VehicleGroup.customer_key == customer_key)
            query = query.filter(VehicleGroup.name_lower == name.lower())
            vehicle_group_key = query.get(keys_only=True)
            if None is not vehicle_group_key:
                return vehicle_group_key.get()

    @property
    def customer(self):
        return self.customer_key.get()

    @property
    def entity_owner_key(self):
        """ Gets this entitys parent; i.e. it's Customer """
        return self.customer_key

    @property
    def vehicles(self):
        # NOTE: Inflation report depends on sorting by vehicle tag
        query = Vehicle.query(Vehicle.vehicle_group_key == self.key).order(Vehicle.vehicle_tag)
        vehicle_keys = query.fetch(keys_only=True)
        return ndb.get_multi(vehicle_keys)

    @property
    def address(self):
        return self.address_key.get() if self.address_key else None

    @property
    def contacts(self):
        return ndb.get_multi(self.contact_keys) if self.contact_keys else []

    @property
    def report_schedules(self):
        schedules = ReportSchedule.find_by_vehicle_group(self)
        existing_report_types = [report.report_type for report in schedules]
        for report_type in SCHEDULED_REPORT_TYPES:
            if report_type not in existing_report_types:
                schedules.append(ReportSchedule(report_type=report_type))

        schedules = sorted(schedules, key=lambda r: r.report_type)

        return schedules

    @property
    def leak_threshold_set(self):
        return ThresholdRangeSet.get_leak_threshold_by_group(self.key)


@ae_ndb_serializer
class ReportSchedule(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    vehicle_group_key = ndb.KeyProperty(kind=VehicleGroup, required=True)
    report_type = ndb.StringProperty(required=True, choices=SCHEDULED_REPORT_TYPES)
    frequency = ndb.StringProperty(required=True, choices=REPORT_FREQUENCIES)
    scheduled_run = ndb.DateTimeProperty()

    @classmethod
    def _random_time(self, on_date):
        """
        Pick a random time during the preferred off-hours-schedule on the given date
        :param on_date: the datetime object on which to pick a random time
        :return: a datetime object representing the random time on the given date
        """
        random_hour = choice(range(config.SCHEDULE_REPORT_WINDOW_START, config.SCHEDULE_REPORT_WINDOW_STOP))
        random_minute = choice(range(1, 59))
        return on_date.replace(hour=random_hour, minute=random_minute)

    @classmethod
    def find_by_vehicle_group(cls, vehicle_group, keys_only=False):
        keys = cls.query(cls.vehicle_group_key == vehicle_group.key).fetch(keys_only=True)
        return keys if keys_only else ndb.get_multi(keys)

    @classmethod
    def find_reports_to_be_scheduled(cls):
        now = datetime.now()
        query = cls.query().filter(ndb.OR(cls.scheduled_run == None, cls.scheduled_run <= now))
        keys = query.fetch(keys_only=True)
        return ndb.get_multi(keys)

    def calculate_next_scheduled_run(self):
        now = datetime.now()

        if self.scheduled_run is not None and self.scheduled_run > now:
            return self.scheduled_run

        utc_now = now.replace(tzinfo=UTC_TZ)
        central_now = utc_now.astimezone(CENTRAL_TZ)
        central_scheduled_run = self.scheduled_run.replace(tzinfo=UTC_TZ).astimezone(
            CENTRAL_TZ) if self.scheduled_run else None

        if self.frequency == DAILY:
            if self.scheduled_run is not None:
                # schedule for same time tomorrow
                utc_scheduled_time = self.scheduled_run + timedelta(days=1)
            else:
                if central_now.hour > config.SCHEDULE_REPORT_WINDOW_START:
                    # it's already after 5pm, scheduled for tomorrow
                    central_scheduled_time = central_now + timedelta(days=1)
                else:
                    central_scheduled_time = central_now
                central_scheduled_time = self._random_time(central_scheduled_time)
                utc_scheduled_time = central_scheduled_time.astimezone(UTC_TZ)

        elif self.frequency == WEEKLY:
            if self.scheduled_run is not None and is_same_week(central_scheduled_run, central_now):
                # already ran this week, schedule for same time next week
                utc_scheduled_time = self.scheduled_run + timedelta(days=7)
            else:
                weekday = DEFAULT_WEEKDAY
                if weekday < central_now.weekday() or central_now.hour > config.SCHEDULE_REPORT_WINDOW_START:
                    # we've already passed the day for this week, schedule for next week
                    central_scheduled_time = date_for_weekday(central_now + timedelta(days=7), weekday)
                else:
                    central_scheduled_time = date_for_weekday(central_now, weekday)

                central_scheduled_time = self._random_time(central_scheduled_time)
                utc_scheduled_time = central_scheduled_time.astimezone(UTC_TZ)

        elif self.frequency == MONTHLY:
            if self.scheduled_run is not None:
                utc_scheduled_time = self.scheduled_run + relativedelta(months=1)
            else:
                monthday = DEFAULT_MONTHDAY
                if monthday < central_now.day or central_now.hour > config.SCHEDULE_REPORT_WINDOW_START:
                    # we've already passed the day for this month, schedule for next month
                    central_scheduled_time = central_now + relativedelta(months=1)
                    central_scheduled_time = central_scheduled_time.replace(day=DEFAULT_MONTHDAY)
                else:
                    central_scheduled_time = central_now.replace(day=DEFAULT_MONTHDAY)

                central_scheduled_time = self._random_time(central_scheduled_time)
                utc_scheduled_time = central_scheduled_time.astimezone(UTC_TZ)
        else:
            raise Exception('Invalid frequency: {}'.format(self.frequency))

        # change back to UTC and then back to naive timestamp
        return utc_scheduled_time.replace(tzinfo=None)

    @property
    def tenant_key(self):
        vehicle_group = self.vehicle_group_key.get()
        customer = vehicle_group.customer_key.get()
        return customer.tenant_key

    @property
    def vehicle_group(self):
        return self.vehicle_group_key.get()


@ae_ndb_serializer
class Vehicle(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    class_version = ndb.IntegerProperty()

    vehicle_group_key = ndb.KeyProperty(kind=VehicleGroup, required=True)
    vehicle_template_key = ndb.KeyProperty(kind=VehicleTemplate, required=True)
    vehicle_id = ndb.StringProperty(required=True)
    vehicle_tag = ndb.StringProperty()
    is_attached_unit = ndb.BooleanProperty(default=False)

    telemetry_provider_key = ndb.ComputedProperty(
        lambda self: self.vehicle_template.telemetry_provider_key if self.vehicle_template is not None else None)

    # data used for GY reference only.  displayed in UI but not used anywhere else
    metadata = ndb.JsonProperty()

    def _pre_put_hook(self):
        self.class_version = 2

    def _post_put_hook(self, future):
        vehicle_key = future.get_result()
        configure_vehicle_thresholds(vehicle_key, self.vehicle_template_key)

    @classmethod
    def _pre_delete_hook(cls, key):
        # delete references

        delete_entities_with_reference(VehicleEvent, 'vehicle_key', key)
        delete_entities_with_reference(Incident, 'vehicle_key', key)
        delete_entities_with_reference(ThresholdSet, 'owner_key', key)
        delete_entities_with_reference(ThresholdRangeSet, 'owner_key', key)

    @classmethod
    def get_by_vehicle_id(cls, telemetry_provider_key, vehicle_id):
        if telemetry_provider_key and vehicle_id:
            query = Vehicle.query(Vehicle.telemetry_provider_key == telemetry_provider_key)
            query = query.filter(Vehicle.vehicle_id == vehicle_id)
            vehicle_key = query.get(keys_only=True)
            if None is not vehicle_key:
                return vehicle_key.get()

    @property
    def vehicle_group(self):
        return self.vehicle_group_key.get()

    @property
    def wheel_positions(self):
        return self.vehicle_template.wheel_positions

    @property
    def axle_positions(self):
        return self.vehicle_template.axle_positions

    def get_wheel_position_by_pressure_label(self, pressure_label):
        wheel_position = next((w for w in self.wheel_positions if w.pressure_label == pressure_label), None)
        return wheel_position

    def get_wheel_position_by_temperature_label(self, temperature_label):
        wheel_position = next((w for w in self.wheel_positions if w.temperature_label == temperature_label), None)
        return wheel_position

    @property
    def vehicle_template(self):
        return self.vehicle_template_key.get()

    @property
    def telemetry_provider(self):
        return self.telemetry_provider_key.get() if self.telemetry_provider_key else None

    @property
    def entity_owner_key(self):
        """ Gets this entity's parent; i.e. its VehicleGroup """
        return self.vehicle_group_key

    def get_most_recent_sensor_readings(self, wheel_position, count, end_time=None, pressure_required=False,
            temperature_required=False):
        query = SensorReading.query(SensorReading.vehicle_key == self.key)
        query = query.filter(SensorReading.wheel_position_key == wheel_position.key)
        if pressure_required or temperature_required:
            if pressure_required:
                query = query.filter(SensorReading.has_pressure == True)
            if temperature_required:
                query = query.filter(SensorReading.has_temperature == True)
        else:
            query = query.filter(SensorReading.has_values == True)  # has pressure and/OR temperature
        if end_time is not None:
            query = query.filter(SensorReading.computed_event_timestamp <= end_time)
        query = query.order(-SensorReading.computed_event_timestamp)
        reading_keys = query.fetch(count, keys_only=True)
        return [reading_key.get() for reading_key in reading_keys]

    def get_most_recent_sensor_reading(self, wheel_position, end_time=None, pressure_required=False,
            temperature_required=False):
        readings = self.get_most_recent_sensor_readings(wheel_position, 1, end_time, pressure_required,
            temperature_required)
        return readings[0] if len(readings) != 0 else None

    def get_most_recent_event_with_readings(self, end_time):
        events = self.get_most_recent_events_with_readings(end_time, 1)
        return events[0] if events is not None and len(events) != 0 else None

    def get_most_recent_events_with_readings(self, end_time, count):
        """ Retrieves <count> of the most recent events for the vehicle, skipping over events with no sensor readings
        and readings with no values.

        One way to do this would be to query for VehicleEvents, check if any of the events don't have sensor readings,
        then query for more events if we don't find enough.  Unfortunately this process would potentially need to be
        repeated multiple times, with the worst case being that the entire event history is traversed.  This results in
        worst-case behavior that is proportional to the number of events in the vehicle's history.

        Another solution (implemented here) would be to first look at SensorReadings then link the readings back to the
        events:  accumulate a list of readings for all sensors, get a timestamp-sorted list of events that belong to
        those readings, then remove duplicates.  This results in worst-case behavior that is proportional to the
        number of sensors on the vehicle.
        """
        wheel_positions = self.wheel_positions
        readings = []
        for wheel_position in wheel_positions:
            wheel_readings = SensorReading.find_history_by_vehicle_wheel(self.key, wheel_position.key,
                newest_event_time=end_time, count=count)
            readings.extend(wheel_readings)

        events = [reading.event for reading in readings]
        events = sorted(events, key=attrgetter('computed_event_timestamp'), reverse=True)
        events = list(k for k, _ in itertools.groupby(events))
        return events[:count]

    def _get_sensor_history_keys(self, end_time):
        """
        Returns day sensor history for a vehicle, from most recent to oldest, excluding readings that have both
        temperature and pressure values missing.
        """
        start_time = end_time - timedelta(days=INFLATION_HISTORY_DAYS)
        query = models_db.SensorReading.all(keys_only=True)
        query = query.filter('vehicle_key =', self.key.to_old_key())
        query = query.filter('has_values =', True)
        query = query.filter('computed_event_timestamp >=', start_time)
        query = query.filter('computed_event_timestamp <=', end_time)
        query = query.order('-computed_event_timestamp')
        keys = [ndb.Key.from_old_key(r) for r in query.run()]
        return keys

    @classmethod
    def _detect_transmitting_sensors_from_sensor_history(cls, sensor_history_keys):
        wheel_position_keys = []
        if len(sensor_history_keys) != 0:
            readings = ndb.get_multi(sensor_history_keys)
            most_recent_timestamp = readings[0].computed_event_timestamp
            cutoff_time = most_recent_timestamp - timedelta(days=2)
            wheel_position_keys = [reading.wheel_position_key for reading in readings if
                reading.computed_event_timestamp >= cutoff_time]

        return set(wheel_position_keys)

    @classmethod
    def _detect_transmitting_sensors_from_vehicle_events(cls, vehicle_events):
        return set([reading.wheel_position_key for reading in flatten([event.sensor_readings for event in
            vehicle_events]) if reading.has_values])

    @classmethod
    def _skip_readings_with_same_location(cls, sensor_history_keys, index):
        if index >= len(sensor_history_keys):
            return -1
        latest = sensor_history_keys[index].get()
        prev = latest
        for i in range(index + 1, len(sensor_history_keys)):
            earliest = sensor_history_keys[i].get()
            if latest.location is not None and earliest.location is not None:
                dist_feet = haversine(earliest.location.lon, earliest.location.lat, latest.location.lon,
                    latest.location.lat)
            else:
                dist_feet = None
            changed = (dist_feet is None or dist_feet >= 200 or
                prev.computed_event_timestamp - earliest.computed_event_timestamp >= timedelta(hours=3))
            if changed:
                return i - 1
            prev = earliest
        return len(sensor_history_keys) - 1

    @classmethod
    def _find_stationary_interval(cls, sensor_history_keys, window_end_time, prev_start_index=-1):
        """ Finds a pair of indices into a sensor history corresponding to the start and end of a stationary interval
        (a gap of three hours or longer between readings or a set of readings with negligible GPS location changes).

        Mathematically speaking, find an interval T that spans three or more hours and for which time 't' in T
        satisfies

           sensor_history[start_index].timestamp <= t < sensor_history[end_index].timestamp

        (where timestamp refers to the computed event timestamp).  Return the interval T in terms of start_index and
        end_index.

        This method is greedy in that it goes back as far as possible to find the largest region of inactivity (as
        compared to stopping as soon as a three hour window is found), allowing the method to be called in an iterative
        manner to find all of the intervals of inactivity.
        """
        if len(sensor_history_keys) != 0 and prev_start_index < len(sensor_history_keys):
            end_index = prev_start_index
            if end_index != -1:
                end_time = sensor_history_keys[end_index].get().computed_event_timestamp
            else:
                end_time = window_end_time

            while True:
                start_index = end_index + 1
                if start_index >= len(sensor_history_keys):
                    # Edge-case: earliest event in sensor history may have a three hour gap before it, in which case the
                    # start index is just outside the sensor history.
                    if (sensor_history_keys[-1].get().computed_event_timestamp >=
                            window_end_time - timedelta(days=INFLATION_HISTORY_DAYS) + timedelta(hours=3)):
                       return len(sensor_history_keys), end_index
                    break

                adjusted_start_index = cls._skip_readings_with_same_location(sensor_history_keys, start_index)
                assert adjusted_start_index >= 0 and adjusted_start_index < len(sensor_history_keys)
                assert adjusted_start_index >= start_index
                adjusted_start_time = sensor_history_keys[adjusted_start_index].get().computed_event_timestamp

                if end_index != -1 and end_time - adjusted_start_time >= timedelta(hours=3):
                    return adjusted_start_index, end_index

                end_index = adjusted_start_index
                end_time = adjusted_start_time

        return -1, -1

    @classmethod
    def _get_sensor_history_key_subset(cls, sensor_history_keys, start_time, end_time):
        """
        Return subset of sensor history that's between start_time and end_time (inclusive).
        """
        first_in_timeframe_func = lambda reading_key: reading_key.get().computed_event_timestamp <= end_time
        start_index = index_of(first_in_timeframe_func, sensor_history_keys)
        if start_index is not None:
            first_outside_timeframe_func = lambda reading_key: reading_key.get().computed_event_timestamp < start_time
            end_index = index_of(first_outside_timeframe_func, sensor_history_keys, start=start_index)
            return sensor_history_keys[start_index: end_index]

        return []

    @classmethod
    def _get_first_temperature_reading_for_sensor(cls, sensor_history_keys, wheel_position_key):
        return next((reading_key.get() for reading_key in reversed(sensor_history_keys) if
            reading_key.get().wheel_position_key == wheel_position_key and reading_key.get().temperature is not None),
            None)

    @classmethod
    def _populate_wheel_map(cls, fifteen_minute_sensor_history_keys, wheel_map):
        """ Populate any missing values from wheel_map with earliest cold-inflation readings within 15-minute window.
        """
        for wheel_position_key in wheel_map:
            if wheel_map[wheel_position_key] is None:
                wheel_map[wheel_position_key] = Vehicle._get_first_temperature_reading_for_sensor(
                    fifteen_minute_sensor_history_keys, wheel_position_key)

    def get_cold_inflation_readings(self, end_time):
        """
        Return a dict of the last cold-inflation pressure readings, indexed by wheel_position key, excluding
        non-transmitting sensors.

        Note that there's a subtle case where a sensor may not be considered non-transmitting because it has sensor
        values within a 2-day window, yet not have any values that are considered for cold-inflation readings; while
        non-transmitting sensors are excluded from the result dict, transmitting sensors with no cold-inflation values
        are marked with None in the corresponding result dict entry.
        """
        sensor_history_keys = self._get_sensor_history_keys(end_time)
        if sensor_history_keys is None or len(sensor_history_keys) == 0:
            # Vehicle is non-transmitting.
            return {}

        two_days_earlier = end_time - timedelta(days=2)
        two_day_keys = Vehicle._get_sensor_history_key_subset(sensor_history_keys, two_days_earlier, end_time)
        last_10_vehicle_events = self.get_most_recent_events_with_readings(end_time, 10)

        assert len(last_10_vehicle_events) != 0  # should have hit non-transmitting vehicle condition above otherwise.
        last_10_last_timestamp = last_10_vehicle_events[-1].computed_event_timestamp
        if len(two_day_keys) == 0 or last_10_last_timestamp < two_day_keys[-1].get().computed_event_timestamp:
            wheel_position_keys = Vehicle._detect_transmitting_sensors_from_vehicle_events(last_10_vehicle_events)
        else:
            wheel_position_keys = Vehicle._detect_transmitting_sensors_from_sensor_history(two_day_keys)

        wheel_map = {}
        for wheel_position_key in wheel_position_keys:
            wheel_map[wheel_position_key] = None

        # Loop through each 3+ hour period of non-transmission; repeat until all non-NTS wheel_map entries are
        # populated or we run out of data.
        start_index = -1
        while None in wheel_map.values():
            start_index, end_index = Vehicle._find_stationary_interval(sensor_history_keys, end_time,
                start_index)
            if start_index == -1:
                # No more stationary intervals.  Note: if any entry is still None at this point the corresponding
                # sensor doesn't have any relevant readings from the last seven days.
                break
            elif end_index != -1:
                fifteen_minute_window_start = sensor_history_keys[end_index].get().computed_event_timestamp
                fifteen_minute_window_end = fifteen_minute_window_start + timedelta(minutes=15)
                fifteen_minute_sensor_history_keys = Vehicle._get_sensor_history_key_subset(sensor_history_keys,
                    fifteen_minute_window_start, fifteen_minute_window_end)
                Vehicle._populate_wheel_map(fifteen_minute_sensor_history_keys, wheel_map)
        return wheel_map

    def get_compensated_pressure(self, wheel_position, reference_temp_reading, end_time):
        last_pressure_readings = self.get_most_recent_sensor_readings(wheel_position, 2, end_time,
            pressure_required=True)
        last_temperature_readings = self.get_most_recent_sensor_readings(wheel_position, 2, end_time,
            temperature_required=True)
        compensated_pressures = [normalize_pressures_metric(pressure_reading.pressure,
            temperature_reading.temperature, reference_temp_reading.temperature)
            for pressure_reading, temperature_reading in zip(last_pressure_readings, last_temperature_readings)]
        return numpy.mean(compensated_pressures) - 0.1 if len(compensated_pressures) != 0 else None

    @classmethod
    def count(cls):
        return Vehicle.query().count()


@ae_ndb_serializer
class SystemUser(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    tenant_key = ndb.KeyProperty(kind=Tenant, required=True)
    username = ndb.StringProperty(required=True, default='System')

    @classmethod
    def get_or_create(cls, tenant_key):
        if tenant_key is None:
            return None

        user = cls.query(cls.tenant_key == tenant_key).get()
        if user is None:
            user = SystemUser(tenant_key=tenant_key)
            user.put()

        return user


@ae_ndb_serializer
class User(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    enabled = ndb.BooleanProperty(default=True)
    tenant_key = ndb.KeyProperty(kind=Tenant, required=True)
    email = ndb.StringProperty(required=True)
    username = ndb.StringProperty(required=True)
    first_name = ndb.StringProperty()
    middle_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    stormpath_account_href = ndb.StringProperty(required=True)

    @property
    def tenant(self):
        return self.tenant_key.get()

    @classmethod
    def get_by_username(cls, tenant_key, username):
        if tenant_key and username:
            query = User.query(User.tenant_key == tenant_key)
            query = query.filter(User.username == username)
            user_key = query.get(keys_only=True)
            if None is not user_key:
                return user_key.get()

    @classmethod
    def get_by_email(cls, email):
        if email:
            query = User.query(User.email == email)
            user_key = query.get(keys_only=True)
            if None is not user_key:
                return user_key.get()

    @classmethod
    def _update_properties(cls, user, account):
        tenant = Tenant.get_by_name(account.directory.name)
        user.tenant_key = tenant.key
        user.email = account.email
        user.username = account.username
        user.first_name = account.given_name
        user.middle_name = account.middle_name
        user.last_name = account.surname
        user.stormpath_account_href = account.href

        if hasattr(account, 'group_memberships') and len(account.group_memberships) > 0:
            user.stormpath_role = account.group_memberships[0].group.name
            user.stormpath_role_href = account.group_memberships[0].group.href
        else:
            user.stormpath_role = None
            user.stormpath_role_href = None

        status = account.status
        if status == 'ENABLED':
            user.enabled = True
        else:
            user.enabled = False

        return user

    @classmethod
    def update_or_create_with_api_account(cls, account):
        if account.href:
            user = cls.query(cls.stormpath_account_href == account.href).get()
            if user is None:
                user = cls()
            user = cls._update_properties(user, account)
            user.put()
            return user

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name or '', self.last_name or '').strip()


@ae_ndb_serializer
class ThresholdRange(ndb.Model):
    MAX_HIGH = sys.float_info.max
    MIN_LOW = -sys.float_info.max

    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    name = ndb.StringProperty(required=True)
    color = ndb.StringProperty(required=True, choices=THRESHOLD_COLORS)
    low_value = ndb.FloatProperty(default=MIN_LOW, required=True)
    high_value = ndb.FloatProperty(default=MAX_HIGH, required=True)
    send_alert = ndb.BooleanProperty(default=False)

    def _pre_put_hook(self):
        # do not allow values to be explicitly set to None, which circumvents default
        if self.low_value is None:
            self.low_value = self.MIN_LOW
        if self.high_value is None:
            self.high_value = self.MAX_HIGH

    def duplicate(self):
        copy = ThresholdRange(
            name=self.name,
            color=self.color,
            low_value=self.low_value,
            high_value=self.high_value,
            send_alert=self.send_alert,
        )
        return copy

    @classmethod
    def find_matching_range(cls, ranges, value):
        assert isinstance(value, float)
        range_within = None
        for threshold_range in ranges:
            if threshold_range.low_value <= value < threshold_range.high_value:
                range_within = threshold_range
                break
        return range_within


@ae_ndb_serializer
class IncidentThresholdRange(ThresholdRange):
    @classmethod
    def create(cls, threshold_range):
        incident_range = IncidentThresholdRange(
            name=threshold_range.name,
            color=threshold_range.color,
            low_value=threshold_range.low_value,
            high_value=threshold_range.high_value,
            send_alert=threshold_range.send_alert,
        )
        incident_range.put()
        return incident_range


# DEPRECATED... WILL EVENTUALLY MIGRATE TO ThresholdRangeSet FOR PRESSURES AND TEMPS. LEAKS ARE ALREADY THERE
@ae_ndb_serializer
class ThresholdSet(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    owner_key = ndb.KeyProperty(required=True)  # may be the key of a Tenant, Customer, VehicleGroup, or Vehicle
    wheel_position_key = ndb.KeyProperty(kind=WheelPosition, required=True)
    optimal_temperature = ndb.FloatProperty(required=True)  # unit is Celcius
    temperature_threshold_range_keys = ndb.KeyProperty(kind=ThresholdRange, repeated=True, indexed=False)  # Celcius
    optimal_pressure = ndb.FloatProperty(required=True) # unit is bar
    pressure_threshold_range_keys = ndb.KeyProperty(kind=ThresholdRange, repeated=True, indexed=False) # unit is bar

    vehicle_template_key = ndb.ComputedProperty(
        lambda self: self.wheel_position.vehicle_template_key if self.wheel_position is not None else None)

    def _pre_put_hook(self):
        if not self.temperature_threshold_range_keys:
            raise Exception("invalid threshold configuration: no temperature thresholds")
        if not self.pressure_threshold_range_keys:
            raise Exception("invalid threshold configuration: no pressure thresholds")

        first_pressure_thresh = self.pressure_threshold_range_keys[0].get()
        last_pressure_thresh = self.pressure_threshold_range_keys[-1].get()
        if first_pressure_thresh.low_value != ThresholdRange.MIN_LOW or last_pressure_thresh.high_value != \
                ThresholdRange.MAX_HIGH:
            raise Exception("invalid threshold range configuration: pressure thresholds do not cover gamut of values")

        first_temp_thresh = self.temperature_threshold_range_keys[0].get()
        last_temp_thresh = self.temperature_threshold_range_keys[-1].get()
        if first_temp_thresh.low_value != ThresholdRange.MIN_LOW or last_temp_thresh.high_value != ThresholdRange \
                .MAX_HIGH:
            raise Exception(
                "invalid threshold range configuration: temperature thresholds do not cover gamut of values")

    @classmethod
    def _pre_delete_hook(cls, key):
        # delete references
        delete_entities_with_reference(UIThresholdFields, 'threshold_set_key', key)

    @classmethod
    def exists(cls, owner_key, vehicle_template_key):
        return cls.query(cls.owner_key == owner_key).filter(
            cls.vehicle_template_key == vehicle_template_key).get(keys_only=True) is not None

    @classmethod
    def _find_by_owner_and_template(cls, owner_key, vehicle_template_key, wheel_position_key=None, keys_only=False):
        results = None
        ns = owner_key.namespace()
        query = cls.query(cls.owner_key == owner_key, namespace=ns)
        query = query.filter(cls.vehicle_template_key == vehicle_template_key)
        if wheel_position_key:
            set_key = query.filter(cls.wheel_position_key == wheel_position_key).get(keys_only=True)
            if None is not set_key:
                results = set_key.get()
        else:
            results = query.fetch(keys_only=True)
            if not keys_only:
                results = ndb.get_multi(results)
        return results

    @classmethod
    def find_by_owner_and_template(cls, owner_key, vehicle_template_key, wheel_position_key=None):
        results = []
        if owner_key and vehicle_template_key:
            results = cls._find_by_owner_and_template(owner_key, vehicle_template_key, wheel_position_key)
            while not results:
                owner = owner_key.get()
                if hasattr(owner, 'entity_owner_key'):
                    owner_key = owner.entity_owner_key
                    results = cls._find_by_owner_and_template(owner_key, vehicle_template_key, wheel_position_key)
                else:
                    break

        return results

    @property
    def pressure_threshold_ranges(self):
        return sorted(ndb.get_multi(self.pressure_threshold_range_keys), key=lambda r: r.low_value)

    @property
    def temperature_threshold_ranges(self):
        return sorted(ndb.get_multi(self.temperature_threshold_range_keys), key=lambda r: r.low_value)

    @property
    def pressure_thresholds(self):
        query = UIThresholdFields.query(UIThresholdFields.threshold_set_key == self.key)
        query = query.filter(UIThresholdFields.nature == PRESSURE_NATURE)
        query = query.order(UIThresholdFields.range_break)
        keys = query.fetch(keys_only=True)
        return ndb.get_multi(keys)

    @property
    def temperature_thresholds(self):
        query = UIThresholdFields.query(UIThresholdFields.threshold_set_key == self.key)
        query = query.filter(UIThresholdFields.nature == TEMPERATURE_NATURE)
        query = query.order(UIThresholdFields.range_break)
        keys = query.fetch(keys_only=True)
        return ndb.get_multi(keys)

    @property
    def wheel_position(self):
        return self.wheel_position_key.get()


@ae_ndb_serializer
class ThresholdRangeSet(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    class_version = ndb.IntegerProperty(required=True)

    nature = ndb.StringProperty(required=True, choices=NATURES)
    owner_key = ndb.KeyProperty(required=True)  # may be the key of a Tenant, Customer, VehicleGroup, or Vehicle
    wheel_position_key = ndb.KeyProperty(kind=WheelPosition) # if None, we have a LEAK range and owner is a VehicleGroup
    optimal_value = ndb.FloatProperty(required=True)  # pressure is in bar; temp is in Celsius
    threshold_range_keys = ndb.KeyProperty(kind=ThresholdRange, repeated=True, indexed=False)

    vehicle_template_key = ndb.ComputedProperty(
        lambda self: self.wheel_position.vehicle_template_key if self.wheel_position is not None else None)

    def _pre_put_hook(self):
        self.class_version = 1

        if not self.threshold_range_keys:
            raise Exception("invalid threshold configuration: no ranges")

    @classmethod
    def _find_by_owner_and_template(cls, nature, owner_key, vehicle_template_key, wheel_position_key=None, keys_only=False):
        query = cls.query(cls.owner_key == owner_key)
        query = query.filter(cls.nature == nature)
        query = query.filter(cls.vehicle_template_key == vehicle_template_key)
        if wheel_position_key:
            set_key = query.filter(cls.wheel_position_key == wheel_position_key).get(keys_only=True)
            results = set_key.get() if not keys_only and set_key is not None else set_key
        else:
            results = query.fetch(keys_only=True)
            if not keys_only:
                results = ndb.get_multi(results)
        return results

    @classmethod
    def find_by_owner_and_template(cls, nature, owner_key, vehicle_template_key, wheel_position_key=None):
        results = []
        if owner_key and vehicle_template_key:
            results = cls._find_by_owner_and_template(nature, owner_key, vehicle_template_key, wheel_position_key)
            while not results:
                owner = owner_key.get()
                if hasattr(owner, 'entity_owner_key'):
                    owner_key = owner.entity_owner_key
                    results = cls._find_by_owner_and_template(nature, owner_key, vehicle_template_key, wheel_position_key)
                else:
                    break

        return results

    @classmethod
    def get_leak_threshold_by_group(cls, vehicle_group_key):
        query = cls.query(cls.owner_key == vehicle_group_key)
        query = query.filter(cls.nature == LEAK_NATURE)
        key = query.get(keys_only=True)
        return key.get() if key is not None else None

    @property
    def threshold_ranges(self):
        return sorted(ndb.get_multi(self.threshold_range_keys), key=lambda r: r.low_value)

    @property
    def wheel_position(self):
        return self.wheel_position_key.get() if self.wheel_position_key is not None else None


@ae_ndb_serializer
class UIThresholdFields(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    threshold_set_key = ndb.KeyProperty(kind=ThresholdSet, required=True)
    nature = ndb.StringProperty(choices=NATURES, required=True)
    less_than_name = ndb.StringProperty(required=True)
    less_than_color = ndb.StringProperty(required=True, choices=THRESHOLD_COLORS)
    less_than_alert = ndb.BooleanProperty(default=False)
    range_break = ndb.FloatProperty(required=True)
    greater_than_name = ndb.StringProperty(required=True)
    greater_than_color = ndb.StringProperty(required=True, choices=THRESHOLD_COLORS)
    greater_than_alert = ndb.BooleanProperty(default=False)


@ae_ndb_serializer
class VehicleEvent(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    location = ndb.GeoPtProperty()
    raw_foreign_document_key = ndb.StringProperty(required=True)
    telemetry_provider_key = ndb.KeyProperty(kind=TelemetryProvider, required=True)
    customer_id = ndb.StringProperty(required=True)
    transmitter_id = ndb.StringProperty()
    transmitting_vehicle_key = ndb.KeyProperty(kind=Vehicle)
    vehicle_key = ndb.KeyProperty(kind=Vehicle, required=True)
    vehicle_tag = ndb.StringProperty()
    event_timestamp = ndb.DateTimeProperty()
    remote_timestamp = ndb.DateTimeProperty()
    router_timestamp = ndb.DateTimeProperty(required=True)
    processing_complete = ndb.DateTimeProperty()
    computed_event_timestamp = ndb.ComputedProperty(
        lambda self: self.event_timestamp or self.remote_timestamp or self.router_timestamp)

    vehicle_group_key = ndb.ComputedProperty(
        lambda self: self.vehicle.vehicle_group_key if self.vehicle is not None else None)

    customer_key = ndb.ComputedProperty(
        lambda self: self.vehicle_group.customer_key if self.vehicle_group is not None else None)

    @classmethod
    def _pre_delete_hook(cls, key):
        # delete references
        delete_entities_with_reference(SensorReading, 'event_key', key)
        delete_entities_with_reference(TireLeakTrend, 'vehicle_event_key', key)

    @property
    def sensor_readings(self):
        keys = SensorReading.query(SensorReading.event_key == self.key).fetch(keys_only=True)
        return ndb.get_multi(keys)

    @property
    def vehicle(self):
        return self.vehicle_key.get()

    @property
    def transmitting_vehicle(self):
        return self.transmitting_vehicle_key.get() if self.transmitting_vehicle_key else None

    @property
    def vehicle_group(self):
        return self.vehicle_group_key.get() if self.vehicle_group_key else None

    @property
    def vehicle_template(self):
        return self.vehicle.vehicle_template

    @property
    def customer(self):
        if self.customer_key:
            return self.customer_key.get()

    @property
    def response_time_ms(self):
        if self.processing_complete is not None:
            delta = self.processing_complete - self.created
            return int(delta.total_seconds() * 1000)
        return None

    @property
    def router_response_time_ms(self):
        if self.processing_complete is not None:
            delta = self.processing_complete - self.router_timestamp
            return int(delta.total_seconds() * 1000)
        return None

    @classmethod
    def _get_threshold_range(cls, wheel_position, reading, pressure=True):
        thresh_set = wheel_position.threshold_set_for(reading.vehicle_key)
        assert thresh_set, "no thresholds found for wheel {} of template {}".format(wheel_position.position_label,
            wheel_position.vehicle_template_key)

        ranges = thresh_set.pressure_threshold_ranges if pressure else thresh_set.temperature_threshold_ranges
        assert 0 < len(ranges), "no threshold ranges found for wheel {} of template {}".format(
            wheel_position.position_label,
            wheel_position.vehicle_template_key)

        sensor_value = reading.pressure if pressure else reading.temperature

        range_within = ThresholdRange.find_matching_range(ranges, sensor_value)
        assert range_within, \
            "no actionable {} threshold range found for wheel_position {} of template {}".format(
                "pressure" if pressure else "temp", wheel_position.pressure_label,
                wheel_position.vehicle_template_key)
        return range_within, ranges, thresh_set

    @classmethod
    def check_pressure(cls, wheel_position, reading):
        if reading.pressure is not None:
            range_within, pressure_ranges, thresh_set = cls._get_threshold_range(wheel_position, reading)
            if range_within.send_alert:  # reading was found to be in alert range
                previous_reading = SensorReading.get_previous_reading(reading.vehicle_key, wheel_position.key,
                    before_reading=reading)
                if previous_reading and previous_reading.pressure is not None:
                    old_range = ThresholdRange.find_matching_range(pressure_ranges, previous_reading.pressure)
                    if old_range and old_range.send_alert:
                        # 2 alert ranges in a row! Elaborate on an active incident or create a new one
                        active_incident = Incident.get_last_in_24_hours_from(PRESSURE_NATURE, reading.vehicle_key,
                            wheel_position.key, newest_datetime=reading.computed_event_timestamp)
                        if active_incident:
                            logging.warn("adding sensor value of {} for wheel_position {} to incident {}".format(
                                reading.pressure, wheel_position.key, active_incident.key))
                            active_incident.sensor_reading_keys.append(reading.key)
                        else:
                            incident = Incident.create(PRESSURE_NATURE, range_within, thresh_set.optimal_pressure, sensor_reading=reading)
                            logging.warn("incident {} created for pressure {} on wheel_position {}".format(incident.key,
                                reading.pressure, wheel_position.key))
                            return incident

    @classmethod
    def check_temperature(cls, wheel_position, reading):
        if reading.temperature is not None:
            range_within, temperature_ranges, thresh_set = cls._get_threshold_range(wheel_position, reading,
                pressure=False)
            if range_within.send_alert:  # reading was found to be in alert range
                active_incident = Incident.get_last_in_24_hours_from(TEMPERATURE_NATURE, reading.vehicle_key,
                    wheel_position.key,
                    newest_datetime=reading.computed_event_timestamp)
                if active_incident:
                    logging.warn(
                        "adding sensor value of {} for wheel_position {} to incident {}".format(reading.temperature,
                            wheel_position.key, active_incident.key))
                    active_incident.sensor_reading_keys.append(reading.key)
                else:
                    incident = Incident.create(TEMPERATURE_NATURE, range_within, thresh_set.optimal_temperature, sensor_reading=reading)
                    logging.warn("incident {} created for temperature {} on wheel_position {}".format(incident.key,
                        reading.temperature, wheel_position.key))
                    return incident

    @classmethod
    def count(cls, since_date):
        query = cls.query(cls.computed_event_timestamp > since_date)
        return query.count()

    @classmethod
    def find_within_timeframe(cls, vehicle_key, time_window_early, time_window_late):
        query = cls.query(cls.vehicle_key == vehicle_key)
        query = query.filter(cls.computed_event_timestamp >= time_window_early)
        query = query.filter(cls.computed_event_timestamp <= time_window_late)
        query = query.order(-cls.computed_event_timestamp)

        keys = query.fetch(keys_only=True)
        return ndb.get_multi(keys)

    @classmethod
    def get_first_within_timeframe(cls, vehicle_key, time_window_early, time_window_late):
        query = cls.query(cls.vehicle_key == vehicle_key)
        query = query.filter(cls.computed_event_timestamp >= time_window_early)
        query = query.filter(cls.computed_event_timestamp <= time_window_late)
        event_key = query.get(keys_only=True)
        if None is not event_key:
            return event_key.get()


@ae_ndb_serializer
class SensorReading(ndb.Model):
    class_version = ndb.IntegerProperty() # TODO: make required after all data is migrated
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    event_key = ndb.KeyProperty(kind=VehicleEvent, required=True)
    wheel_position_key = ndb.KeyProperty(kind=WheelPosition, required=True)
    wheel_position_label = ndb.StringProperty()
    pressure_label = ndb.StringProperty()
    pressure = ndb.FloatProperty()
    temperature_label = ndb.StringProperty()
    temperature = ndb.FloatProperty()

    event_timestamp = ndb.ComputedProperty(lambda self: self.event.event_timestamp if self.event else None)
    computed_event_timestamp = ndb.DateTimeProperty()  # value set in _pre_put_hook - necessary for report mapreduce
    location = ndb.ComputedProperty(lambda self: self.event.location if self.event else None)

    axle_sequence = ndb.ComputedProperty(
        lambda self: self.wheel_position.axle_position.sequence if self.wheel_position and
                                                                    self.wheel_position.axle_position else None)

    # query and sorting fields
    customer_key = ndb.ComputedProperty(lambda self: self.event.customer_key if self.event else None)
    vehicle_group_key = ndb.ComputedProperty(lambda self: self.event.vehicle_group_key if self.event else None)
    vehicle_key = ndb.ComputedProperty(lambda self: self.event.vehicle_key if self.event else None)
    wheel_sequence = ndb.ComputedProperty(lambda self: self.wheel_position.sequence if self.wheel_position else None)

    has_values = ndb.ComputedProperty(
        lambda self: self.pressure is not None or self.temperature is not None)

    has_pressure = ndb.ComputedProperty(lambda self: self.pressure is not None)
    has_temperature = ndb.ComputedProperty(lambda self: self.temperature is not None)

    def _pre_put_hook(self):
        self.class_version = 1

        # make sure key is ours
        namespace = self.event_key.namespace()
        if self.key is None or self.key.id() is None:
            self.key = self.build_key(self.event_key, self.wheel_position_key, namespace)

        self.computed_event_timestamp = self.event.computed_event_timestamp if self.event else None

    @classmethod
    def _pre_delete_hook(cls, key):
        # delete references
        ns = key.namespace()
        reading = key.get()
        incidents = Incident.find_by_vehicle_and_wheel_position(reading.vehicle_key, reading.wheel_position_key,
            namespace=ns)
        entities_to_save = []
        for incident in incidents:
            if key in incident.sensor_reading_keys:
                incident.sensor_reading_keys.remove(key)
                entities_to_save.append(incident)

        if entities_to_save:
            ndb.put_multi(entities_to_save)

    @classmethod
    def build_key(cls, event_key, wheel_position_key, namespace=''):
        key_str = '{}_{}'.format(event_key.urlsafe(), wheel_position_key.urlsafe())
        key = ndb.Key(cls, key_str, namespace=namespace)
        return key

    @classmethod
    def get_by_wheel_position(cls, event_key, wheel_position_key):
        if event_key and wheel_position_key:
            key = cls.build_key(event_key, wheel_position_key)
            return key.get()

    @classmethod
    def get_previous_reading(cls, vehicle_key, wheel_position_key, before_reading):
        query = cls.query(cls.vehicle_key == vehicle_key)
        query = query.filter(cls.wheel_position_key == wheel_position_key)
        query = query.filter(cls.computed_event_timestamp < before_reading.computed_event_timestamp)
        query = query.order(-cls.computed_event_timestamp)

        previous_reading_key = query.get(keys_only=True)
        if None is not previous_reading_key:
            return previous_reading_key.get()

    @classmethod
    def find_history_by_vehicle_wheel(cls, vehicle_key, wheel_position_key, newest_event_time=None,
            oldest_event_time=None, count=None):

        if newest_event_time is None:
            newest_event_time = datetime.now()
        query = cls.query(cls.vehicle_key == vehicle_key)
        if oldest_event_time is not None:
            query = query.filter(cls.computed_event_timestamp > oldest_event_time)
        query = query.filter(cls.wheel_position_key == wheel_position_key)
        query = query.filter(cls.computed_event_timestamp <= newest_event_time)
        query = query.filter(cls.has_values == True)
        query = query.order(-cls.computed_event_timestamp)
        if count is not None:
            keys = query.fetch(keys_only=True, limit=count)
        else:
            keys = query.fetch(keys_only=True)

        return ndb.get_multi(keys)

    @property
    def wheel_position(self):
        return self.wheel_position_key.get() if self.wheel_position_key else None

    @property
    def event(self):
        return self.event_key.get() if self.event_key else None

    @property
    def vehicle(self):
        return self.vehicle_key.get() if self.vehicle_key else None

    @property
    def vehicle_group(self):
        return self.vehicle_group_key.get() if self.vehicle_group_key else None

    @classmethod
    def get_first_within_timeframe(cls, vehicle_key, wheel_position_key, time_window_early, time_window_late):
        query = cls.query(cls.vehicle_key == vehicle_key)
        query = query.filter(cls.wheel_position_key == wheel_position_key)
        query = query.filter(cls.computed_event_timestamp >= time_window_early)
        query = query.filter(cls.computed_event_timestamp <= time_window_late)
        query = query.order(cls.computed_event_timestamp)

        reading_key = query.get(keys_only=True)
        if None is not reading_key:
            return reading_key.get()


class TireLeakTrend(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True, indexed=False)
    class_version = ndb.IntegerProperty(required=True)
    completed = ndb.DateTimeProperty(indexed=False)
    vehicle_event_key = ndb.KeyProperty(kind=VehicleEvent, required=True)
    wheel_position_key = ndb.KeyProperty(kind=WheelPosition, required=True)
    leak_rate = ndb.FloatProperty(required=True)  # leak rate is in BAR

    has_been_completed = ndb.ComputedProperty(lambda self: self.completed is not None)
    vehicle_key = ndb.ComputedProperty(lambda self: self.vehicle_event.vehicle_key if self.vehicle_event else None)

    @classmethod
    def _pre_delete_hook(cls, key):
        # delete references
        ns = key.namespace()
        trend = key.get()
        incidents = Incident.find_by_vehicle_and_wheel_position(trend.vehicle_key, trend.wheel_position_key,
            namespace=ns)

        entities_to_save = []
        for incident in incidents:
            if key in incident.tire_leak_keys:
                incident.tire_leak_keys.remove(key)
                entities_to_save.append(incident)

        if entities_to_save:
            ndb.put_multi(entities_to_save)

    @classmethod
    def create(cls, vehicle_event_key, wheel_position_key, leak_rate, namespace='', save=True):
        tl = cls(vehicle_event_key=vehicle_event_key,
            wheel_position_key=wheel_position_key,
            leak_rate=leak_rate, namespace=namespace)
        if save:
            tl.put()
        return tl

    @classmethod
    def find_active_leaks(cls):
        return cls.query(cls.has_been_completed == False).order(cls.created).fetch()

    def mark_complete(self):
        self.completed = datetime.now()
        self.put()

    def _pre_put_hook(self):
        self.class_version = 1

    @property
    def wheel_position(self):
        return self.wheel_position_key.get()

    @property
    def vehicle_event(self):
        return self.vehicle_event_key.get()

    @property
    def vehicle(self):
        return self.vehicle_key.get()

    def check_leak(self):
        incident = None
        if '' == self.vehicle_key.namespace():  # only check this if the vehicle is in the default namespace
            threshold_range_set = self.vehicle.vehicle_group.leak_threshold_set if self.vehicle and \
                                                                                   self.vehicle.vehicle_group else None
            range_within = ThresholdRange.find_matching_range(threshold_range_set.threshold_ranges,
                self.leak_rate) if threshold_range_set else None

            if range_within is not None and range_within.send_alert:
                active_incident = Incident.get_last_in_24_hours_from(PRESSURE_NATURE, self.vehicle_key,
                    self.wheel_position_key, newest_datetime=self.vehicle_event.computed_event_timestamp)
                if active_incident:
                    logging.warn("adding leak rate of {} for wheel_position {} to pressure incident {}".format(
                        self.leak_rate, self.wheel_position, active_incident.key))
                    active_incident.tire_leak_keys.append(self.key)
                else:
                    active_leak_incident = Incident.get_last_in_24_hours_from(LEAK_NATURE, self.vehicle_key,
                        self.wheel_position_key, newest_datetime=self.vehicle_event.computed_event_timestamp)
                    if active_leak_incident:
                        logging.warn("adding leak rate of {} for wheel_position {} to leak incident {}".format(
                            self.leak_rate, self.wheel_position, active_leak_incident.key))
                        active_leak_incident.tire_leak_keys.append(self.key)
                    else:
                        incident = Incident.create(LEAK_NATURE, range_within, self.leak_rate, tire_leak=self)
                        logging.warn(
                            "incident {} created for leak rate {} on wheel_position {}".format(incident.key,
                                self.leak_rate, self.wheel_position_key))
        return incident

    @classmethod
    def get_worst_by_vehicle_wheel_position(cls, vehicle_key, wheel_position_key, from_timestamp, to_timestamp):
        query = cls.query(cls.vehicle_key == vehicle_key)
        query = query.filter(cls.wheel_position_key == wheel_position_key)
        query = query.filter(cls.created >= from_timestamp)
        query = query.filter(cls.created < to_timestamp)
        keys = query.fetch(keys_only=True)
        results = ndb.get_multi(keys)

        return max(results, key=lambda o: o.leak_rate) if results else None


@ae_ndb_serializer
class Incident(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    class_version = ndb.IntegerProperty()
    initial_event_timestamp = ndb.DateTimeProperty(required=True)
    sensor_reading_keys = ndb.KeyProperty(kind=SensorReading, repeated=True, indexed=False)
    tire_leak_keys = ndb.KeyProperty(kind=TireLeakTrend, repeated=True, indexed=False)
    wheel_position_key = ndb.KeyProperty(kind=WheelPosition, required=True)
    vehicle_key = ndb.KeyProperty(kind=Vehicle, required=True)
    initial_alert_sent = ndb.DateTimeProperty()
    followup_alert_sent = ndb.DateTimeProperty()
    nature = ndb.StringProperty(choices=NATURES, required=True)
    incident_range_key = ndb.KeyProperty(required=True)
    optimal_value = ndb.FloatProperty(required=True)

    def _pre_put_hook(self):
       self.class_version = 1

    @classmethod
    def create(cls, nature, threshold_range, optimal_value, sensor_reading=None, tire_leak=None):
        assert sensor_reading is not None or tire_leak is not None
        incident_range = IncidentThresholdRange.create(threshold_range)
        if sensor_reading:
            incident = Incident(vehicle_key=sensor_reading.vehicle_key,
                nature=nature,
                initial_event_timestamp=sensor_reading.computed_event_timestamp,
                sensor_reading_keys=[sensor_reading.key],
                tire_leak_keys=[],
                wheel_position_key=sensor_reading.wheel_position_key,
                incident_range_key=incident_range.key,
                optimal_value=optimal_value)
        else:
            incident = Incident(vehicle_key=tire_leak.vehicle_key,
                nature=nature,
                initial_event_timestamp=tire_leak.vehicle_event.computed_event_timestamp,
                sensor_reading_keys=[],
                tire_leak_keys=[tire_leak.key],
                wheel_position_key=tire_leak.wheel_position_key,
                incident_range_key=incident_range.key,
                optimal_value=optimal_value,
                namespace=tire_leak.key.namespace()) # simulated tire leaks should create simulated incidents
        incident.put()
        return incident

    @classmethod
    def get_last_in_24_hours_from(cls, nature, vehicle_key, wheel_position_key, newest_datetime):
        query = cls.query(cls.nature == nature)
        query = query.filter(cls.vehicle_key == vehicle_key)
        query = query.filter(cls.wheel_position_key == wheel_position_key)

        twenty_four_hours_ago = newest_datetime - timedelta(hours=24)
        query = query.filter(cls.initial_event_timestamp > twenty_four_hours_ago)

        incident_key = query.get(keys_only=True)
        if None is not incident_key:
            return incident_key.get()

    @classmethod
    def get_active_incidents_since(cls, newest_datetime):
        twenty_four_hours_ago = newest_datetime - timedelta(hours=24)
        incident_keys = cls.query().filter(cls.initial_event_timestamp > twenty_four_hours_ago).fetch(keys_only=True)
        active_incidents = []
        if len(incident_keys) > 0:
            active_incidents = ndb.get_multi(incident_keys)
        return active_incidents

    def sensor_reading(self, ordinal):
        return self.sensor_reading_keys[ordinal].get()

    @property
    def sensor_readings(self):
        return ndb.get_multi(self.sensor_reading_keys)

    @property
    def incident_range(self):
        return self.incident_range_key.get()

    @property
    def wheel_position(self):
        return self.wheel_position_key.get()

    @property
    def vehicle(self):
        return self.vehicle_key.get()

    @classmethod
    def count(cls, since_date):
        query = cls.query(cls.initial_event_timestamp > since_date)
        return query.count()

    @classmethod
    def find_by_vehicle_and_wheel_position(cls, vehicle_key, wheel_position_key, namespace=''):
        query = Incident.query(Incident.vehicle_key == vehicle_key, namespace=namespace)
        query = query.filter(Incident.wheel_position_key == wheel_position_key)
        return ndb.get_multi(query.fetch(keys_only=True))


class WheelSchematicImageInfo(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    vehicle_template_key = ndb.KeyProperty(kind=VehicleTemplate)
    gcs_path_in_bucket = ndb.StringProperty()
    bucket_name = ndb.StringProperty()
    content_type = ndb.StringProperty(indexed=False)

    retry_params = gcs.RetryParams(initial_delay=0.2,
        max_delay=5.0,
        backoff_factor=1.1,
        max_retry_period=15)

    def delete_cascade(self):
        if self.gcs_path_in_bucket:
            gcs.delete(WheelSchematicImageInfo._get_uri(self.bucket_name, self.gcs_path_in_bucket))
            self.key.delete()

    @classmethod
    def delete_image_infos_of_template(cls, vehicle_template_key):
        # DO NOT cache this query, since we're deleting!
        infos = cls.query(cls.vehicle_template_key == vehicle_template_key).fetch()
        for info in infos:
            info.delete_cascade()

    @classmethod
    def determine_path_in_bucket(cls, vehicle_template_key, orientation, language, *indicated_wheel_position_keys):
        wheels_str = ""
        for wheel_position_key in indicated_wheel_position_keys:
            wheels_str = "{},{}".format(wheels_str, wheel_position_key.urlsafe())
        gcs_path_in_bucket = "{}__{}__{}__{}.png".format(vehicle_template_key.urlsafe(), orientation, language,
            wheels_str)
        return gcs_path_in_bucket

    @classmethod
    def find_infos(cls):
        keys = cls.query().order(-WheelSchematicImageInfo.created).fetch(500, keys_only=True)
        return ndb.get_multi(keys)

    @classmethod
    def _get_uri(cls, bucket_name, path_in_buck):
        return "/{}/{}/{}".format(bucket_name, config.WHEEL_SCHEMATIC_PREFIX_GCS, path_in_buck)

    @classmethod
    def get_or_create(cls, vehicle_template, language, orientation=PORTRAIT, *indicated_wheel_position_keys):
        """
        NOTE Might exceed deadline on a cache miss
        :return: instance of ImageInfo with ephemeral instance property '_file_contents' containing image bytes
        """
        path_in_buck = cls.determine_path_in_bucket(vehicle_template.key, orientation, language,
            *indicated_wheel_position_keys)
        image_info = cls.query(cls.gcs_path_in_bucket == path_in_buck, cls.bucket_name == config.BUCKET_NAME).get()
        if None is image_info:
            pil_image = create_wheel_schematic(vehicle_template, language, orientation, *indicated_wheel_position_keys)
            with gcs.open(cls._get_uri(config.BUCKET_NAME, path_in_buck), mode='w', content_type='image/png',
                    retry_params=cls.retry_params) as fd:
                pil_image.save(fd, format="PNG")  # notice format isn't a MIME type, grrrr...
            image_info = cls(
                vehicle_template_key=vehicle_template.key,
                content_type="image/png",
                gcs_path_in_bucket=path_in_buck,
                bucket_name=config.BUCKET_NAME)
            image_info.put()
        image_info.check_load_binary_image()
        return image_info

    def check_load_binary_image(self):
        # Only load image data once
        if not hasattr(self, "_file_contents"):
            if self.gcs_path_in_bucket:
                uri = WheelSchematicImageInfo._get_uri(self.bucket_name, self.gcs_path_in_bucket)
                with gcs.open(uri, 'r') as handle:
                    self._file_contents = handle.read()
            else:
                logging.warn("No path in GCS")
                self._file_contents = None
        return self._file_contents


@ae_ndb_serializer
class Report(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    completed = ndb.DateTimeProperty()
    report_type = ndb.StringProperty(required=True, choices=REPORT_TYPES)
    state = ndb.StringProperty(choices=REPORT_STATES)
    creator_key = ndb.KeyProperty(required=True)  # kind should be a User.key or SystemUser.key
    vehicle_group_key = ndb.KeyProperty(kind=VehicleGroup, required=True)
    start_date = ndb.DateTimeProperty()
    end_date = ndb.DateTimeProperty()
    base_filename = ndb.StringProperty()
    gcs_filename = ndb.StringProperty()
    url = ndb.StringProperty()
    expiration_date = ndb.DateProperty()
    language = ndb.StringProperty(choices=SUPPORTED_LANGUAGES)

    def _pre_put_hook(self):
        if not self.base_filename:  # only set once
            assert self.key.parent() is not None
            tenant_id = self.key.parent().id()
            tenant = ndb.Key(Tenant, tenant_id).get()
            now = datetime.now()
            metadata = REPORT_METADATA[self.report_type]
            self.base_filename = 'report-{}.{}'.format(now, metadata.file_extension)
            self.gcs_filename = '/{}/reports/{}/{}'.format(config.BUCKET_NAME, tenant.name_lower, self.base_filename)
            if on_development_server or not on_server:
                self.url = build_uri('get-report', params_dict={'key': self.key.urlsafe()})
            else:
                self.url = sign_cloud_storage_url(self.gcs_filename)

    @classmethod
    def ancestor_key(cls, tenant_key):
        return ndb.Key('report', tenant_key.id())

    @classmethod
    def create(cls, tenant_key, report_type, creator_key, vehicle_group_key, language, state=STATE_IN_PROGRESS,
            start_date=None, end_date=None, created_date=None, save=True):

        # _pre_put_hook requires key to exist before it saves in order to generate a download url.
        ancestor_key = Report.ancestor_key(tenant_key)
        ids = Report.allocate_ids(size=1, parent=ancestor_key)
        report = Report(parent=ancestor_key, id=ids[0])
        report.report_type = report_type
        report.state = state
        report.creator_key = creator_key
        report.vehicle_group_key = vehicle_group_key
        report.start_date = start_date
        report.end_date = end_date
        if created_date is not None:
            report.created = created_date
        report.expiration_date = None  # TODO: determine expiration date.
        report.language = language
        if save:
            report.put()
        return report

    @property
    def tenant(self):
        return self.customer.tenant

    @property
    def customer_key(self):
        return self.vehicle_group.customer_key

    @property
    def customer(self):
        return self.customer_key.get()

    @property
    def vehicle_group(self):
        return self.vehicle_group_key.get()

    @property
    def creator(self):
        return self.creator_key.get()


@ae_ndb_serializer
class ScheduledReport(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    tenant_key = ndb.KeyProperty(kind=Tenant, required=True)
    report_type = ndb.StringProperty(required=True, choices=REPORT_TYPES)
    creator_key = ndb.KeyProperty(kind=SystemUser, required=True)
    vehicle_group_key = ndb.KeyProperty(kind=VehicleGroup, required=True)
    language = ndb.StringProperty(choices=SUPPORTED_LANGUAGES)
    emails = ndb.StringProperty(repeated=True, indexed=False)
    report_key = ndb.KeyProperty(kind=Report)

    @classmethod
    def create(cls, tenant_key, report_type, creator_key, vehicle_group_key, language, emails, save=True):
        scheduled_report = ScheduledReport()
        scheduled_report.tenant_key = tenant_key
        scheduled_report.report_type = report_type
        scheduled_report.creator_key = creator_key
        scheduled_report.vehicle_group_key = vehicle_group_key
        scheduled_report.language = language
        scheduled_report.emails = emails
        if save:
            scheduled_report.put()
        return scheduled_report

    @property
    def vehicle_group(self):
        return self.vehicle_group_key.get()


@ae_ndb_serializer
class UnregisteredVehicle(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    class_version = ndb.IntegerProperty()
    customer_key = ndb.KeyProperty(kind=Customer)
    telemetry_provider_key = ndb.KeyProperty(kind=TelemetryProvider, required=True)
    vehicle_id = ndb.StringProperty(required=True)
    vehicle_tag = ndb.StringProperty()
    is_attached_unit = ndb.BooleanProperty(default=False)

    def _pre_put_hook(self):
        self.class_version = 2

        # make sure key is ours
        key = UnregisteredVehicle.build_key(self.telemetry_provider_key, self.vehicle_id)
        if self.key != key:
            self.key = key

    @classmethod
    def build_key(cls, telemetry_provider_key, vehicle_id):
        key_str = '{}_{}'.format(vehicle_id, telemetry_provider_key.urlsafe())
        key = ndb.Key(cls, key_str)
        return key

    @classmethod
    def get_by_vehicle_id(cls, telemetry_provider_key, vehicle_id):
        return UnregisteredVehicle.build_key(telemetry_provider_key, vehicle_id).get()

    @property
    def customer(self):
        return self.customer_key.get() if self.customer_key else None

    @property
    def customer_name(self):
        return self.customer.name if self.customer else None

    @property
    def telemetry_provider(self):
        return self.telemetry_provider_key.get()


class MonitorConfig(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    api_key = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    time_window = ndb.IntegerProperty()  # last X minutes
    min_sample_size = ndb.IntegerProperty()
    max_sample_size = ndb.IntegerProperty()

    def _pre_put_hook(self):
        if self.api_key is None:
            self.api_key = uuid.uuid4().hex

    @classmethod
    def get_by_name(cls, name):
        monitor_config = None
        if name:
            config_key = cls.query(cls.name == name).get(keys_only=True)
            if config_key is not None:
                monitor_config = config_key.get()
        return monitor_config


class MonitorProbe(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    count = ndb.IntegerProperty(default=0)


def configure_vehicle_thresholds_task(vehicle_key, vehicle_template_key):
    parent_threshold_sets = ThresholdSet.find_by_owner_and_template(vehicle_key, vehicle_template_key)
    for parent_threshold_set in parent_threshold_sets:
        if parent_threshold_set.owner_key != vehicle_key:
            # only create threshold sets if they don't exist yet for this vehicle
            parent_temperature_threshold_ranges = ndb.get_multi(parent_threshold_set.temperature_threshold_range_keys)
            temperature_threshold_range_keys = []
            for parent_range in parent_temperature_threshold_ranges:
                threshold_range = parent_range.duplicate()
                threshold_range.put()
                temperature_threshold_range_keys.append(threshold_range.key)

            parent_pressure_threshold_ranges = ndb.get_multi(parent_threshold_set.pressure_threshold_range_keys)
            pressure_threshold_range_keys = []
            for parent_range in parent_pressure_threshold_ranges:
                threshold_range = parent_range.duplicate()
                threshold_range.put()
                pressure_threshold_range_keys.append(threshold_range.key)

            vehicle_threshold_set = ThresholdSet(
                owner_key=vehicle_key,
                wheel_position_key=parent_threshold_set.wheel_position_key,
                optimal_temperature=parent_threshold_set.optimal_temperature,
                optimal_pressure=parent_threshold_set.optimal_pressure,
                temperature_threshold_range_keys=temperature_threshold_range_keys,
                pressure_threshold_range_keys=pressure_threshold_range_keys)
            vehicle_threshold_set.put()

            parent_pressure_ui_fields = parent_threshold_set.pressure_thresholds
            for parent_pressure_ui_field in parent_pressure_ui_fields:
                vehicle_pressure_ui_field = UIThresholdFields(threshold_set_key=vehicle_threshold_set.key)
                vehicle_pressure_ui_field.nature = parent_pressure_ui_field.nature
                vehicle_pressure_ui_field.less_than_name = parent_pressure_ui_field.less_than_name
                vehicle_pressure_ui_field.less_than_color = parent_pressure_ui_field.less_than_color
                vehicle_pressure_ui_field.less_than_alert = parent_pressure_ui_field.less_than_alert
                vehicle_pressure_ui_field.range_break = parent_pressure_ui_field.range_break
                vehicle_pressure_ui_field.greater_than_name = parent_pressure_ui_field.greater_than_name
                vehicle_pressure_ui_field.greater_than_color = parent_pressure_ui_field.greater_than_color
                vehicle_pressure_ui_field.greater_than_alert = parent_pressure_ui_field.greater_than_alert
                vehicle_pressure_ui_field.put()

            parent_temperature_ui_fields = parent_threshold_set.temperature_thresholds
            for parent_temperature_ui_field in parent_temperature_ui_fields:
                vehicle_temperature_ui_field = UIThresholdFields(threshold_set_key=vehicle_threshold_set.key)
                vehicle_temperature_ui_field.nature = parent_temperature_ui_field.nature
                vehicle_temperature_ui_field.less_than_name = parent_temperature_ui_field.less_than_name
                vehicle_temperature_ui_field.less_than_color = parent_temperature_ui_field.less_than_color
                vehicle_temperature_ui_field.less_than_alert = parent_temperature_ui_field.less_than_alert
                vehicle_temperature_ui_field.range_break = parent_temperature_ui_field.range_break
                vehicle_temperature_ui_field.greater_than_name = parent_temperature_ui_field.greater_than_name
                vehicle_temperature_ui_field.greater_than_color = parent_temperature_ui_field.greater_than_color
                vehicle_temperature_ui_field.greater_than_alert = parent_temperature_ui_field.greater_than_alert
                vehicle_temperature_ui_field.put()


def configure_vehicle_thresholds(vehicle_key, vehicle_template_key):
    deferred.defer(configure_vehicle_thresholds_task, vehicle_key, vehicle_template_key, _queue='housekeeping')


def delete_entities_with_reference_task(cls, property, key):
    query = cls.query(getattr(cls, property) == key, namespace=key.namespace())
    keys = query.fetch(keys_only=True)
    if keys:
        ndb.delete_multi(keys)


def delete_entities_with_reference(cls, property, key):
    deferred.defer(delete_entities_with_reference_task, cls, property, key, _queue='housekeeping')

