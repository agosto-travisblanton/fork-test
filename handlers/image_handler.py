from extended_session_request_handler import ExtendedSessionRequestHandler

from models import Tenant, Image
from restler.serializers import json_response


class ImageHandler(ExtendedSessionRequestHandler):
    def get(self, tenant_urlsafe_key):
        tenant = self.validate_and_get(tenant_urlsafe_key, Tenant, abort_on_not_found=True)

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
        image = self.validate_and_get(image_urlsafe_key, Image, abort_on_not_found=True)
        return json_response(
            self.response, {
                "svg_rep": image.svg_rep,
                "name": image.name
            }
        )

    def post(self, tenant_urlsafe_key):
        name = self.check_and_get_field('name')
        svg_rep = self.check_and_get_field('svg_rep')
        tenant = self.validate_and_get(tenant_urlsafe_key, Tenant, abort_on_not_found=True)

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
