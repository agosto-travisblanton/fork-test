__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'

import json
import requests


class ContentManagerApi(object):
    """ Facade around our Content Manager API. """
    CONTENT_MANAGER_API_SERVER_KEY = '6C346588BD4C6D722A1165B43C51C'
    CONTENT_MANAGER_API_URL = 'https://some-url'

    HEADERS = {
        'Content-Type': 'application/json'
    }

    def __init__(self):
        self.HEADERS['Authorization'] = 'key={0}'.format(self.CONTENT_MANAGER_API_SERVER_KEY)

    def create_tenant(self, name, admin_email):
        tenant = {
            "name": name,
            "admin_email": admin_email
        }
        json_payload = json.dumps(tenant)
        response = requests.post(self.CONTENT_MANAGER_API_URL, json_payload, timeout=60, headers=self.HEADERS)
        if response.status_code == 201:
            response_json = response.json()
            return response_json.get(u'tenant_key')
        elif response.status_code == 400:
            return None
        elif response.status_code == 422:
            return None
        else:
            raise RuntimeError('Unable to create tenant in Content Manager. Unexpected http status code: {0}'.
                               format(response.status_code))
