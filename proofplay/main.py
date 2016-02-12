from webapp2 import RequestHandler
from utils import create_merged_dictionary
from database_calls import *
from data_processing import *
import logging
import json
from models import Domain, Tenant, TenantEntityGroup
from google.appengine.ext import deferred, ndb


def get_tenant_list_from_distributor_key(distributor_key):
    distributor = ndb.Key(urlsafe=distributor_key)
    domain_keys = Domain.query(Domain.distributor_key == distributor).fetch(100, keys_only=True)
    tenant_list = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
    tenant_list = filter(lambda x: x.active is True, tenant_list)
    result = filter(lambda x: x.domain_key in domain_keys, tenant_list)
    return result


class GetTenant(RequestHandler):
    def get(self):
        distributor_key = self.request.headers.get('X-Provisioning-Distributor')
        results = get_tenant_list_from_distributor_key(distributor_key)
        final = [result.name for result in results]
        json_final = json.dumps({"result": final})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json_final)


class RetrieveAllResources(RequestHandler):
    def get(self):
        distributor_key = self.request.headers.get('X-Provisioning-Distributor')
        result = get_tenant_list_from_distributor_key(distributor_key)
        print result
        resources = retrieve_all_resources()
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


class MultiResourceByDate(RequestHandler):
    def get(self, start_date, end_date, resources):
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

        all_of_the_dictionaries_to_get_data_on = [
            {
                "resource": resource,
                "raw_data": get_raw_program_record_data_for_resource_between_date_ranges_by_date(
                        midnight_start_day,
                        just_before_next_day_end_date,
                        resource
                )
            } for resource in all_the_resources_final]

        resulting_dictionaries_of_data = list(map(
                get_total_play_count_of_resource_between_date_range_for_all_locations,
                all_of_the_dictionaries_to_get_data_on
        ))

        merged_dict = create_merged_dictionary(resulting_dictionaries_of_data)

        now = datetime.datetime.now()

        csv_to_publish = generate_date_range_csv_for_a_multiple_resources(
                midnight_start_day,
                just_before_next_day_end_date,
                all_the_resources_final,
                merged_dict,
                now
        )

        self.response.headers['Content-Type'] = 'application/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=multi-resource-by-date.csv'
        self.response.write(bytes(csv_to_publish.getvalue()))


class OneResourceByDate(RequestHandler):
    def get(self, start_date, end_date, resource):
        start_date = datetime.datetime.fromtimestamp(int(start_date))
        end_date = datetime.datetime.fromtimestamp(int(end_date))

        if end_date < start_date:
            self.response.out.write("ERROR: YOUR START DAY IS AFTER YOUR END DAY")

        midnight_start_day = datetime.datetime.combine(start_date.date(), datetime.time())
        midnight_end_day = datetime.datetime.combine(end_date.date(), datetime.time())
        just_before_next_day_end_date = (midnight_end_day + datetime.timedelta(days=1)) - datetime.timedelta(
                seconds=1
        )

        raw_data = get_raw_program_record_data_for_resource_between_date_ranges_by_date(
                midnight_start_day,
                just_before_next_day_end_date,
                resource
        )

        to_put_in = {
            "raw_data": raw_data,
            "resource": resource
        }

        dictionary = get_total_play_count_of_resource_between_date_range_for_all_locations(
                to_put_in
        )

        now = datetime.datetime.now()

        csv_to_publish = generate_date_range_csv_for_a_single_resource(
                midnight_start_day,
                just_before_next_day_end_date,
                resource,
                dictionary,
                now
        )

        self.response.headers['Content-Type'] = 'application/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=one-resource-by-date.csv'
        self.response.write(bytes(csv_to_publish.getvalue()))


class OneResourceByDevice(RequestHandler):
    def get(self, start_date, end_date, resource):
        start_date = datetime.datetime.fromtimestamp(int(start_date))
        end_date = datetime.datetime.fromtimestamp(int(end_date))

        if end_date < start_date:
            self.response.out.write("ERROR: YOUR START DAY IS AFTER YOUR END DAY")

        midnight_start_day = datetime.datetime.combine(start_date.date(), datetime.time())
        midnight_end_day = datetime.datetime.combine(end_date.date(), datetime.time())
        just_before_next_day_end_date = (midnight_end_day + datetime.timedelta(days=1)) - datetime.timedelta(
                seconds=1
        )

        dictionary = get_raw_program_record_data_for_resource_between_date_ranges_by_location(
                midnight_start_day, just_before_next_day_end_date, resource
        )

        formatted_dictionary = format_raw_program_record_data_for_single_resource_by_location(dictionary)

        csv_to_publish = generate_date_range_csv_for_single_resource_by_location(
                midnight_start_day,
                just_before_next_day_end_date,
                resource,
                formatted_dictionary,
                datetime.datetime.now()
        )

        self.response.headers['Content-Type'] = 'application/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=one-resource-by-device.csv'
        self.response.write(bytes(csv_to_publish.getvalue()))


def handle_posting_a_new_program_play(incoming_data):
    for each_log in incoming_data["data"]:
        logging.info("INCOMING JSON ARRAY")
        logging.info(each_log)
        try:
            raw_event_id = insert_raw_program_play_event_data(each_log)
            resource = each_log["resource_name"]
            resource_id = each_log["resource_id"]
            serial_number = each_log["serial_number"]
            device_key = each_log["device_key"]
            tenant_code = each_log["tenant_code"]
            started_at = datetime.datetime.strptime(each_log["started_at"], '%Y-%m-%dT%H:%M:%S.%fZ')
            ended_at = datetime.datetime.strptime(each_log["ended_at"], '%Y-%m-%dT%H:%M:%S.%fZ')

            if 'location_id' in each_log:
                location_name = each_log["location_id"]
                location_id = insert_new_location_or_get_existing(location_name)

            else:
                location_id = None

            resource_id = insert_new_resource_or_get_existing(resource, resource_id)
            device_id = insert_new_device_or_get_existing(location_id, serial_number, device_key, tenant_code)
            insert_new_program_record(location_id, device_id, resource_id, started_at, ended_at)
            mark_raw_event_complete(raw_event_id)

        except KeyError:
            logging.warn("ERROR: KEYERROR IN POSTING A NEW PROGRAM PLAY")
