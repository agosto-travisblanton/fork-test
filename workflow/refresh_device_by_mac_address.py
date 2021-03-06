import logging

from google.appengine.ext import ndb
from google.appengine.ext.deferred import deferred

from app_config import config
from integrations.content_manager.content_manager_api import ContentManagerApi
from integrations.directory_api.chrome_os_devices_api import ChromeOsDevicesApi
from model_entities.integration_events_log_model import IntegrationEventLog

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


def refresh_device_by_mac_address(device_urlsafe_key, device_mac_address,
                                  device_has_previous_directory_api_info=False, page_token=None):
    """
    A function that is meant to be run asynchronously to update the device entity
    with ChromeOsDevice information from Directory API using the MAC address to match.
    :param device_has_previous_directory_api_info: indicates if device has any info from Directory API.
    :param page_token: a google api page marker for where you are in the larger list. Fetches in chunks of 100 records.
    :param device_mac_address: the device's MAC address
    :param device_urlsafe_key: our device key
    """
    if device_urlsafe_key is None:
        raise deferred.PermanentTaskFailure('The device URL-safe key parameter is None. It is required.')
    if device_mac_address is None:
        raise deferred.PermanentTaskFailure('The device MAC address parameter is None. It is required.')
    device_key = ndb.Key(urlsafe=device_urlsafe_key)
    device = device_key.get()
    if None == device:
        logging.error('Unable to find device by device_urlsafe_key: {0}'.format(device_urlsafe_key))
        return
    if device.tenant_key is None:
        logging.info('Tenant not known. Unable to refresh device by device_urlsafe_key: {0}'.format(device_urlsafe_key))
        return
    tenant = device.get_tenant()
    impersonation_email = tenant.get_domain().impersonation_admin_email_address
    if None == impersonation_email:
        logging.info('Impersonation email not found for device with device key {0}.'.format(device_urlsafe_key))
        return
    chrome_os_devices_api = ChromeOsDevicesApi(impersonation_email)
    chrome_os_devices, new_page_token = chrome_os_devices_api.cursor_list(customer_id=config.GOOGLE_CUSTOMER_ID,
                                                                          next_page_token=page_token)
    if chrome_os_devices is not None and len(chrome_os_devices) > 0:
        lowercase_device_mac_address = device_mac_address.lower()
        loop_comprehension = (x for x in chrome_os_devices if x.get('macAddress') == lowercase_device_mac_address or
                              x.get('ethernetMacAddress') == lowercase_device_mac_address)
        chrome_os_device = next(loop_comprehension, None)
        if chrome_os_device is not None:
            device_key = ndb.Key(urlsafe=device_urlsafe_key)
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
            device.put()
            logging.info('Refreshed device_id = {0} by MAC address = {1}'.
                         format(device.device_id, lowercase_device_mac_address))

            if device.registration_correlation_identifier:
                correlation_id = device.registration_correlation_identifier
            else:
                correlation_id = 'NA'
            if not device_has_previous_directory_api_info:
                cm_create_device_event_request = IntegrationEventLog.create(
                     event_category='Registration',
                     component_name='Content Manager',
                     workflow_step='Request to Content Manager for a create_device',
                     mac_address=device.mac_address,
                     gcm_registration_id=device.gcm_registration_id,
                     device_urlsafe_key=device_urlsafe_key,
                     serial_number=device.serial_number,
                     correlation_identifier=correlation_id,
                     details='refresh_device_by_mac_address: Found device. Will notify Content Manager.')
                cm_create_device_event_request.put()
                deferred.defer(ContentManagerApi().create_device,
                               device_urlsafe_key=device_urlsafe_key,
                               correlation_id=correlation_id,
                               _queue='content-server')
            return device
        else:
            if new_page_token is not None:
                deferred.defer(refresh_device_by_mac_address,
                               device_urlsafe_key=device_urlsafe_key,
                               device_mac_address=device_mac_address,
                               page_token=new_page_token,
                               _queue='directory-api')
