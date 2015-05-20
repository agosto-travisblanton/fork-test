import json
from webapp2 import RequestHandler
from device_commands_processor import (update_device, check_schedule, register_device, reset_device, change_channel)
from models import ChromeOsDevice

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class DeviceCommandsHandler(RequestHandler):
    def get(self, device_id):
        pass

    def post(self, device_id):
        chrome_os_device = ChromeOsDevice.get_by_device_id(device_id)
        self.response.headers.pop('Content-Type', None)
        if chrome_os_device:
            try:
                if self.request.body is not None:
                    request_json = json.loads(self.request.body)
                    command = request_json['command']
                    payload = request_json['payload']
                    if command == 'change_channel':
                        change_channel(chrome_os_device.gcm_registration_id, payload)
                        self.response.set_status(200)
                    else:
                        self.response.set_status(422, 'Unrecognized command')
            except Exception, e:
                self.response.set_status(422, 'An error occurred while processing the device command: {0}'.
                                         format(e.message))
        else:
            self.response.set_status(422, 'Unable to find an existing ChromeOS device entity by device ID: {0}'.
                                     format(device_id))

    def put(self, device_id):
        pass

    def delete(self, device_id):
        pass

