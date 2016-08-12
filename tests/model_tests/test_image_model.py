from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
from models import Image


class TestImageModel(BaseTest):
    def setUp(self):
        self.image_str = 'some_string'
        super(TestImageModel, self).setUp()

    def test_image_create(self):
        self.assertFalse(Image.query().fetch())
        self._create_image_entity()
        self.assertTrue(Image.query().fetch())

    def test_exists(self):
        self.assertFalse(Image.exists(self.image_str))
        self._create_image_entity()
        self.assertTrue(Image.exists(self.image_str))

    def _create_image_entity(self):
        Image.create(self.image_str)
