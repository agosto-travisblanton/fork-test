from google_cloud_messaging import GoogleCloudMessaging
from app_config import config


__author__ = 'Christopher Bartling <chris.bartling@agosto.com>, Bob MacNeal <bob.macneal@agosto.com>'


def change_intent(gcm_registration_id, payload):
    registration_ids = [gcm_registration_id]
    data_dictionary = {"intent": payload}
    google_cloud_messaging = GoogleCloudMessaging()
    test_mode = config.GCM_TEST_MODE
    google_cloud_messaging.notify(registration_ids, data_dictionary, test_mode=test_mode)
