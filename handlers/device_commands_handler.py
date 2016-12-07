import inspect
import json

from app_config import config
from device_message_processor import change_intent
from extended_session_request_handler import ExtendedSessionRequestHandler
from utils.auth_util import requires_auth
from utils.device_util import resolve_device

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>. Bob MacNeal <bob.macneal@agosto.com>'


class DeviceCommandsHandler(ExtendedSessionRequestHandler):

    @requires_auth
    def reset(self, device_urlsafe_key):
        status, message, device = resolve_device(device_urlsafe_key)
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

    @requires_auth
    def volume(self, device_urlsafe_key):
        request_json = json.loads(self.request.body)
        volume = request_json.get('volume')
        if volume is None or volume == '' or self.is_valid_volume(volume) is False:
            status = 400
            message = 'DeviceCommandsHandler.volume: Invalid volume.'
        else:
            status, message, device = resolve_device(device_urlsafe_key)
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

    @requires_auth
    def custom(self, device_urlsafe_key):
        request_json = json.loads(self.request.body)
        intent = request_json.get('command')
        if intent is None or intent == '':
            status = 400
            message = 'DeviceCommandsHandler: Invalid command.'
        else:
            status, message, device = resolve_device(device_urlsafe_key)
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

    @requires_auth
    def power_on(self, device_urlsafe_key):
        status, message, device = resolve_device(device_urlsafe_key)
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

    @requires_auth
    def power_off(self, device_urlsafe_key):
        status, message, device = resolve_device(device_urlsafe_key)
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

    @requires_auth
    def content_delete(self, device_urlsafe_key):
        status, message, device = resolve_device(device_urlsafe_key)
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

    @requires_auth
    def content_update(self, device_urlsafe_key):
        status, message, device = resolve_device(device_urlsafe_key)
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

    @requires_auth
    def refresh_device_representation(self, device_urlsafe_key):
        status, message, device = resolve_device(device_urlsafe_key)
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

    @requires_auth
    def diagnostics_toggle(self, device_urlsafe_key):
        status, message, device = resolve_device(device_urlsafe_key)
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

    @requires_auth
    def restart(self, device_urlsafe_key):
        status, message, device = resolve_device(device_urlsafe_key)
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

    @requires_auth
    def post_log(self, device_urlsafe_key):
        status, message, device = resolve_device(device_urlsafe_key)
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
    def is_valid_volume(volume):
        if str(volume).isdigit():
            int_volume = int(volume)
            if 0 < int_volume < 101:
                return True
            else:
                return False
        else:
            return False
