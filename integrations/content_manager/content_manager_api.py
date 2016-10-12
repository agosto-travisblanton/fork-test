import json
import logging

from google.appengine.ext import ndb

from app_config import config
from http_client import HttpClient, HttpClientRequest
from model_entities.chrome_os_device_model_and_overlays import Tenant, ChromeOsDevice
from model_entities.integration_events_log_model import IntegrationEventLog
from ndb_mixins import KeyValidatorMixin
from device_message_processor import change_intent
import time

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class ContentManagerApi(KeyValidatorMixin, object):
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

    def cm_request(self, url, payload, headers, device_urlsafe_key, chrome_os_device, tenant, correlation_id,
                   gcm_registration_id=None, retry=0):
        http_client_request = HttpClientRequest(url=url,
                                                payload=payload,
                                                headers=headers)
        http_client_response = HttpClient().post(http_client_request)
        if http_client_response.status_code == 201:
            message = 'ContentManagerApi.create_device: http_status={0}, url={1}, device_key={2}, \
                            api_key={3}, tenant_code={4}, SN={5}'.format(
                http_client_response.status_code,
                url,
                device_urlsafe_key,
                chrome_os_device.api_key,
                tenant.tenant_code,
                chrome_os_device.serial_number)
            logging.info(message)
            workflow_step = 'Response from Content Manager for create_device request (201 Created)'
            if retry != 0:
                workflow_step = "Retry: {}; ".format(retry) + workflow_step
            cm_create_device_event_success = IntegrationEventLog.create(
                event_category='Registration',
                component_name='Content Manager',
                workflow_step=workflow_step,
                mac_address=chrome_os_device.mac_address,
                gcm_registration_id=chrome_os_device.gcm_registration_id,
                device_urlsafe_key=device_urlsafe_key,
                serial_number=chrome_os_device.serial_number,
                correlation_identifier=correlation_id,
                details=message)
            cm_create_device_event_success.put()
            if not gcm_registration_id:
                try:
                    gcm_registration_id = ndb.Key(urlsafe=device_urlsafe_key).get().gcm_registration_id
                except Exception, e:
                    logging.exception("Failure to send change intent because device key is bad")
            if gcm_registration_id:
                change_intent(
                    gcm_registration_id=gcm_registration_id,
                    payload=config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                    device_urlsafe_key=device_urlsafe_key,
                    host='unknown',
                    user_identifier='system (CM update succesful)')
            return True
        # cm response was 4xx
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
            workflow_step = 'Response from Content Manager for create_device request (Failed)'
            if retry != 0:
                workflow_step = "Retry: {}; ".format(retry) + workflow_step
            cm_create_device_event_failure = IntegrationEventLog.create(
                event_category='Registration',
                component_name='Content Manager',
                workflow_step=workflow_step,
                mac_address=chrome_os_device.mac_address,
                gcm_registration_id=chrome_os_device.gcm_registration_id,
                device_urlsafe_key=device_urlsafe_key,
                serial_number=chrome_os_device.serial_number,
                correlation_identifier=correlation_id,
                details=message)
            cm_create_device_event_failure.put()
            return False

    def create_device(self, device_urlsafe_key, correlation_id, gcm_registration_id=None, retry=0):
        if retry < 5:
            chrome_os_device = self.get_or_except(device_urlsafe_key, ChromeOsDevice)
            cm_create_device_event_request = IntegrationEventLog.create(
                event_category='Registration',
                component_name='Content Manager',
                workflow_step='Request to Content Manager for a create_device' if retry == 0 else 'Retry {}: Request to Content Manager for a create_device'.format(
                    retry),
                mac_address=chrome_os_device.mac_address,
                gcm_registration_id=chrome_os_device.gcm_registration_id,
                device_urlsafe_key=device_urlsafe_key,
                serial_number=chrome_os_device.serial_number,
                correlation_identifier=correlation_id)
            cm_create_device_event_request.put()
            tenant = None
            if chrome_os_device.tenant_key:
                tenant = self.get_or_except(chrome_os_device.tenant_key.urlsafe(), Tenant)
            if tenant:
                cms_payload = {
                    "device_key": device_urlsafe_key,
                    "api_key": chrome_os_device.api_key,
                    "tenant_code": tenant.tenant_code,
                    "serial_number": chrome_os_device.serial_number
                }
                if chrome_os_device.content_manager_display_name:
                    cms_payload['name'] = chrome_os_device.content_manager_display_name
                if chrome_os_device.content_manager_location_description:
                    cms_payload['location'] = chrome_os_device.content_manager_location_description
                url = "{content_manager_base_url}/provisioning/v1/displays".format(
                    content_manager_base_url=tenant.content_manager_base_url)
                cm_create_device_event_request.tenant_code = tenant.tenant_code
                cm_create_device_event_request.details = 'Request url: {0} for call to CM.'.format(url)
                cm_create_device_event_request.put()

                cm_request_success = self.cm_request(
                    url=url,
                    payload=json.dumps(cms_payload),
                    headers=self.HEADERS,
                    device_urlsafe_key=device_urlsafe_key,
                    chrome_os_device=chrome_os_device,
                    tenant=tenant,
                    correlation_id=correlation_id,
                    gcm_registration_id=gcm_registration_id,
                    retry=retry
                )

                if not cm_request_success:
                    # exponential backoff
                    time.sleep((retry + 1) * (retry + 1))
                    return self.create_device(device_urlsafe_key, correlation_id, gcm_registration_id, retry=retry + 1)
                else:
                    return True

            else:
                message = 'ContentManagerApi.create_device unable to resolve tenant: device_key={0}, \
                        api_key={1}, tenant_code={2}, SN={3}'.format(
                    device_urlsafe_key,
                    chrome_os_device.api_key,
                    tenant.tenant_code,
                    chrome_os_device.serial_number)
                logging.error(message)
                cm_create_device_event_request.details = message
                cm_create_device_event_request.put()
            return False
        else:
            chrome_os_device = self.get_or_except(device_urlsafe_key, ChromeOsDevice)
            cm_create_device_event_request = IntegrationEventLog.create(
                event_category='Registration',
                component_name='Content Manager',
                workflow_step='Ending Retry',
                mac_address=chrome_os_device.mac_address,
                gcm_registration_id=chrome_os_device.gcm_registration_id,
                device_urlsafe_key=device_urlsafe_key,
                serial_number=chrome_os_device.serial_number,
                correlation_identifier=correlation_id)
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
