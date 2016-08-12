from google.appengine.ext import ndb
from agar.sessions import SessionRequestHandler
from models import OverlayTemplate
import logging
import json
from models import ChromeOsDevice
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response
import ndb_json


class OverlayHandler(SessionRequestHandler, KeyValidatorMixin):
    def post(self, device_urlsafe_key):
        request_json = json.loads(self.request.body)
        device = self.validate_and_get(device_urlsafe_key, ChromeOsDevice, abort_on_not_found=True)

        # array of dictionaries that contain data about each overlay
        overlay_template = OverlayTemplate.create_or_get_by_device_key(device.key)

        for each_key in request_json.keys():
            if each_key.upper() not in ["BOTTOM_LEFT", "BOTTOM_RIGHT", "TOP_RIGHT", "TOP_LEFT"]:
                return json_response(self.response, {
                    "success": False,
                    "message": "ONE OF YOUR KEYS WAS NOT VALID."
                }, status_code=400)

        # key representes position
        for key, value in request_json.iteritems():
            overlay_type = self.check_and_get_field('type', value)

            # image_key can be None, it is optional
            image_key = value.get("image_key")

            overlay_template.set_overlay(position=key, overlay_type=overlay_type,
                                         image_urlsafe_key=image_key)

        # re-get the template after the changes set_overlay made
        overlay_template = OverlayTemplate.create_or_get_by_device_key(device.key)
        # This method is offered because restler doesn't support keyProperty serialization beyond a single child
        overlay_template_intermediate_json = ndb_json.dumps(overlay_template)
        overlay_template_dict = ndb_json.loads(overlay_template_intermediate_json)

        return json_response(self.response, {
            "success": True,
            "overlay_template": overlay_template_dict
        }, status_code=200)
