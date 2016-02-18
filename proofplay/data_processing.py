import csv
import StringIO
import datetime
from collections import OrderedDict


def transform_resource_data_between_date_range_by_location_to_dict_by_device(from_db):
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


def generate_date_range_csv_by_date(start_date, end_date, resources, dictionary, now):
    tmp = StringIO.StringIO()
    writer = csv.writer(tmp)
    all_resources_as_string = ', '.join(resources)
    writer.writerow(["Creation Date", "Start Date", "End Date", "Start Time", "End Time", "All Content"])
    writer.writerow([str(now), str(start_date), str(end_date), "12:00 AM", "11:59 PM",
                     all_resources_as_string])
    writer.writerow(["Content", "Date", "Location Count", "Display Count", "Play Count"])

    for key, value in dictionary.iteritems():
        for sub_key, sub_value in dictionary[key].iteritems():
            writer.writerow([key, str(sub_key), sub_value["LocationCount"],
                             sub_value["PlayerCount"], sub_value["PlayCount"]])

    tmp.seek(0)
    return tmp


def format_program_record_data_with_array_of_resources(incoming_array):
    to_return = {}

    for item in incoming_array:
        to_return[item["resource"]] = OrderedDict()
        ordered_raw_data = OrderedDict(sorted(item["raw_data"].items(), key=lambda t: t))

        for key, value in ordered_raw_data.iteritems():
            to_return[item["resource"]][key] = {}
            to_return[item["resource"]][key]["LocationCount"] = calculate_location_count(value)
            to_return[item["resource"]][key]["PlayerCount"] = calculate_serial_count(value)
            to_return[item["resource"]][key]["PlayCount"] = len(value)

    return to_return


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


def reformat_program_record_by_location(dictionary):
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


def count_resource_plays_from_dict_by_device(the_dict):
    temp_dict = {}

    """
    sets up temp_dict to contain an amount of times resource played per device:
    temp_dict = {
        "my-device": {
            "location": "3443",
            "resource_55442": 54,
             "resource_3342": 34,
        },
        "my-device-2": {
            "location": "3443",
            "resource_55442": 54,
             "resource_3342": 34,
             "resource_3342": 3,
        }
    }
    """
    for key, value in the_dict.iteritems():
        if key not in temp_dict:
            temp_dict[key] = {
                "location": value["location_id"]
            }

        if value["resource_id"] not in temp_dict[key]:
            temp_dict[key][value["resource_id"]] = 0

        temp_dict[key][value["resource_id"]] += 1

    return temp_dict


def format_raw_program_data_for_all_devices(array_of_raw_db):
    to_return = []

    transformed_to_by_device = transform_resource_data_between_date_range_by_location_to_dict_by_device(array_of_raw_db)
    temp_dict = count_resource_plays_from_dict_by_device(transformed_to_by_device)

    for key, value in temp_dict.iteritems():
        dictionary_to_append_to_to_return = {
            "display": key,
            "location": value["location"],
        }

        for another_key, another_value in temp_dict[key].iteritems():
            if another_key == "location":
                pass
            else:
                dictionary_to_append_to_to_return["content"] = another_key
                dictionary_to_append_to_to_return["playcount"] = temp_dict[key][another_key]

        to_return.append(dictionary_to_append_to_to_return)

    return to_return


def generate_summarized_csv_by_device(start_date, end_date, displays, array_of_data, created_time):
    tmp = StringIO.StringIO()
    writer = csv.writer(tmp)

    writer.writerow(["Creation Date", "Start Date", "End Date", "Displays"])
    writer.writerow([str(created_time), str(start_date), str(end_date), ', '.join(displays)])
    writer.writerow(["Display", "Location", "Content", "Play Count"])

    for item in array_of_data:
        writer.writerow([item["display"], item["location"], item["content"], item["playcount"]])

    tmp.seek(0)
    return tmp
