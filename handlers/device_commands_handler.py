import httplib
import inspect
import json
import logging

from google.appengine.api.datastore_errors import BadRequestError
from google.appengine.ext import ndb
from google.net.proto.ProtocolBuffer import ProtocolBufferDecodeError

from app_config import config
from decorators import requires_auth
from device_message_processor import change_intent
from extended_session_request_handler import ExtendedSessionRequestHandler

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>. Bob MacNeal <bob.macneal@agosto.com>'


class DeviceCommandsHandler(ExtendedSessionRequestHandler):
    @requires_auth
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

    @requires_auth
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

    @requires_auth
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

    @requires_auth
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

    @requires_auth
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

    @requires_auth
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

    @requires_auth
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

    @requires_auth
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

    @requires_auth
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

    @requires_auth
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

    @requires_auth
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


    @requires_auth
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
    def resolve_device(urlsafe_key):
        status = httplib.OK
        message = 'OK'
        try:
            device_key = ndb.Key(urlsafe=urlsafe_key)
            chrome_os_device = device_key.get()
        except TypeError, type_error:
            logging.exception(type_error.message)
            message = 'Invalid input (Type Error). {0} in urlsafe key'.format(type_error.message)
            status = httplib.BAD_REQUEST
            return status, message, None
        except BadRequestError, bad_request_error:
            logging.exception(bad_request_error.message)
            message = 'Invalid input. (Bad Request Error) {0} in urlsafe key'.format(bad_request_error.message)
            status = httplib.BAD_REQUEST
            return status, message, None
        except ProtocolBufferDecodeError, protocol_buffer_decode_error:
            logging.exception(protocol_buffer_decode_error.message)
            message = 'Invalid urlsafe string (Protocol Buffer Decode Error): {0}'.format(
                protocol_buffer_decode_error.message)
            status = httplib.BAD_REQUEST
            return status, message, None
        except Exception, exception:
            logging.exception(exception)
            message = exception.message
            status = httplib.BAD_REQUEST
            return status, message, None
        if None is chrome_os_device:
            status = httplib.NOT_FOUND
            calling_method_name = inspect.stack()[1][3]
            message = '{0} method not executed because device unresolvable with urlsafe key: {1}'.format(
                calling_method_name, urlsafe_key)
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
