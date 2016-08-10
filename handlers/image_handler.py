from google.appengine.ext import ndb
from agar.sessions import SessionRequestHandler
from models import Image
import logging
import json
from ndb_mixins import KeyValidatorMixin
from restler.serializers import json_response


class ImageHandler(SessionRequestHandler, KeyValidatorMixin):
    def get(self, tenant_urlsafe_key):
        try:
            tenant = ndb.Key(urlsafe=tenant_urlsafe_key).get()
        except Exception, e:
            logging.exception(e)
        if tenant is None:
            status = 404
            message = 'Unrecognized tenant with key: {0}'.format(tenant)
            return self.response.set_status(status, message)

        images = Image.get_by_tenant_key(tenant.key)
        return json_response(
            self.response, [
                {
                    "key": image.key.urlsafe(),
                    "name": image.name
                } for image in images
                ]
        )

    def get_image_by_key(self, image_urlsafe_key):
        try:
            image = ndb.Key(urlsafe=image_urlsafe_key).get()
        except Exception, e:
            logging.exception(e)
        if image is None:
            status = 404
            message = 'Unrecognized image with key: {0}'.format(image)
            return self.response.set_status(status, message)

        image_entity = ndb.Key(urlsafe=image_urlsafe_key).get()
        return json_response(
            self.response, {
                "svg_rep": image_entity.svg_rep,
                "name": image_entity.name
            }
        )

    def post(self, tenant_urlsafe_key):
        request_json = json.loads(self.request.body)
        svg_rep = request_json.get("svg_rep")
        name = request_json.get("name")

        try:
            tenant = ndb.Key(urlsafe=tenant_urlsafe_key).get()
        except Exception, e:
            logging.exception(e)
        if tenant is None:
            status = 404
            message = 'Unrecognized tenant with key: {0}'.format(tenant)
            return self.response.set_status(status, message)

        if not name or name == '':
            return json_response(self.response, {
                "success": False,
                "message": "Missing name"
            }, status_code=400)

        if not svg_rep or svg_rep == '':
            return json_response(self.response, {
                "success": False,
                "message": "Missing svg_rep"
            }, status_code=400)

        image_entity = Image.create(svg_rep=svg_rep, name=name, tenant_key=tenant.key)

        if image_entity:
            json_response(self.response, {
                "success": True,
                "key": image_entity.key.urlsafe()
            })

        else:
            json_response(self.response, {
                "success": False,
            }, status_code=409)
