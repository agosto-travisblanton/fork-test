import json

from app_config import config
from http_client import HttpClient, HttpClientRequest

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class ContentManagerApi(object):
    """ Facade around our Skykit Content Manager API. """

    HEADERS = {
        'Content-Type': 'application/json'
    }

    def __init__(self):
        self.HEADERS['Authorization'] = 'key={0}'.format(config.CONTENT_MANAGER_API_SERVER_KEY)

    def create_tenant(self, tenant):
        """

        :param tenant:
        :return:
        """

        payload = {
            "name": tenant.tenant_code,
            "admin_email": tenant.admin_email
        }
        http_client_response = HttpClient().post(HttpClientRequest(url=config.CONTENT_MANAGER_API_URL,
                                                                   payload=(json.dumps(payload)),
                                                                   headers=self.HEADERS))
        if http_client_response.status_code == 201:
            response_json = http_client_response.json_content()
            return response_json.get(u'tenant_key')
        elif http_client_response.status_code == 400:
            return None
        elif http_client_response.status_code == 422:
            return None
        else:
            raise RuntimeError('Unable to create tenant in Content Manager. Unexpected http status code: {0}'.
                               format(http_client_response.status_code))


    def create_device(self, chrome_os_device):
        """
        Create a new device in Content Manager system.

        :param chrome_os_device: A ChromeOsDevice object.
        :return:
        """

        tenant = chrome_os_device.key.parent().get()
        payload = {
            "device_key": chrome_os_device.key.urlsafe(),
            "player_cms_api_key": tenant.content_server_api_key
        }
        url = "{content_manager_base_url}/api/v1/devices".format(content_manager_base_url=tenant.content_server_url)
        http_client_request = HttpClientRequest(url=url, payload=json.dumps(payload), headers=self.HEADERS)
        http_client_response = HttpClient().post(http_client_request)
        if http_client_response.status_code != 201:
            raise RuntimeError('Unable to create device in Content Manager. Unexpected http status code: {0}'.
                               format(http_client_response.status_code))
