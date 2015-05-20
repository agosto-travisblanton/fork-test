from google_cloud_messaging import GoogleCloudMessaging

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


def register_device():
    pass


def reset_device():
    pass


def update_device():
    pass


def check_schedule():
    pass


def change_channel(gcm_registration_id, payload):
    registration_ids = [gcm_registration_id]
    data_dictionary = {'command': 'change_channel', 'payload': payload}
    google_cloud_messaging = GoogleCloudMessaging()
    google_cloud_messaging.notify(registration_ids, data_dictionary, test_mode=False)

