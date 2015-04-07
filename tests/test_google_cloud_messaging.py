from agar.test import BaseTest
from google_cloud_messaging import GoogleCloudMessaging
from app_config import config
import pprint

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TestGoogleCloudMessaging(BaseTest):
    def setUp(self):
        super(TestGoogleCloudMessaging, self).setUp()
        self.google_cloud_messaging = GoogleCloudMessaging()

    def testConstruction(self):
        expected_authorization_header = 'key={0}'.format(config.PUBLIC_API_SERVER_KEY)
        self.assertEqual(expected_authorization_header,
                         self.google_cloud_messaging.HEADERS['Authorization'])

    def testNotifySuccessful(self):
        registration_ids = ['1', '2']
        data_dictionary = {'foo': 'bar', 'fuu': 'Barfly'}
        result = self.google_cloud_messaging.notify(registration_ids=registration_ids,
                                                    data_dictionary=data_dictionary,
                                                    test_mode=True)
        self.assertIsNotNone(result)
        pprint.pprint(result, indent=3, width=80)