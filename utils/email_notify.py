import json
import logging

from app_config import config
from models import Tenant
from utils.mail_util import MailUtil

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class EmailNotify(object):
    subject = None
    tenant_name = None
    serial_number = None
    body = None
    close = None

    def device_enrolled(self, tenant_code, tenant_name, device_mac_address, timestamp):
        tenant_notification_emails = Tenant.find_by_tenant_code(tenant_code).notification_emails
        if tenant_notification_emails is not None and len(tenant_notification_emails) > 0:
            self.subject = 'Skykit Device Enrolled for {0}'.format(tenant_name)
            self.tenant_name = 'Tenant: {0}'.format(tenant_name)
            self.body = 'This email is to notify you that a device was enrolled on {0} UTC from MAC address {1}.'.format(
                timestamp, device_mac_address)
            self.close = 'If you have access to Skykit Provisioning, you can log into your account to obtain ' \
                         'additional details.  Or, you can contact your Skykit managed partner.'
            response = MailUtil.send_message(
                recipients=tenant_notification_emails,
                subject=self.subject,
                text='{0}\n\n{1}\n\n{2}\n\nThank you.'.format(self.tenant_name, self.body, self.close),
                html='{0}<br/><br/>{1}<br/><br/>{2}<br/><br/>Thank you.'.format(self.tenant_name, self.body, self.close))
            response_json = json.loads(response)
            if str(response_json['message']) != config.MAIL_SERVER_QUEUED_RESPONSE_MESSAGE:
                logging.warning('Device enroll email with MAC address {0} and tenant {1} was not queued on mail server.'
                                .format(device_mac_address, tenant_name))

    def device_down(self, tenant_code, tenant_name, device_serial_number, timestamp):
        tenant_notification_emails = Tenant.find_by_tenant_code(tenant_code).notification_emails
        if tenant_notification_emails is not None and len(tenant_notification_emails) > 0:
            self.subject = 'Skykit Device Down Alert - {0}'.format(device_serial_number)
            self.tenant_name = 'Tenant: {0}'.format(tenant_name)
            self.serial_number = 'Device Serial Number: {0}'.format(device_serial_number)
            self.body = 'This email is to notify you that the Skykit device with the above serial number is ' \
                        'not communicating with Skykit. The last communication was received from this device ' \
                        'at {0} UTC. Skykit devices can run without an internet connection, so this device may still ' \
                        'be displaying content. The device may not be communicating with Skykit''s cloud service ' \
                        'because the player has been powered down, has lost its internet connection, or is ' \
                        'misconfigured.'.format(timestamp)
            self.close = 'If you have access to Skykit Provisioning, you can log into your account to obtain ' \
                         'additional details.  Or, you can contact your Skykit managed partner.'
            response = MailUtil.send_message(
                recipients=tenant_notification_emails,
                subject=self.subject,
                text='{0}\n{1}\n\n{2}\n\n{3}\n\nThank you.'.format(self.tenant_name, self.serial_number, self.body,
                                                                   self.close),
                html='{0}<br/>{1}<br/><br/>{2}<br/><br/>{3}<br/><br/>Thank you.'.format(self.tenant_name,
                                                                                        self.serial_number,
                                                                                        self.body,
                                                                                        self.close)
            )
            response_json = json.loads(response)
            if str(response_json['message']) != config.MAIL_SERVER_QUEUED_RESPONSE_MESSAGE:
                logging.warning('Device down email for {0} was not queued on mail server.'.format(self.serial_number))

    def device_up(self, tenant_code, tenant_name, device_serial_number):
        tenant_notification_emails = Tenant.find_by_tenant_code(tenant_code).notification_emails
        if tenant_notification_emails is not None and len(tenant_notification_emails) > 0:
            self.subject = 'Skykit Device Up Alert - {0}'.format(device_serial_number)
            self.tenant_name = 'Tenant: {0}'.format(tenant_name)
            self.serial_number = 'Device Serial Number: {0}'.format(device_serial_number)
            self.body = 'This email is to notify you that the Skykit device with the above serial number is active again. ' \
                        'We are now receiving monitoring information from the device.'
            self.close = 'If you have access to Skykit Provisioning, you can log into your account to obtain additional ' \
                         'details. Or, you can contact us at contact us at support@skykit.com.'
            response = MailUtil.send_message(
                recipients=tenant_notification_emails,
                subject=self.subject,
                text='{0}\n{1}\n\n{2}\n\n{3}\n\nThank you.'.format(self.tenant_name, self.serial_number, self.body,
                                                                   self.close),
                html='{0}<br/>{1}<br/><br/>{2}<br/><br/>{3}<br/><br/>Thank you.'.format(self.tenant_name,
                                                                                        self.serial_number,
                                                                                        self.body,
                                                                                        self.close)
            )
            response_json = json.loads(response)
            if str(response_json['message']) != config.MAIL_SERVER_QUEUED_RESPONSE_MESSAGE:
                logging.warning('Device up email for {0} was not queued on mail server.'.format(device_serial_number))
