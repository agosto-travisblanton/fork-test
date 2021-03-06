import httplib
import logging

from datetime import datetime
from webapp2 import RequestHandler

from decorators import requires_api_token
from models import PlayerCommandEvent
from ndb_mixins import KeyValidatorMixin

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class CommandHandler(RequestHandler, KeyValidatorMixin):

    @requires_api_token
    def player_confirmation(self, urlsafe_event_key):
        try:
            command_event = self.validate_and_get(urlsafe_event_key, PlayerCommandEvent, abort_on_not_found=True)
        except Exception, e:
            logging.exception(e)
        command_event.confirmed = datetime.utcnow()
        command_event.player_has_confirmed = True
        command_event.put()
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(httplib.NOT_FOUND)
