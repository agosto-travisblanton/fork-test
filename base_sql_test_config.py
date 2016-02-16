from env_setup import setup_test_paths

setup_test_paths()

import unittest
from proofplay.proofplay_models import Base
from proofplay.db import Session
from sqlalchemy import create_engine
from agar.test import BaseTest

engine = create_engine('sqlite:///:memory:')


class SQLBaseTest(BaseTest):
    def setUp(self):
        super(SQLBaseTest, self).setUp()
        engine = create_engine('sqlite:///:memory:')
        Session.configure(bind=engine)
        Base.metadata.create_all(engine)
        self.db_session = Session()

    def teardown(self):
        Session.remove()
        Base.metadata.drop_all(bind=engine)

#
# from env_setup import setup_test_paths
#
# setup_test_paths()
#
# from proofplay.proofplay_models import Base
# from proofplay.db import Session
# from sqlalchemy import create_engine
# from agar.test import BaseTest
#
#
# class SQLBaseTest(BaseTest):
#     def setUp(self):
#         super(SQLBaseTest, self).setUp()
#         engine = create_engine('sqlite:///:memory:')
#         Session.configure(bind=engine)
#         self.db_session = Session()
#         Base.metadata.create_all(engine)
#
#     def tearDown(self):
#         Session.remove()
#         Base.metadata.drop_all(self.engine)
