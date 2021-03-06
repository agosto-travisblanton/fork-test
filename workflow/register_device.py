import logging

from datetime import datetime
from google.appengine.ext import ndb
from google.appengine.ext.deferred import deferred

from agar.env import on_development_server
from app_config import config
from integrations.content_manager.content_manager_api import ContentManagerApi
from integrations.directory_api.chrome_os_devices_api import ChromeOsDevicesApi
from model_entities.chrome_os_device_model_and_overlays import Tenant
from model_entities.domain_model import Domain
from model_entities.integration_events_log_model import IntegrationEventLog
from utils.email_notify import EmailNotify
from workflow.update_chrome_os_device import update_chrome_os_device

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


def register_device(urlsafe_key=None,
                    mac_address=None,
                    gcm_registration_id=None,
                    correlation_id=None,
                    domain_name=None,
                    page_token=None):
    """
    A function that is meant to be run asynchronously to fetch information about the device entity
    with ChromeOsDevice information from Directory API using the device's MAC address to match.
    :param domain_name: the domain needed to connect to in CDM to search for the device.
    :param page_token: a google api page marker for where you are in the larger list. Fetches in chunks of 100 records.
    :param correlation_id: our generated id to track the registration process
    :param gcm_registration_id: google cloud messaging id the player sends to us for messaging purposes.
    :param mac_address: the device's MAC address
    :param urlsafe_key: our device key
    """
    api_request_event = IntegrationEventLog.create(
        event_category='Registration',
        component_name='Chrome Directory API',
        workflow_step='Request for device information',
        mac_address=mac_address,
        device_urlsafe_key=urlsafe_key,
        gcm_registration_id=gcm_registration_id,
        correlation_identifier=correlation_id)
    api_request_event.put()
    if not urlsafe_key:
        error_message = 'register_device: The device URL-safe key parameter is None. It is required.'
        api_request_event.details = error_message
        api_request_event.put()
        raise deferred.PermanentTaskFailure(error_message)
    if not mac_address:
        error_message = 'register_device: The device MAC address parameter is None. It is required.'
        api_request_event.details = error_message
        api_request_event.put()
        raise deferred.PermanentTaskFailure(error_message)
    device_key = ndb.Key(urlsafe=urlsafe_key)
    device = device_key.get()
    if None == device:
        error_message = 'Unable to find device by device_urlsafe_key: {0}'.format(urlsafe_key)
        logging.error(error_message)
        api_request_event.details = error_message
        api_request_event.put()
        raise deferred.PermanentTaskFailure(error_message)
    if domain_name:
        impersonation_email = Domain.get_impersonation_email_by_domain_name(domain_name=domain_name)
    else:
        tenant = device.get_tenant()
        impersonation_email = tenant.get_domain().impersonation_admin_email_address
    if not impersonation_email:
        api_request_event.details = 'register_device: Impersonation email is not resolvable.'
        api_request_event.put()
        error_message = 'register_device: Impersonation email is not resolvable for device with device key {0}.'.format(
            urlsafe_key)
        logging.error(error_message)
        raise deferred.PermanentTaskFailure(error_message)

    api_response_event = IntegrationEventLog.create(
        event_category='Registration',
        component_name='Chrome Directory API',
        workflow_step='Response for device information request',
        mac_address=mac_address,
        device_urlsafe_key=urlsafe_key,
        gcm_registration_id=gcm_registration_id,
        correlation_identifier=correlation_id)
    api_response_event.put()

    chrome_os_devices_api = ChromeOsDevicesApi(impersonation_email)
    chrome_os_devices, new_page_token = chrome_os_devices_api.cursor_list(customer_id=config.GOOGLE_CUSTOMER_ID,
                                                                          next_page_token=page_token)
    if chrome_os_devices and len(chrome_os_devices) > 0:
        lowercase_device_mac_address = mac_address.lower()
        loop_comprehension = (x for x in chrome_os_devices if x.get('macAddress') == lowercase_device_mac_address or
                              x.get('ethernetMacAddress') == lowercase_device_mac_address)
        chrome_os_device = next(loop_comprehension, None)
        if chrome_os_device:
            device_key = ndb.Key(urlsafe=urlsafe_key)
            device = device_key.get()
            device.device_id = chrome_os_device.get('deviceId')
            device.mac_address = chrome_os_device.get('macAddress')
            device.serial_number = chrome_os_device.get('serialNumber')
            device.status = chrome_os_device.get('status')
            device.last_sync = chrome_os_device.get('lastSync')
            device.kind = chrome_os_device.get('kind')
            device.ethernet_mac_address = chrome_os_device.get('ethernetMacAddress')
            device.org_unit_path = chrome_os_device.get('orgUnitPath')
            device.annotated_user = chrome_os_device.get('annotatedUser')
            device.annotated_location = chrome_os_device.get('annotatedLocation')
            device.content_manager_location_description = chrome_os_device.get('annotatedLocation')
            device.annotated_asset_id = chrome_os_device.get('annotatedAssetId')
            device.content_manager_display_name = chrome_os_device.get('annotatedAssetId')
            device.notes = chrome_os_device.get('notes')
            device.boot_mode = chrome_os_device.get('bootMode')
            device.last_enrollment_time = chrome_os_device.get('lastEnrollmentTime')
            device.platform_version = chrome_os_device.get('platformVersion')
            device.model = chrome_os_device.get('model')
            device.os_version = chrome_os_device.get('osVersion')
            device.firmware_version = chrome_os_device.get('firmwareVersion')
            device.etag = chrome_os_device.get('etag')

            # Registration process sends the customer's display in the annotatedAssetId field of
            # the Directory API ChromeOsDevice resource representation.
            device.customer_display_name = chrome_os_device.get('annotatedAssetId')
            device.annotated_asset_id = urlsafe_key
            device.put()

            api_response_event.serial_number = device.serial_number
            api_response_event.details = 'Chrome Directory API call success! Notifying Content Manager.'
            api_response_event.put()

            info = 'register_device: retrieved directory API for MAC address = {0}. Notifying Content Manager.' \
                .format(lowercase_device_mac_address)
            logging.info(info)

            if device.tenant_key is None:
                if device.org_unit_path:
                    tenant = Tenant.find_by_organization_unit_path(device.org_unit_path)
                    if tenant:
                        device.tenant_key = tenant.key
                        device.put()
            notifier = EmailNotify()
            tenant_name = device.get_tenant().name
            notification_emails = device.get_tenant().notification_emails
            notifier.device_enrolled(tenant_code=device.get_tenant().tenant_code,
                                     tenant_name=tenant_name,
                                     device_mac_address=mac_address,
                                     timestamp=datetime.utcnow())
            device_enrollment_email_event = IntegrationEventLog.create(
                event_category='Registration',
                component_name='Provisioning',
                workflow_step='Device enrolled email notification sent',
                mac_address=mac_address,
                device_urlsafe_key=urlsafe_key,
                gcm_registration_id=gcm_registration_id,
                details='Device enrollment email for {0} sent to: {1}'.format(tenant_name, notification_emails),
                correlation_identifier=correlation_id)
            device_enrollment_email_event.put()

            deferred.defer(ContentManagerApi().create_device,
                           device_urlsafe_key=urlsafe_key,
                           correlation_id=correlation_id,
                           _queue='content-server')

            # Update Directory API with the device key in the annotated asset ID.
            if not device.is_unmanaged_device:
                details = 'annotated_asset_id={0}. Success!'.format(
                    device.annotated_asset_id)
                directory_api_update_event = IntegrationEventLog.create(
                    event_category='Registration',
                    component_name='Chrome Directory API',
                    workflow_step='Update Directory API with device key in annotatedAssetId field.',
                    mac_address=mac_address,
                    gcm_registration_id=gcm_registration_id,
                    correlation_identifier=correlation_id,
                    device_urlsafe_key=device.key.urlsafe(),
                    details=details)
                directory_api_update_event.put()
                deferred.defer(update_chrome_os_device,
                               device_urlsafe_key=device.key.urlsafe(),
                               _queue='directory-api',
                               _countdown=60)
            return device
        else:
            info = 'register_device: requested device not found in directory API for MAC address = {0}.'.format(
                lowercase_device_mac_address)
            logging.info(info)
            device_not_found_event = IntegrationEventLog.create(
                event_category='Registration',
                component_name='Chrome Directory API',
                workflow_step='Requested device not found',
                mac_address=mac_address,
                gcm_registration_id=gcm_registration_id,
                device_urlsafe_key=urlsafe_key,
                correlation_identifier=correlation_id)
            device_not_found_event.put()
            if new_page_token:
                device_not_found_event.details = 'Calling register_device with new page token.'
                device.put()
                deferred.defer(register_device,
                               urlsafe_key=urlsafe_key,
                               mac_address=mac_address,
                               gcm_registration_id=gcm_registration_id,
                               correlation_id=correlation_id,
                               domain_name=domain_name,
                               page_token=new_page_token)
    else:
        api_response_event.details = 'No devices returned from Chrome Directory API.'
        api_response_event.put()
