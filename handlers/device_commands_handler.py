import json
import logging
import re

from google.appengine.ext import ndb

from webapp2 import RequestHandler

from decorators import api_token_required
from device_commands_processor import (change_intent)

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>. Bob MacNeal <bob.macneal@agosto.com>'


class DeviceCommandsHandler(RequestHandler):
    DEVICE_RESET = 'skykit.com/skdchromeapp/reset'

    @api_token_required
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
                device_key = ndb.Key(urlsafe=device_urlsafe_key)
                chrome_os_device = device_key.get()
            except Exception, e:
                logging.exception(e)
            if None is chrome_os_device:
                status = 404
                message = 'DeviceCommandsHandler: Device not found with key: {0}'.format(device_urlsafe_key)
                logging.info(message)
            else:
                change_intent(chrome_os_device.gcm_registration_id, intent)
        self.response.set_status(status, message)

    @api_token_required
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
            change_intent(chrome_os_device.gcm_registration_id, self.DEVICE_RESET)
        self.response.set_status(status, message)

    @api_token_required
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
                intent = "skykit.com/skdchromeapp/volume/{0}".format(int(volume))
                change_intent(chrome_os_device.gcm_registration_id, intent)
        self.response.set_status(status, message)

    @api_token_required
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
