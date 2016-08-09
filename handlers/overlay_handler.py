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

        # key representes position
        for key, value in request_json.iteritems():
            print value
            overlay_template.set_overlay(position=key, overlay_type=value["type"], image_urlsafe_key=value["image_urlsafe_key"])

        # re-get the template after the changes set_overlay made
        overlay_template = OverlayTemplate.create_or_get_by_device_key(associated_device_key)
        # This method is offered because restler doesn't support keyProperty serialization beyond a single child
        overlay_template_intermediate_json = ndb_json.dumps(overlay_template)
        overlay_template_dict = ndb_json.loads(overlay_template_intermediate_json)

        return json_response(self.response, {
            "success": True,
            "overlay_template": overlay_template_dict
        }, status_code=200)
