import json
import logging

from google.appengine.ext import ndb
from google.appengine.ext.deferred import deferred
from webapp2 import RequestHandler

from app_config import config
from chrome_os_devices_api import (refresh_device, refresh_device_by_mac_address, update_chrome_os_device)
from content_manager_api import ContentManagerApi
from decorators import requires_api_token, requires_registration_token, requires_unmanaged_registration_token
from device_message_processor import post_unmanaged_device_info, change_intent
from models import ChromeOsDevice, Tenant, Domain, TenantEntityGroup, DeviceHeartbeat
from ndb_mixins import PagingListHandlerMixin, KeyValidatorMixin
from restler.serializers import json_response
from strategy import CHROME_OS_DEVICE_STRATEGY, DEVICE_PAIRING_CODE_STRATEGY

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class DeviceHeartbeatHandler(RequestHandler, PagingListHandlerMixin, KeyValidatorMixin):

    @requires_api_token
    def put(self, heartbeat_device_urlsafe_key):
        status = 204
        message = None
        heartbeat = DeviceHeartbeat.find_by_device_key(heartbeat_device_urlsafe_key)
        if heartbeat is None:
            status = 404
            message = 'Unrecognized heartbeat device_key: {0}'.format(heartbeat_device_urlsafe_key)
        else:
            request_json = json.loads(self.request.body)
            disk_utilization = request_json.get('diskUtilization')
            if disk_utilization:
                heartbeat.disk_utilization = disk_utilization
            memory_utilization = request_json.get('memoryUtilization')
            if memory_utilization:
                heartbeat.memory_utilization = memory_utilization
            program = request_json.get('program')
            if program:
                heartbeat.currently_playing = program
            heartbeat.put()
            self.response.headers.pop('Content-Type', None)
        self.response.set_status(status, message)

