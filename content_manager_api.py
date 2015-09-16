import json
import logging

from app_config import config
from http_client import HttpClient, HttpClientRequest

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class ContentManagerApi(object):
    HEADERS = {
        'Content-Type': 'application/json'
    }

    def __init__(self):
        self.HEADERS['Authorization'] = config.CONTENT_MANAGER_API_SERVER_KEY

    def create_tenant(self, tenant):
        payload = {
            "tenant_code": tenant.tenant_code,
            "admin_email": tenant.admin_email
        }
        url = "{content_manager_base_url}/provisioning/v1/tenants".format(
            content_manager_base_url=tenant.content_manager_base_url)
        http_client = HttpClient()
        http_client.set_default_fetch_deadline(limit_in_seconds=60)
        http_client_response = http_client.post(HttpClientRequest(url=url,
                                                                  payload=(json.dumps(payload)),
                                                                  headers=self.HEADERS))
        if http_client_response.status_code == 201:
            logging.info('create_tenant to Content Mgr: url={0}, admin_email={1}, tenant_code={2}'.format(
                url, tenant.admin_email, tenant.tenant_code))
            return True
        else:
            error_message = 'Unable to create tenant {0} in Content Manager. Status code: {1}'.format(
                tenant.name, http_client_response.status_code)
            logging.error(error_message)
            raise RuntimeError(error_message)

    def create_device(self, chrome_os_device):
        if chrome_os_device.tenant_key is not None:
            tenant = chrome_os_device.tenant_key.get()
            payload = {
                "device_key": chrome_os_device.key.urlsafe(),
                "api_key": chrome_os_device.api_key,
                "tenant_code": tenant.tenant_code
            }
            url = "{content_manager_base_url}/provisioning/v1/displays".format(
                content_manager_base_url=tenant.content_manager_base_url)
            http_client_request = HttpClientRequest(url=url,
                                                    payload=json.dumps(payload),
                                                    headers=self.HEADERS)
            http_client_response = HttpClient().post(http_client_request)
            if http_client_response.status_code == 201:
                logging.info(
                    'create_device to Content Mgr: url={0}, device_key={1}, api_key={2}, tenant_code={3}'.format(
                        url,
                        chrome_os_device.key.urlsafe(),
                        chrome_os_device.api_key,
                        tenant.tenant_code))
                return True
            else:
                error_message = 'Unable to create device in Content Manager with tenant code {0}. Status code: {1}, ' \
                                'url={2}'.format(tenant.tenant_code, http_client_response.status_code, url)
                logging.error(error_message)
                raise RuntimeError(error_message)
                return False
        else:
            error_message = 'No tenant_key for device'
            logging.error(error_message)
            raise RuntimeError(error_message)
