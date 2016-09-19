import json
from models import Image
from routes import application
from integrations.cloud_storage.cloud_storage_api import create_file

from provisioning_distributor_user_base_test import ProvisioningDistributorUserBase


class ImageHandlerTest(ProvisioningDistributorUserBase):
    def setUp(self):
        super(ImageHandlerTest, self).setUp()
        self.fileContent = open('testFile.png').read()
        self.fileName = "aFile.png"
        self.contentType = "image/png"

    def test_get(self):
        self._create_image()
        request_parameters = {}
        uri = application.router.build(None, 'manage-image', None, {'tenant_urlsafe_key': self.tenant_key.urlsafe()})
        response = self.app.get(uri, params=request_parameters)
        json_response = json.loads(response.body)
        self.assertEqual(json_response[0]["name"], self.fileName)

    def test_get_by_key(self):
        key = self._create_image()
        request_parameters = {}
        uri = application.router.build(None, 'get_image_by_key', None, {'image_urlsafe_key': key})
        response = self.app.get(uri, params=request_parameters)
        json_response = json.loads(response.body)
        self.assertEqual(json_response["name"], self.fileName)

    def test_post_image_creates_entry(self):
        self.assertFalse(Image.query().fetch())
        self._create_image()
        self.assertTrue(Image.query().fetch())

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
