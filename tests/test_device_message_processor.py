from app_config import config
from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
from google_cloud_messaging import GoogleCloudMessaging
from device_message_processor import (change_intent, post_unmanaged_device_info)
from mockito import when

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestDeviceMessageProcessor(BaseTest):
    TEST_GCM_REGISTRATION_ID = '8d70a8d78a6dfa6df76dfasd'
    DEVICE_KEY = '00d70a8d78a6dfa6df76d112'

    def setUp(self):
        super(TestDeviceMessageProcessor, self).setUp()

    def test_change_intent_invokes_google_cloud_messaging_notify_method(self):
        gcm_registration_id = self.TEST_GCM_REGISTRATION_ID
        registration_ids = [gcm_registration_id]
        payload = 'skykit.com/skdchromeapp/reset'
        data_dictionary = {'intent': payload}
        when(GoogleCloudMessaging).notify(registration_ids, data_dictionary, test_mode=False).thenReturn(None)
        change_intent(
                gcm_registration_id=gcm_registration_id,
                payload=payload,
                device_urlsafe_key='asdlkfjadksfj',
                host='http://localhost:3000',
                user_identifier='bob.macneal@agosto.com')

    def test_send_unmanaged_device_info_invokes_google_cloud_messaging_notify_method(self):
        gcm_registration_id = self.TEST_GCM_REGISTRATION_ID
        registration_ids = [gcm_registration_id]
        device_urlsafe_key = 'ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyGwsSDkNocm9tZU9zRGV2aWNlGICAgIDrop4KDA'
        data_dictionary = dict(deviceKey=device_urlsafe_key, apiToken=config.UNMANAGED_API_TOKEN)
        when(GoogleCloudMessaging).notify(registration_ids, data_dictionary, test_mode=False).thenReturn(None)
        post_unmanaged_device_info(gcm_registration_id, device_urlsafe_key, 'http://localhost:3000/')
