import logging

from google.appengine.ext import ndb
from google.appengine.ext.deferred import deferred

from app_config import config
from chrome_os_devices_api import (ChromeOsDevicesApi)

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


def update_chrome_os_device(device_urlsafe_key=None):
    """
    A function that is meant to be run asynchronously to update the ChromeOsDevice
    information from Directory API with information found on the device entity.
    :param device_urlsafe_key: our device key
    """
    if device_urlsafe_key is None:
        raise deferred.PermanentTaskFailure('The device URL-safe key parameter is None.  It is required.')
    device = ndb.Key(urlsafe=device_urlsafe_key).get()
    impersonation_admin_email_address = device.get_impersonation_email()
    if None == impersonation_admin_email_address:
        logging.info('Impersonation email not found for device with device key {0}.'.format(device_urlsafe_key))
        return
    chrome_os_devices_api = ChromeOsDevicesApi(impersonation_admin_email_address)
    annotated_asset_id = device_urlsafe_key
    if not None == device.annotated_asset_id:
        annotated_asset_id = device.annotated_asset_id
    chrome_os_devices_api.update(config.GOOGLE_CUSTOMER_ID,
                                 device.device_id,
                                 annotated_user=device.annotated_user,
                                 annotated_location=device.annotated_location,
                                 notes=device.notes,
                                 org_unit_path=device.org_unit_path,
                                 annotated_asset_id=annotated_asset_id)
