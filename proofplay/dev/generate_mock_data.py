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
            {"name": "ACME_5553", "id": "086b8e3df6a211e5b4256003088f14f4"},
            {"name": "ACME_5447", "id": "11ff1887f6a211e585a16003088f14f4"},
            {"name": "ACME_2222", "id": "1fcad2a3f6a211e589336003088f14f4"},
            {"name": "ACME_5533", "id": "2434f099f6a211e580826003088f14f4"},
            {"name": "ACME_4334", "id": "1234"},
            {"name": "ACME_4334-V2", "id": "1234"}  # to show that name can change
        ],
        "locations": {
            "acme-one-location": {
                "acme-one-device": {
                    "serial_number": "2bbb8f2bf6a211e5b3576003088f14f4",
                    "device_key": "300386b5f6a211e5b1d56003088f14f4",
                    "new_customer_location_code": "acme-new-one-location",
                    "new_customer_display_code": "acme-new-one-device"
                },
                "acme-two-device": {
                    "serial_number": "33b560d7f6a211e5b2d16003088f14f4",
                    "device_key": "38afad94f6a211e5990f6003088f14f4",
                    "new_customer_location_code": "acme-new-one-location",
                    "new_customer_display_code": "acme-new-two-device"
                }
            },
            "shared-two-location": {
                "acme-three-device": {
                    "serial_number": "3d38f5c7f6a211e5b1876003088f14f4",
                    "device_key": "40a31a73f6a211e59eac6003088f14f4",
                    "new_customer_location_code": "shared-new-two-location",
                    "new_customer_display_code": "acme-new-three-device"
                },
                "acme-four-device": {
                    "serial_number": "45039f2ef6a211e5ad3a6003088f14f4",
                    "device_key": "48757b00f6a211e594a36003088f14f4",
                    "new_customer_location_code": "shared-new-two-location",
                    "new_customer_display_code": "acme-new-four-device"
                },
                "acme-five-device": {
                    "serial_number": "4d2f247af6a211e5a2606003088f14f4",
                    "device_key": "526848e8f6a211e5955a6003088f14f4",
                    "new_customer_location_code": "shared-new-two-location",
                    "new_customer_display_code": "acme-new-five-device"
                }
            }
        }

    },
    "davedistribution": {
        "resource_choices": [
            {"name": "DILB_5553", "id": "5ae556f3f6a211e5b21a6003088f14f4"},
            {"name": "DILB_5447", "id": "5fccaba1f6a211e5bd5d6003088f14f4"},
            {"name": "DILB_2222", "id": "63ae65e3f6a211e5b31e6003088f14f4"},
            {"name": "DILB_5533", "id": "68ce6c0cf6a211e5bb756003088f14f4"},
            {"name": "DILB_4334", "id": "3333"},
            {"name": "DILB_4334-V2", "id": "3333"}  # to show that name can change
        ],
        "locations": {
            "dave-one-location": {
                "dave-one-device": {
                    "serial_number": "6c24b233f6a211e58ce96003088f14f4",
                    "device_key": "70e3af1cf6a211e5b0f06003088f14f4",
                    "new_customer_location_code": "dave-new-one-location",
                    "new_customer_display_code": "dave-new-one-device"
                },
                "dave-two-device": {
                    "serial_number": "7402af8ff6a211e5b43e6003088f14f4",
                    "device_key": "782de0a8f6a211e5b0596003088f14f4",
                    "new_customer_location_code": "dave-new-one-location",
                    "new_customer_display_code": "dave-new-two-device"
                }
            },
            "shared-two-location": {
                "dave-three-device": {
                    "serial_number": "7b5a2582f6a211e58ad46003088f14f4",
                    "device_key": "7eeae48ff6a211e5867b6003088f14f4",
                    "new_customer_location_code": "shared-new-two-location",
                    "new_customer_display_code": "dave-new-three-device"
                },
                "dave-four-device": {
                    "serial_number": "829b4f6bf6a211e5a24d6003088f14f4",
                    "device_key": "8918ba94f6a211e58ac26003088f14f4",
                    "new_customer_location_code": "shared-new-two-location",
                    "new_customer_display_code": "dave-new-four-device"
                },
                "dave-five-device": {
                    "serial_number": "8d0296a3f6a211e587076003088f14f4",
                    "device_key": "906748a8f6a211e5a6426003088f14f4",
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

    for item in xrange(1, amount_a_day + 1):
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


def batch_up_one_day_without_changing_data(
        amount_a_day,
        started_at,
        tenant,
):
    to_return = {
        "data": []
    }

    should_use_no_location_code = False
    should_use_no_display_code = False
    should_use_new_location_code = False
    should_use_new_display_code = False

    for item in xrange(1, amount_a_day + 1):
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
        for each in reversed(xrange(1, days_of_logs + 1)):
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
