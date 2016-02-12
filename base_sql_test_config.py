from env_setup import setup_test_paths

setup_test_paths()

import unittest
from proofplay.models import Base
from proofplay.db import Session
from sqlalchemy import create_engine
from agar.test import BaseTest

engine = create_engine('sqlite:///:memory:')


def setup():
    engine = create_engine('sqlite:///:memory:')
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)


class SQLBaseTest(BaseTest):
    def setUp(self):
        super(SQLBaseTest, self).setUp()

        setup()
        self.db_session = Session()

    def teardown(self):
        Session.remove()
        Base.metadata.drop_all(bind=engine)
