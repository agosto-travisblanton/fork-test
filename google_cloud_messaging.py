
import json
import logging

from app_config import config


__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class GoogleCloudMessaging(object):
    """ Facade around Google's Cloud Messaging for Android. """

    URL_CLOUD_MESSAGING_SEND = 'https://android.googleapis.com/gcm/send'
    HEADERS = {
        'Content-Type': 'application/json'
    }

    def __init__(self):
        pass
        self.HEADERS['Authorization'] = 'key={0}'.format(config.PUBLIC_API_SERVER_KEY)

    def sendMessage(self, registration_ids, message):
        cloud_message_payload_dictionary = {
            "data": {
                "message": message
            },
            "registration_ids": registration_ids
        }
        json_payload = json.dumps(cloud_message_payload_dictionary)
        logging.info('>>> Google Cloud Messaging::JSON payload: {0}'.format(json_payload))
        urlfetch.set_default_fetch_deadline(60)
        return urlfetch.fetch(url=self.URL_CLOUD_MESSAGING_SEND,
                              payload=json_payload,
                              method=urlfetch.POST,
                              headers=self.HEADERS)