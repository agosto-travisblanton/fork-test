__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'

from env_setup import setup_test_paths;

setup_test_paths()

from agar.test import BaseTest
from content_manager_api import ContentManagerApi


class TestContentManagerApi(BaseTest):
    ADMIN_ACCOUNT_TO_IMPERSONATE = 'administrator@skykit.com'


def setUp(self):
    super(TestContentManagerApi, self).setUp()
    self.content_manager_api = ContentManagerApi(self.ADMIN_ACCOUNT_TO_IMPERSONATE)


def test_create_tenant(self):
    pass
