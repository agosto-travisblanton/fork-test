from env_setup import setup_test_paths

setup_test_paths()

import webtest
from base_sql_test_config import SQLBaseTest
from proofplay.proofplay_models import Resource, ProgramRecord
from routes_proofplay import application
import json
from proofplay.dev.make_mock_data import make_one_days_worth_of_data
from utils.web_util import build_uri
import datetime


class TestMain(SQLBaseTest):
    def setUp(self):
        super(TestMain, self).setUp()
        self.app = webtest.TestApp(application)

    # def test_get_all_resources(self):
    #     new_resource = Resource(
    #             resource_name="test",
    #             resource_identifier="1234",
    #             tenant_code="gamestop"
    #     )
    #     self.db_session.add(new_resource)
    #     another_new_resource = Resource(
    #             resource_name="test2",
    #             resource_identifier="5678",
    #             tenant_code="gamestop"
    #
    #     )
    #     self.db_session.add(another_new_resource)
    #     self.db_session.commit()
    #
    #     uri = build_uri('RetrieveAllResources', module='proofplay', params_dict={'tenant': 'gamestop'})
    #     response = self.app.get(uri)
    #     self.assertEqual(500, response.status)

    def test_post_new_program_play(self):
        uri = build_uri('PostNewProgramPlay', module='proofplay')
        resp = self.app.post(uri, params=json.dumps(make_one_days_worth_of_data(10, datetime.datetime.now())))
        self.assertRunAndClearTasksInQueue(1, queue_names="default")
        self.assertTrue(self.db_session.query(ProgramRecord).first())
