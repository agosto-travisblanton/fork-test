import json
import logging

from google.appengine.ext import ndb

from webapp2 import RequestHandler

from decorators import api_token_required
from device_commands_processor import (change_intent)

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class DisplayCommandsHandler(RequestHandler):
    @api_token_required
    def post(self, display_urlsafe_key):
        status = 200
        message = None
        request_json = json.loads(self.request.body)
        intent = request_json.get('intent')
        if intent is None or intent == '':
            status = 400
            message = 'DisplayCommandsHandler: Invalid intent.'
        else:
            display = None
            try:
                display_key = ndb.Key(urlsafe=display_urlsafe_key)
                display = display_key.get()
            except Exception, e:
                logging.exception(e)
            if display:
                change_intent(display.gcm_registration_id, intent)
            else:
                status = 404
                message = 'DisplayCommandsHandler: Display not found with key: {0}'.format(display_urlsafe_key)
                logging.error(message)
        self.response.set_status(status, message)
