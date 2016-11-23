import httplib
import json
import logging
import time

from google.appengine.ext import ndb

from app_config import config
from device_message_processor import change_intent
from http_client import HttpClient, HttpClientRequest
from model_entities.chrome_os_device_model_and_overlays import Tenant, ChromeOsDevice
from model_entities.integration_events_log_model import IntegrationEventLog
from ndb_mixins import KeyValidatorMixin

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class ContentManagerApi(KeyValidatorMixin, object):

    def create_device(self, device_urlsafe_key, correlation_id, gcm_registration_id=None, retry=0):
        if retry < 5:
            chrome_os_device = self.get_or_except(device_urlsafe_key, ChromeOsDevice)

            workflow_step = 'Request to Content Manager for a create_device'
            if retry != 0:
                workflow_step = "Retry {0}: {1}".format(retry, workflow_step)
            cm_create_device_request = IntegrationEventLog.create(
                event_category='Registration',
                component_name='Content Manager',
                workflow_step=workflow_step,
                mac_address=chrome_os_device.mac_address,
                gcm_registration_id=chrome_os_device.gcm_registration_id,
                device_urlsafe_key=device_urlsafe_key,
                serial_number=chrome_os_device.serial_number,
                correlation_identifier=correlation_id)
            cm_create_device_request.put()
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
                cm_create_device_request.tenant_code = tenant.tenant_code
                cm_create_device_request.details = 'Request url: {0} for call to CM.'.format(url)
                cm_create_device_request.put()

                cm_request_success = self.new_device_post(
                    url=url,
                    cms_payload=cms_payload,
                    device_urlsafe_key=device_urlsafe_key,
                    chrome_os_device=chrome_os_device,
                    tenant=tenant,
                    correlation_id=correlation_id,
                    gcm_registration_id=gcm_registration_id,
                    retry=retry
                )

                if not cm_request_success:
                    # exponential back off
                    time.sleep((retry + 1) * (retry + 1))
                    return self.create_device(device_urlsafe_key, correlation_id, gcm_registration_id, retry=retry + 1)
                else:
                    return True

            else:
                error_message = 'ContentManagerApi.create_device unable to resolve tenant: device_key={0}, \
                        api_key={1}, tenant_code={2}, SN={3}'.format(
                    device_urlsafe_key, chrome_os_device.api_key, tenant.tenant_code, chrome_os_device.serial_number)
                logging.error(error_message)
                cm_create_device_request.details = error_message
                cm_create_device_request.put()
            return False
        else:
            chrome_os_device = self.get_or_except(device_urlsafe_key, ChromeOsDevice)
            cm_create_device_request = IntegrationEventLog.create(
                event_category='Registration',
                component_name='Content Manager',
                workflow_step='Ending Retry',
                mac_address=chrome_os_device.mac_address,
                gcm_registration_id=chrome_os_device.gcm_registration_id,
                device_urlsafe_key=device_urlsafe_key,
                serial_number=chrome_os_device.serial_number,
                correlation_identifier=correlation_id)
            cm_create_device_request.put()
            return False

    def delete_device(self, device_urlsafe_key, correlation_id):
        device = self.get_or_except(device_urlsafe_key, ChromeOsDevice)
        tenant = device.tenant_key.get()
        url = "{content_manager_base_url}/provisioning/v1/displays/{device_key}".format(
            content_manager_base_url=tenant.content_manager_base_url,
            device_key=device_urlsafe_key)
        http_client_request = HttpClientRequest(url=url, headers=self.HEADERS)
        http_client_response = HttpClient().delete(http_client_request)

        logging_info = 'ContentManagerApi.delete_device: http_status={0}, url={1}, device_key={2}, \
                            api_key={3}, tenant_code={4}, SN={5}'.format(
            http_client_response.status_code, url, device_urlsafe_key, device.api_key, tenant.tenant_code,
            device.serial_number)

        if http_client_response.status_code == httplib.NO_CONTENT:
            logging.info(logging_info)
            cm_delete_device_success = IntegrationEventLog.create(
                event_category='Delete Device',
                component_name='Content Manager',
                workflow_step='Successful request to CM',
                mac_address=device.mac_address,
                gcm_registration_id=device.gcm_registration_id,
                device_urlsafe_key=device_urlsafe_key,
                serial_number=device.serial_number,
                correlation_identifier=correlation_id,
                details=logging_info)
            cm_delete_device_success.put()

            return True
        else:
            logging.error(logging_info)
            cm_delete_device_failure = IntegrationEventLog.create(
                event_category='Delete Device',
                component_name='Content Manager',
                workflow_step='Successful request to CM',
                mac_address=device.mac_address,
                gcm_registration_id=device.gcm_registration_id,
                device_urlsafe_key=device_urlsafe_key,
                serial_number=device.serial_number,
                correlation_identifier=correlation_id,
                details=logging_info)
            cm_delete_device_failure.put()

            return False

    def update_device(self, device_urlsafe_key):
        correlation_id = IntegrationEventLog.generate_correlation_id()

        if self.delete_device(device_urlsafe_key=device_urlsafe_key, correlation_id=correlation_id):
            return self.create_device(device_urlsafe_key, correlation_id)
        else:
            error_message = 'ContentManagerApi.update_device failed deleting device in Content Manager. device_key={0}'.format(
                device_urlsafe_key)
            logging.error(error_message)
            raise RuntimeError(error_message)

    @staticmethod
    def create_tenant(tenant, correlation_id):
        headers = {'Content-Type': 'application/json', 'Authorization': config.CONTENT_MANAGER_API_SERVER_KEY}
        cms_payload = {
            "tenant_name": tenant.name,
            "tenant_code": tenant.tenant_code,
            "admin_email": tenant.admin_email
        }
        url = "{content_manager_base_url}/provisioning/v1/tenants".format(
            content_manager_base_url=tenant.content_manager_base_url)

        http_client = HttpClient()
        http_client.set_default_fetch_deadline(limit_in_seconds=60)
        http_client_request = HttpClientRequest(url=url, payload=(json.dumps(cms_payload)), headers=headers)
        http_client_response = http_client.post(http_client_request)

        if http_client_response.status_code == httplib.CREATED:
            details = 'Tenant created in Content Manager: url={0}, admin_email={1}, tenant_code={2}'.format(
                url, tenant.admin_email, tenant.tenant_code)
            workflow_step = 'Response from Content Manager for create_tenant request (201 Created)'
            IntegrationEventLog.create(event_category='Tenant Creation',
                                       component_name='Content Manager',
                                       workflow_step=workflow_step,
                                       tenant_code=tenant.tenant_code,
                                       details=details,
                                       correlation_identifier=correlation_id).put()
            return True
        else:
            error_message = 'Failed to create tenant {0} in Content Manager. Status code: {1}'.format(
                tenant.name, http_client_response.status_code)
            workflow_step = 'Response from Content Manager for create_tenant request (Failed)'
            IntegrationEventLog.create(event_category='Tenant Creation',
                                       component_name='Content Manager',
                                       workflow_step=workflow_step,
                                       tenant_code=tenant.tenant_code,
                                       details=error_message,
                                       correlation_identifier=correlation_id).put()
            logging.error(error_message)
            return False

    @staticmethod
    def new_device_post(url, cms_payload, device_urlsafe_key, chrome_os_device, tenant, correlation_id,
                        gcm_registration_id=None, retry=0):
        headers = {'Content-Type': 'application/json', 'Authorization': config.CONTENT_MANAGER_API_SERVER_KEY}
        http_client = HttpClient()
        http_client.set_default_fetch_deadline(limit_in_seconds=60)
        http_client_request = HttpClientRequest(url=url, payload=(json.dumps(cms_payload)), headers=headers)
        http_client_response = http_client.post(http_client_request)
        log_info = 'ContentManagerApi.new_device_post: http_status={0}, url={1}, device_key={2}, \
                            api_key={3}, tenant_code={4}, SN={5}'.format(
            http_client_response.status_code, url, device_urlsafe_key, chrome_os_device.api_key, tenant.tenant_code,
            chrome_os_device.serial_number)
        logging.info(log_info)

        if http_client_response.status_code == httplib.CREATED:
            workflow_step = 'Response from Content Manager for create_device request (201 Created)'
            if retry != 0:
                workflow_step = "Retry {0}: {1}".format(retry, workflow_step)
            cm_create_device_event_success = IntegrationEventLog.create(
                event_category='Registration',
                component_name='Content Manager',
                workflow_step=workflow_step,
                mac_address=chrome_os_device.mac_address,
                gcm_registration_id=chrome_os_device.gcm_registration_id,
                device_urlsafe_key=device_urlsafe_key,
                serial_number=chrome_os_device.serial_number,
                correlation_identifier=correlation_id,
                details=log_info)
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
            workflow_step = 'Response from Content Manager for create_device request (Failed)'
            if retry != 0:
                workflow_step = "Retry {0}: {1}".format(retry, workflow_step)
            cm_create_device_event_failure = IntegrationEventLog.create(
                event_category='Registration',
                component_name='Content Manager',
                workflow_step=workflow_step,
                mac_address=chrome_os_device.mac_address,
                gcm_registration_id=chrome_os_device.gcm_registration_id,
                device_urlsafe_key=device_urlsafe_key,
                serial_number=chrome_os_device.serial_number,
                correlation_identifier=correlation_id,
                details=log_info)
            cm_create_device_event_failure.put()
            return False
