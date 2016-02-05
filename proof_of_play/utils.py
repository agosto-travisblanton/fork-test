import requests
from itertools import chain
from database_calls import get_gamestop_store_location_from_serial_via_db, insert_new_gamestop_store_location


def get_dict_of_stores_and_serials():
    o = 'https://skykit-gamestop-processor.appspot.com/api/v1/9839d92ca9be4a68bd62b5f77eafdd8c/give_the_serials'
    r = requests.get(o)
    return r.json()


def get_location_from_serial(serial):
    location_from_db = get_gamestop_store_location_from_serial_via_db(serial)

    if location_from_db:
        return location_from_db
    else:
        stores = get_dict_of_stores_and_serials()["entities"]
        for item in stores:
            insert_new_gamestop_store_location(str(item["location_id"]), item["serial_number"])

        for item in stores:
            if item["serial_number"] == serial:
                return item["location_id"]
    return None


def create_merged_dictionary(array_of_dictionaries_to_merge):
    return dict(chain.from_iterable(d.iteritems() for d in array_of_dictionaries_to_merge))


def order_dictionary_with_datetimes_as_keys(the_dict):
    ordered_array = []
    for item in sorted(the_dict):
        ordered_array.append(item)
    return ordered_array


def join_array_of_strings(array_of_strings):
    to_return = ''
    for item in array_of_strings:
        to_return = to_return + item + ";"
    return to_return
