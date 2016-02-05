from webapp2 import RequestHandler as BaseHandler
import datetime
from utils import get_location_from_serial, create_merged_dictionary
from data_processing import *
from database_calls import *


class MultiResourceByDate(BaseHandler):
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

        self.response.headers['Content-Type'] = 'text/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=one-resource-by-date.csv'
        self.response.write(csv_to_publish)


class OneResourceByDate(BaseHandler):
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

        self.response.headers['Content-Type'] = 'text/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=one-resource-by-date.csv'
        self.response.write(csv_to_publish)


class OneResourceByLocation(BaseHandler):
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

        self.response.headers['Content-Type'] = 'text/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=one-resource-by-date.csv'
        self.response.write(csv_to_publish)
