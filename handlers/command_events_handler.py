from webapp2 import RequestHandler

from decorators import requires_api_token
from models import PlayerCommandEvent
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response
from strategy import PLAYER_COMMAND_EVENT_STRATEGY

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class CommandEventsHandler(RequestHandler, KeyValidatorMixin):

    @requires_api_token
    def get_player_command_events(self, device_urlsafe_key, prev_cursor_str, next_cursor_str):
        next_cursor_str = next_cursor_str if next_cursor_str != "null" else None
        prev_cursor_str = prev_cursor_str if prev_cursor_str != "null" else None

        events = PlayerCommandEvent.get_events_by_device_key(
            device_urlsafe_key=device_urlsafe_key,
            prev_cursor_str=prev_cursor_str,
            next_cursor_str=next_cursor_str

        )

        prev_cursor = events["prev_cursor"]
        next_cursor = events["next_cursor"]
        events = events["objects"]

        return json_response(
            self.response,
            {
                "events": events,
                "next_cursor": next_cursor,
                "prev_cursor": prev_cursor,
            },
            strategy=PLAYER_COMMAND_EVENT_STRATEGY
        )
