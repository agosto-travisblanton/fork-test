from webapp2 import RequestHandler

from workflow.interrogate_chrome_os_device_by_mac_address import interrogate_chrome_os_device_by_mac_address

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class DirectoryApiHandler(RequestHandler):

    def get_device_by_parameter(self):
        device_mac_address = self.request.get('macAddress')
        if device_mac_address:
            interrogate_chrome_os_device_by_mac_address(device_mac_address=device_mac_address,
                                                        impersonation_admin_email_address='skykit.api@fschrome.com')
        self.response.set_status(200, 'OK')
