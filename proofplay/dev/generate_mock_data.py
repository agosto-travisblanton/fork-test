import requests
import json
import datetime
import random
import uuid

information_to_post = {
    "myacmeservices": {
        "resource_choices": [
            {"name": "ACME_5553", "id": uuid.uuid1().hex},
            {"name": "ACME_5447", "id": uuid.uuid1().hex},
            {"name": "ACME_2222", "id": uuid.uuid1().hex},
            {"name": "ACME_5533", "id": uuid.uuid1().hex},
            {"name": "ACME_4334", "id": "1234"},
            {"name": "ACME_4334-V2", "id": "1234"}  # to show that name can change
        ],
        "locations": {
            "acme-one-location": {
                "acme-one-device": {
                    "serial_number": uuid.uuid1().hex,
                    "device_key": uuid.uuid1().hex,
                    "new_customer_location_code": "acme-super-one-location",
                    "new_customer_display_code": "acme-super-one-device"
                }
            }
        }

    },
    "dilbertdistribution": {
        "locations": {
            "dilbert-one-location": {

            }
        }

    },
    "johnsonsjaguars": {
        "locations": {
            "johnson-one-location": {

            }
        }

    }
}


# TODO
# REQUIREMENTS:
# MULTIPLE TENANTS #
# CHANGING customer_location_codes
# CHANGING customer_display_codes
# CHANGING resource_names
# NONE customer_display_codes
# NONE customer_location_codes


def send_mock_data(to_send, integration=False):
    if integration:
        first_part = "http://skykit-display-device-int.appspot.com"
    else:
        first_part = "http://localhost:8080"
    url = first_part + "/proofplay/api/v1/0ac1b95dc3f93d9132b796986ed11cd4/post_new_program_play"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(to_send), headers=headers)


def create_one_log(started_at, ended_at, tenant):
    should_make_device_none = random.randint(1, 30)
    should_make_location_none = random.randint(1, 30)

    to_return = {
        'resource_name': '',  #
        'resource_id': '',  #
        'device_key': '',  #
        'serial_number': '',  #
        'customer_location_code': '',  #
        'customer_display_code': '',  #
        'started_at': started_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'ended_at': ended_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'tenant_code': tenant
    }

    return to_return


def batch_up_logs_for_tenant(amount_a_day, started_at, tenant):
    to_return = {
        "data": []
    }

    for item in xrange(1, amount_a_day):
        ended_at = started_at + datetime.timedelta(minutes=10)
        one_log = create_one_log(started_at, ended_at, tenant)
        to_return["data"].append(one_log)
        started_at += datetime.timedelta(minutes=10)

    return to_return


def generate_mock_data(days_of_logs, amount_a_day):
    print "Generating..."

    for key, value in information_to_post.iteritems():
        for each in reversed(xrange(1, days_of_logs)):
            started_at = datetime.datetime.now() - datetime.timedelta(days=each)

            # to not post some 1/10 days
            if not random.randint(1, 10) == 5:
                batched_up_logs = batch_up_logs_for_tenant(amount_a_day, started_at, key)
                send_mock_data(batched_up_logs)
