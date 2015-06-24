from agar.test import BaseTest
from mock import patch

from device_commands_processor import (change_intent)

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestDeviceCommandsProcessor(BaseTest):
    def setUp(self):
        super(TestDeviceCommandsProcessor, self).setUp()

    @staticmethod
    def test_change_intent_invokes_google_cloud_messaging_notify_method():
        payload = {'https://www.content-manager/something'}
        gcm_registration_id = 'd23784972038845ab3963412'
        registration_ids = [gcm_registration_id]
        data_dictionary = {'intent': payload}
        with patch('google_cloud_messaging.GoogleCloudMessaging.notify') as mock_notify:
            change_intent(gcm_registration_id, payload)
        mock_notify.assert_called_once_with(registration_ids, data_dictionary, test_mode=False)
