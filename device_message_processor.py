import logging

from app_config import config
from google_cloud_messaging import GoogleCloudMessaging
from models import PlayerCommandEvent
from utils.web_util import build_uri


__author__ = 'Christopher Bartling <chris.bartling@agosto.com>, Bob MacNeal <bob.macneal@agosto.com>'


def change_intent(gcm_registration_id, payload, device_urlsafe_key, host, user_identifier):
    test_mode = config.GCM_TEST_MODE
    player_command_event = PlayerCommandEvent.create(
            device_urlsafe_key=device_urlsafe_key,
            payload=payload,
            gcm_registration_id=gcm_registration_id,
            user_identifier=user_identifier)
    event_key = player_command_event.put()
    confirmation_uri = "{0}{1}".format(host, build_uri('manage-event',
                                                       params_dict={'urlsafe_event_key': event_key.urlsafe()}))
    data_dictionary = {"intent": payload,
                       "confirmation": confirmation_uri}
    registration_ids = [gcm_registration_id]
    google_cloud_messaging = GoogleCloudMessaging()
    try:
        google_cloud_messaging.notify(registration_ids, data_dictionary, test_mode=test_mode)
        logging.info('change_intent {0} posted to GCM with gcm_registration_id = {1} and test_mode = {2}.'.format(
            str(data_dictionary),
            gcm_registration_id,
            test_mode))
    except Exception, e:
        logging.exception(e)


def post_unmanaged_device_info(gcm_registration_id, device_urlsafe_key, host):
    payload = "skykit.com/skdchromeapp/unmanaged/{0}/{1}".format(device_urlsafe_key, config.UNMANAGED_API_TOKEN)
    change_intent(gcm_registration_id=gcm_registration_id, payload=payload, device_urlsafe_key=device_urlsafe_key,
                  host=host)
