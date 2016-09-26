from models import OverlayTemplate
import json
from models import ChromeOsDevice, Tenant
from app_config import config
from device_message_processor import change_intent
from restler.serializers import json_response
from extended_session_request_handler import ExtendedSessionRequestHandler


class OverlayHandler(ExtendedSessionRequestHandler):
    def post(self, device_urlsafe_key):
        request_json = json.loads(self.request.body)
        device = self.validate_and_get(device_urlsafe_key, ChromeOsDevice, abort_on_not_found=True)

        # array of dictionaries that contain data about each overlay
        overlay_template = OverlayTemplate.create_or_get_by_device_key(device.key)

        for each_key in request_json.keys():
            if each_key.lower() not in ["bottom_left", "bottom_right", "top_right", "top_left"]:
                return json_response(self.response, {
                    "success": False,
                    "message": "ONE OF YOUR KEYS WAS NOT VALID."
                }, status_code=400)

        # key representes position
        for key, value in request_json.iteritems():
            # type can be None, but its not optional. None is an overlay Type
            overlay_type = value.get("type")
            # image_key can be None, it is optional
            image_key = value.get("image_key")
            size = value.get("size")

            overlay_template.set_overlay(position=key,
                                         size=size.lower() if size else None,
                                         overlay_type=overlay_type,
                                         image_urlsafe_key=image_key)

        if device.overlays_available:
            change_intent(
                gcm_registration_id=device.gcm_registration_id,
                payload=config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                device_urlsafe_key=device_urlsafe_key,
                host=self.request.host_url,
                user_identifier='system (overlay update)'
            )

        return json_response(self.response, {
            "success": True,
            "overlay_template": device.overlays_as_dict
        }, status_code=200)

    def post_tenant_overlay(self, tenant_urlsafe_key):
        request_json = json.loads(self.request.body)
        tenant = self.validate_and_get(tenant_urlsafe_key, Tenant, abort_on_not_found=True)

        # array of dictionaries that contain data about each overlay
        overlay_template = OverlayTemplate.create_or_get_by_tenant_key(tenant.key)

        for each_key in request_json.keys():
            if each_key.lower() not in ["bottom_left", "bottom_right", "top_right", "top_left"]:
                return json_response(self.response, {
                    "success": False,
                    "message": "ONE OF YOUR KEYS WAS NOT VALID."
                }, status_code=400)

        # key represents position
        for key, value in request_json.iteritems():
            # type can be None, but its not optional. None is an overlay Type
            overlay_type = value.get("type")
            # image_key can be None, it is optional
            image_key = value.get("image_key")
            size = value.get("size")

            overlay_template.set_overlay(position=key,
                                         size=size.lower() if size else None,
                                         overlay_type=overlay_type,
                                         image_urlsafe_key=image_key)

        # if tenant.overlays_override:
            # !!! SENDS GCM UPDATE TO ALL DEVICES IN TENANT
            # tenant.gcm_update_devices(host=self.request.host_url, user_identifier="system (overlay override)")

        return json_response(self.response, {
            "success": True,
            "overlay_template": tenant.overlays_as_dict
        }, status_code=200)


    def tenant_override_device_overlays(self, tenant_urlsafe_key):
        tenant = self.validate_and_get(tenant_urlsafe_key, Tenant, abort_on_not_found=True)
        tenant.overlays_override = True
        tenant.put()
        tenant.gcm_update_devices(host=self.request.host_url, user_identifier="system (overlay override)")
        return json_response(self.response, {
            "success": True,
            "overlay_template": tenant.overlays_as_dict
        }, status_code=200)

    def tenant_apply_overlay_to_devices(self, tenant_urlsafe_key):
        tenant = self.validate_and_get(tenant_urlsafe_key, Tenant, abort_on_not_found=True)
        tenant_overlay_template = OverlayTemplate.create_or_get_by_tenant_key(tenant.key)
        tenant_overlay_template.apply_overlay_template_to_all_tenant_devices(host=self.request.host_url, user_identifier="system (overlay override)")
        tenant.gcm_update_devices(host=self.request.host_url, user_identifier="system (overlay override)")
        return json_response(self.response, {
            "success": True,
            "overlay_template": tenant.overlays_as_dict
        }, status_code=200)