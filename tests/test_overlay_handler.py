import json
from routes import application
from webtest import AppError

from provisioning_distributor_user_base_test import ProvisioningDistributorUserBase


class OverlayHandlerTest(ProvisioningDistributorUserBase):
    def setUp(self):
        super(OverlayHandlerTest, self).setUp()
        self.svg_rep = "ffdkfdkfsklfsljkflksfjlkfsa"

    def test_post_overlay_fails_without_associated_image_key(self):
        uri = application.router.build(None, 'post-overlay', None, {"device_urlsafe_key": self.device_key.urlsafe()})
        request_parameters = {
            "position": "TOP_LEFT",
            "type": "LOGO",
            "image_key": None
        }
        with self.assertRaises(AppError) as cm:
            response = self.app.post_json(uri, params=request_parameters)
            self.assertEqual(response.status_int, 400)

    def _create_image(self):
        request_parameters = {'svg_rep': self.svg_rep, 'name': 'some_name'}
        uri = application.router.build(None, 'manage-image', None, {'tenant_urlsafe_key': self.tenant_key.urlsafe()})
        response = self.app.post_json(uri, params=request_parameters)
        json_response = json.loads(response.body)
        return json_response["key"]

    def test_post_overlay_succeeds_with_associated_image_key(self):
        key = self._create_image()

        uri = application.router.build(None, 'post-overlay', None, {"device_urlsafe_key": self.device_key.urlsafe()})

        request_parameters = {
            "top_left": {
                "type": "LOGO",
                "image_key": key
            }
        }

        # ensure post responds with data about entity that was created
        response = self.app.post_json(uri, params=request_parameters)
        response_json = json.loads(response.body)
        self.assertEqual(response_json["success"], True)
        overlays = response_json["overlay_template"]
        self.assertEqual(overlays["top_left"]["type"], "LOGO")
        self.assertEqual(overlays["top_left"]["image_key"]["key"], key)
        self.assertEqual(response.status_int, 200)

        # ensure get chromeosdevice does not yet respond with overlays
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': self.device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        overlay = response_json["overlay"]
        self.assertFalse(overlay)

        # enable overlays for device so that the posted overlay will be included in the device representation
        self.device.enable_overlays()

        # check if device get returns newly created overlay
        uri = application.router.build(None,
                                       'device',
                                       None,
                                       {'device_urlsafe_key': self.device_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters, headers=self.api_token_authorization_header)
        response_json = json.loads(response.body)
        overlay = response_json["overlay"]
        self.assertEqual(overlay["top_left"]["type"], "LOGO")
        self.assertEqual(overlay["top_left"]["image_key"]["key"], key)
