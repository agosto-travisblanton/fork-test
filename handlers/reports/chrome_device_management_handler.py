from webapp2 import RequestHandler

from integrations.directory_api.get_chrome_os_devices import get_chrome_os_devices, get_chrome_os_devices_count, \
    get_chrome_os_device_by_mac_address
from restler.serializers import json_response
from strategy import CHROME_OS_DEVICE_STRATEGY

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class ChromeDeviceManagementHandler(RequestHandler):
    def get_device_by_parameters(self):
        impersonation_email = self.request.get('impersonationEmail')
        device_mac_address = self.request.get('macAddress')
        if device_mac_address and impersonation_email:
            device = get_chrome_os_device_by_mac_address(device_mac_address=device_mac_address,
                                                         impersonation_email=impersonation_email)
            print('{0}; {1}; {2}; {3}'.format(
                device.get('macAddress'),
                device.get('serialNumber'),
                device.get('orgUnitPath'),
                device.get('status')))
            json_response(self.response, device, strategy=CHROME_OS_DEVICE_STRATEGY)
        else:
            message = 'Missing information in request body.'
            return self.response.set_status(400, message)
        self.response.set_status(200, 'OK')

    def get_device_list(self):
        impersonation_email = self.request.get('impersonationEmail')
        if impersonation_email:
            active_only = self.request.get('activeOnly')
            inactive_only = self.request.get('inactiveOnly')
            if active_only:
                status_filter = 'active'
            elif inactive_only:
                status_filter = 'inactive'
            else:
                status_filter = None
            devices = get_chrome_os_devices(impersonation_email=impersonation_email, status_filter=status_filter)
            for device in devices:
                print('{0}; {1}; {2}; {3}'.format(
                    device.get('macAddress'),
                    device.get('serialNumber'),
                    device.get('orgUnitPath'),
                    device.get('status')))
            json_response(self.response, devices, strategy=CHROME_OS_DEVICE_STRATEGY)
        else:
            message = 'Missing information in request body.'
            return self.response.set_status(400, message)
        self.response.set_status(200, 'OK')

    def get_devices_count(self):
        impersonation_email = self.request.get('impersonationEmail')
        if impersonation_email:
            active_only = self.request.get('activeOnly')
            inactive_only = self.request.get('inactiveOnly')
            if active_only:
                status_filter = 'active'
            elif inactive_only:
                status_filter = 'inactive'
            else:
                status_filter = None
            count = get_chrome_os_devices_count(impersonation_email=impersonation_email, status_filter=status_filter)
            print('{0}'.format(count.get('chrome_os_devices_count')))
            json_response(self.response, count)
        else:
            message = 'Missing information in request body.'
            return self.response.set_status(400, message)
        self.response.set_status(200, 'OK')
