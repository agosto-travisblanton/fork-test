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

    def test_get_events_by_device_key_in_reverse_order_updated(self):
        number_of_device_events = 3
        self.__build_command_events(device_urlsafe_key='some-other-key', number_of_events=2)
        self.__build_command_events(device_urlsafe_key=self.DEVICE_URLSAFE_KEY,
                                    number_of_events=number_of_device_events)
        device_events_list = PlayerCommandEvent.get_events_by_device_key(self.DEVICE_URLSAFE_KEY)
        self.assertLength(number_of_device_events, device_events_list)
        self.assertEqual(device_events_list[0].payload, 'payload-2')
        self.assertEqual(device_events_list[1].payload, 'payload-1')
        self.assertEqual(device_events_list[2].payload, 'payload-0')

    def __build_command_events(self, device_urlsafe_key, number_of_events):
        for i in range(number_of_events):
            payload = 'payload-{0}'.format(i)
            event = PlayerCommandEvent.create(
                    device_urlsafe_key=device_urlsafe_key,
                    payload=payload,
                    gcm_registration_id=self.GCM_REGISTRATION_ID)
            event.put()
