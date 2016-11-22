from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest, WebTest
from models import PlayerCommandEvent
from routes import application
from utils.web_util import build_uri
from app_config import config
import json
from provisioning_distributor_user_base_test import ProvisioningDistributorUserBase


class TestCommandEventsHandler(ProvisioningDistributorUserBase):
    APPLICATION = application
    INTENT = 'skykit.com/skdchromeapp/reset'
    GCM_REGISTRATION_ID = 'APA91bH0sONxgUSSUtERv-SGZHYvThi3jRv_p4ASYdTTLjgLntaZhyL9ti8aE-SWZm8ju1z0stjziWLvVdRt0'
    DEVICE_URLSAFE_KEY = 'kljlkjlkjlkjlkjlkjljlkj'

    def setUp(self):
        super(TestCommandEventsHandler, self).setUp()
        self.event = PlayerCommandEvent.create(device_urlsafe_key=self.DEVICE_URLSAFE_KEY,
                                               payload=self.INTENT,
                                               gcm_registration_id=self.GCM_REGISTRATION_ID)
        self.headers = {
            'Authorization': config.API_TOKEN
        }
        self.bad_authorization_header = {
            'Authorization': 'Forget about it!'
        }

    def test_get_device_command_events_returns_expected_events_list(self):
        request_parameters = {}
        number_of_device_events = 27
        self.__build_command_events(device_urlsafe_key='some-other-key', number_of_events=2)
        self.__build_command_events(device_urlsafe_key=self.DEVICE_URLSAFE_KEY,
                                    number_of_events=number_of_device_events)

        uri = build_uri('player-command-events', params_dict={
            'device_urlsafe_key': self.DEVICE_URLSAFE_KEY,
            'prev_cursor_str': 'null',
            'next_cursor_str': 'null'
        })
        response = self.app.get(uri, params=request_parameters, headers=self.JWT_DEFUALT_HEADER)
        response_json = json.loads(response.body)

        self.assertLength(25, response_json["events"])
        self.assertEqual(response_json["events"][0]['payload'], 'payload-26')
        self.assertEqual(response_json["events"][1]['payload'], 'payload-25')
        self.assertEqual(response_json["events"][2]['payload'], 'payload-24')
        self.assertTrue(response_json["next_cursor"])
        self.assertFalse(response_json["prev_cursor"])

    def __build_command_events(self, device_urlsafe_key, number_of_events):
        for i in range(number_of_events):
            payload = 'payload-{0}'.format(i)
            event = PlayerCommandEvent.create(
                device_urlsafe_key=device_urlsafe_key,
                payload=payload,
                gcm_registration_id=self.GCM_REGISTRATION_ID)
            event.put()
