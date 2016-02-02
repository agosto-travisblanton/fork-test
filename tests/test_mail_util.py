import json
from datetime import datetime, timedelta

from agar.test import BaseTest
from env_setup import setup_test_paths
from utils.mail_util import MailUtil

setup_test_paths()

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestMailUtil(BaseTest):
    RECIPIENTS = ['bob.macneal@agosto.com']
    QUEUED_MESSAGE = 'Queued. Thank you.'
    MAIL_DOMAIN = 'skykit.com>'
    EMAIL_SUPPORT_FALSE = 'Email support is set to False.'

    def setUp(self):
        super(TestMailUtil, self).setUp()

    ##################################################################################################################
    ## Note: to run commented out tests, set the EMAIL_SUPPORT flag to True in appengine_config.py as follows:
    ##  def _EMAIL_SUPPORT():
    ##    if on_development_server or not on_server:
    ##      return True
    ##################################################################################################################
    def test_send_message_returns_no_message_sent(self):
        response = MailUtil.send_message(
            recipients=self.RECIPIENTS,
            subject='my subject',
            text='my message')
        self.assertEqual(self.EMAIL_SUPPORT_FALSE, response)

    # def test_send_get_recipient_log_entries_returns_expected_item(self):
    #     subject = 'Mysterious silence.'
    #     recipient = self.RECIPIENTS[0]
    #     entry_limit = 1
    #     MailUtil.send_message(
    #         recipients=self.RECIPIENTS,
    #         subject=subject,
    #         text='some text')
    #     begin_datetime = (datetime.utcnow() - timedelta(seconds=15)).strftime('%a, %d %b %Y %H:%M:%S -0000')
    #     log_response = MailUtil.get_recipient_log_entries(recipient,
    #                                                       entry_limit=entry_limit,
    #                                                       begin_datetime=begin_datetime)
    #     log_response_json = json.loads(log_response.content)
    #     self.assertGreaterEqual(len(log_response_json['items']), entry_limit)
    #     item = log_response_json['items'][0]
    #     self.assertEqual(subject, item['message']['headers']['subject'])
    #
    # def test_send_message_returns_response_message(self):
    #     response = MailUtil.send_message(
    #         recipients=self.RECIPIENTS,
    #         subject='my subject',
    #         text='my message')
    #     response_json = json.loads(response)
    #     self.assertEqual(self.QUEUED_MESSAGE, response_json['message'])
    #
    # def test_send_message_returns_response_message_id_with_expected_domain(self):
    #     response = MailUtil.send_message(
    #         recipients=self.RECIPIENTS,
    #         subject='my subject',
    #         text='my message')
    #     response_json = json.loads(response)
    #     id_returned = response_json['id']
    #     expected_mail_domain = id_returned.split('@')[1]
    #     self.assertEqual(self.MAIL_DOMAIN, expected_mail_domain)

