from env_setup import setup_test_paths;

setup_test_paths()

from agar.test import BaseTest
from google_cloud_messaging import GoogleCloudMessaging
from app_config import config


__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TestGoogleCloudMessaging(BaseTest):
    def setUp(self):
        super(TestGoogleCloudMessaging, self).setUp()
        self.google_cloud_messaging = GoogleCloudMessaging()

    def test_construction(self):
        expected_authorization_header = 'key={0}'.format(config.PUBLIC_API_SERVER_KEY)
        self.assertEqual(expected_authorization_header,
                         self.google_cloud_messaging.HEADERS['Authorization'])

    # def testNotifySucceeds(self):
    # registration_ids = ['1', '2']
    #     data_dictionary = {'foo': 'bar', 'fuu': 'Barfly'}
    #     result = self.google_cloud_messaging.notify(registration_ids=registration_ids,
    #                                                 data_dictionary=data_dictionary,
    #                                                 test_mode=True)
    #     self.assertIsNotNone(result)

    def test_notify_fails_when_registration_ids_list_is_none(self):
        registration_ids = None
        data_dictionary = {'foo': 'bar', 'fuu': 'Barfly'}
        with self.assertRaises(RuntimeError):
            self.google_cloud_messaging.notify(registration_ids=registration_ids,
                                               data_dictionary=data_dictionary,
                                               test_mode=True)

            # def testNotifySucceeds_WhenDataDictionaryIsNone(self):
            #     registration_ids = ['1', '2']
            #     data_dictionary = None
            #     result = self.google_cloud_messaging.notify(registration_ids=registration_ids,
            #                                                 data_dictionary=data_dictionary,
            #                                                 test_mode=True)
            #     self.assertIsNotNone(result)


