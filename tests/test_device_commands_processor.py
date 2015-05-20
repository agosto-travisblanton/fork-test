from agar.test import BaseTest
from mock import patch

from device_commands_processor import (change_channel)

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestDeviceCommandsProcessor(BaseTest):
    def setUp(self):
        super(TestDeviceCommandsProcessor, self).setUp()

    @staticmethod
    def test_change_channel_invokes_google_cloud_messaging_notify_method():
        payload = {'channel': {'name': 'Quality On Demand', 'program': 'Program 1'}}
        gcm_registration_id = 'd23784972038845ab3963412'
        registration_ids = [gcm_registration_id]
        data_dictionary = {'command': 'change_channel', 'payload': payload}
        with patch('google_cloud_messaging.GoogleCloudMessaging.notify') as mock_notify:
            change_channel(gcm_registration_id, payload)
        mock_notify.assert_called_once_with(registration_ids, data_dictionary, test_mode=False)

