from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
from google_cloud_messaging import GoogleCloudMessaging
from app_config import config

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'

# TODO: Mock the interaction to GCM.
class TestGoogleCloudMessaging(BaseTest):

    def setUp(self):
        super(TestGoogleCloudMessaging, self).setUp()

    def test_construction(self):
        self.google_cloud_messaging = GoogleCloudMessaging()
        expected_authorization_header = 'key={0}'.format(config.PUBLIC_API_SERVER_KEY)
        self.assertEqual(expected_authorization_header,
                         self.google_cloud_messaging.HEADERS['Authorization'])

    # def test_notify_fails_when_registration_ids_list_is_none(self):
    #     self.google_cloud_messaging = GoogleCloudMessaging()
    #     registration_ids = None
    #     data_dictionary = {'foo': 'bar', 'fuu': 'Barfly'}
    #     with self.assertRaises(RuntimeError) as context:
    #         self.google_cloud_messaging.notify(registration_ids=registration_ids,
    #                                            data_dictionary=data_dictionary,
    #                                            test_mode=True)
    #     self.assertTrue('Unable to notify devices via GCM.  HTTP status code: 400'
    #                     in str(context.exception))

    def test_notify_successful(self):
        self.google_cloud_messaging = GoogleCloudMessaging()
        registration_ids = ["238947298370189475"]
        data_dictionary = {'foo': 'bar', 'fuu': 'Barfly'}
        result = self.google_cloud_messaging.notify(registration_ids=registration_ids,
                                               data_dictionary=data_dictionary,
                                               test_mode=True)
        self.assertIsNone(result)