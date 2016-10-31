from app_config import config
from models import ChromeOsDevice
from routes import application
from provisioning_distributor_user_base_test import ProvisioningDistributorUserBase
import json
from webtest import AppError

class ContentManagerHandlerTest(ProvisioningDistributorUserBase):
    def setUp(self):
        super(ContentManagerHandlerTest, self).setUp()

    def test_update_name(self):
        uri = application.router.build(None, 'update-content-manager', None,
                                       {'device_urlsafe_key': self.device.key.urlsafe()})
        headers = {"Authorization": config.API_TOKEN}
        request_parameters = {
            "name": "SO_NEW_NAME"
        }
        response = self.app.put(uri, json.dumps(request_parameters), headers=headers)
        self.assertOK(response)
        device = ChromeOsDevice.get_by_device_id(self.device.device_id)
        self.assertEqual(device.content_manager_display_name, request_parameters["name"])

    def test_update_name_with_bad_credentials_fails(self):
        uri = application.router.build(None, 'update-content-manager', None,
                                       {'device_urlsafe_key': self.device.key.urlsafe()})
        headers = {"Authorization": 'blah'}
        request_parameters = {
            "name": "SO_NEW_NAME"
        }
        with self.assertRaises(AppError) as context:
            response = self.app.put(uri, json.dumps(request_parameters), headers=headers)
            self.assertEqual(response.status_int, 403)