import requests
import json
import datetime
import random
import uuid
from app_config import config

analytics = {}

information_to_post = {
    "acme_inc": {
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
                    "new_customer_location_code": "acme-new-one-location",
                    "new_customer_display_code": "acme-new-one-device"
                },
                "acme-two-device": {
                    "serial_number": uuid.uuid1().hex,
                    "device_key": uuid.uuid1().hex,
                    "new_customer_location_code": "acme-new-one-location",
                    "new_customer_display_code": "acme-new-two-device"
                }
            },
            "shared-two-location": {
                "acme-three-device": {
                    "serial_number": uuid.uuid1().hex,
                    "device_key": uuid.uuid1().hex,
                    "new_customer_location_code": "shared-new-two-location",
                    "new_customer_display_code": "acme-new-three-device"
                },
                "acme-four-device": {
                    "serial_number": uuid.uuid1().hex,
                    "device_key": uuid.uuid1().hex,
                    "new_customer_location_code": "shared-new-two-location",
                    "new_customer_display_code": "acme-new-four-device"
                },
                "acme-five-device": {
                    "serial_number": uuid.uuid1().hex,
                    "device_key": uuid.uuid1().hex,
                    "new_customer_location_code": "shared-new-two-location",
                    "new_customer_display_code": "acme-new-five-device"
                }
            }
        }

    },
    "davedistribution": {
        "resource_choices": [
            {"name": "DILB_5553", "id": uuid.uuid1().hex},
            {"name": "DILB_5447", "id": uuid.uuid1().hex},
            {"name": "DILB_2222", "id": uuid.uuid1().hex},
            {"name": "DILB_5533", "id": uuid.uuid1().hex},
            {"name": "DILB_4334", "id": "3333"},
            {"name": "DILB_4334-V2", "id": "3333"}  # to show that name can change
        ],
        "locations": {
            "dave-one-location": {
                "dave-one-device": {
                    "serial_number": uuid.uuid1().hex,
                    "device_key": uuid.uuid1().hex,
                    "new_customer_location_code": "dave-new-one-location",
                    "new_customer_display_code": "dave-new-one-device"
                },
                "dave-two-device": {
                    "serial_number": uuid.uuid1().hex,
                    "device_key": uuid.uuid1().hex,
                    "new_customer_location_code": "dave-new-one-location",
                    "new_customer_display_code": "dave-new-two-device"
                }
            },
            "shared-two-location": {
                "dave-three-device": {
                    "serial_number": uuid.uuid1().hex,
                    "device_key": uuid.uuid1().hex,
                    "new_customer_location_code": "shared-new-two-location",
                    "new_customer_display_code": "dave-new-three-device"
                },
                "dave-four-device": {
                    "serial_number": uuid.uuid1().hex,
                    "device_key": uuid.uuid1().hex,
                    "new_customer_location_code": "shared-new-two-location",
                    "new_customer_display_code": "dave-new-four-device"
                },
                "dave-five-device": {
                    "serial_number": uuid.uuid1().hex,
                    "device_key": uuid.uuid1().hex,
                    "new_customer_location_code": "shared-new-two-location",
                    "new_customer_display_code": "dave-new-five-device"
                }
            }
        }

    }
}


def create_one_log(
        started_at,
        ended_at,
        tenant,
        should_use_no_location_code,
        should_use_no_display_code,
        should_use_new_location_code,
        should_use_new_display_code
):
    # array resource dicts
    tenant_resources = information_to_post[tenant]["resource_choices"]

    # dict name and id of resource
    chosen_resource = random.choice(tenant_resources)

    # dict tenant locations
    tenant_locations = information_to_post[tenant]["locations"]

    # string of location
    chosen_location = random.choice(tenant_locations.keys())

    # string chosen device
    chosen_device = random.choice(information_to_post[tenant]["locations"][chosen_location].keys())

    # json chosen device
    full_chosen_device = information_to_post[tenant]["locations"][chosen_location][chosen_device]

    customer_display_code = chosen_device
    customer_location_code = chosen_location

    if should_use_no_location_code:
        customer_location_code = None

    if should_use_no_display_code:
        customer_display_code = None

    if should_use_new_location_code:
        customer_location_code = full_chosen_device["new_customer_location_code"]

    if should_use_new_display_code:
        customer_display_code = full_chosen_device["new_customer_display_code"]

    if tenant not in analytics:
        analytics[tenant] = {}
    if customer_location_code not in analytics[tenant]:
        analytics[tenant][customer_location_code] = {}
    if customer_display_code not in analytics[tenant][customer_location_code]:
        analytics[tenant][customer_location_code][customer_display_code] = {}

    if chosen_resource["name"] not in analytics[tenant][customer_location_code][customer_display_code]:
        analytics[tenant][customer_location_code][customer_display_code][chosen_resource["name"]] = 0

    analytics[tenant][customer_location_code][customer_display_code][chosen_resource["name"]] += 1

    return {
        'resource_name': chosen_resource["name"],  #
        'resource_id': chosen_resource["id"],  #
        'device_key': full_chosen_device["device_key"],  #
        'serial_number': full_chosen_device["serial_number"],  #
        'customer_location_code': customer_location_code,  #
        'customer_display_code': customer_display_code,  #
        'started_at': started_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'ended_at': ended_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'tenant_code': tenant
    }


def batch_up_logs_for_tenant(
        amount_a_day,
        started_at,
        tenant,
        total_number_of_days,
        number_of_days_before_today
):
    to_return = {
        "data": []
    }

    decimal_of_way_through = 1.0 - (number_of_days_before_today / float(total_number_of_days))

    should_use_no_location_code = False
    should_use_no_display_code = False
    should_use_new_location_code = False
    should_use_new_display_code = False

    if decimal_of_way_through <= 0.25:
        should_use_no_location_code = False
        should_use_no_display_code = True

    elif decimal_of_way_through >= 0.25 and decimal_of_way_through <= 0.75:
        should_use_no_location_code = False
        should_use_no_display_code = False

    else:
        should_use_new_location_code = True
        should_use_new_display_code = True

    for item in xrange(1, amount_a_day):
        ended_at = started_at + datetime.timedelta(minutes=10)
        one_log = create_one_log(
            started_at,
            ended_at,
            tenant,
            should_use_no_location_code=should_use_no_location_code,
            should_use_no_display_code=should_use_no_display_code,
            should_use_new_location_code=should_use_new_location_code,
            should_use_new_display_code=should_use_new_display_code
        )
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
                batched_up_logs = batch_up_logs_for_tenant(amount_a_day, started_at, key, days_of_logs, each)
                send_mock_data(batched_up_logs)

    print "THE FOLLOWING IS ANALYTICS ABOUT YOUR POSTED DATA"
    print analytics


def send_mock_data(to_send, integration=False):
    if integration:
        first_part = "http://skykit-display-device-int.appspot.com"
    else:
        first_part = "http://localhost:8080"

    url = first_part + "/proofplay/api/v1/post_new_program_play"

    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain',
        "Authorization": config.API_TOKEN
    }
    requests.post(url, data=json.dumps(to_send), headers=headers)
