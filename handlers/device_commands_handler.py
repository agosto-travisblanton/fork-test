import json
import logging

from google.appengine.ext import ndb

from webapp2 import RequestHandler

from decorators import api_token_required
from device_commands_processor import (change_intent)
from models import ChromeOsDevice


__author__ = 'Christopher Bartling <chris.bartling@agosto.com>. Bob MacNeal <bob.macneal@agosto.com>'


class DeviceCommandsHandler(RequestHandler):

    @api_token_required
    def post(self, device_urlsafe_key):
        logging.info("Device intent change")
        self.response.headers.pop('Content-Type', None)
        chrome_os_device = None
        try:
            device_key = ndb.Key(urlsafe=device_urlsafe_key)
            chrome_os_device = device_key.get()
        except Exception, e:
            logging.info("Problem fetching the device key. About to blow chunks.")
            logging.exception(e)
        if chrome_os_device:
            try:
                if self.request.body is not None:
                    request_json = json.loads(self.request.body)
                    intent = request_json.get('intent')
                    if intent:
                        change_intent(chrome_os_device.gcm_registration_id, intent)
            except Exception, e:
                logging.info("Found device, but 422 about to be returned due to exception")
                logging.exception(e, exc_info=True)
                self.response.set_status(422, 'An error occurred while processing intent: {0}'.
                                         format(e.message))
        else:
            error_message = 'Unable to find ChromeOS device by key: {0}'.format(device_urlsafe_key)
            logging.exception(error_message)
            self.response.set_status(422, error_message)
