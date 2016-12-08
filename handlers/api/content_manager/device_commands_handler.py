import inspect
import json

from decorators import requires_api_token
from device_message_processor import change_intent
from extended_session_request_handler import ExtendedSessionRequestHandler
from utils.device_util import resolve_device

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>. Bob MacNeal <bob.macneal@agosto.com>'


class DeviceCommandsHandler(ExtendedSessionRequestHandler):
    @requires_api_token
    def post(self, device_urlsafe_key):
        method_name = inspect.stack()[0][3]
        request_json = json.loads(self.request.body)
        intent = request_json.get('intent')
        if intent is None or intent == '':
            status = 400
            message = 'DeviceCommandsHandler.{0}: Invalid intent.'.format(method_name)
        else:
            status, message, device = resolve_device(device_urlsafe_key)
            if device:
                user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
                if user_identifier is None or user_identifier == '':
                    user_identifier = 'system'
                change_intent(
                    gcm_registration_id=device.gcm_registration_id,
                    payload=intent,
                    device_urlsafe_key=device_urlsafe_key,
                    host=self.request.host_url,
                    user_identifier=user_identifier)
        self.response.set_status(status, message)
