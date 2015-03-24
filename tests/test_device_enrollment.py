from agar.test import BaseTest, WebTest
from routes import application


class TestDeviceEnrollmentHandler(BaseTest, WebTest):
    APPLICATION = application

    def setUp(self):
        super(TestDeviceEnrollmentHandler, self).setUp()
        self.mac_address = '00:0a:95:9d:68:16'
        self.uri = application.router.build(None, 'device-enrollment', None, {})
        # self.user = build(User, email=self.email, password=self.password)
        # self.user.put()

    def test_enroll(self):
        resp = self.app.get(self.uri, params={'mac_address': self.mac_address})
        self.assertOK(resp)

