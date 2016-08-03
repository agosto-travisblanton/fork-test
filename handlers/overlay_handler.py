from google.appengine.ext import ndb
from agar.sessions import SessionRequestHandler
from models import Image, Overlay
import json
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response


class OverlayHandler(SessionRequestHandler, KeyValidatorMixin):
    def post(self):
        request_json = json.loads(self.request.body)
        position = request_json["position"]
        overlay_type = request_json["overlay_type"]

        Overlay.create(overlay_type=overlay_type, overlay_position=position)

        # image_entity = Image.create(svg_rep=svg_rep)
        # return json_response(self.response, {
        #     "success": True,
        #     "key": image_entity.key.urlsafe()
        # }), 209
