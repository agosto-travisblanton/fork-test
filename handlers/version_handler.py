from webapp2 import RequestHandler

from app_config import config

from restler.serializers import json_response

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class VersionHandler(RequestHandler):
    def get(self):
        data = {
            'version': config.APP_VERSION_NUMBER,
            'tag': config.APP_VERSION_TAG
        }
        json_response(self.response, data)
