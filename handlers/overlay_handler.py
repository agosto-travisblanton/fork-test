from google.appengine.ext import ndb
from agar.sessions import SessionRequestHandler
from models import OverlayTemplate
import json
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response
import ndb_json


class OverlayHandler(SessionRequestHandler, KeyValidatorMixin):
    def post(self):
        request_json = json.loads(self.request.body)
        associated_device_key = ndb.Key(urlsafe=request_json["device_urlsafe_key"]).get().key
        # array of dictionaries that contain data about each overlay
        overlays = request_json["overlays"]
        overlay_template = OverlayTemplate.create_or_get_by_device_key(associated_device_key)

        for overlay_config in overlays:
            try:
                overlay_template.set_overlay(overlay_config)

            except ValueError as exp:
                return json_response(self.response, {
                    "success": False,
                    "message": exp
                }, status_code=400)

        overlay_template = OverlayTemplate.create_or_get_by_device_key(associated_device_key)
        # This method is offered because restler doesn't support keyProperty serialization beyond a single child
        overlay_template_intermediate_json = ndb_json.dumps(overlay_template)

        return json_response(self.response, {
            "success": True,
            "overlay_template": overlay_template_intermediate_json
        }, status_code=200)
