from webapp2 import RequestHandler

from workflow.interrogate_chrome_os_device_by_mac_address import interrogate_chrome_os_device_by_mac_address

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class ChromeDeviceManagementHandler(RequestHandler):

    def get_by_parameters(self):
        impersonation_email = self.request.get('impersonationEmail')
        device_mac_address = self.request.get('macAddress')
        if device_mac_address and impersonation_email:
            interrogate_chrome_os_device_by_mac_address(device_mac_address=device_mac_address,
                                                        impersonation_email=impersonation_email)
        else:
            message = 'Missing information in request body.'
            return self.response.set_status(400, message)
        self.response.set_status(200, 'OK')

    def get_list(self):
        impersonation_email = self.request.get('impersonationEmail')
        self.response.set_status(200, 'OK')

    def get_count(self):
        impersonation_email = self.request.get('impersonationEmail')
        self.response.set_status(200, 'OK')
