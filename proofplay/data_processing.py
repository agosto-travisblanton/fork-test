import csv
import StringIO
import datetime
from collections import OrderedDict
from itertools import chain


def create_merged_dictionary(array_of_dictionaries_to_merge):
    return dict(chain.from_iterable(d.iteritems() for d in array_of_dictionaries_to_merge))


def transform_db_data_to_by_device(from_db):
    to_return = {}

    for item in from_db:
        device_id = item["device_id"]
        if device_id not in to_return:
            to_return[device_id] = []

        to_return[device_id].append(item)

    return to_return


def transform_db_data_to_by_date(from_db):
    to_return = {}

    for item in from_db:
        started_at = item["started_at"]
        midnight_start_day = str(datetime.datetime.combine(started_at.date(), datetime.time()))

        if midnight_start_day not in to_return:
            to_return[midnight_start_day] = []

        to_return[midnight_start_day].append(item)

    return to_return


def generate_resource_csv_by_device(start_date, end_date, resources, array_of_data, created_time):
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


def generate_resource_csv_by_date(start_date, end_date, resources, dictionary, now):
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


def ensure_raw_data_dictionary_has_keys_through_date_range(start_date, end_date, dictionary):
    while start_date <= end_date:
        if str(start_date) not in dictionary:
            dictionary[str(start_date)] = None
        start_date += datetime.timedelta(days=1)

    return OrderedDict(sorted(dictionary.items(), key=lambda t: t))


def ensure_dictionary_has_keys_through_date_range(start_date, end_date, dictionary):
    while start_date <= end_date:
        if str(start_date) not in dictionary:
            dictionary[str(start_date)] = {
                "PlayerCount": 0,
                "LocationCount": 0,
                "PlayCount": 0
            }
        start_date += datetime.timedelta(days=1)

    return OrderedDict(sorted(dictionary.items(), key=lambda t: t))


def format_program_record_data_with_array_of_resources_by_date(start_date, end_date, incoming_array):
    to_return = {}

    for item in incoming_array:
        to_return[item["resource"]] = OrderedDict()
        ordered_raw_data = OrderedDict(sorted(item["raw_data"].items(), key=lambda t: t))

        for key, value in ordered_raw_data.iteritems():
            to_return[item["resource"]][key] = {}
            to_return[item["resource"]][key]["LocationCount"] = calculate_location_count(value)
            to_return[item["resource"]][key]["PlayerCount"] = calculate_serial_count(value)
            to_return[item["resource"]][key]["PlayCount"] = len(value)

        to_return[item["resource"]] = ensure_dictionary_has_keys_through_date_range(
                start_date,
                end_date,
                to_return[item["resource"]]
        )

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


def reformat_program_record_array_by_location(dictionary):
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


def prepare_for_csv_transformed_query_by_device_program_data_to_by_date(start_date, end_date, incoming_array):
    """
    Returns:
    {
        "device-id": {
            "12-01-2000": {
                "GSAD_1555": {
                    "location": "5003",
                    "playcount": 25
                },
                "GSAD_1111": {
                    "location": "2342",
                    "playcount": 22
                }
            },
            "12-02-2000": {
                "GSAD_1555": {
                    "location": "5003",
                    "playcount": 25
                },
                "GSAD_1111": {
                    "location": "2342",
                    "playcount": 22
                }
            }
        }
    }
    """

    to_return = OrderedDict()

    for item in incoming_array:
        to_return[item["device"]] = OrderedDict()
        ordered_raw_data = OrderedDict(sorted(item["raw_data"].items(), key=lambda t: t))

        # this key is a date object
        for key, value in ordered_raw_data.iteritems():
            to_return[item["device"]][key] = {}

            for each_log in ordered_raw_data[key]:
                if each_log["resource_id"] not in to_return[item["device"]][key]:
                    to_return[item["device"]][key][each_log["resource_id"]] = {}
                    to_return[item["device"]][key][each_log["resource_id"]]["playcount"] = 0

                to_return[item["device"]][key][each_log["resource_id"]]["playcount"] += 1
                to_return[item["device"]][key][each_log["resource_id"]]["location"] = each_log["location_id"]

    return to_return


def count_resource_plays_from_dict_by_device(the_dict):
    """
    returns
    {
        "my-device": {
            "location": "3443",
            "resource_55442": 54,
            "resource_3342": 34,
        }
    }
    """
    to_return = {}

    for key, value in the_dict["raw_data"].iteritems():
        if key not in to_return:
            to_return[key] = {
                # since one serial will always have the same location
                "location": the_dict["raw_data"][key][0]["location_id"]
            }

        for each in the_dict["raw_data"][key]:
            if each["resource_id"] not in to_return[key]:
                to_return[key][each["resource_id"]] = 0

            to_return[key][each["resource_id"]] += 1

    return to_return


def format_transformed_program_data_by_device(array_of_transformed):
    to_return = []

    array_of_unmerged_dictionaries = map(count_resource_plays_from_dict_by_device, array_of_transformed)

    merged_dict_of_all_devices = create_merged_dictionary(array_of_unmerged_dictionaries)

    for key, value in merged_dict_of_all_devices.iteritems():
        for another_key, another_value in merged_dict_of_all_devices[key].iteritems():
            dictionary_to_append_to_to_return = {
                "display": key,
                "location": value["location"],
            }
            if another_key == "location":
                pass
            else:
                dictionary_to_append_to_to_return["content"] = another_key
                dictionary_to_append_to_to_return["playcount"] = another_value
                to_return.append(dictionary_to_append_to_to_return)

    return to_return


def generate_device_csv_summarized(start_date, end_date, displays, array_of_data, created_time):
    tmp = StringIO.StringIO()
    writer = csv.writer(tmp)

    writer.writerow(["Creation Date", "Start Date", "End Date", "Displays"])
    writer.writerow([str(created_time), str(start_date), str(end_date), ', '.join(displays)])
    writer.writerow(["Display", "Location", "Content", "Play Count"])

    for item in array_of_data:
        writer.writerow([item["display"], item["location"], item["content"], item["playcount"]])

    tmp.seek(0)
    return tmp


def generate_device_csv_by_date(created_time, start_date, end_date, displays, dictionary_of_data):
    tmp = StringIO.StringIO()
    writer = csv.writer(tmp)

    writer.writerow(["Creation Date", "Start Date", "End Date", "Displays"])
    writer.writerow([str(created_time), str(start_date), str(end_date), ', '.join(displays)])
    writer.writerow(["Display", "Location", "Date", "Content", "Play Count"])

    for key, value in dictionary_of_data.iteritems():
        for another_key, another_value in dictionary_of_data[key].iteritems():
            for guess_what_another_key, guess_what_another_value in dictionary_of_data[key][another_key].iteritems():
                writer.writerow([key, guess_what_another_value["location"], another_key, guess_what_another_key,
                                 guess_what_another_value["playcount"]])

    tmp.seek(0)
    return tmp
