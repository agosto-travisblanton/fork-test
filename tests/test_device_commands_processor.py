from agar.test import BaseTest, WebTest
from mock import patch
from models import ChromeOsDevice
from google_cloud_messaging import GoogleCloudMessaging

from device_commands_processor import (change_channel)

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestDeviceCommandsProcessor(BaseTest, WebTest):
    def setUp(self):
        super(TestDeviceCommandsProcessor, self).setUp()
        self.device_id = '132e235a-b346-4a37-a100-de49fa753a2a'
        self.chrome_os_device = ChromeOsDevice(device_id=self.device_id,
                                               gcm_registration_id='d23784972038845ab3963412')
        self.chrome_os_device.put()

    def test_change_channel_invokes_google_cloud_messaging_notify_method(self):
        payload = {'channel': {'name': 'Quality On Demand', 'program': 'Program 1'}}
        gcm_registration_id = self.chrome_os_device.gcm_registration_id
        registration_ids = [gcm_registration_id]
        data_dictionary = {'command': 'change_channel', 'payload': payload}
        mock_gcm = GoogleCloudMessaging()
        mock_gcm.notify = MagicMock(name='notify')

#         >>> real = SomeClass()
# >>> real.method = MagicMock(name='method')
# >>> real.method(3, 4, 5, key='value')
# <MagicMock name='method()' id='...'>

        with patch('GoogleCloudMessaging.notify', return_value=None) as mock_notify:
            change_channel(gcm_registration_id, payload)
        mock_notify.assert_called_once_with(registration_ids, data_dictionary, test_mode=False)

        # def change_channel(gcm_registration_id, payload):
        # registration_ids = [gcm_registration_id]
        # data_dictionary = {'command': 'change_channel', 'payload': payload}
        # google_cloud_messaging = GoogleCloudMessaging()
        #     google_cloud_messaging.notify(registration_ids, data_dictionary, test_mode=False)

