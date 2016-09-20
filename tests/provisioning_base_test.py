from ae_test_data import build

from env_setup import setup_test_paths, setup

setup_test_paths()
setup()

import json
import stormpath_api
from agar.test import BaseTest, WebTest
from ndb_mixins import KeyValidatorMixin
from routes import application
from utils.web_util import build_uri
from models import (
    Distributor,
    User,
)
import unittest
from google.appengine.ext import testbed
from google.appengine.ext import deferred

from appengine_config import basedir


class MockStormpathResponse:
    def __init__(self, email):
        self.email = email
        self.href = 'https://fake.stormpath.com/{}'.format(email)


class TaskQueueTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_app_identity_stub()
        self.testbed.init_app_identity_stub()
        self.testbed.init_urlfetch_stub()
        self.testbed.init_blobstore_stub()

        self.testbed.init_taskqueue_stub(
            root_path=basedir)
        self.taskqueue_stub = self.testbed.get_stub(
            testbed.TASKQUEUE_SERVICE_NAME)

    def tearDown(self):
        self.testbed.deactivate()

    def run_all_tasks(self):
        for task in self.taskqueue_stub.get_filtered_tasks():
            deferred.run(task.payload)


class ProvisioningBaseTest(TaskQueueTestCase, BaseTest, WebTest, KeyValidatorMixin):
    APPLICATION = application

    def setUp(self):
        super(ProvisioningBaseTest, self).setUp()

    def tearDown(self):
        super(ProvisioningBaseTest, self).tearDown()

    def create_distributor_if_unique(self, distributor_name):
        distributor_is_unique = Distributor.is_unique(distributor_name)

        if distributor_is_unique:
            distributor = Distributor.create(name=distributor_name)
            distributor.put()
        else:
            distributor = Distributor.find_by_name(name=distributor_name)

        return distributor

    def create_user(self, email, distributor_name="a distributor"):
        distributor = self.create_distributor_if_unique(distributor_name)

        user = User.update_or_create_with_api_account(MockStormpathResponse(email))
        user.add_distributor(distributor.key)
        user.put()
        return user

    def create_platform_admin(self, email, distributor_name):
        distributor = self.create_distributor_if_unique(distributor_name)

        user = User.update_or_create_with_api_account(MockStormpathResponse(email))
        user.is_administrator = True
        user.add_distributor(distributor.key)
        user.put()
        return user

    def create_distributor_admin(self, email, distributor_name):
        distributor = self.create_distributor_if_unique(distributor_name)

        user = User.update_or_create_with_api_account(MockStormpathResponse(email))
        user.add_distributor(distributor.key, role=1)
        user.put()
        return user

    def create_user_of_distributor(self, user, distributor, role=0):
        user.add_distributor(distributor.key, role=role)

    def login(self, email, administrator=False):

        identity_url = build_uri('identity')
        response = self.get(identity_url)
        self.assertOK(response)

        body = json.loads(response.body)
        state = body.get('STATE')
        params = {
            'state': state,
            'administrator': administrator
        }

        user = User.update_or_create_with_api_account(MockStormpathResponse(email))

        from mock import patch
        with patch.object(stormpath_api, 'google_login', return_value=user):
            resp = self.app.post_json(build_uri('login'), params)
        self.assertTrue("Successful Login" in resp)
