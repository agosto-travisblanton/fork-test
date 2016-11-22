import json
from webtest import AppError

import mock
from models import User
from provisioning_distributor_user_base_test import ProvisioningDistributorUserBase
from routes import application
import httplib

class LoginHandlerTest(ProvisioningDistributorUserBase):
    some_user = {
        "email": "one@gmail.com",
        "name": "Sam Smith"
    }

    def setUp(self):
        super(LoginHandlerTest, self).setUp()

    @mock.patch('handlers.login_handler.verify_google_token')
    def test_issues_new_jwt_after_valid_google_token(self, verify_google_token):
        verify_google_token.return_value = self.some_user
        self.assertTrue(User.query(User.email == self.some_user["email"]).fetch() == [])

        uri = application.router.build(None, 'login', None, {})

        res = self.app.get(
            uri,
            headers={"oAuth": '2342342334fddadf'},
        )

        self.assertEqual(res.status_code, 200)
        self.assertTrue(json.loads(res.body.decode("utf-8"))["token"])
        user_entity = User.query(User.email == self.some_user["email"]).fetch()[0]
        self.assertEqual(user_entity.email, self.some_user["email"])

    @mock.patch('handlers.login_handler.verify_google_token')
    def test_returns_forbidden_when_invalid_google_token(self, verify_google_token):
        verify_google_token.return_value = None
        self.assertTrue(User.query(User.email == self.some_user["email"]).fetch() == [])

        uri = application.router.build(None, 'login', None, {})

        with self.assertRaises(AppError) as context:
            res = self.app.get(
                uri,
                headers={"oAuth": '2342342334fddadf'}
            )

            self.assertEqual(res.status_code, httplib.FORBIDDEN)
