import json
from models import Image, Overlay, OverlayTemplate
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

    def test_delete(self):
        key = self._create_image()
        overlay_type = "logo"
        Overlay.create_or_get(overlay_type, image_urlsafe_key=key)
        overlay_template = OverlayTemplate.get_overlay_template_for_device(self.device.key)
        overlay_template.set_overlay("top_left", overlay_type, image_urlsafe_key=key)
        request_parameters = {}
        uri = application.router.build(None, 'delete_image', None, {'image_urlsafe_key': key})
        response = self.app.delete(uri, params=request_parameters)
        self.assertOK(response)
        tasks = self.taskqueue_stub.GetTasks("default")
        self.assertEqual(len(tasks), 1)
        self.run_all_tasks()
        overlay_template_new = OverlayTemplate.get_overlay_template_for_device(self.device.key)
        none_overlay = Overlay.create_or_get(None)
        self.assertEqual(overlay_template_new.top_left.get(), none_overlay)

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
