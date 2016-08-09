import json
from models import Image
from routes import application

from provisioning_distributor_user_base_test import ProvisioningDistributorUserBase


class ImageHandlerTest(ProvisioningDistributorUserBase):
    def setUp(self):
        super(ImageHandlerTest, self).setUp()
        self.svg_rep = '332lk23ljk23jkl243ljk423ljk423jkl423ljk234ljk23jkl243jkl234ljk23jkl234jkl'

    def test_get_by_key(self):
        key = self._create_image()
        request_parameters = {}
        uri = application.router.build(None, 'get_image_by_key', None, {'image_urlsafe_key': key})
        response = self.app.get(uri, params=request_parameters)
        json_response = json.loads(response.body)
        self.assertEqual(json_response["svg_rep"], self.svg_rep)

    def test_post_image_creates_entry(self):
        self.assertFalse(Image.query().fetch())
        self._create_image()
        self.assertTrue(Image.query().fetch())

    def _create_image(self):
        request_parameters = {'svg_rep': self.svg_rep, 'name': 'some_name'}
        uri = application.router.build(None, 'manage-image', None, {'tenant_urlsafe_key': self.tenant_key.urlsafe()})
        response = self.app.post_json(uri, params=request_parameters)
        json_response = json.loads(response.body)
        return json_response["key"]
