from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
from models import PlayerCommandEvent

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestPlayerCommandEventModel(BaseTest):
    INTENT = 'skykit.com/skdchromeapp/reset'
    GCM_REGISTRATION_ID = 'APA91bH0sONxgUSSUtERv-SGZHYvThi3jRv_p4ASYdTTLjgLntaZhyL9ti8aE-SWZm8ju1z0stjziWLvVdRt0'
    DEVICE_URLSAFE_KEY = 'kljlkjlkjlkjlkjlkjljlkj'
    CURRENT_CLASS_VERSION = 1

    def setUp(self):
        super(TestPlayerCommandEventModel, self).setUp()

    def test_create_returns_expected_player_command_event_representation(self):
        event = PlayerCommandEvent.create(device_urlsafe_key=self.DEVICE_URLSAFE_KEY,
                                          payload=self.INTENT, gcm_registration_id=self.GCM_REGISTRATION_ID)
        self.assertIsNone(event.created)
        self.assertIsNone(event.updated)
        self.assertFalse(event.player_has_confirmed)
        event_key = event.put()
        persisted_event = event_key.get()
        self.assertIsNotNone(persisted_event.key)
        self.assertEqual(persisted_event.payload, self.INTENT)
        self.assertEqual(persisted_event.gcm_registration_id, self.GCM_REGISTRATION_ID)
        self.assertIsNotNone(persisted_event.created)
        self.assertIsNotNone(persisted_event.updated)
        self.assertFalse(persisted_event.player_has_confirmed)

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        event = PlayerCommandEvent.create(device_urlsafe_key=self.DEVICE_URLSAFE_KEY,
                                          payload=self.INTENT, gcm_registration_id=self.GCM_REGISTRATION_ID)
        event.class_version = 47
        event.put()
        self.assertEqual(event.class_version, self.CURRENT_CLASS_VERSION)
