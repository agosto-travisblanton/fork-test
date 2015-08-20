import json

from webapp2 import RequestHandler

from restler.serializers import json_response

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class VersionHandler(RequestHandler):
    def get(self):
        data = {
            'version': '10',
            'tag': '5789d5aca7'
        }
        json_response(self.response, data)
