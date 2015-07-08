import json
import logging

from google.appengine.api import urlfetch

from app_config import config

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class GoogleCloudMessaging(object):
    """ Facade around Google's Cloud Messaging for Android. """

    URL_CLOUD_MESSAGING_SEND = 'https://android.googleapis.com/gcm/send'
    HEADERS = {
        'Content-Type': 'application/json'
    }

    def __init__(self):
        # self.HEADERS['Authorization'] = 'key={0}'.format(config.PUBLIC_API_SERVER_KEY)
        self.HEADERS['Authorization'] = 'key={0}'.format('AIzaSyCXKJrn9dVpePXGsfVdyfHxxaaesRuLm0w')

    def notify(self, registration_ids, data_dictionary, test_mode=False):
        cloud_message_payload_dictionary = {
            "data": data_dictionary,
            "registration_ids": registration_ids
        }
        if test_mode:
            cloud_message_payload_dictionary['dry_run'] = True
        json_payload = json.dumps(cloud_message_payload_dictionary)
        response = None
        try:
            response = urlfetch.fetch(url=self.URL_CLOUD_MESSAGING_SEND,
                                      payload=json_payload,
                                      method=urlfetch.POST,
                                      headers=self.HEADERS,
                                      validate_certificate=False)
        except Exception, e:
            logging.exception(e)

        if response.status_code != 200:
            error_message = 'Unable to notify devices via GCM.  HTTP status code: {0}'.format(response.status_code)
            logging.error(error_message)
            raise RuntimeError(error_message)
