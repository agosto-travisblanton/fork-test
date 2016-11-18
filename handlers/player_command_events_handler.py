import logging
from webapp2 import RequestHandler
from utils.auth_util import requires_auth
from models import PlayerCommandEvent
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response
from strategy import PLAYER_COMMAND_EVENT_STRATEGY
from datetime import datetime
from extended_session_request_handler import ExtendedSessionRequestHandler

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class PlayerCommandEventsHandler(ExtendedSessionRequestHandler):
    @requires_auth
    def command_confirmation(self, urlsafe_event_key):
        try:
            command_event = self.validate_and_get(urlsafe_event_key, PlayerCommandEvent, abort_on_not_found=True)
        except Exception, e:
            logging.exception(e)
        command_event.confirmed = datetime.utcnow()
        command_event.player_has_confirmed = True
        command_event.put()
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)

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
