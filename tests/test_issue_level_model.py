from env_setup import setup_test_paths

setup_test_paths()

from agar.test import BaseTest
from models import IssueLevel

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestIssueLevelModel(BaseTest):

    def setUp(self):
        super(TestIssueLevelModel, self).setUp()

    def test_issue_level_stringify_returns_expected_descriptors(self):
        self.assertEqual('normal', IssueLevel.stringify(IssueLevel.Normal))
        self.assertEqual('warning', IssueLevel.stringify(IssueLevel.Warning))
        self.assertEqual('danger', IssueLevel.stringify(IssueLevel.Danger))

    def test_issue_level_stringify_on_unsupported_enumeration_returns_none(self):
        self.assertIsNone(IssueLevel.stringify(100))

    def test_issue_level_returns_expected_integers(self):
        self.assertEqual(0, IssueLevel.Normal)
        self.assertEqual(1, IssueLevel.Warning)
        self.assertEqual(2, IssueLevel.Danger)

