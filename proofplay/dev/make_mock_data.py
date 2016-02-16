import requests
import json
import datetime
import random

resource_choices = [
    {"name": "GSAD_5553", "id": "1000"},
    {"name": "GSAD_5447", "id": "1001"},
    {"name": "GSAD_2222", "id": "1002"},
    {"name": "GSAD_5533", "id": "1003"},
    {"name": "GSAD_4334", "id": "1004"}
]

first_random_numb = random.randint(0, 3)
gamestop_stores_dict = {
    "6034": {
        "devices": [
            {"serial_number": "F5MSCX001000", "device_key": "838383", "customer_display_code": "my-device-1"},
            {"serial_number": "F5MSCX001001", "device_key": "4848484", "customer_display_code": "my-device-2"},
            {"serial_number": "F5MSCX001002", "device_key": "3838383", "customer_display_code": "my-device-3"}
        ],
        "customer_location_code": "my-6034-location",
        "tenant_code": "gamestop",
        "resources": resource_choices
    }
}


def create_data_to_send(started_at, ended_at):
    gamestop_store = random.choice(gamestop_stores_dict.keys())
    resource_choice = random.choice(gamestop_stores_dict[gamestop_store]["resources"])
    device_choice = random.choice(gamestop_stores_dict[gamestop_store]["devices"])
    return {
        'resource_name': resource_choice["name"],
        'resource_id': resource_choice["id"],
        'device_key': device_choice["device_key"],
        'serial_number': device_choice["serial_number"],
        'customer_location_code': gamestop_store,
        'customer_display_code': gamestop_stores_dict[gamestop_store]["customer_location_code"],
        'started_at': started_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'ended_at': ended_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'tenant_code': gamestop_stores_dict[gamestop_store]["tenant_code"]
    }


def generate_mock_data(to_send):
    url = "http://localhost:8080/proofplay/api/v1/0ac1b95dc3f93d9132b796986ed11cd4/post_new_program_play"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(to_send), headers=headers)
    print to_send["data"][-1]["ended_at"]


def make_one_days_worth_of_data(amount_a_day, started_at):
    to_return = {}
    to_return["data"] = []

    for item in xrange(1, amount_a_day):
        ended_at = started_at + datetime.timedelta(minutes=10)
        to_return["data"].append(create_data_to_send(started_at, ended_at))
        started_at += datetime.timedelta(minutes=10)

    return to_return


def queue_up_mock_data(day_amount, amount_a_day):
    for each in reversed(xrange(1, day_amount)):
        started_at = datetime.datetime.now() - datetime.timedelta(days=each)
        generate_mock_data(make_one_days_worth_of_data(amount_a_day, started_at))


def run():
    queue_up_mock_data(500, 10)


def just_one():
    queue_up_mock_data(1, 10)
