from env_setup import setup_test_paths

setup_test_paths()

from tests.provisioning_distributor_user_base_test import ProvisioningDistributorUserBase
from models import Overlay, OverlayTemplate, Image


class TestOverlayModel(ProvisioningDistributorUserBase):
    def setUp(self):
        self.image_str = 'some_string'
        super(TestOverlayModel, self).setUp()

    def test_create_overlay_without_image(self):
        type = 'TIME'
        self.assertFalse(Overlay.query().fetch())
        Overlay.create_or_get(type)
        self.assertEqual(Overlay.query().fetch()[0].type, type)
        self.assertEqual(Overlay.query().fetch()[0].image_key, None)

    def test_create_overlay_with_image(self):
        type = 'TIME'
        image_urlsafe_key = Image.create('some_str', 'some_name', self.tenant_key).key.urlsafe()
        self.assertFalse(Overlay.query().fetch())
        Overlay.create_or_get(type, image_urlsafe_key=image_urlsafe_key)
        self.assertEqual(Overlay.query().fetch()[0].type, type)
        self.assertEqual(Overlay.query().fetch()[0].image_key.urlsafe(), image_urlsafe_key)
    #
    def test_create_device_overlay_template(self):
        overlay_template = OverlayTemplate.create_or_get_by_device_key(self.device_key)
        self.assertEqual(self.device, overlay_template.device_key.get())

    def test_set_overlay_to_overlay_template(self):
        overlay_template = OverlayTemplate.create_or_get_by_device_key(self.device_key)
        overlay_template.set_overlay("TOP_LEFT", "TIME")
        overlay_template = OverlayTemplate.create_or_get_by_device_key(self.device_key)
        self.assertTrue(overlay_template.top_left)