from webapp2 import RequestHandler
from database_calls import *
from data_processing import *
import logging
import json
from google.appengine.ext import deferred


class GetTenants(RequestHandler):
    def get(self):
        distributor = self.request.headers.get('X-Provisioning-Distributor')
        if not distributor:
            self.response.write("YOU ARE NOT ALLOWED TO QUERY THIS CONTENT")
            self.abort(403)

        tenants = get_tenant_names_for_distributor(distributor)
        json_final = json.dumps({"tenants": tenants})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json_final)


class RetrieveAllDevicesOfTenant(RequestHandler):
    def get(self, tenant):
        tenants = get_tenant_names_for_distributor(self.request.headers.get('X-Provisioning-Distributor'))
        if tenant not in tenants:
            self.response.write("YOU ARE NOT ALLOWED TO QUERY THIS CONTENT")
            self.abort(403)

        devices = retrieve_all_devices_of_tenant(tenant)
        final = json.dumps({"devices": devices})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(final)


class RetrieveAllResourcesOfTenant(RequestHandler):
    def get(self, tenant):
        tenants = get_tenant_names_for_distributor(self.request.headers.get('X-Provisioning-Distributor'))
        if tenant not in tenants:
            self.response.write("YOU ARE NOT ALLOWED TO QUERY THIS CONTENT")
            self.abort(403)

        resources = retrieve_all_resources_of_tenant(tenant)
        final = json.dumps({"resources": resources})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(final)


class PostNewProgramPlay(RequestHandler):
    def post(self):
        incoming = json.loads(self.request.body)
        deferred.defer(handle_posting_a_new_program_play, incoming)
        final = json.dumps({"success": True, "message": "NEW PROGRAM WILL BE PROCESSED IN THE TASK QUEUE"})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(final)


class MultiResourceByDevice(RequestHandler):
    def get(self, start_date, end_date, resources, tenant, distributor_key):

        if tenant not in get_tenant_names_for_distributor(distributor_key):
            self.response.write("YOU ARE NOT ALLOWED TO QUERY THIS CONTENT")
            self.abort(403)

        ###########################################################
        # SETUP VARIABLES
        ###########################################################
        start_date = datetime.datetime.fromtimestamp(int(start_date))
        end_date = datetime.datetime.fromtimestamp(int(end_date))

        if end_date < start_date:
            self.response.out.write("ERROR: YOUR START DAY IS AFTER YOUR END DAY")

        midnight_start_day = datetime.datetime.combine(start_date.date(), datetime.time())
        midnight_end_day = datetime.datetime.combine(end_date.date(), datetime.time())
        just_before_next_day_end_date = (midnight_end_day + datetime.timedelta(days=1)) - datetime.timedelta(
                seconds=1
        )

        all_the_resources = resources.split('-')
        all_the_resources_final = all_the_resources[1:]
        now = datetime.datetime.now()
        ###########################################################

        list_of_transformed_record_data_by_location = [
            {
                "resource": resource,
                "raw_data": program_record_for_resource_by_location(
                        midnight_start_day,
                        just_before_next_day_end_date,
                        resource,
                        tenant
                )
            } for resource in all_the_resources_final]

        formatted_record_data_for_each_resource = list(map(
                reformat_program_record_by_location,
                list_of_transformed_record_data_by_location
        ))

        csv_to_publish = generate_date_range_csv_by_location(
                midnight_start_day,
                just_before_next_day_end_date,
                all_the_resources_final,
                formatted_record_data_for_each_resource,
                now
        )

        self.response.headers['Content-Type'] = 'application/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=one-resource-by-device.csv'
        self.response.write(bytes(csv_to_publish.getvalue()))


class MultiResourceByDate(RequestHandler):
    def get(self, start_date, end_date, resources, tenant, distributor_key):

        if tenant not in get_tenant_names_for_distributor(distributor_key):
            self.response.write("YOU ARE NOT ALLOWED TO QUERY THIS CONTENT")
            self.abort(403)

        ###########################################################
        # SETUP VARIABLES
        ###########################################################
        start_date = datetime.datetime.fromtimestamp(int(start_date))
        end_date = datetime.datetime.fromtimestamp(int(end_date))
        if end_date < start_date:
            self.response.out.write("ERROR: YOUR START DAY IS AFTER YOUR END DAY")

        midnight_start_day = datetime.datetime.combine(start_date.date(), datetime.time())
        midnight_end_day = datetime.datetime.combine(end_date.date(), datetime.time())
        just_before_next_day_end_date = (midnight_end_day + datetime.timedelta(days=1)) - datetime.timedelta(
                seconds=1
        )

        all_the_resources = resources.split('-')
        all_the_resources_final = all_the_resources[1:]
        now = datetime.datetime.now()

        ###########################################################

        pre_formatted_program_record_by_date = [
            {
                "resource": resource,
                # program_record is the transformed program record table data
                "raw_data": program_record_for_resource_by_date(
                        midnight_start_day,
                        just_before_next_day_end_date,
                        resource,
                        tenant
                )
            } for resource in all_the_resources_final]

        formatted_data = format_program_record_data_with_array_of_resources(midnight_start_day,
                                                                            just_before_next_day_end_date,
                                                                            pre_formatted_program_record_by_date)

        csv_to_publish = generate_date_range_csv_by_date(
                midnight_start_day,
                just_before_next_day_end_date,
                all_the_resources_final,
                formatted_data,
                now
        )

        self.response.headers['Content-Type'] = 'application/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=multi-resource-by-date.csv'
        self.response.write(bytes(csv_to_publish.getvalue()))


class MultiDeviceSummarized(RequestHandler):
    def get(self, start_date, end_date, devices, tenant, distributor_key):

        if tenant not in get_tenant_names_for_distributor(distributor_key):
            self.response.write("YOU ARE NOT ALLOWED TO QUERY THIS CONTENT")
            self.abort(403)

        ###########################################################
        # SETUP VARIABLES
        ###########################################################
        start_date = datetime.datetime.fromtimestamp(int(start_date))
        end_date = datetime.datetime.fromtimestamp(int(end_date))
        if end_date < start_date:
            self.response.out.write("ERROR: YOUR START DAY IS AFTER YOUR END DAY")

        midnight_start_day = datetime.datetime.combine(start_date.date(), datetime.time())
        midnight_end_day = datetime.datetime.combine(end_date.date(), datetime.time())
        just_before_next_day_end_date = (midnight_end_day + datetime.timedelta(days=1)) - datetime.timedelta(
                seconds=1
        )

        all_the_devices = devices.split('-')
        all_the_devices_final = all_the_devices[1:]
        now = datetime.datetime.now()

        ###########################################################

        raw_program_data_for_all_devices = [
            {
                "device": device,
                # program_record is the transformed program record table data
                "raw_data": get_raw_program_data_by_device(
                        midnight_start_day,
                        just_before_next_day_end_date,
                        device,
                        tenant
                )
            } for device in all_the_devices_final]

        formatted_data = format_raw_program_data_for_all_devices(raw_program_data_for_all_devices)

        csv_to_publish = generate_summarized_csv_by_device(
                start_date=midnight_start_day,
                end_date=just_before_next_day_end_date,
                displays=all_the_devices_final,
                array_of_data=formatted_data,
                created_time=now
        )

        self.response.headers['Content-Type'] = 'application/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=multi-resource-by-date.csv'
        self.response.write(bytes(csv_to_publish.getvalue()))


def handle_posting_a_new_program_play(incoming_data):
    for each_log in incoming_data["data"]:
        logging.info("INCOMING JSON ARRAY")
        logging.info(each_log)
        try:
            raw_event_id = insert_raw_program_play_event_data(each_log)
            resource_name = each_log["resource_name"]
            resource_id = each_log["resource_id"]
            serial_number = each_log["serial_number"]
            device_key = each_log["device_key"]
            tenant_code = each_log["tenant_code"]
            customer_display_code = each_log["customer_display_code"]
            started_at = datetime.datetime.strptime(each_log["started_at"], '%Y-%m-%dT%H:%M:%S.%fZ')
            ended_at = datetime.datetime.strptime(each_log["ended_at"], '%Y-%m-%dT%H:%M:%S.%fZ')

            if 'customer_location_code' in each_log:
                customer_location_code = each_log["customer_location_code"]  # e.g. 6023 or "Store_6023"
                location_id = insert_new_location_or_get_existing(customer_location_code)

            else:
                location_id = None

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
            logging.warn("ERROR: KEYERROR IN POSTING A NEW PROGRAM PLAY")
