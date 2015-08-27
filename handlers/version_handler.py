from webapp2 import RequestHandler
from google.appengine.api import modules

from restler.serializers import json_response

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class VersionHandler(RequestHandler):
    def get(self):
        version = {
            'name': modules.get_current_version_name()
        }
        json_response(self.response, version)
