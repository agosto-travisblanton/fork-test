from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest, WebTest
from models import PlayerCommandEvent
from routes import application
from utils.web_util import build_uri
from app_config import config


class TestCommandHandler(BaseTest, WebTest):
    APPLICATION = application
    INTENT = 'skykit.com/skdchromeapp/reset'
    GCM_REGISTRATION_ID = 'APA91bH0sONxgUSSUtERv-SGZHYvThi3jRv_p4ASYdTTLjgLntaZhyL9ti8aE-SWZm8ju1z0stjziWLvVdRt0'
    DEVICE_URLSAFE_KEY = 'kljlkjlkjlkjlkjlkjljlkj'

    def setUp(self):
        super(TestCommandHandler, self).setUp()
        self.player_command_event = PlayerCommandEvent.create(device_urlsafe_key=self.DEVICE_URLSAFE_KEY,
                                                              payload=self.INTENT,
                                                              gcm_registration_id=self.GCM_REGISTRATION_ID)
        self.event_key = self.player_command_event.put()
        self.headers = {
            'Authorization': config.API_TOKEN
        }
        self.bad_authorization_header = {
            'Authorization': 'Forget about it!'
        }

    def test_put_no_authorization_header_returns_forbidden(self):
        uri = build_uri('player-confirmation', params_dict={'urlsafe_event_key': self.event_key.urlsafe()})
        request_body = {}
        response = self.put(uri, params=request_body, headers=self.bad_authorization_header)
        self.assertForbidden(response)

    def test_put_http_status_no_content(self):
        uri = build_uri('player-confirmation', params_dict={'urlsafe_event_key': self.event_key.urlsafe()})
        request_body = {}
        response = self.put(uri, params=request_body, headers=self.headers)
        self.assertNotFound(response)

    def test_put_updates_player_has_confirmed(self):
        uri = build_uri('player-confirmation', params_dict={'urlsafe_event_key': self.event_key.urlsafe()})
        request_body = {}
        self.assertFalse(self.player_command_event.player_has_confirmed)
        self.put(uri, params=request_body, headers=self.headers)
        updated_event = self.event_key.get()
        self.assertTrue(updated_event.player_has_confirmed)
