import inspect
import json
import logging

from google.appengine.ext import ndb
from webapp2 import RequestHandler

from app_config import config
from decorators import requires_api_token
from device_message_processor import change_intent
from ndb_mixins import KeyValidatorMixin

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>. Bob MacNeal <bob.macneal@agosto.com>'


class DeviceCommandsHandler(RequestHandler, KeyValidatorMixin):
    @requires_api_token
    def post(self, device_urlsafe_key):
        method_name = inspect.stack()[0][3]
        request_json = json.loads(self.request.body)
        intent = request_json.get('intent')
        if intent is None or intent == '':
            status = 400
            message = 'DeviceCommandsHandler.{0}: Invalid intent.'.format(method_name)
        else:
            status, message, device = DeviceCommandsHandler.resolve_device(device_urlsafe_key)
            if device:
                user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
                if user_identifier is None or user_identifier == '':
                    user_identifier = 'system'
                change_intent(
                    gcm_registration_id=device.gcm_registration_id,
                    payload=intent,
                    device_urlsafe_key=device_urlsafe_key,
                    host=self.request.host_url,
                    user_identifier=user_identifier)
        self.response.set_status(status, message)

    @requires_api_token
    def reset(self, device_urlsafe_key):
        status, message, device = DeviceCommandsHandler.resolve_device(device_urlsafe_key)
        if device:
            user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
            if user_identifier is None or user_identifier == '':
                user_identifier = 'system'
            change_intent(
                gcm_registration_id=device.gcm_registration_id,
                payload=config.PLAYER_RESET_COMMAND,
                device_urlsafe_key=device_urlsafe_key,
                host=self.request.host_url,
                user_identifier=user_identifier)
        self.response.set_status(status, message)

    @requires_api_token
    def volume(self, device_urlsafe_key):
        request_json = json.loads(self.request.body)
        volume = request_json.get('volume')
        if volume is None or volume == '' or self.is_valid_volume(volume) is False:
            status = 400
            message = 'DeviceCommandsHandler.volume: Invalid volume.'
        else:
            status, message, device = DeviceCommandsHandler.resolve_device(device_urlsafe_key)
            if device:
                user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
                if user_identifier is None or user_identifier == '':
                    user_identifier = 'system'
                intent = "{0}{1}".format(config.PLAYER_VOLUME_COMMAND, int(volume))
                change_intent(gcm_registration_id=device.gcm_registration_id,
                              payload=intent,
                              device_urlsafe_key=device_urlsafe_key,
                              host=self.request.host_url,
                              user_identifier=user_identifier)
        self.response.set_status(status, message)

    @requires_api_token
    def custom(self, device_urlsafe_key):
        request_json = json.loads(self.request.body)
        intent = request_json.get('command')
        if intent is None or intent == '':
            status = 400
            message = 'DeviceCommandsHandler: Invalid command.'
        else:
            status, message, device = DeviceCommandsHandler.resolve_device(device_urlsafe_key)
            if device:
                user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
                if user_identifier is None or user_identifier == '':
                    user_identifier = 'system'
                change_intent(gcm_registration_id=device.gcm_registration_id,
                              payload=intent,
                              device_urlsafe_key=device_urlsafe_key,
                              host=self.request.host_url,
                              user_identifier=user_identifier)
        self.response.set_status(status, message)

    @requires_api_token
    def power_on(self, device_urlsafe_key):
        status, message, device = DeviceCommandsHandler.resolve_device(device_urlsafe_key)
        if device:
            user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
            if user_identifier is None or user_identifier == '':
                user_identifier = 'system'
            change_intent(
                gcm_registration_id=device.gcm_registration_id,
                payload=config.PLAYER_POWER_ON_COMMAND,
                device_urlsafe_key=device_urlsafe_key,
                host=self.request.host_url,
                user_identifier=user_identifier)
        self.response.set_status(status, message)

    @requires_api_token
    def power_off(self, device_urlsafe_key):
        status, message, device = DeviceCommandsHandler.resolve_device(device_urlsafe_key)
        if device:
            user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
            if user_identifier is None or user_identifier == '':
                user_identifier = 'system'
            change_intent(
                gcm_registration_id=device.gcm_registration_id,
                payload=config.PLAYER_POWER_OFF_COMMAND,
                device_urlsafe_key=device_urlsafe_key,
                host=self.request.host_url,
                user_identifier=user_identifier)
        self.response.set_status(status, message)

    @requires_api_token
    def content_delete(self, device_urlsafe_key):
        status, message, device = DeviceCommandsHandler.resolve_device(device_urlsafe_key)
        if device:
            user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
            if user_identifier is None or user_identifier == '':
                user_identifier = 'system'
            change_intent(
                gcm_registration_id=device.gcm_registration_id,
                payload=config.PLAYER_DELETE_CONTENT_COMMAND,
                device_urlsafe_key=device_urlsafe_key,
                host=self.request.host_url,
                user_identifier=user_identifier)
        self.response.set_status(status, message)

    @requires_api_token
    def content_update(self, device_urlsafe_key):
        status, message, device = DeviceCommandsHandler.resolve_device(device_urlsafe_key)
        if device:
            user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
            if user_identifier is None or user_identifier == '':
                user_identifier = 'system'
            change_intent(
                gcm_registration_id=device.gcm_registration_id,
                payload=config.PLAYER_UPDATE_CONTENT_COMMAND,
                device_urlsafe_key=device_urlsafe_key,
                host=self.request.host_url,
                user_identifier=user_identifier)
        self.response.set_status(status, message)

    @requires_api_token
    def refresh_device_representation(self, device_urlsafe_key):
        status, message, device = DeviceCommandsHandler.resolve_device(device_urlsafe_key)
        if device:
            user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
            if user_identifier is None or user_identifier == '':
                user_identifier = 'system'
            change_intent(
                gcm_registration_id=device.gcm_registration_id,
                payload=config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                device_urlsafe_key=device_urlsafe_key,
                host=self.request.host_url,
                user_identifier=user_identifier)
        self.response.set_status(status, message)

    @requires_api_token
    def diagnostics_toggle(self, device_urlsafe_key):
        status, message, device = DeviceCommandsHandler.resolve_device(device_urlsafe_key)
        if device:
            user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
            if user_identifier is None or user_identifier == '':
                user_identifier = 'system'
            change_intent(
                gcm_registration_id=device.gcm_registration_id,
                payload=config.PLAYER_DIAGNOSTICS_TOGGLE_COMMAND,
                device_urlsafe_key=device_urlsafe_key,
                host=self.request.host_url,
                user_identifier=user_identifier)
        self.response.set_status(status, message)

    @requires_api_token
    def restart(self, device_urlsafe_key):
        status, message, device = DeviceCommandsHandler.resolve_device(device_urlsafe_key)
        if device:
            user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
            if user_identifier is None or user_identifier == '':
                user_identifier = 'system'
            change_intent(
                gcm_registration_id=device.gcm_registration_id,
                payload=config.PLAYER_RESTART_COMMAND,
                device_urlsafe_key=device_urlsafe_key,
                host=self.request.host_url,
                user_identifier=user_identifier)
        self.response.set_status(status, message)


    @requires_api_token
    def post_log(self, device_urlsafe_key):
        status, message, device = DeviceCommandsHandler.resolve_device(device_urlsafe_key)
        if device:
            user_identifier = self.request.headers.get('X-Provisioning-User-Identifier')
            if user_identifier is None or user_identifier == '':
                user_identifier = 'system'
            change_intent(
                gcm_registration_id=device.gcm_registration_id,
                payload=config.PLAYER_POST_LOG_COMMAND,
                device_urlsafe_key=device_urlsafe_key,
                host=self.request.host_url,
                user_identifier=user_identifier)
        self.response.set_status(status, message)

    @staticmethod
    def resolve_device(device_urlsafe_key):
        status = 200
        message = 'OK'
        chrome_os_device = None
        try:
            device_key = ndb.Key(urlsafe=device_urlsafe_key)
            chrome_os_device = device_key.get()
        except Exception, e:
            logging.exception(e)
        if None is chrome_os_device:
            status = 404
            calling_method_name = inspect.stack()[1][3]
            message = '{0} command not executed because device not found with key: {1}'.format(
                calling_method_name, device_urlsafe_key)
            logging.warning(message)
        return status, message, chrome_os_device

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
