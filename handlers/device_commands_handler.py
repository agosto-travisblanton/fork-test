import json
import logging

from google.appengine.ext import ndb
from webapp2 import RequestHandler

from app_config import config
from decorators import requires_api_token
from device_message_processor import change_intent
from models import ChromeOsDevice
from ndb_mixins import KeyValidatorMixin

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>. Bob MacNeal <bob.macneal@agosto.com>'


class DeviceCommandsHandler(RequestHandler, KeyValidatorMixin):

    @requires_api_token
    def post(self, device_urlsafe_key):
        status = 200
        message = None
        request_json = json.loads(self.request.body)
        intent = request_json.get('intent')
        if intent is None or intent == '':
            status = 400
            message = 'DeviceCommandsHandler: Invalid intent.'
        else:
            chrome_os_device = None
            try:
                chrome_os_device = self.validate_and_get(device_urlsafe_key, ChromeOsDevice, abort_on_not_found=True)
            except Exception, e:
                logging.exception(e)
                logging.error("Exception info: device_urlsafe_key = {0}, intent = {1}".format(
                    device_urlsafe_key, intent))
            if None is chrome_os_device:
                status = 404
                message = 'DeviceCommandsHandler: Device not found with key: {0}'.format(device_urlsafe_key)
                logging.info(message)
            else:
                change_intent(chrome_os_device.gcm_registration_id, intent)
        self.response.set_status(status, message)

    @requires_api_token
    def reset(self, device_urlsafe_key):
        status = 200
        message = None
        chrome_os_device = None
        try:
            device_key = ndb.Key(urlsafe=device_urlsafe_key)
            chrome_os_device = device_key.get()
        except Exception, e:
            logging.exception(e)
        if None is chrome_os_device:
            status = 404
            message = 'DeviceCommandsHandler reset: Device not found with key: {0}'.format(device_urlsafe_key)
            logging.info(message)
        else:
            change_intent(chrome_os_device.gcm_registration_id, config.PLAYER_RESET_COMMAND)
        self.response.set_status(status, message)

    @requires_api_token
    def volume(self, device_urlsafe_key):
        status = 200
        message = None
        request_json = json.loads(self.request.body)
        volume = request_json.get('volume')
        if volume is None or volume == '' or self.is_valid_volume(volume) is False:
            status = 400
            message = 'DeviceCommandsHandler: Invalid volume.'
        else:
            chrome_os_device = None
            try:
                device_key = ndb.Key(urlsafe=device_urlsafe_key)
                chrome_os_device = device_key.get()
            except Exception, e:
                logging.exception(e)
            if None is chrome_os_device:
                status = 404
                message = 'DeviceCommandsHandler volume: Device not found with key: {0}'.format(device_urlsafe_key)
                logging.info(message)
            else:
                intent = "{0}{1}".format(config.PLAYER_VOLUME_COMMAND, int(volume))
                change_intent(chrome_os_device.gcm_registration_id, intent)
        self.response.set_status(status, message)

    @requires_api_token
    def custom(self, device_urlsafe_key):
        status = 200
        message = None
        request_json = json.loads(self.request.body)
        intent = request_json.get('command')
        if intent is None or intent == '':
            status = 400
            message = 'DeviceCommandsHandler: Invalid command.'
        else:
            chrome_os_device = None
            try:
                device_key = ndb.Key(urlsafe=device_urlsafe_key)
                chrome_os_device = device_key.get()
            except Exception, e:
                logging.exception(e)
            if None is chrome_os_device:
                status = 404
                message = 'DeviceCommandsHandler command: Device not found with key: {0}'.format(device_urlsafe_key)
                logging.info(message)
            else:
                change_intent(chrome_os_device.gcm_registration_id, intent)
        self.response.set_status(status, message)

    @staticmethod
    def is_valid_volume(volume):
        if str(volume).isdigit():
            int_volume = int(volume)
            if 0 < int_volume < 101:
                return True
            else:
                return False
        else:
            return False
