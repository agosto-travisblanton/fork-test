from env_setup import setup_test_paths

setup_test_paths()

from tests.provisioning_distributor_user_base_test import ProvisioningDistributorUserBase
from models import Overlay, DeviceOverlayAssociation, Image


class TestOverlayModel(ProvisioningDistributorUserBase):
    def setUp(self):
        self.image_str = 'some_string'
        super(TestOverlayModel, self).setUp()

    def test_create_overlay_without_image(self):
        type = 'TIME'
        position = 'TOP_LEFT'
        self.assertFalse(Overlay.query().fetch())
        Overlay.create(position, type)
        self.assertEqual(Overlay.query().fetch()[0].type, type)
        self.assertEqual(Overlay.query().fetch()[0].position, position)
        self.assertEqual(Overlay.query().fetch()[0].image_key, None)

    def test_create_overlay_with_image(self):
        type = 'TIME'
        position = 'TOP_LEFT'
        image_key = Image.create('some_str').key
        self.assertFalse(Overlay.query().fetch())
        Overlay.create(position, type, image=image_key)
        self.assertEqual(Overlay.query().fetch()[0].type, type)
        self.assertEqual(Overlay.query().fetch()[0].position, position)
        self.assertEqual(Overlay.query().fetch()[0].image_key, image_key)

    def test_create_device_overlay_association(self):
        type = 'TIME'
        position = 'TOP_LEFT'
        overlay = Overlay.create(position, type)
        association = DeviceOverlayAssociation.create_association(self.device_key, overlay.key)
        self.assertEqual(self.device, association.device_key.get())
        self.assertEqual(overlay, association.overlay_key.get())
