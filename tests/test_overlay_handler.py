import json
from routes import application
from webtest import AppError
from models import Image, Domain, Tenant
from integrations.cloud_storage.cloud_storage_api import create_file

from provisioning_distributor_user_base_test import ProvisioningDistributorUserBase


class OverlayHandlerTest(ProvisioningDistributorUserBase):
    def setUp(self):
        super(OverlayHandlerTest, self).setUp()

    def test_post_overlay_fails_without_associated_image_key(self):
        uri = application.router.build(None, 'post-overlay', None, {"device_urlsafe_key": self.device_key.urlsafe()})
        request_parameters = {
            "position": "top_left",
            "type": "logo",
            "image_key": None
        }
        with self.assertRaises(AppError) as cm:
            response = self.app.post_json(uri, params=request_parameters)
            self.assertEqual(response.status_int, 400)

    def _create_image(self):
        fileContent = open('testFile.png').read()
        fileName = "aFile.png"
        contentType = "image/png"
        filepath = create_file(fileContent,
                               fileName,
                               contentType,
                               self.tenant.tenant_code)

        image_entity = Image.create(filepath=filepath, name=fileName,
                                    tenant_key=self.tenant.key)
        return image_entity.key.urlsafe()

    def test_post_overlay_succeeds_with_associated_image_key(self):
        key = self._create_image()

        uri = application.router.build(None, 'post-overlay', None, {"device_urlsafe_key": self.device_key.urlsafe()})

        request_parameters = {
            "top_left": {
                "type": "logo",
                "image_key": key
            }
        }

        # ensure post responds with data about entity that was created
        response = self.app.post_json(uri, params=request_parameters)
        response_json = json.loads(response.body)
        self.assertEqual(response_json["success"], True)
        overlays = response_json["overlay_template"]
        self.assertEqual(overlays["top_left"]["type"], "logo")
        self.assertEqual(overlays["top_left"]["imageKey"]["key"], key)
        self.assertEqual(response.status_int, 200)

        # ensure get chromeosdevice does not yet respond with overlays
        uri = application.router.build(None,
                                       'internal-device-get',
                                       None,
                                       {'device_urlsafe_key': self.device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        overlay = response_json["overlays"]
        self.assertFalse(overlay)

        # enable overlays for device so that the posted overlay will be included in the device representation
        self.device.enable_overlays()

        # check if device get returns newly created overlay
        uri = application.router.build(None,
                                       'internal-device-get',
                                       None,
                                       {'device_urlsafe_key': self.device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        overlay = response_json["overlays"]
        self.assertEqual(overlay["top_left"]["type"], "logo")
        self.assertEqual(overlay["top_left"]["imageKey"]["key"], key)

    def test_post_tenant_overlay_succeeds_with_associated_image_key(self):
        key = self._create_image()

        uri = application.router.build(None, 'post_tenant_overlay', None,
                                       {"tenant_urlsafe_key": self.tenant_key.urlsafe()})

        request_parameters = {
            "top_left": {
                "type": "logo",
                "image_key": key
            }
        }

        # ensure post responds with data about entity that was created
        response = self.app.post_json(uri, params=request_parameters)
        response_json = json.loads(response.body)
        self.assertEqual(response_json["success"], True)
        overlays = response_json["overlay_template"]
        self.assertEqual(overlays["top_left"]["type"], "logo")
        self.assertEqual(overlays["top_left"]["imageKey"]["key"], key)
        self.assertEqual(response.status_int, 200)

        # ensure get tenant does not yet respond with overlays
        uri = application.router.build(None,
                                       'manage-tenant',
                                       None,
                                       {'tenant_key': self.tenant.key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        overlay = response_json["overlays"]
        self.assertFalse(overlay)

        # enable overlays for device so that the posted overlay will be included in the device representation
        self.tenant.overlays_available = True
        self.tenant.put()

        # check if device get returns newly created overlay
        uri = application.router.build(None,
                                       'manage-tenant',
                                       None,
                                       {'tenant_key': self.tenant_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        overlay = response_json["overlays"]
        self.assertEqual(overlay["top_left"]["type"], "logo")
        self.assertEqual(overlay["top_left"]["imageKey"]["key"], key)
        return key

    def test_tenant_apply_overlay_to_tenant_devices(self):
        # to setup the tenant to the specified overlay
        key = self.test_post_tenant_overlay_succeeds_with_associated_image_key()

        # apply tenant overlay to devices
        uri = application.router.build(None,
                                       'tenant_apply_overlay_to_devices',
                                       None,
                                       {'tenant_urlsafe_key': self.tenant_key.urlsafe()})
        self.app.post(uri, params={}, headers=self.api_token_authorization_header)
        # run deffered tasks
        self.run_all_tasks()

        # grab any device to see that it matches the tenant
        uri = application.router.build(None,
                                       'internal-device-get',
                                       None,
                                       {'device_urlsafe_key': self.device_key.urlsafe()})
        response = self.app.get(uri, params={}, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        overlay = response_json["overlays"]
        self.assertEqual(overlay["top_left"]["type"], "logo")
        self.assertEqual(overlay["top_left"]["imageKey"]["key"], key)
