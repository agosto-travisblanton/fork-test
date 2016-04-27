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
        self.assertIsNotNone(event.posted)
        self.assertIsNone(event.confirmed)
        self.assertFalse(event.player_has_confirmed)
        event_key = event.put()
        persisted_event = event_key.get()
        self.assertIsNotNone(persisted_event.key)
        self.assertEqual(persisted_event.payload, self.INTENT)
        self.assertEqual(persisted_event.gcm_registration_id, self.GCM_REGISTRATION_ID)
        self.assertIsNotNone(persisted_event.posted)
        self.assertIsNone(persisted_event.confirmed)
        self.assertFalse(persisted_event.player_has_confirmed)

    def test_class_version_is_only_set_by_pre_put_hook_method(self):
        event = PlayerCommandEvent.create(device_urlsafe_key=self.DEVICE_URLSAFE_KEY,
                                          payload=self.INTENT, gcm_registration_id=self.GCM_REGISTRATION_ID)
        event.class_version = 47
        event.put()
        self.assertEqual(event.class_version, self.CURRENT_CLASS_VERSION)

    def test_get_events_by_device_key_in_reverse_order_updated(self):
        self.__build_command_events(device_urlsafe_key='some-other-key', number_of_events=2)
        self.__build_command_events(device_urlsafe_key=self.DEVICE_URLSAFE_KEY,
                                    number_of_events=51)

        device_events_list = PlayerCommandEvent.get_events_by_device_key(self.DEVICE_URLSAFE_KEY)
        self.assertLength(25, device_events_list["objects"])
        self.assertEqual(device_events_list["objects"][0].payload, 'payload-50')
        self.assertEqual(device_events_list["objects"][1].payload, 'payload-49')
        self.assertEqual(device_events_list["objects"][2].payload, 'payload-48')


        next_device_events_list = PlayerCommandEvent.get_events_by_device_key(self.DEVICE_URLSAFE_KEY, next_cursor_str=device_events_list["next_cursor"])
        self.assertLength(25, next_device_events_list["objects"])
        self.assertEqual(next_device_events_list["objects"][0].payload, 'payload-25')

        prev_device_events_list = PlayerCommandEvent.get_events_by_device_key(self.DEVICE_URLSAFE_KEY,
                                                                              prev_cursor_str=device_events_list[
                                                                                  "prev_cursor"])
        self.assertLength(25, prev_device_events_list["objects"])
        self.assertEqual(prev_device_events_list["objects"][0].payload, 'payload-50')

    def __build_command_events(self, device_urlsafe_key, number_of_events):
        for i in range(number_of_events):
            payload = 'payload-{0}'.format(i)
            event = PlayerCommandEvent.create(
                    device_urlsafe_key=device_urlsafe_key,
                    payload=payload,
                    gcm_registration_id=self.GCM_REGISTRATION_ID)
            event.put()
