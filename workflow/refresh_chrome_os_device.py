import logging

from google.appengine.ext import ndb
from google.appengine.ext.deferred import deferred

from agar.env import on_development_server
from app_config import config
from chrome_os_devices_api import (ChromeOsDevicesApi)

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


def refresh_chrome_os_device(device_urlsafe_key):
    if on_development_server:
        return
    """
    A function that is meant to be run asynchronously to update the device entity
    with ChromeOsDevice information from Directory API using the device ID to match.
    """
    if device_urlsafe_key is None:
        raise deferred.PermanentTaskFailure('The device url-safe key parameter is None. It is required.')
    device_key = ndb.Key(urlsafe=device_urlsafe_key)
    device = device_key.get()
    if None == device.device_id:
        logging.error('Did not refresh in refresh_chrome_os_device because no device_id available.')
        return
    impersonation_admin_email_address = device.get_impersonation_email()
    if None == impersonation_admin_email_address:
        logging.info('Impersonation email not found for device with device key {0}.'.format(device_urlsafe_key))
        return
    chrome_os_device = None
    chrome_os_devices_api = ChromeOsDevicesApi(impersonation_admin_email_address)
    try:
        chrome_os_device = chrome_os_devices_api.get(config.GOOGLE_CUSTOMER_ID, device.device_id)
    except Exception, e:
        logging.exception(e)
    if chrome_os_device is not None:
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
        device.annotated_asset_id = chrome_os_device.get('annotatedAssetId')
        device.notes = chrome_os_device.get('notes')
        device.boot_mode = chrome_os_device.get('bootMode')
        device.last_enrollment_time = chrome_os_device.get('lastEnrollmentTime')
        device.platform_version = chrome_os_device.get('platformVersion')
        device.model = chrome_os_device.get('model')
        device.os_version = chrome_os_device.get('osVersion')
        device.firmware_version = chrome_os_device.get('firmwareVersion')
        device.etag = chrome_os_device.get('etag')
        device.put()
        logging.info('Refreshed device_id = {0}, impersonating {1}'.
                     format(device.device_id, impersonation_admin_email_address))
    else:
        logging.info('Directory API lookup failure for device_id = {0}, impersonating {1}'.
                     format(device.device_id, impersonation_admin_email_address))
