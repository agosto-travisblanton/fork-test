from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest, WebTest
from models import PlayerCommandEvent
from routes import application
from utils.web_util import build_uri
from app_config import config


class TestPlayerCommandEventsHandler(BaseTest, WebTest):
    APPLICATION = application
    INTENT = 'skykit.com/skdchromeapp/reset'
    GCM_REGISTRATION_ID = 'APA91bH0sONxgUSSUtERv-SGZHYvThi3jRv_p4ASYdTTLjgLntaZhyL9ti8aE-SWZm8ju1z0stjziWLvVdRt0'

    def setUp(self):
        super(TestPlayerCommandEventsHandler, self).setUp()
        self.event = PlayerCommandEvent.create(payload=self.INTENT, gcm_registration_id=self.GCM_REGISTRATION_ID)
        self.event_key = self.event.put()
        self.headers = {
            'Authorization': config.API_TOKEN
        }
        self.bad_authorization_header = {
            'Authorization': 'Forget about it!'
        }
        self.uri = build_uri('manage-event', params_dict={'urlsafe_event_key': self.event_key.urlsafe()})

    def test_put_no_authorization_header_returns_forbidden(self):
        request_body = {}
        response = self.put(self.uri, params=request_body, headers=self.bad_authorization_header)
        self.assertForbidden(response)

    def test_put_http_status_no_content(self):
        request_body = {}
        response = self.put(self.uri, params=request_body, headers=self.headers)
        self.assertEqual('204 No Content', response.status)

    def test_put_updates_player_has_confirmed(self):
        request_body = {}
        self.assertFalse(self.event.player_has_confirmed)
        self.put(self.uri, params=request_body, headers=self.headers)
        updated_event = self.event_key.get()
        self.assertTrue(updated_event.player_has_confirmed)
