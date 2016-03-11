import requests
import json
import datetime
import random
from app_config import config

resource_choices = [
    {"name": "GSAD_5553", "id": "1000"},
    {"name": "GSAD_5447", "id": "1001"},
    {"name": "GSAD_2222", "id": "1002"},
    {"name": "GSAD_5533", "id": "1003"},
    {"name": "GSAD_4334", "id": "1004"},
    {"name": "GSAD_4334-V2", "id": "1004"}  # name changed here but identifier the same, this can happen

]

myacmeservices_stores_dict = {
    "1001": {
        "devices": [
            {"serial_number": "F5MSCX001000", "device_key": "100", "customer_display_code": "my-device-1"},
            {"serial_number": "F5MSCX001001", "device_key": "101", "customer_display_code": "my-device-2"},
            {"serial_number": "F5MSCX001002", "device_key": "102", "customer_display_code": "my-device-3"}
        ],
        "customer_location_code": None,
        "tenant_code": "myacmeservices",
    },
    "2001": {
        "devices": [
            {"serial_number": "F5MSCX002000", "device_key": "200", "customer_display_code": "my-device-4"},
            {"serial_number": "F5MSCX002001", "device_key": "201", "customer_display_code": "my-device-5"},
            {"serial_number": "F5MSCX002003", "device_key": "202", "customer_display_code": None}
        ],
        "customer_location_code": "my-2004-location",
        "tenant_code": "myacmeservices",
    },
    "3001": {
        "devices": [
            {"serial_number": "F5MSCX003000", "device_key": "300", "customer_display_code": None},
            {"serial_number": "F5MSCX003001", "device_key": "301", "customer_display_code": "my-device-8"},
            {"serial_number": "F5MSCX003003", "device_key": "302", "customer_display_code": "my-device-9"}
        ],
        "customer_location_code": None,
        "tenant_code": "myacmeservices",
    }
}


def create_data_to_send(started_at, ended_at):
    myacmeservices_store = random.choice(myacmeservices_stores_dict.keys())
    resource_choice = random.choice(resource_choices)
    device_choice = random.choice(myacmeservices_stores_dict[myacmeservices_store]["devices"])
    customer_location_code = myacmeservices_stores_dict[myacmeservices_store]["customer_location_code"]

    to_return = {
        'resource_name': resource_choice["name"],  # string
        'resource_id': resource_choice["id"],  # string
        'device_key': device_choice["device_key"],  # string
        'serial_number': device_choice["serial_number"],  # string
        'customer_location_code': customer_location_code,  # string
        'customer_display_code': device_choice["customer_display_code"],  # string
        'started_at': started_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'ended_at': ended_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'tenant_code': myacmeservices_stores_dict[myacmeservices_store]["tenant_code"]  # string
    }

    return to_return


def make_one_days_worth_of_data(amount_a_day, started_at):
    to_return = {
        "data": []
    }

    for item in xrange(1, amount_a_day):
        ended_at = started_at + datetime.timedelta(minutes=10)
        to_return["data"].append(create_data_to_send(started_at, ended_at))
        started_at += datetime.timedelta(minutes=10)

    return to_return


def queue_up_mock_data(day_amount, amount_a_day):
    print "Generating..."
    for each in reversed(xrange(1, day_amount)):
        started_at = datetime.datetime.now() - datetime.timedelta(days=each)

        # to not post some days
        if random.randint(1, 7) == 5:
            pass
        else:
            generate_mock_data(make_one_days_worth_of_data(amount_a_day, started_at))


def generate_mock_data(to_send):
    first_part = "http://skykit-display-device-int.appspot.com"
    # first_part = "http://localhost:8080"
    url = first_part + "/proofplay/api/v1/post_new_program_play"
    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain',
        "Authorization": config.API_TOKEN
    }
    print headers
    requests.post(url, data=json.dumps(to_send), headers=headers)


queue_up_mock_data(500, 10)
