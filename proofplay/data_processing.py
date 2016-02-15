import csv
import StringIO
from utils import join_array_of_strings, order_dictionary_with_datetimes_as_keys
import datetime


def transform_resource_data_between_date_range_by_location(from_db):
    to_return = {}

    for item in from_db:
        device_id = item["device_id"]
        if device_id not in to_return:
            to_return[device_id] = []

        to_return[device_id].append(item)

    return to_return


def transform_resource_data_between_date_ranges_by_date(from_db):
    to_return = {}

    for item in from_db:
        started_at = item["started_at"]
        midnight_start_day = str(datetime.datetime.combine(started_at.date(), datetime.time()))

        if midnight_start_day not in to_return:
            to_return[midnight_start_day] = []

        to_return[midnight_start_day].append(item)

    return to_return


def format_raw_program_record_data_for_single_resource_by_location(dictionary):
    all_results = {}

    for key, value in dictionary.iteritems():
        all_results[key] = {
            "PlayCount": len(value),
            "Device": value[0]["device_id"]
        }

    return all_results


def generate_date_range_csv_by_location(start_date, end_date, resources, array_of_data, created_time):
    tmp = StringIO.StringIO()
    writer = csv.writer(tmp)

    writer.writerow(["Creation Date", "Start Date", "End Date", "Content"])
    writer.writerow([str(created_time), str(start_date), str(end_date), ', '.join(resources)])
    writer.writerow(["Content", "Display", "Location", "Play Count"])

    for item in array_of_data:
        for key, value in item.iteritems():
            writer.writerow([value["Content"], value["Display"], value["Location"], value["Play Count"]])

    tmp.seek(0)
    return tmp


def generate_date_range_csv_for_a_multiple_resources(start_date, end_date, resources, dictionary, now):
    tmp = StringIO.StringIO()
    writer = csv.writer(tmp)
    all_resources_as_string = join_array_of_strings(resources)
    writer.writerow(["Creation Date", "Start Date", "End Date", "Start Time", "End Time", "Content"])
    writer.writerow([str(now), str(start_date), str(end_date), "12:00 AM", "11:59 PM",
                     all_resources_as_string])
    writer.writerow(["File", "Date", "Location Count", "Display Count", "Play Count"])

    for resource in resources:
        resource_data = dictionary[resource]
        for item in order_dictionary_with_datetimes_as_keys(resource_data):
            writer.writerow([resource, str(item), resource_data[item]["LocationCount"],
                             resource_data[item]["PlayerCount"], resource_data[item]["PlayCount"]])

    tmp.seek(0)
    return tmp


def generate_date_range_csv_for_a_single_resource(start_date, end_date, resource, dictionary, now):
    tmp = StringIO.StringIO()
    writer = csv.writer(tmp)
    writer.writerow(["Creation Date", "Start Date", "End Date", "Start Time", "End Time", "Content"])
    writer.writerow([str(now), str(start_date), str(end_date), "12:00 AM", "11:59 PM", resource])
    writer.writerow(["File", "Date", "Location Count", "Player Count", "Play Count"])

    resource_data = dictionary[resource]
    for item in order_dictionary_with_datetimes_as_keys(resource_data):
        writer.writerow([resource, str(item), resource_data[item]["LocationCount"],
                         resource_data[item]["PlayerCount"], resource_data[item]["PlayCount"]])

    tmp.seek(0)
    return tmp


def calculate_location_count(value):
    locations = []
    for item in value:
        if item["location_id"] not in locations:
            locations.append(item["location_id"])

    return len(locations)


def calculate_serial_count(array_of_db_data):
    serials = []
    for item in array_of_db_data:
        if item["device_id"] not in serials:
            serials.append(item["device_id"])
    return len(serials)


def get_total_play_count_of_resource_between_date_range_for_all_locations(dictionary):
    resource = dictionary["resource"]
    raw_data = dictionary["raw_data"]

    to_return = {}

    for key, value in raw_data.iteritems():
        to_return[key] = {
            "Content": resource,
            "Display": key,
            "Location": value[0]["location_id"],
            "Play Count": len(value),
        }

    return to_return
