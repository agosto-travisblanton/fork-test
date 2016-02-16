from env_setup import setup_test_paths

setup_test_paths()
import webtest
from base_sql_test_config import SQLBaseTest
import webapp2
from proofplay.models import Resource, ProgramRecord
from routes_proofplay import application
import json
from proofplay.dev.make_mock_data import get_one_to_send
import base64
import pickle
from google.appengine.ext import deferred
from utils.web_util import build_uri


def submit_deferred(taskq):
    tasks = taskq.GetTasks("default")
    taskq.FlushQueue("default")
    while tasks:
        for task in tasks:
            (func, args, opts) = pickle.loads(base64.b64decode(task["body"]))
            func(*args)
        tasks = taskq.GetTasks("default")
        taskq.FlushQueue("default")


class TestMain(SQLBaseTest):
    def setUp(self):
        super(TestMain, self).setUp()
        self.app = webtest.TestApp(application)

    def test_get_all_resources(self):
        new_resource = Resource(
                resource_name="test",
                resource_identifier="1234"
        )
        self.db_session.add(new_resource)
        another_new_resource = Resource(
                resource_name="test2",
                resource_identifier="5678"
        )
        self.db_session.add(another_new_resource)
        self.db_session.commit()

        uri = build_uri('RetrieveAllResources', module='proofplay')
        response = self.app.get(uri)
        self.assertEqual({u"resources": [u"test", u"test2"]}, response.json)

    def test_post_new_program_play(self):
        uri = build_uri('PostNewProgramPlay', module='proofplay')
        resp = self.app.post(uri, params=json.dumps(get_one_to_send()))
        self.assertRunAndClearTasksInQueue(1, queue_names="default")
        self.assertTrue(self.db_session.query(ProgramRecord).first())