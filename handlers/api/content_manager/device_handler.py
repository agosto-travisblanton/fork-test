import json

from decorators import requires_cm_key
from extended_session_request_handler import ExtendedSessionRequestHandler
from models import ChromeOsDevice
from restler.serializers import json_response
from strategy import CHROME_OS_DEVICE_STRATEGY


class DeviceHandler(ExtendedSessionRequestHandler):

    @requires_cm_key
    def put(self, device_urlsafe_key):
        request_json = json.loads(self.request.body)
        new_content_manager_display_name = request_json["name"]
        device = self.validate_and_get(device_urlsafe_key, ChromeOsDevice, abort_on_not_found=True, use_app_engine_memcache=False)
        device.content_manager_display_name = new_content_manager_display_name
        device.put()
        device = self.validate_and_get(device_urlsafe_key, ChromeOsDevice, abort_on_not_found=True, use_app_engine_memcache=False)
        json_response(self.response, device, strategy=CHROME_OS_DEVICE_STRATEGY)

