from app_config import config
from integrations.device_management.chrome_os_devices_api import ChromeOsDevicesApi

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


def interrogate_chrome_os_devices(impersonation_email, page_token=None):
    active_devices = []
    chrome_os_devices_api = ChromeOsDevicesApi(impersonation_email, prod_credentials=True)
    # chrome_os_devices, new_page_token = chrome_os_devices_api.cursor_list(customer_id=config.GOOGLE_CUSTOMER_ID,
    #                                                                       next_page_token=page_token)
    chrome_os_devices = chrome_os_devices_api.list(customer_id=config.GOOGLE_CUSTOMER_ID)
    if chrome_os_devices is not None and len(chrome_os_devices) > 0:
        # foobars = (x for x in chrome_os_devices if x.get('status') == 'ACTIVE')
        for chrome_os_device in chrome_os_devices:
            if chrome_os_device.get('status') == 'ACTIVE':
                device = {'org_unit_path': chrome_os_device.get('orgUnitPath'),
                          'serial_number': chrome_os_device.get('serialNumber')
                }
                # org_unit_path = chrome_os_device.get('orgUnitPath')
                # serial_number = chrome_os_device.get('serialNumber')
                # org_unit_path = chrome_os_device.get('orgUnitPath')
                # device_id = chrome_os_device.get('deviceId')
                # status = chrome_os_device.get('status')
                active_devices.append(device)

        # if chrome_os_device is not None:
        #     device_id = chrome_os_device.get('deviceId')
        #     mac_address = chrome_os_device.get('macAddress')
        #     serial_number = chrome_os_device.get('serialNumber')
        #     org_unit_path = chrome_os_device.get('orgUnitPath')
        #     status = chrome_os_device.get('status')
        return active_devices

