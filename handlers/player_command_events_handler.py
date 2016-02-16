import logging

from webapp2 import RequestHandler

from decorators import requires_api_token
from models import PlayerCommandEvent
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response
from strategy import PLAYER_COMMAND_EVENT_STRATEGY
from datetime import datetime


__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class PlayerCommandEventsHandler(RequestHandler, KeyValidatorMixin):
    @requires_api_token
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

    @requires_api_token
    def get_player_command_events(self, device_urlsafe_key):
        events = PlayerCommandEvent.get_events_by_device_key(device_urlsafe_key)
        return json_response(self.response, events, strategy=PLAYER_COMMAND_EVENT_STRATEGY)
