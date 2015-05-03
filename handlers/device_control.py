from webapp2 import RequestHandler

from device_commands_processor import (updateDevice, checkSchedule, registerDevice, resetDevice)

from models import ChromeOsDevice


__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class DeviceCommandsHandler(RequestHandler):
    def get(self, device_id):
        pass

    def post(self, device_id):
        if device_id:
            chrome_os_device = ChromeOsDevice.get_by_device_id(device_id)
            if chrome_os_device:
                try:
                    # processor.execute([chrome_os_device.gcm_registration_id],
                    #                   self.request.get('command'),
                    #                   self.request.get('payload'))

                    self.response.headers.pop('Content-Type', None)
                    self.response.set_status(200)
                except Exception, e:
                    self.abort(422, 'An error occurred while processing the device command: {0}'.format(e.message))
            else:
                self.abort(422, 'Unable to find an existing ChromeOS device entity by device ID: {0}'.format(device_id))
        else:
            self.abort(422, 'A device_id is required to send commands to an existing ChromeOS device entity.')


    def put(self, device_id):
        pass

    def delete(self, device_id):
        pass

