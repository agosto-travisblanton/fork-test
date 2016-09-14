from extended_session_request_handler import ExtendedSessionRequestHandler
from models import Tenant, Image
from restler.serializers import json_response
from integrations.cloud_storage.cloud_storage_api import create_file


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
        tenant = self.validate_and_get(tenant_urlsafe_key, Tenant, abort_on_not_found=True)
        tenant_code = tenant.tenant_code
        files = [
            {
                'content': f.file.read(),
                'filename': f.filename,
                'content_type': f.type
            } for f in self.request.POST.getall('files')
            ]

        if len(files) > 1 or len(files) < 1:
            return json_response(self.response, {
                "message": "At this time, you must include exactly one image to upload.",
            }, status_code=400)

        else:
            uploaded_file = files[0]

            try:
                filepath = create_file(uploaded_file["content"],
                                       uploaded_file["filename"],
                                       uploaded_file["content_type"],
                                       tenant_code)
                try:
                    image_entity = Image.create(filepath=filepath, name=uploaded_file["filename"],
                                                tenant_key=tenant.key)

                    json_response(self.response, {
                        "success": True,
                        "key": image_entity.key.urlsafe()
                    })

                except ValueError:
                    json_response(self.response, {
                        "success": False,
                    }, status_code=409)

            except ValueError:
                json_response(self.response, {
                    "success": False,
                }, status_code=409)
