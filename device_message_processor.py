import logging

from app_config import config
from google_cloud_messaging import GoogleCloudMessaging

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>, Bob MacNeal <bob.macneal@agosto.com>'


def change_intent(gcm_registration_id, payload):
    registration_ids = [gcm_registration_id]
    data_dictionary = {"intent": payload}
    google_cloud_messaging = GoogleCloudMessaging()
    test_mode = config.GCM_TEST_MODE
    try:
        google_cloud_messaging.notify(registration_ids, data_dictionary, test_mode=test_mode)
        logging.info('change_intent {0} posted to GCM with gcm_registration_id = {1} and test_mode = {2}.'.format(
            str(data_dictionary),
            gcm_registration_id,
            test_mode))
    except Exception, e:
        logging.exception(e)


def send_unmanaged_device_info(gcm_registration_id, device_urlsafe_key):
    registration_ids = [gcm_registration_id]
    data_dictionary = dict(deviceKey=device_urlsafe_key, apiToken=config.UNMANAGED_API_TOKEN)
    google_cloud_messaging = GoogleCloudMessaging()
    test_mode = config.GCM_TEST_MODE
    try:
        google_cloud_messaging.notify(registration_ids, data_dictionary, test_mode=test_mode)
        logging.info(
            'send_unmanaged_device_info posted {0} to GCM with gcm_registration_id = {1} and test_mode = {2}.'.format(
                str(data_dictionary),
                gcm_registration_id,
                test_mode))
    except Exception, e:
        logging.exception(e)