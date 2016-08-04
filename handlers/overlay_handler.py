from google.appengine.ext import ndb
from agar.sessions import SessionRequestHandler
from models import Overlay, OverlayTemplate
import json
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response
from strategy import OVERLAY_TEMPLATE
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
        # restler doesn't serialize keyProperties properly, so ndb_json was used
        overlay_template_intermediate_json = ndb_json.dumps(overlay_template)
        overlay_template_dict = ndb_json.loads(overlay_template_intermediate_json)
        overlay_template_json_final = json.dumps(overlay_template_dict)

        return json_response(self.response, {
            "success": True,
            "overlay_template": overlay_template_json_final
        }, status_code=200)