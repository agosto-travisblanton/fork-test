from ae_test_data import build
from agar.test import BaseTest
from models import User, Distributor
from tests.provisioning_base_test import MockStormpathResponse


class UserTest(BaseTest):
    def setUp(self):
        super(UserTest, self).setUp()
        self.user = build(User)

    def test_get_by_email(self):
        user = User.get_by_email(self.user.email)
        self.assertEqual(self.user, user)

    def test_get_by_unknown_email(self):
        user = User.get_by_email('mickey@mouse.com')
        self.assertIsNone(user)

    def test_update_or_create_with_api_account(self):
        account = MockStormpathResponse('donald.schrute@demo.agosto.com')

        user = User.get_by_email('donald.schrute@demo.agosto.com')
        self.assertIsNone(user)

        user = User.update_or_create_with_api_account(account)
        self.assertIsNotNone(user)

    def test_update_or_create_with_api_account_no_href(self):
        account = MockStormpathResponse('dwight.schrute@demo.agosto.com')
        account.href = None
        user = User.update_or_create_with_api_account(account)
        self.assertIsNone(user)

    def test_distributor_keys(self):
        user = build(User)
        distributor_keys = []
        for _ in range(3):
            dist = build(Distributor)
            distributor_keys.append(dist.key)
            user.add_distributor(dist.key)

        self.assertEqual(distributor_keys, user.distributor_keys)


    def test_distributors(self):
        user = build(User)
        distributors = []
        for _ in range(3):
            dist = build(Distributor)
            distributors.append(dist)
            user.add_distributor(dist.key)

        self.assertEqual(distributors, user.distributors)

    def test_add_distributor(self):
        user = build(User)
        distributors = []
        for _ in range(3):
            dist = build(Distributor)
            distributors.append(dist)
            user.add_distributor(dist.key)

        self.assertLess(3, user.distributors)
        self.assertEqual(distributors, user.distributors)



