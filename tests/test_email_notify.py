import json

from datetime import datetime

from agar.test import BaseTest
from env_setup import setup_test_paths
# from mockito import when, any as any_matcher
from models import Distributor, Domain, Tenant
from utils.email_notify import EmailNotify
# from utils.mail_util import MailUtil

setup_test_paths()

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TestEmailNotify(BaseTest):
    CHROME_DEVICE_DOMAIN = 'skykit.agosto.com'
    DISTRIBUTOR_NAME = 'Agosto'
    IMPERSONATION_EMAIL = 'skykit.api@skykit.agosto.com'
    RECIPIENTS = ['bob.macneal@agosto.com']
    TENANT_NAME = 'Acme, Inc.'
    TENANT_CODE = 'acme_inc'
    MAC_ADDRESS = '54271ed9c4c9'
    SERIAL_NUMBER = 'F9MSCX006666'
    MAIL_SERVER_RESPONSE_JSON = {u'message': u'Queued. Thank you.'}

    def setUp(self):
        super(TestEmailNotify, self).setUp()
        self.distributor = Distributor.create(name=self.DISTRIBUTOR_NAME,
                                              content_manager_url=None,
                                              player_content_url=None,
                                              active=True)
        self.distributor_key = self.distributor.put()
        self.domain = Domain.create(name=self.CHROME_DEVICE_DOMAIN,
                                    distributor_key=self.distributor_key,
                                    impersonation_admin_email_address=self.IMPERSONATION_EMAIL,
                                    active=True)
        self.domain_key = self.domain.put()
        self.tenant = Tenant.create(tenant_code=self.TENANT_CODE,
                                    name=self.TENANT_NAME,
                                    admin_email='bob@skykit.com',
                                    content_server_url='https://skykit-contentmanager.appspot.com/content',
                                    content_manager_base_url='https://skykit-contentmanager.appspot.com',
                                    domain_key=self.domain_key,
                                    active=True)
        self.tenant.notification_emails = self.RECIPIENTS
        self.tenant.put()

    ##################################################################################################################
    # device_down
    ##################################################################################################################

    def test_email_notify_device_down_has_expected_body(self):
        # when(MailUtil).send_message(any_matcher(str),
        #                             any_matcher(str),
        #                             any_matcher(str),
        #                             any_matcher(str)).thenReturn(None)
        # when(json).loads(any_matcher()).thenReturn(self.MAIL_SERVER_RESPONSE_JSON)
        now = datetime.utcnow()
        notifier = EmailNotify()
        notifier.device_down(tenant_code=self.TENANT_CODE,
                             tenant_name=self.TENANT_NAME,
                             device_serial_number=self.SERIAL_NUMBER,
                             timestamp=now)
        expected_body = 'This email is to notify you that the Skykit device with the above serial number is ' \
                        'not communicating with Skykit. The last communication was received from this device ' \
                        'at {0} UTC. Skykit devices can run without an internet connection, so this device may still ' \
                        'be displaying content. The device may not be communicating with Skykit''s cloud service ' \
                        'because the player has been powered down, has lost its internet connection, or is ' \
                        'misconfigured.'.format(now)
        self.assertEqual(notifier.body, expected_body)

    def test_email_notify_device_down_has_expected_subject(self):
        # when(MailUtil).send_message(any_matcher(str),
        #                             any_matcher(str),
        #                             any_matcher(str),
        #                             any_matcher(str)).thenReturn(None)
        # when(json).loads(any_matcher()).thenReturn(self.MAIL_SERVER_RESPONSE_JSON)
        notifier = EmailNotify()
        notifier.device_down(tenant_code=self.TENANT_CODE,
                             tenant_name=self.TENANT_NAME,
                             device_serial_number=self.SERIAL_NUMBER,
                             timestamp=datetime.utcnow())
        expected_subject = 'Skykit Device Down Alert - {0}'.format(self.SERIAL_NUMBER)
        self.assertEqual(notifier.subject, expected_subject)

    def test_email_notify_device_down_has_expected_tenant_name(self):
        # when(MailUtil).send_message(recipients=any_matcher(self.RECIPIENTS),
        #                             subject=any_matcher(),
        #                             text=any_matcher()).thenReturn(None)
        # when(json).loads(any_matcher()).thenReturn(self.MAIL_SERVER_RESPONSE_JSON)
        notifier = EmailNotify()
        notifier.device_down(tenant_code=self.TENANT_CODE,
                             tenant_name=self.TENANT_NAME,
                             device_serial_number=self.SERIAL_NUMBER,
                             timestamp=datetime.utcnow())
        expected_tenant = 'Tenant: {0}'.format(self.TENANT_NAME)
        self.assertEqual(notifier.tenant_name, expected_tenant)

    def test_email_notify_device_down_has_expected_serial_number(self):
        # when(MailUtil).send_message(any_matcher(str),
        #                             any_matcher(str),
        #                             any_matcher(str),
        #                             any_matcher(str)).thenReturn(None)
        # when(json).loads(any_matcher()).thenReturn(self.MAIL_SERVER_RESPONSE_JSON)
        notifier = EmailNotify()
        notifier.device_down(tenant_code=self.TENANT_CODE,
                             tenant_name=self.TENANT_NAME,
                             device_serial_number=self.SERIAL_NUMBER,
                             timestamp=datetime.utcnow())
        expected_serial = 'Device Serial Number: {0}'.format(self.SERIAL_NUMBER)
        self.assertEqual(notifier.serial_number, expected_serial)

    ##################################################################################################################
    # device_up
    ##################################################################################################################

    def test_email_notify_device_up_has_expected_body(self):
        # when(MailUtil).send_message(any_matcher(str),
        #                             any_matcher(str),
        #                             any_matcher(str),
        #                             any_matcher(str)).thenReturn(None)
        # when(json).loads(any_matcher()).thenReturn(self.MAIL_SERVER_RESPONSE_JSON)
        notifier = EmailNotify()
        notifier.device_up(tenant_code=self.TENANT_CODE,
                           tenant_name=self.TENANT_NAME,
                           device_serial_number=self.SERIAL_NUMBER)
        expected_body = 'This email is to notify you that the Skykit device with the above serial number is active ' \
                        'again. We are now receiving monitoring information from the device.'
        self.assertEqual(notifier.body, expected_body)

    def test_email_notify_device_up_has_expected_subject(self):
        # when(MailUtil).send_message(any_matcher(str),
        #                             any_matcher(str),
        #                             any_matcher(str),
        #                             any_matcher(str)).thenReturn(None)
        # when(json).loads(any_matcher()).thenReturn(self.MAIL_SERVER_RESPONSE_JSON)
        notifier = EmailNotify()
        notifier.device_up(tenant_code=self.TENANT_CODE,
                           tenant_name=self.TENANT_NAME,
                           device_serial_number=self.SERIAL_NUMBER)
        expected_subject = 'Skykit Device Up Alert - {0}'.format(self.SERIAL_NUMBER)
        self.assertEqual(notifier.subject, expected_subject)

    def test_email_notify_device_up_has_expected_tenant_name(self):
        # when(MailUtil).send_message(any_matcher(str),
        #                             any_matcher(str),
        #                             any_matcher(str),
        #                             any_matcher(str)).thenReturn(None)
        # when(json).loads(any_matcher()).thenReturn(self.MAIL_SERVER_RESPONSE_JSON)
        notifier = EmailNotify()
        notifier.device_up(tenant_code=self.TENANT_CODE,
                           tenant_name=self.TENANT_NAME,
                           device_serial_number=self.SERIAL_NUMBER)
        expected_tenant = 'Tenant: {0}'.format(self.TENANT_NAME)
        self.assertEqual(notifier.tenant_name, expected_tenant)

    def test_email_notify_device_up_has_expected_serial_number(self):
        # when(MailUtil).send_message(any_matcher(str),
        #                             any_matcher(str),
        #                             any_matcher(str),
        #                             any_matcher(str)).thenReturn(None)
        # when(json).loads(any_matcher()).thenReturn(self.MAIL_SERVER_RESPONSE_JSON)
        notifier = EmailNotify()
        notifier.device_up(tenant_code=self.TENANT_CODE,
                           tenant_name=self.TENANT_NAME,
                           device_serial_number=self.SERIAL_NUMBER)
        expected_serial = 'Device Serial Number: {0}'.format(self.SERIAL_NUMBER)
        self.assertEqual(notifier.serial_number, expected_serial)

    ##################################################################################################################
    # device_enrolled
    ##################################################################################################################
    # def test_email_notify_device_enrolled_has_expected_body(self):
    #     # when(MailUtil).send_message(any_matcher(str),
    #     #                             any_matcher(str),
    #     #                             any_matcher(str),
    #     #                             any_matcher(str)).thenReturn(None)
    #     # when(json).loads(any_matcher()).thenReturn(self.MAIL_SERVER_RESPONSE_JSON)
    #     now = datetime.utcnow()
    #     notifier = EmailNotify()
    #     notifier.device_enrolled(tenant_code=self.TENANT_CODE,
    #                              tenant_name=self.TENANT_NAME,
    #                              device_mac_address=self.MAC_ADDRESS,
    #                              timestamp=now)
    #     expected_body = 'This email is to notify you that a device was enrolled on {0} UTC from MAC address {1}.'\
    #         .format(now, self.MAC_ADDRESS)
    #     self.assertEqual(notifier.body, expected_body)
    #
    # def test_email_notify_device_enrolled_has_expected_subject(self):
    #     # when(MailUtil).send_message(any_matcher(str),
    #     #                             any_matcher(str),
    #     #                             any_matcher(str),
    #     #                             any_matcher(str)).thenReturn(None)
    #     # when(json).loads(any_matcher()).thenReturn(self.MAIL_SERVER_RESPONSE_JSON)
    #     notifier = EmailNotify()
    #     notifier.device_enrolled(tenant_code=self.TENANT_CODE,
    #                              tenant_name=self.TENANT_NAME,
    #                              device_mac_address=self.MAC_ADDRESS,
    #                              timestamp=datetime.utcnow())
    #     expected_subject = 'Skykit Device Enrolled for {0}'.format(self.TENANT_NAME)
    #     self.assertEqual(notifier.subject, expected_subject)
