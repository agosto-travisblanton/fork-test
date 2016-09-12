from extended_session_request_handler import ExtendedSessionRequestHandler
import json
from models import Tenant, Image
from restler.serializers import json_response
import urllib
import cgi
from google.appengine.ext.webapp import blobstore_handlers


class ImageHandler(ExtendedSessionRequestHandler, blobstore_handlers.BlobstoreUploadHandler):
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

        files = self.request.POST.getall('files')

        _files = [{'content': f.file.read(),
                         'filename': f.filename} for f in files]

        print _files


        return
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
