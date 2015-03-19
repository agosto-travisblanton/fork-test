import json
from webapp2 import RequestHandler
from restler.serializers import json_response

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class DeviceRegistrationHandler(RequestHandler):
    def get(self):
        self.response.out.write('Hello from skykit-display-device/device registration!')

    
    def post(self):
    	body = json.loads(self.request.body)
        # json_response(self.response, None)

