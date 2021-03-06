# main.py
import datetime
import json
import logging
import os

from alembic import command
from google.appengine.ext import deferred
from webapp2 import RequestHandler

from data_processing import *
from database_calls import *
from decorators import (
    has_tenant_in_distributor_header,
    has_distributor_key,
    has_tenant_in_distributor_param,
    requires_api_token
)
from dev.generate_mock_data import generate_mock_data
from proofplay_config import config
from routes_proofplay import basedir
from utils.tenant_util import get_tenant_names_for_distributor


####################################################################################
# SEED
####################################################################################
class Seed(RequestHandler):
    def get(self, days, amount_a_day):
        deferred.defer(generate_mock_data, int(days), int(amount_a_day))
        json_final = json.dumps({
            "result": "success",
            "message": "The seed script has begun with {} days worth of data being posted {} times a day".format(
                days, amount_a_day)
        })
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json_final)


####################################################################################
# ALEMBIC MIGRATION
####################################################################################
class MakeMigration(RequestHandler):
    def get(self):
        try:
            from alembic.config import Config
            path = os.path.join(basedir, "alembic.ini")
            alembic_cfg = Config(path)
            alembic_cfg.set_main_option('sqlalchemy.url', config.SQLALCHEMY_DATABASE_URI)
            command.upgrade(alembic_cfg, "head")
            self.response.out.write(
                "SUCCESS. Migrations Applied Successfully (or no change to model schema necessary).")

        except Exception as e:
            logging.error(e)
            self.response.out.write(
                "FAILURE. Exception caught during alembic migrations. Check the developer console logs.")


####################################################################################
# DELETE MIGRATION
####################################################################################
class ManageRawPayloadTable(RequestHandler):
    def get(self):
        delete_raw_event_entries_older_than_thirty_days()
        json_final = json.dumps({
            "result": "success",
            "message": "raw events older than thirty days were deleted"
        })
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json_final)


####################################################################################
# REST CALLS
####################################################################################
class GetTenants(RequestHandler):
    @has_distributor_key
    def get(self):
        distributor = self.request.headers.get('X-Provisioning-Distributor')
        tenants = get_tenant_names_for_distributor(distributor)
        json_final = json.dumps({"tenants": tenants})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json_final)


class RetrieveAllDevicesOfTenant(RequestHandler):
    @has_tenant_in_distributor_header
    def get(self, tenant):
        devices = retrieve_all_devices_of_tenant(tenant)
        final = json.dumps({"devices": devices})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(final)


class RetrieveAllResourcesOfTenant(RequestHandler):
    @has_tenant_in_distributor_header
    def get(self, tenant):
        resources = retrieve_all_resources_of_tenant(tenant)
        final = json.dumps({"resources": resources})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(final)


class RetrieveAllLocationsOfTenant(RequestHandler):
    @has_tenant_in_distributor_header
    def get(self, tenant):
        locations = retrieve_all_locations_of_tenant(tenant)
        final = json.dumps({"locations": locations})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(final)


####################################################################################
# MAIN ENTRY FOR POSTING NEW PROGRAM PLAY
####################################################################################
class PostNewProgramPlay(RequestHandler):
    @requires_api_token
    def post(self):
        incoming = json.loads(self.request.body)
        logging.info("NEW BATCH OF LOGS: ")
        logging.info(incoming)
        deferred.defer(handle_posting_a_new_program_play,
                       incoming,
                       _queue="proof-of-play")
        final = json.dumps({"success": True, "message": "NEW PROGRAM WILL BE PROCESSED IN THE TASK QUEUE"})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(final)


####################################################################################
# CSV QUERY HANDLERS
####################################################################################
####################################################################################
# RESOURCES
####################################################################################
class MultiResourceByDevice(RequestHandler):
    @has_tenant_in_distributor_param
    def get(self, start_date, end_date, resource_identifiers, tenant, distributor_key):
        ###########################################################
        # SETUP VARIABLES
        ###########################################################
        start_date = datetime.datetime.fromtimestamp(int(start_date))
        end_date = datetime.datetime.fromtimestamp(int(end_date))

        if end_date < start_date:
            return self.response.out.write("ERROR: YOUR START DAY IS AFTER YOUR END DAY")

        midnight_start_day = datetime.datetime.combine(start_date.date(), datetime.time())
        midnight_end_day = datetime.datetime.combine(end_date.date(), datetime.time())
        just_before_next_day_end_date = (midnight_end_day + datetime.timedelta(days=1)) - datetime.timedelta(
            seconds=1
        )

        all_the_resource_identifiers = resource_identifiers.split("|")
        all_the_resource_identifiers_final = all_the_resource_identifiers[1:]
        now = datetime.datetime.now()
        ###########################################################
        # BUSINESS LOGIC
        ###########################################################
        array_of_transformed_record_data_by_location = [
            {
                "resource": resource_identifier,
                "raw_data": program_record_for_resource_by_device(
                    midnight_start_day,
                    just_before_next_day_end_date,
                    resource_identifier,
                    tenant
                )
            } for resource_identifier in all_the_resource_identifiers_final]

        formatted_record_data_for_each_resource = [
            reformat_program_record_array_by_location(record_data) for record_data in
            array_of_transformed_record_data_by_location]

        resource_identifiers_to_resource_names = [
            retrieve_resource_name_from_resource_identifier(resource_identifier) for
            resource_identifier in
            all_the_resource_identifiers_final]

        csv_to_publish = generate_resource_csv_by_device(
            midnight_start_day,
            just_before_next_day_end_date,
            resource_identifiers_to_resource_names,
            formatted_record_data_for_each_resource,
            now
        )

        self.response.headers['Content-Type'] = 'application/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=MultiResourceByDevice.csv'
        self.response.write(bytes(csv_to_publish.getvalue()))


class MultiResourceByDate(RequestHandler):
    @has_tenant_in_distributor_param
    def get(self, start_date, end_date, resource_identifiers, tenant, distributor_key):
        ###########################################################
        # SETUP VARIABLES
        ###########################################################
        start_date = datetime.datetime.fromtimestamp(int(start_date))
        end_date = datetime.datetime.fromtimestamp(int(end_date))
        if end_date < start_date:
            return self.response.out.write("ERROR: YOUR START DAY IS AFTER YOUR END DAY")

        midnight_start_day = datetime.datetime.combine(start_date.date(), datetime.time())
        midnight_end_day = datetime.datetime.combine(end_date.date(), datetime.time())
        just_before_next_day_end_date = (midnight_end_day + datetime.timedelta(days=1)) - datetime.timedelta(
            seconds=1
        )

        all_the_resource_identifiers = resource_identifiers.split("|")
        all_the_resource_identifiers_final = all_the_resource_identifiers[1:]
        now = datetime.datetime.now()
        ###########################################################
        # BUSINESS LOGIC
        ###########################################################
        pre_formatted_program_record_by_date = [
            {
                "resource": resource_identifier,
                # program_record is the transformed program record table data
                "raw_data": program_record_for_resource_by_date(
                    midnight_start_day,
                    just_before_next_day_end_date,
                    resource_identifier,
                    tenant
                )
            } for resource_identifier in all_the_resource_identifiers_final]

        formatted_data = format_program_record_data_with_array_of_resources_by_date(
            midnight_start_day,
            just_before_next_day_end_date,
            pre_formatted_program_record_by_date
        )

        resource_identifiers_to_resource_names = [retrieve_resource_name_from_resource_identifier(resource_identifier)
                                                  for
                                                  resource_identifier in
                                                  all_the_resource_identifiers_final]

        csv_to_publish = generate_resource_csv_by_date(
            midnight_start_day,
            just_before_next_day_end_date,
            resource_identifiers_to_resource_names,
            formatted_data,
            now
        )

        self.response.headers['Content-Type'] = 'application/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=MultiResourceByDate.csv'
        self.response.write(bytes(csv_to_publish.getvalue()))


####################################################################################
# DEVICES
####################################################################################
class MultiDeviceSummarized(RequestHandler):
    @has_tenant_in_distributor_param
    def get(self, start_date, end_date, devices, tenant, distributor_key):
        ###########################################################
        # SETUP VARIABLES
        ###########################################################
        start_date = datetime.datetime.fromtimestamp(int(start_date))
        end_date = datetime.datetime.fromtimestamp(int(end_date))
        if end_date < start_date:
            return self.response.out.write("ERROR: YOUR START DAY IS AFTER YOUR END DAY")

        midnight_start_day = datetime.datetime.combine(start_date.date(), datetime.time())
        midnight_end_day = datetime.datetime.combine(end_date.date(), datetime.time())
        just_before_next_day_end_date = (midnight_end_day + datetime.timedelta(days=1)) - datetime.timedelta(
            seconds=1
        )

        all_the_devices = devices.split("|")
        all_the_devices_final = all_the_devices[1:]
        now = datetime.datetime.now()

        ###########################################################

        array_of_transformed_program_data_by_device = [
            {
                "device": device,
                # program_record is the transformed program record table data
                "raw_data": program_record_for_device_summarized(
                    midnight_start_day,
                    just_before_next_day_end_date,
                    device,
                    tenant
                )
            } for device in all_the_devices_final]

        formatted_data = format_transformed_program_data_by_device(array_of_transformed_program_data_by_device)

        csv_to_publish = generate_device_csv_summarized(
            start_date=midnight_start_day,
            end_date=just_before_next_day_end_date,
            displays=all_the_devices_final,
            array_of_data=formatted_data,
            created_time=now
        )

        self.response.headers['Content-Type'] = 'application/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=MultiDeviceSummarized.csv'
        self.response.write(bytes(csv_to_publish.getvalue()))


class MultiDeviceByDate(RequestHandler):
    @has_tenant_in_distributor_param
    def get(self, start_date, end_date, devices, tenant, distributor_key):
        ###########################################################
        # SETUP VARIABLES
        ###########################################################
        start_date = datetime.datetime.fromtimestamp(int(start_date))
        end_date = datetime.datetime.fromtimestamp(int(end_date))
        if end_date < start_date:
            return self.response.out.write("ERROR: YOUR START DAY IS AFTER YOUR END DAY")

        midnight_start_day = datetime.datetime.combine(start_date.date(), datetime.time())
        midnight_end_day = datetime.datetime.combine(end_date.date(), datetime.time())
        just_before_next_day_end_date = (midnight_end_day + datetime.timedelta(days=1)) - datetime.timedelta(
            seconds=1
        )

        all_the_devices = devices.split("|")
        all_the_devices_final = all_the_devices[1:]
        now = datetime.datetime.now()

        ###########################################################

        transformed_query_by_device_program_data_to_by_date = [
            {
                "device": device,
                # program_record is the transformed program record table data
                "raw_data": program_record_for_device_by_date(
                    midnight_start_day,
                    just_before_next_day_end_date,
                    device,
                    tenant
                )
            } for device in all_the_devices_final]

        formatted_data = prepare_transformed_query_by_device_to_csv_by_date(
            midnight_start_day,
            just_before_next_day_end_date,
            transformed_query_by_device_program_data_to_by_date
        )

        csv_to_publish = generate_device_csv_by_date(
            start_date=midnight_start_day,
            end_date=just_before_next_day_end_date,
            displays=all_the_devices_final,
            dictionary_of_data=formatted_data,
            created_time=now
        )

        self.response.headers['Content-Type'] = 'application/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=MultiDeviceByDate.csv'
        self.response.write(bytes(csv_to_publish.getvalue()))


####################################################################################
# LOCATIONS
####################################################################################
class MultiLocationSummarized(RequestHandler):
    @has_tenant_in_distributor_param
    def get(self, start_date, end_date, locations, tenant, distributor_key):
        ###########################################################
        # SETUP VARIABLES
        ###########################################################
        start_date = datetime.datetime.fromtimestamp(int(start_date))
        end_date = datetime.datetime.fromtimestamp(int(end_date))
        if end_date < start_date:
            return self.response.out.write("ERROR: YOUR START DAY IS AFTER YOUR END DAY")

        midnight_start_day = datetime.datetime.combine(start_date.date(), datetime.time())
        midnight_end_day = datetime.datetime.combine(end_date.date(), datetime.time())
        just_before_next_day_end_date = (midnight_end_day + datetime.timedelta(days=1)) - datetime.timedelta(
            seconds=1
        )

        all_the_locations = locations.split("|")
        all_the_locations_final = all_the_locations[1:]
        now = datetime.datetime.now()

        ###########################################################

        array_of_transformed_program_data_by_device = [
            {
                "location": location,
                # program_record is the transformed program record table data
                "raw_data": program_record_for_location_summarized(
                    midnight_start_day,
                    just_before_next_day_end_date,
                    location,
                    tenant
                )
            } for location in all_the_locations_final]

        formatted_data = [
            format_multi_location_summarized(the_data) for the_data in
            array_of_transformed_program_data_by_device
            ]

        merged_formatted_data = create_merged_dictionary(formatted_data)

        csv_to_publish = generate_location_csv_summarized(
            start_date=midnight_start_day,
            end_date=just_before_next_day_end_date,
            locations=all_the_locations_final,
            dictionary_of_data=merged_formatted_data,
            created_time=now
        )

        self.response.headers['Content-Type'] = 'application/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=MultiLocationSummarized.csv'
        self.response.write(bytes(csv_to_publish.getvalue()))


class MultiLocationByDevice(RequestHandler):
    @has_tenant_in_distributor_param
    def get(self, start_date, end_date, locations, tenant, distributor_key):
        ###########################################################
        # SETUP VARIABLES
        ###########################################################
        start_date = datetime.datetime.fromtimestamp(int(start_date))
        end_date = datetime.datetime.fromtimestamp(int(end_date))
        if end_date < start_date:
            return self.response.out.write("ERROR: YOUR START DAY IS AFTER YOUR END DAY")

        midnight_start_day = datetime.datetime.combine(start_date.date(), datetime.time())
        midnight_end_day = datetime.datetime.combine(end_date.date(), datetime.time())
        just_before_next_day_end_date = (midnight_end_day + datetime.timedelta(days=1)) - datetime.timedelta(
            seconds=1
        )

        all_the_locations = locations.split("|")
        all_the_locations_final = all_the_locations[1:]
        now = datetime.datetime.now()

        ###########################################################

        array_of_transformed_program_data_by_device = [
            {
                "location": location,
                # program_record is the transformed program record table data
                "raw_data": program_record_for_location_summarized(
                    midnight_start_day,
                    just_before_next_day_end_date,
                    location,
                    tenant
                )
            } for location in all_the_locations_final]

        formatted_data = [
            format_multi_location_by_device(program_data) for program_data in
            array_of_transformed_program_data_by_device
            ]

        merged_formatted_data = create_merged_dictionary(formatted_data)

        csv_to_publish = generate_location_csv_by_device(
            start_date=midnight_start_day,
            end_date=just_before_next_day_end_date,
            locations=all_the_locations_final,
            dictionary_of_data=merged_formatted_data,
            created_time=now
        )

        self.response.headers['Content-Type'] = 'application/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=MultiLocationByDevice.csv'
        self.response.write(bytes(csv_to_publish.getvalue()))


####################################################################################
# FUNCTION THAT GETS CALLED VIA DEFERRED ON NEW PROGRAM PLAY POST
####################################################################################
def handle_posting_a_new_program_play(incoming_data):
    for each_log in incoming_data["data"]:
        try:
            if each_log['customer_location_code'] and each_log['customer_display_code']:
                raw_event_id = insert_raw_program_play_event_data(each_log)
                resource_name = each_log["resource_name"]
                resource_id = each_log["resource_id"]
                serial_number = each_log["serial_number"]
                device_key = each_log["device_key"]
                tenant_code = each_log["tenant_code"]
                started_at = datetime.datetime.strptime(each_log["started_at"], '%Y-%m-%dT%H:%M:%S.%fZ')
                ended_at = datetime.datetime.strptime(each_log["ended_at"], '%Y-%m-%dT%H:%M:%S.%fZ')
                customer_location_code = each_log["customer_location_code"]
                customer_display_code = each_log["customer_display_code"]

                # an unmanaged device will have these potential attributes
                if not serial_number or serial_number == "null" or serial_number == "undefined" or serial_number == "":
                    serial_number = "None"

                if not customer_location_code:
                    customer_location_code = "None"

                if not customer_display_code:
                    customer_display_code = "None"

                logging.info(each_log)

                tenant_id = insert_new_tenant_code_or_get_existing(
                    tenant_code
                )

                location_id = insert_new_location_or_get_existing(customer_location_code, tenant_id)

                resource_id = insert_new_resource_or_get_existing(
                    resource_name,
                    resource_id,
                    tenant_code
                )

                device_id = insert_new_device_or_get_existing(
                    location_id,
                    serial_number,
                    device_key,
                    customer_display_code,
                    tenant_code
                )

                insert_new_program_record(
                    location_id, device_id, resource_id, started_at, ended_at)

                mark_raw_event_complete(raw_event_id)

        except KeyError:
            logging.warn("ERROR: KEYERROR IN POSTING A NEW PROGRAM PLAY. THE RECORD WILL NOT BE STORED. ")
