from extended_session_request_handler import ExtendedSessionRequestHandler
from models import Tenant, Image, ChromeOsDevice, OverlayTemplate
from restler.serializers import json_response
from integrations.cloud_storage.cloud_storage_api import create_file, delete_file
import logging


class ImageHandler(ExtendedSessionRequestHandler):
    def delete(self, image_urlsafe_key, device_urlsafe_key):
        device = self.validate_and_get(device_urlsafe_key, ChromeOsDevice, abort_on_not_found=True)
        device_overlay_template = OverlayTemplate.get_overlay_template_for_device(device.key)

        image = self.validate_and_get(image_urlsafe_key, Tenant, abort_on_not_found=True)
        image_in_use = device_overlay_template.image_in_use(image.key)

        if image_in_use:
            json_response(self.response,
                          {
                              "success": False,
                              "message": "Image is currently in use"
                          },
                          status_code=400)

        else:
            deleted_file = delete_file(image.gcs_path)
            if deleted_file:
                image.key.delete()
                json_response(self.response,
                              {
                                  "success": True,
                                  "message": "Image was succesfully deleted"
                              })
            else:
                message = "Image key {} could not be deleted".format(image.key)
                logging.error(message)
                json_response(self.response,
                              {
                                  "success": False,
                                  "message": message
                              },
                              status_code=400)

    def get(self, tenant_urlsafe_key):
        tenant = self.validate_and_get(tenant_urlsafe_key, Tenant, abort_on_not_found=True)

        images = Image.get_by_tenant_key(tenant.key)
        return json_response(
            self.response, [
                {
                    "key": image.key.urlsafe(),
                    "name": image.name,
                    "filepath": image.filepath
                } for image in images
                ]
        )

    def get_image_by_key(self, image_urlsafe_key):
        image = self.validate_and_get(image_urlsafe_key, Image, abort_on_not_found=True)
        return json_response(
            self.response, {
                "filepath": image.filepath,
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

            except ValueError as e:
                json_response(self.response, {
                    "success": False,
                }, status_code=409)
