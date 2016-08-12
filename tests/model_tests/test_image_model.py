from env_setup import setup_test_paths

setup_test_paths()

from tests.provisioning_distributor_user_base_test import ProvisioningDistributorUserBase
from models import Image


class TestImageModel(ProvisioningDistributorUserBase):
    def setUp(self):
        self.image_str = 'some_string'
        self.image_name = 'some_name'
        super(TestImageModel, self).setUp()

    def test_image_create(self):
        self.assertFalse(Image.query().fetch())
        self._create_image_entity()
        self.assertTrue(Image.query().fetch())

    def test_exists(self):
        self.assertFalse(Image.exists_within_tenant(self.tenant_key, self.image_name))
        self._create_image_entity()
        self.assertTrue(Image.exists_within_tenant(self.tenant_key, self.image_name))

    def _create_image_entity(self):
        Image.create(self.image_str, self.image_name, self.tenant_key)
