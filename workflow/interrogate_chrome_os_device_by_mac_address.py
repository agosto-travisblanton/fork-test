from google.appengine.ext.deferred import deferred

from app_config import config
from chrome_os_devices_api import ChromeOsDevicesApi

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


def interrogate_chrome_os_device_by_mac_address(device_mac_address, impersonation_admin_email_address, page_token=None):
    if device_mac_address is None:
        raise deferred.PermanentTaskFailure('The device MAC address parameter is None. It is required.')
    chrome_os_devices_api = ChromeOsDevicesApi(impersonation_admin_email_address, prod_credentials=True)
    chrome_os_devices, new_page_token = chrome_os_devices_api.cursor_list(customer_id=config.GOOGLE_CUSTOMER_ID,
                                                                          next_page_token=page_token)
    if chrome_os_devices is not None and len(chrome_os_devices) > 0:
        lowercase_device_mac_address = device_mac_address.lower()
        loop_comprehension = (x for x in chrome_os_devices if x.get('macAddress') == lowercase_device_mac_address or
                              x.get('ethernetMacAddress') == lowercase_device_mac_address)
        chrome_os_device = next(loop_comprehension, None)
        if chrome_os_device is not None:
            device_id = chrome_os_device.get('deviceId')
            mac_address = chrome_os_device.get('macAddress')
            serial_number = chrome_os_device.get('serialNumber')
            status = chrome_os_device.get('status')
            last_sync = chrome_os_device.get('lastSync')
            kind = chrome_os_device.get('kind')
            ethernet_mac_address = chrome_os_device.get('ethernetMacAddress')
            org_unit_path = chrome_os_device.get('orgUnitPath')
            annotated_user = chrome_os_device.get('annotatedUser')
            annotated_location = chrome_os_device.get('annotatedLocation')
            annotated_asset_id = chrome_os_device.get('annotatedAssetId')
            notes = chrome_os_device.get('notes')
            boot_mode = chrome_os_device.get('bootMode')
            last_enrollment_time = chrome_os_device.get('lastEnrollmentTime')
            platform_version = chrome_os_device.get('platformVersion')
            model = chrome_os_device.get('model')
            os_version = chrome_os_device.get('osVersion')
            firmware_version = chrome_os_device.get('firmwareVersion')
            etag = chrome_os_device.get('etag')
            return
        else:
            if new_page_token is not None:
                deferred.defer(interrogate_chrome_os_device_by_mac_address,
                               device_mac_address=device_mac_address,
                               page_token=new_page_token)
