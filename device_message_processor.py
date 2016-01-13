import logging

from app_config import config
from google_cloud_messaging import GoogleCloudMessaging
from models import PlayerCommandEvent
from utils.web_util import build_uri


__author__ = 'Christopher Bartling <chris.bartling@agosto.com>, Bob MacNeal <bob.macneal@agosto.com>'


def change_intent(gcm_registration_id, payload):
    test_mode = config.GCM_TEST_MODE
    player_command_event = PlayerCommandEvent.create(
            payload=payload,
            gcm_registration_id=gcm_registration_id)
    player_command_event_key = player_command_event.put()
    confirmation_uri = build_uri(route_name='command-confirmation', params_dict={'player_command_event_key':
                                                                               player_command_event_key.urlsafe()})
    registration_ids = [gcm_registration_id]
    data_dictionary = {"intent": payload,
                       "confirmation": confirmation_uri}
    google_cloud_messaging = GoogleCloudMessaging()
    try:
        google_cloud_messaging.notify(registration_ids, data_dictionary, test_mode=test_mode)
        logging.info('change_intent {0} posted to GCM with gcm_registration_id = {1} and test_mode = {2}.'.format(
            str(data_dictionary),
            gcm_registration_id,
            test_mode))
    except Exception, e:
        logging.exception(e)


def post_unmanaged_device_info(gcm_registration_id, device_urlsafe_key):
    payload = "skykit.com/skdchromeapp/unmanaged/{0}/{1}".format(device_urlsafe_key, config.UNMANAGED_API_TOKEN)
    change_intent(gcm_registration_id=gcm_registration_id, payload=payload)
