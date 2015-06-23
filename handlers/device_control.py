import json
from webapp2 import RequestHandler
from decorators import api_token_required
from device_commands_processor import (change_intent)
from models import ChromeOsDevice

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class DeviceCommandsHandler(RequestHandler):

    @api_token_required
    def post(self, device_urlsafe_key):
        chrome_os_device = ChromeOsDevice.get_by_device_id(device_urlsafe_key)
        self.response.headers.pop('Content-Type', None)
        if chrome_os_device:
            try:
                if self.request.body is not None:
                    request_json = json.loads(self.request.body)
                    intent = request_json.get('intent')
                    if intent:
                        change_intent(chrome_os_device.gcm_registration_id, intent)
            except Exception, e:
                self.response.set_status(422, 'An error occurred while processing intent: {0}'.
                                         format(e.message))
        else:
            self.response.set_status(422, 'Unable to find ChromeOS device by device key: {0}'.
                                     format(device_urlsafe_key))
