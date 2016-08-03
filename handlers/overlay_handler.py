from google.appengine.ext import ndb
from agar.sessions import SessionRequestHandler
from models import Overlay, DeviceOverlayAssociation
import json
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response


class OverlayHandler(SessionRequestHandler, KeyValidatorMixin):
    def post(self):
        request_json = json.loads(self.request.body)
        associated_device_key = ndb.Key(urlsafe=request_json["associated_device_urlsafe"]).get().key

        position = request_json["position"]
        overlay_type = request_json["overlay_type"]
        # expects the front-end to already know the urlsafe_key of a previously posted image
        associated_image = request_json["associated_image"]
        if associated_image != None:
            # gets it first to make sure it is a valid key. Will except if it is not
            # uses this key instead of
            associated_image = ndb.Key(urlsafe=associated_image).get().key

        overlay_key = Overlay.create(overlay_type=overlay_type, overlay_position=position, image_key=associated_image)
        DeviceOverlayAssociation.create_association(device_key=associated_device_key, overlay_key=overlay_key.key)

        return json_response(self.response, {
            "success": True,
        }), 209

