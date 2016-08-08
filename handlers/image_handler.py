from google.appengine.ext import ndb
from agar.sessions import SessionRequestHandler
from models import Image
import json
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response
from strategy import IMAGE_STRATEGY


class ImageHandler(SessionRequestHandler, KeyValidatorMixin):
    def get(self, tenant_urlsafe_key):
        tenant_key = ndb.Key(urlsafe=tenant_urlsafe_key).get().key
        images = Image.get_by_tenant_key(tenant_key)
        return json_response(
            self.response, images, strategy=IMAGE_STRATEGY
        )

    def get_image_by_key(self, image_urlsafe_key):
        image_entity = ndb.Key(urlsafe=image_urlsafe_key).get()
        return json_response(
            self.response, {
                "svg_rep": image_entity.svg_rep,
                "name": image_entity.name
            }
        )

    def post(self, tenant_urlsafe_key):
        request_json = json.loads(self.request.body)
        tenant_key = ndb.Key(urlsafe=tenant_urlsafe_key).get().key
        svg_rep = request_json["svg_rep"]
        name = request_json["name"]
        image_entity = Image.create(svg_rep=svg_rep, name=name, tenant_key=tenant_key)
        return json_response(self.response, {
            "success": True,
            "key": image_entity.key.urlsafe()
        })
