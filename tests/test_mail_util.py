import json

from agar.test import BaseTest
from env_setup import setup_test_paths
from utils.mail_util import MailUtil

setup_test_paths()

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestMailUtil(BaseTest):
    RECIPIENTS = ['bob.macneal@agosto.com']
    QUEUED_MESSAGE = 'Queued. Thank you.'
    MAIL_DOMAIN = 'skykit.com>'

    def setUp(self):
        super(TestMailUtil, self).setUp()

    def test_send_message_returns_response_message(self):
        response = MailUtil.send_message(
            recipients=self.RECIPIENTS,
            subject='Mailgun Test',
            text='test message')
        response_json = json.loads(response)
        self.assertEqual(self.QUEUED_MESSAGE, response_json['message'])

    def test_send_message_returns_response_message_id_with_expected_domain(self):
        response = MailUtil.send_message(
            recipients=self.RECIPIENTS,
            subject='Mailgun Test',
            text='test message')
        response_json = json.loads(response)
        id_returned = response_json['id']
        expected_mail_domain = id_returned.split('@')[1]
        self.assertEqual(self.MAIL_DOMAIN, expected_mail_domain)
