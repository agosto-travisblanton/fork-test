import json
import logging

from app_config import config
from models import Tenant
from utils.mail_util import MailUtil

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class EmailNotify(object):
    @staticmethod
    def device_enrolled(tenant_code, device_mac_address):
        tenant_notification_emails = Tenant.find_by_tenant_code(tenant_code).notification_emails
        if tenant_notification_emails is not None and len(tenant_notification_emails) > 0:
            response = MailUtil.send_message(
                recipients=tenant_notification_emails,
                subject='Device Added',
                text='A new device was added with MAC address {0}.'.format(device_mac_address))
            response_json = json.loads(response)
            if response_json['message'] is not config.MAIL_SERVER_QUEUED_RESPONSE_MESSAGE:
                logging.warning('Tenant notification email for device add was not queued.')

    @staticmethod
    def device_down(tenant_code, tenant_name, device_serial_number):
        tenant_notification_emails = Tenant.find_by_tenant_code(tenant_code).notification_emails
        if tenant_notification_emails is not None and len(tenant_notification_emails) > 0:
            subject = 'Skykit Device Up Alert - {0}'.format(device_serial_number)
            tenant = 'Tenant: {0}'.format(tenant_name)
            serial_number = 'Device Serial Number: {0}.'.format(device_serial_number)
            body = 'This email is to notify you that the Skykit device with the above serial number is active again. ' \
                   'We are now receiving monitoring information from the device.'
            close = 'If you have access to Skykit Provisioning, you can log into your account to obtain additional ' \
                    'details. Or, you can contact us at contact us at support@skykit.com.'
            response = MailUtil.send_message(
                recipients=tenant_notification_emails,
                subject=subject,
                text='{0}\n{1}\n\n{2}\n\n{3}\n\nThank you.'.format(tenant, serial_number, body, close),
                html='{0}<br/>{1}<br/><br/>{2}<br/><br/>{3}<br/><br/>Thank you.'.format(tenant,
                                                                                        serial_number,
                                                                                        body,
                                                                                        close)
            )
            response_json = json.loads(response)
            if response_json['message'] is not config.MAIL_SERVER_QUEUED_RESPONSE_MESSAGE:
                logging.warning('Device up email for {0} was not queued on mail server.'.format(device_serial_number))

    @staticmethod
    def device_up(tenant_code, tenant_name, device_serial_number):
        tenant_notification_emails = Tenant.find_by_tenant_code(tenant_code).notification_emails
        if tenant_notification_emails is not None and len(tenant_notification_emails) > 0:
            subject = 'Skykit Device Up Alert - {0}'.format(device_serial_number)
            tenant = 'Tenant: {0}'.format(tenant_name)
            serial_number = 'Device Serial Number: {0}.'.format(device_serial_number)
            body = 'This email is to notify you that the Skykit device with the above serial number is active again. ' \
                   'We are now receiving monitoring information from the device.'
            close = 'If you have access to Skykit Provisioning, you can log into your account to obtain additional ' \
                    'details. Or, you can contact us at contact us at support@skykit.com.'
            response = MailUtil.send_message(
                recipients=tenant_notification_emails,
                subject=subject,
                text='{0}\n{1}\n\n{2}\n\n{3}\n\nThank you.'.format(tenant, serial_number, body, close),
                html='{0}<br/>{1}<br/><br/>{2}<br/><br/>{3}<br/><br/>Thank you.'.format(tenant,
                                                                                        serial_number,
                                                                                        body,
                                                                                        close)
            )
            response_json = json.loads(response)
            if response_json['message'] is not config.MAIL_SERVER_QUEUED_RESPONSE_MESSAGE:
                logging.warning('Device up email for {0} was not queued on mail server.'.format(device_serial_number))
