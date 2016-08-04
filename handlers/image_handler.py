from google.appengine.ext import ndb
from agar.sessions import SessionRequestHandler
from models import Image
import json
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response


class ImageHandler(SessionRequestHandler, KeyValidatorMixin):
    def get_image_by_key(self, image_urlsafe_key):
        image_entity = ndb.Key(urlsafe=image_urlsafe_key).get()
        return json_response(
            self.response, {
                "svg_rep": image_entity.svg_rep
            }
        ), 200

    def post(self):
        request_json = json.loads(self.request.body)
        svg_rep = request_json["svg_rep"]
        image_entity = Image.create(svg_rep=svg_rep)
        return json_response(self.response, {
            "success": True,
            "key": image_entity.key.urlsafe()
        }), 209
