import json
import logging

from datetime import datetime
from google.appengine.ext import ndb
from google.appengine.ext.deferred import deferred
from webapp2 import RequestHandler

from app_config import config
from content_manager_api import ContentManagerApi
from decorators import requires_api_token, requires_registration_token, requires_unmanaged_registration_token
from device_message_processor import post_unmanaged_device_info, change_intent
from model_entities.integration_events_log_model import IntegrationEventLog
from models import ChromeOsDevice, Tenant, Domain, TenantEntityGroup, DeviceIssueLog
from ndb_mixins import PagingListHandlerMixin, KeyValidatorMixin
from restler.serializers import json_response
from strategy import CHROME_OS_DEVICE_STRATEGY, DEVICE_PAIRING_CODE_STRATEGY, DEVICE_ISSUE_LOG_STRATEGY
from utils.email_notify import EmailNotify
from utils.timezone_util import TimezoneUtil
from workflow.refresh_device import refresh_device
from workflow.refresh_device_by_mac_address import refresh_device_by_mac_address
from workflow.register_device import register_device
from workflow.update_chrome_os_device import update_chrome_os_device

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class DirectoryApiHandler(RequestHandler):

    def get_device_by_parameter(self):
        device_mac_address = self.request.get('macAddress')
        if device_mac_address:
            pass
        self.response.set_status(200, 'OK')
