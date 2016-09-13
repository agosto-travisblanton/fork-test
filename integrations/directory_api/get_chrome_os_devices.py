from app_config import config
from integrations.directory_api.chrome_os_devices_api import ChromeOsDevicesApi

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


def get_chrome_os_devices(impersonation_email, status_filter=None, int_credentials=True, prod_credentials=False):
    devices = []
    chrome_os_devices_api = ChromeOsDevicesApi(impersonation_email, int_credentials=int_credentials,
                                               prod_credentials=prod_credentials)
    chrome_os_devices = chrome_os_devices_api.list(
        customer_id=config.GOOGLE_CUSTOMER_ID,
        projection='FULL',
        max_results=1000)
    if chrome_os_devices is not None and len(chrome_os_devices) > 0:
        for chrome_os_device in chrome_os_devices:
            if status_filter is 'active':
                if chrome_os_device.get('status') == 'ACTIVE' or chrome_os_device.get('status') == 'PROVISIONED':
                    devices.append(chrome_os_device)
            elif status_filter is 'inactive':
                if chrome_os_device.get('status') != 'ACTIVE' and chrome_os_device.get('status') != 'PROVISIONED':
                    devices.append(chrome_os_device)
            else:
                devices.append(chrome_os_device)
        return devices


def get_chrome_os_devices_count(impersonation_email, status_filter=None):
    chrome_os_devices_api = ChromeOsDevicesApi(impersonation_email, prod_credentials=True)
    chrome_os_devices = chrome_os_devices_api.list(
        customer_id=config.GOOGLE_CUSTOMER_ID,
        projection='BASIC',
        max_results=1000)
    count = 0
    if chrome_os_devices is not None and len(chrome_os_devices) > 0:
        for chrome_os_device in chrome_os_devices:
            if status_filter is 'active':
                if chrome_os_device.get('status') == 'ACTIVE' or chrome_os_device.get('status') == 'PROVISIONED':
                    count += 1
            elif status_filter is 'inactive':
                if chrome_os_device.get('status') != 'ACTIVE' and chrome_os_device.get('status') != 'PROVISIONED':
                    count += 1
            else:
                count += 1
    return {
        'chrome_os_devices_count': count
    }


def get_chrome_os_device_by_mac_address(device_mac_address, impersonation_email):
    chrome_os_devices_api = ChromeOsDevicesApi(impersonation_email, int_credentials=True)
    chrome_os_devices = chrome_os_devices_api.list(
        customer_id=config.GOOGLE_CUSTOMER_ID,
        projection='FULL',
        max_results=1000)
    device = None
    if chrome_os_devices is not None and len(chrome_os_devices) > 0:
        lowercase_mac_address = device_mac_address.lower()
        for chrome_os_device in chrome_os_devices:
            if chrome_os_device.get('macAddress') == lowercase_mac_address or chrome_os_device.get(
                    'ethernetMacAddress') == lowercase_mac_address:
                device = chrome_os_device
    return device
