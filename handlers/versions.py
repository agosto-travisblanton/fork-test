from google.appengine.api.modules import get_modules, get_default_version
from webapp2 import RequestHandler
from restler.serializers import json_response


class VersionHandler(RequestHandler):
    def get(self):
        result_data = {}
        modules = get_modules()
        for module in modules:
            default_version = get_default_version(module=module)
            result_data[module] = default_version

        json_response(self.response, result_data)
