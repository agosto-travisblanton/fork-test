import requests
import json
import datetime
import random


def create_data_to_send(to_go_back):
    to_send = {
        "data": []
    }

    for number in xrange(1, 5):
        serial_number_choices = ["F5MSCX001896", "F5MSCX001736", "F5MSCX001889"]
        location_ids = ["6034", "6023", "6022"]
        tenant_code = ["gamestop", "gamestop", "gamestop"]
        serial_number_key_choices = ["2342344", "434234", "455566"]
        device_codes = ["my-device-1", "my-device-2", "my-device-3"]
        resource_choices = ["GSAD_5553", "GSAD_5447", "GSAD_2222"]
        resource_ids = ["234234", "55555", "342433"]

        started_at = datetime.datetime.now() - datetime.timedelta(days=to_go_back) - datetime.timedelta(
                hours=number)

        ended_at = started_at + datetime.timedelta(minutes=10)

        random_num = random.randint(0, 2)
        data = {
            'resource_name': resource_choices[random_num],
            'resource_id': resource_ids[random_num],
            'device_key': serial_number_key_choices[random.randint(0, 2)],
            'serial_number': serial_number_choices[random.randint(0, 2)],
            'customer_location_code': location_ids[random_num],
            'customer_display_code': device_codes[random_num],
            'started_at': started_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'ended_at': ended_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'tenant_code': tenant_code[random_num]
        }

        to_send["data"].append(data)

    return to_send


def generate_mock_data(to_go_back):
    url = "http://localhost:8080/proofplay/api/v1/0ac1b95dc3f93d9132b796986ed11cd4/post_new_program_play"
    to_send = create_data_to_send(to_go_back)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(to_send), headers=headers)
    print to_go_back


def run():
    for each in reversed(xrange(1, 501)):
        generate_mock_data(each)


def just_one():
    generate_mock_data(1000)
    return True


def get_one_to_send():
    return create_data_to_send(700)
