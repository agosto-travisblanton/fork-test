from webapp2 import RequestHandler

from restler.serializers import json_response


__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class DeviceEnrollmentHandler(RequestHandler):
    def get(self):
        self.response.out.write('Hello from skykit-display-device/device registration!')
        json_response(self.response, None)

