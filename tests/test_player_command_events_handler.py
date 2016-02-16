from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest, WebTest
from models import PlayerCommandEvent
from routes import application
from utils.web_util import build_uri
from app_config import config
import json


class TestPlayerCommandEventsHandler(BaseTest, WebTest):
    APPLICATION = application
    INTENT = 'skykit.com/skdchromeapp/reset'
    GCM_REGISTRATION_ID = 'APA91bH0sONxgUSSUtERv-SGZHYvThi3jRv_p4ASYdTTLjgLntaZhyL9ti8aE-SWZm8ju1z0stjziWLvVdRt0'
    DEVICE_URLSAFE_KEY = 'kljlkjlkjlkjlkjlkjljlkj'

    def setUp(self):
        super(TestPlayerCommandEventsHandler, self).setUp()
        self.event = PlayerCommandEvent.create(device_urlsafe_key=self.DEVICE_URLSAFE_KEY,
                                               payload=self.INTENT, gcm_registration_id=self.GCM_REGISTRATION_ID)
        self.headers = {
            'Authorization': config.API_TOKEN
        }
        self.bad_authorization_header = {
            'Authorization': 'Forget about it!'
        }

    def test_get_device_command_events_returns_expected_events_list(self):
        request_parameters = {}
        number_of_device_events = 3
        self.__build_command_events(device_urlsafe_key='some-other-key', number_of_events=2)
        self.__build_command_events(device_urlsafe_key=self.DEVICE_URLSAFE_KEY,
                                    number_of_events=number_of_device_events)
        uri = build_uri('player-command-events', params_dict={'device_urlsafe_key': self.DEVICE_URLSAFE_KEY})
        response = self.app.get(uri, params=request_parameters, headers=self.headers)
        response_json = json.loads(response.body)
        self.assertLength(number_of_device_events, response_json)
        self.assertEqual(response_json[0]['payload'], 'payload-2')
        self.assertEqual(response_json[1]['payload'], 'payload-1')
        self.assertEqual(response_json[2]['payload'], 'payload-0')

    def test_put_no_authorization_header_returns_forbidden(self):
        event_key = self.event.put()
        uri = build_uri('manage-event', params_dict={'urlsafe_event_key': event_key.urlsafe()})
        request_body = {}
        response = self.put(uri, params=request_body, headers=self.bad_authorization_header)
        self.assertForbidden(response)

    def test_put_http_status_no_content(self):
        event_key = self.event.put()
        uri = build_uri('manage-event', params_dict={'urlsafe_event_key': event_key.urlsafe()})
        request_body = {}
        response = self.put(uri, params=request_body, headers=self.headers)
        self.assertEqual('204 No Content', response.status)

    def test_put_updates_player_has_confirmed(self):
        event_key = self.event.put()
        uri = build_uri('manage-event', params_dict={'urlsafe_event_key': event_key.urlsafe()})
        request_body = {}
        self.assertFalse(self.event.player_has_confirmed)
        self.put(uri, params=request_body, headers=self.headers)
        updated_event = event_key.get()
        self.assertTrue(updated_event.player_has_confirmed)

    def __build_command_events(self, device_urlsafe_key, number_of_events):
        for i in range(number_of_events):
            payload = 'payload-{0}'.format(i)
            event = PlayerCommandEvent.create(
                    device_urlsafe_key=device_urlsafe_key,
                    payload=payload,
                    gcm_registration_id=self.GCM_REGISTRATION_ID)
            event.put()
