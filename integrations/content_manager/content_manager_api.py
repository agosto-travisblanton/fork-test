import json
import logging

from google.appengine.ext import ndb

from app_config import config
from http_client import HttpClient, HttpClientRequest
from model_entities.integration_events_log_model import IntegrationEventLog

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class ContentManagerApi(object):
    HEADERS = {
        'Content-Type': 'application/json'
    }

    def __init__(self):
        self.HEADERS['Authorization'] = config.CONTENT_MANAGER_API_SERVER_KEY

    def create_tenant(self, tenant):
        payload = {
            "tenant_name": tenant.name,
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

    def create_device(self, device_urlsafe_key, correlation_id):
        key = ndb.Key(urlsafe=device_urlsafe_key)
        chrome_os_device = key.get()
        cm_create_device_event_request = IntegrationEventLog.create(
                event_category='Registration',
                component_name='Content Manager',
                workflow_step='Request to Content Manager for a create_device',
                mac_address=chrome_os_device.mac_address,
                gcm_registration_id=chrome_os_device.gcm_registration_id,
                device_urlsafe_key=device_urlsafe_key,
                serial_number=chrome_os_device.serial_number,
                correlation_identifier=correlation_id)
        cm_create_device_event_request.put()
        if chrome_os_device.tenant_key:
            tenant = chrome_os_device.tenant_key.get()
            if tenant:
                payload = {
                    "device_key": device_urlsafe_key,
                    "api_key": chrome_os_device.api_key,
                    "tenant_code": tenant.tenant_code,
                    "serial_number": chrome_os_device.serial_number
                }
                if chrome_os_device.content_manager_display_name:
                    payload['name'] = chrome_os_device.content_manager_display_name
                if chrome_os_device.content_manager_location_description:
                    payload['location'] = chrome_os_device.content_manager_location_description

                url = "{content_manager_base_url}/provisioning/v1/displays".format(
                    content_manager_base_url=tenant.content_manager_base_url)
                if cm_create_device_event_request:
                    cm_create_device_event_request.tenant_code = tenant.tenant_code
                    cm_create_device_event_request.details = 'Request url: {0} for call to CM.'.format(url)
                    cm_create_device_event_request.put()
                http_client_request = HttpClientRequest(url=url,
                                                        payload=json.dumps(payload),
                                                        headers=self.HEADERS)
                http_client_response = HttpClient().post(http_client_request)
                if http_client_response.status_code == 201:
                    if chrome_os_device.content_manager_display_name:
                        display_name = chrome_os_device.content_manager_display_name
                    else:
                        display_name = 'Not available'
                    if chrome_os_device.content_manager_location_description:
                        location_description = chrome_os_device.content_manager_location_description
                    else:
                        location_description = 'Not available'
                    message = 'ContentManagerApi.create_device: http_status={0}, url={1}, device_key={2}, \
                    api_key={3}, tenant_code={4}, SN={5}, display_name={6}, location_description={7}. Success!'.format(
                        http_client_response.status_code,
                        url,
                        device_urlsafe_key,
                        chrome_os_device.api_key,
                        tenant.tenant_code,
                        chrome_os_device.serial_number,
                        display_name,
                        location_description)
                    logging.info(message)
                    cm_create_device_event_response = IntegrationEventLog.create(
                        event_category='Registration',
                        component_name='Content Manager',
                        workflow_step='Response from Content Manager for a create_device',
                        mac_address=chrome_os_device.mac_address,
                        gcm_registration_id=chrome_os_device.gcm_registration_id,
                        device_urlsafe_key=device_urlsafe_key,
                        serial_number=chrome_os_device.serial_number,
                        correlation_identifier=correlation_id,
                        details=message)
                    cm_create_device_event_response.put()
                    return True
                else:
                    message = 'ContentManagerApi.create_device: http_status={0}, url={1}, device_key={2}, \
                    api_key={3}, tenant_code={4}, SN={5}'.format(
                        http_client_response.status_code,
                        url,
                        device_urlsafe_key,
                        chrome_os_device.api_key,
                        tenant.tenant_code,
                        chrome_os_device.serial_number)
                    logging.error(message)
                    cm_create_device_event_response = IntegrationEventLog.create(
                        event_category='Registration',
                        component_name='Content Manager',
                        workflow_step='Response from Content Manager for create_device',
                        mac_address=chrome_os_device.mac_address,
                        gcm_registration_id=chrome_os_device.gcm_registration_id,
                        device_urlsafe_key=device_urlsafe_key,
                        serial_number=chrome_os_device.serial_number,
                        correlation_identifier=correlation_id,
                        details=message)
                    cm_create_device_event_response.put()
            else:
                message = 'ContentManagerApi.create_device unable to resolve tenant: device_key={0}, \
                    api_key={1}, tenant_code={2}, SN={3}'.format(
                        device_urlsafe_key,
                        chrome_os_device.api_key,
                        tenant.tenant_code,
                        chrome_os_device.serial_number)
                logging.error(message)
                if cm_create_device_event_request:
                    cm_create_device_event_request.details = message
                    cm_create_device_event_request.put()
        else:
            message = 'Error: ContentManagerApi.create_device no tenant key: device_key={0}, \
                    api_key={1}, SN={3}'.format(
                        device_urlsafe_key,
                        chrome_os_device.api_key,
                        chrome_os_device.serial_number)
            logging.error(message)
            if cm_create_device_event_request:
                cm_create_device_event_request.details = message
                cm_create_device_event_request.put()

        return False

    def delete_device(self, device_urlsafe_key):
        key = ndb.Key(urlsafe=device_urlsafe_key)
        device = key.get()
        tenant = device.tenant_key.get()
        url = "{content_manager_base_url}/provisioning/v1/displays/{device_key}".format(
            content_manager_base_url=tenant.content_manager_base_url,
            device_key=device_urlsafe_key)
        http_client_request = HttpClientRequest(url=url, headers=self.HEADERS)
        http_client_response = HttpClient().delete(http_client_request)
        if http_client_response.status_code == 204:
            logging.info(
                'delete_device to Content Mgr successful: url={0}, device_key={1}, tenant_code={2}'.format(
                    url,
                    device_urlsafe_key,
                    tenant.tenant_code))
            return True
        else:
            error_message = 'Failed deleting device in Content Manager. device_key: {0}. Status code: {1}. ' \
                            'url: {2}'.format(device_urlsafe_key, http_client_response.status_code, url)
            logging.error(error_message)
            return False

    def update_device(self, device_urlsafe_key, correlation_id=None):
        if self.delete_device(device_urlsafe_key):
            return self.create_device(device_urlsafe_key, correlation_id)
        else:
            error_message = 'update_device failed deleting device in Content Manager. device_key={0}'.format(
                device_urlsafe_key)
            logging.error(error_message)
            raise RuntimeError(error_message)
