import json
import logging

import requests

from app_config import config

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class GoogleCloudMessaging(object):
    """ Facade around Google's Cloud Messaging for Android. """

    URL_CLOUD_MESSAGING_SEND = 'https://android.googleapis.com/gcm/send'
    HEADERS = {
        'Content-Type': 'application/json'
    }

    def __init__(self):
        self.HEADERS['Authorization'] = 'key={0}'.format(config.PUBLIC_API_SERVER_KEY)

    def notify(self, registration_ids, data_dictionary, test_mode=False):
        cloud_message_payload_dictionary = {
            "data": data_dictionary,
            "registration_ids": registration_ids
        }
        if test_mode:
            cloud_message_payload_dictionary['dry_run'] = True
        json_payload = json.dumps(cloud_message_payload_dictionary)
        logging.info('>>> GCM JSON payload: {0}'.format(json_payload))
        response = requests.post(self.URL_CLOUD_MESSAGING_SEND, json_payload, timeout=60, headers=self.HEADERS)
        if response and response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError('Unable to notify devices via GCM.  HTTP status code: {0}'.format(response.status_code))
