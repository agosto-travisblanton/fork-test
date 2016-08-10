from google.appengine.ext import ndb
from agar.sessions import SessionRequestHandler
from models import OverlayTemplate
import json
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response
import ndb_json


class OverlayHandler(SessionRequestHandler, KeyValidatorMixin):
    def post(self, device_urlsafe_key):
        request_json = json.loads(self.request.body)
        associated_device_key = ndb.Key(urlsafe=device_urlsafe_key).get().key
        # array of dictionaries that contain data about each overlay
        overlay_template = OverlayTemplate.create_or_get_by_device_key(associated_device_key)

        for each_key in request_json.keys():
            if each_key.upper() not in ["BOTTOM_LEFT", "BOTTOM_RIGHT", "TOP_RIGHT", "TOP_LEFT"]:
                return json_response(self.response, {
                    "success": False,
                    "message": "ONE OF YOUR KEYS WAS NOT VALID."
                }, status_code=400)

        # key representes position
        for key, value in request_json.iteritems():
            overlay_type = value.get("type")

            # image_key can be None, it is optional
            image_key = value.get("image_key")

            if not overlay_type or overlay_type == '':
                return json_response(self.response, {
                    "success": False,
                    "message": "Missing overlay_type"
                }, status_code=400)

            overlay_template.set_overlay(position=key, overlay_type=overlay_type,
                                         image_urlsafe_key=image_key)

        # re-get the template after the changes set_overlay made
        overlay_template = OverlayTemplate.create_or_get_by_device_key(associated_device_key)
        # This method is offered because restler doesn't support keyProperty serialization beyond a single child
        overlay_template_intermediate_json = ndb_json.dumps(overlay_template)
        overlay_template_dict = ndb_json.loads(overlay_template_intermediate_json)

        return json_response(self.response, {
            "success": True,
            "overlay_template": overlay_template_dict
        }, status_code=200)
