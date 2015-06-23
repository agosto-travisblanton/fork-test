from google_cloud_messaging import GoogleCloudMessaging

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>, Bob MacNeal <bob.macneal@agosto.com>'


def change_intent(gcm_registration_id, payload):
    registration_ids = [gcm_registration_id]
    data_dictionary = {'intent': payload}
    google_cloud_messaging = GoogleCloudMessaging()
    google_cloud_messaging.notify(registration_ids, data_dictionary, test_mode=False)
