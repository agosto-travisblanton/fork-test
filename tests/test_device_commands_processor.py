from env_setup import setup_test_paths
setup_test_paths()

from agar.test import BaseTest
from google_cloud_messaging import GoogleCloudMessaging

from device_commands_processor import (change_intent)
from mockito import when

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestDeviceCommandsProcessor(BaseTest):
    def setUp(self):
        super(TestDeviceCommandsProcessor, self).setUp()

    def test_change_intent_invokes_google_cloud_messaging_notify_method(self):
        gcm_registration_id = 'd23784972038845ab3963412'
        registration_ids = [gcm_registration_id]
        payload = {'https://www.content-manager/something'}
        data_dictionary = {'intent': payload}
        when(GoogleCloudMessaging).notify(registration_ids, data_dictionary, test_mode=False).thenReturn(None)
        change_intent(gcm_registration_id, payload)
