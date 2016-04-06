import json

from agar.test import BaseTest
from env_setup import setup_test_paths
from mockito import when, any as any_matcher
from utils.mail_util import MailUtil

setup_test_paths()

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestMailUtil(BaseTest):
    RECIPIENTS = ['bob.macneal@agosto.com']
    QUEUED_MESSAGE = 'Queued. Thank you.'
    MAIL_DOMAIN = 'skykit.com>'
    MAIL_SERVER_RESPONSE_JSON = {u'message': u'Queued. Thank you.',
                                 u'id': u'<20160406193009.35436.13795.B6ACD847@skykit.com>'}

    def setUp(self):
        super(TestMailUtil, self).setUp()

    def test_send_message_returns_response_message(self):
        # when(MailUtil).send_message(recipients=any_matcher(self.RECIPIENTS),
        #                             subject=any_matcher(str),
        #                             text=any_matcher(str),
        #                             html=any_matcher(str)).thenReturn(None)
        # when(json).loads(any_matcher()).thenReturn(self.MAIL_SERVER_RESPONSE_JSON)
        response = MailUtil.send_message(
            recipients=self.RECIPIENTS,
            subject='Mailgun Test',
            text='test message',
            html='test message')
        response_json = json.loads(response)
        self.assertEqual(self.QUEUED_MESSAGE, response_json['message'])

    def test_send_message_returns_response_message_id_with_expected_domain(self):
        # when(MailUtil).send_message(recipients=any_matcher(self.RECIPIENTS),
        #                             subject=any_matcher(str),
        #                             text=any_matcher(str),
        #                             html=any_matcher(str)).thenReturn(None)
        # when(json).loads(any_matcher()).thenReturn(self.MAIL_SERVER_RESPONSE_JSON)
        response = MailUtil.send_message(
            recipients=self.RECIPIENTS,
            subject='Mailgun Test',
            text='test message',
            html='test message')
        response_json = json.loads(response)
        id_returned = response_json['id']
        expected_mail_domain = id_returned.split('@')[1]
        self.assertEqual(self.MAIL_DOMAIN, expected_mail_domain)
