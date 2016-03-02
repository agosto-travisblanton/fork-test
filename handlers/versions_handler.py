from google.appengine.api import modules
from webapp2 import RequestHandler

from app_config import config
from restler.serializers import json_response

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class VersionsHandler(RequestHandler):
    def get(self):
        version = {
            'number': '{0}.{1}.{2}'.format(config.SPRINT_NUMBER, config.DEPLOYMENT_COUNTER,
                                           config.PRODUCTION_HOTFIX_COUNTER),
            'web_version_name': modules.get_current_version_name(),
            'web_module_name': modules.get_current_module_name(),
            'current_instance_id': modules.get_current_instance_id(),
            'default_version': modules.get_default_version(),
            'hostname': modules.get_hostname()
        }
        json_response(self.response, version)
