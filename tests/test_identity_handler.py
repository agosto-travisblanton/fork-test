import json
from provisioning_distributor_user_base_test import ProvisioningDistributorUserBase
from routes import application
from utils.auth_util import generate_token


class IdentityHandlerTest(ProvisioningDistributorUserBase):
    def setUp(self):
        super(IdentityHandlerTest, self).setUp()

    def test_valid_jwt_gives_you_access_to_identity_handler(self):
        uri = application.router.build(None, 'identity', None, {})

        res = self.app.get(
            uri,
            headers={"JWT": str(generate_token(self.user))},
        )

        json_res = json.loads(res.body)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(json_res["user"]["email"])
        self.assertTrue(json_res["valid"])

    def test_invalid_jwt_gives_you_a_message_saying_not_authenticated(self):
        uri = application.router.build(None, 'identity', None, {})

        res = self.app.get(
            uri,
            headers={"JWT": 'lkfsdljkfsdljkfsadljkfsdljksdflkfasd'}
        )
        json_res = json.loads(res.body)

        self.assertEqual(json_res["message"], "YOU ARE NOT AUTHENTICATED")
