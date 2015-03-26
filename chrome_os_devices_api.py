from google.appengine.api import urlfetch
import httplib2
from apiclient import discovery
from oauth2client.client import SignedJwtAssertionCredentials

from app_config import config


__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class ChromeOsDevicesApi(object):
    """ Facade encapsulating the Directory API of the Admin SDK. """

    DIRECTORY_SERVICE_SCOPES = [
        'https://www.googleapis.com/auth/admin.directory.device.chromeos'
    ]

    def __init__(self, domain):
        self.domain = domain
        self.admin_user = domain.any_google_admin()
        self.any_user = self.admin_user if self.admin_user is not None else domain.any_active_user()

    def scopes_enabled(self):
        impersonate = None
        view_type = 'domain_public'
        if self.admin_user:
            impersonate = self.admin_user.email
            view_type = 'admin_view'
        elif self.any_user:
            impersonate = self.any_user.email

        result = False
        if impersonate:
            credentials = SignedJwtAssertionCredentials(config.SERVICE_ACCOUNT_EMAIL,
                                                        config.PRIVATE_KEY,
                                                        self.DIRECTORY_SERVICE_SCOPES,
                                                        sub=impersonate)
            http_auth = credentials.authorize(httplib2.Http())
            try:
                directory_service = discovery.build('admin', 'directory_v1', http=http_auth)
                # directory_service.users().get(userKey=impersonate, viewType=view_type).execute()
                result = True
            except:
                pass

        return result


    # https://developers.google.com/admin-sdk/directory/v1/reference/chromeosdevices/list
    def list(self, customer_id):
        """
        Obtain a list of Chrome OS devices associated with a customer.

        :param customer_id: An identifier for a customer.
        :return: An array of Chrome OS devices.
        """
        urlfetch.set_default_fetch_deadline(60)
        url = 'https://www.googleapis.com/admin/directory/v1/customer/{0}/devices/chromeos'.format(customer_id)
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

        response = urlfetch.fetch(url=url, method=urlfetch.GET, headers=headers)
        if response.status_code == 200:
            pass
        else:
            pass


    # https://developers.google.com/admin-sdk/directory/v1/reference/chromeosdevices/update
    def update(self, customer_id, device_id, annotated_user=None, annotated_location=None, notes=None):
        """
        Update a Chrome OS device with annotated user, location and notes information.

        :param customer_id:
        :param device_id:
        :param annotated_user:
        :param annotated_location:
        :param notes:
        :return:
        """
        pass
