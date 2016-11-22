from utils.auth_util import requires_auth
from models import PlayerCommandEvent
from restler.serializers import json_response
from strategy import PLAYER_COMMAND_EVENT_STRATEGY
from extended_session_request_handler import ExtendedSessionRequestHandler

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class CommandEventsHandler(ExtendedSessionRequestHandler):
    @requires_auth
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

        json_response(
            self.response,
            {
                "events": events,
                "next_cursor": next_cursor,
                "prev_cursor": prev_cursor,
            },
            strategy=PLAYER_COMMAND_EVENT_STRATEGY
        )
