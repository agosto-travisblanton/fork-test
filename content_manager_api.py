import uuid

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'

from app_config import config
import json
import requests


class ContentManagerApi(object):
    """ Facade around our Content Manager API. """

    HEADERS = {
        'Content-Type': 'application/json'
    }

    def __init__(self):
        self.HEADERS['Authorization'] = 'key={0}'.format(config.CONTENT_MANAGER_API_SERVER_KEY)

    def create_tenant(self, name, admin_email):
        """ Returns tenant's content key (to be persisted with the tenant) """
        tenant = {
            "name": name,
            "admin_email": admin_email
        }
        return str(uuid.uuid4())
        # json_payload = json.dumps(tenant)
        # response = requests.post(config.CONTENT_MANAGER_API_URL, json_payload, timeout=60, headers=self.HEADERS)
        # if response.status_code == 200:
        #     content_key = response.json.get(u'tenant_key')
        #     return content_key
        # else:
        #     raise RuntimeError('Unable to post tenant to Content Manager. HTTP status code: {0}'.
        #                        format(response.status_code))
