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

    MAX_RESULTS = 100
    PROJECTION_FULL = 'FULL'
    PROJECTION_BASIC = 'BASIC'
    SORT_ORDER_ASCENDING = 'ASCENDING'
    SORT_ORDER_DESCENDING = 'DESCENDING'

    def __init__(self, admin_email_address):
        self.credentials = SignedJwtAssertionCredentials(config.SERVICE_ACCOUNT_EMAIL,
                                                    config.PRIVATE_KEY,
                                                    scope=self.DIRECTORY_SERVICE_SCOPES,
                                                    sub=admin_email_address)
        self.authorized_http = self.credentials.authorize(httplib2.Http())
        self.discovery_service = discovery.build('admin', 'directory_v1', http=self.authorized_http)

    # https://developers.google.com/admin-sdk/directory/v1/reference/chromeosdevices/list
    def list(self, customer_id):
        """
        Obtain a list of Chrome OS devices associated with a customer.

        :param customer_id: An identifier for a customer.
        :return: An array of Chrome OS devices.
        """
        KEY_CHROMEOSDEVICES = 'chromeosdevices'
        KEY_NEXTPAGETOKEN = 'nextPageToken'
        results = []
        page_token = None
        chromeosdevices_api = self.discovery_service.chromeosdevices()
        while True:
            # https://google-api-client-libraries.appspot.com/documentation/admin/directory_v1/python/latest/admin_directory_v1.chromeosdevices.html#list
            request = chromeosdevices_api.list(customerId=customer_id,
                                               orderBy='serialNumber',
                                               projection=self.PROJECTION_FULL,
                                               pageToken=page_token,
                                               maxResults=self.MAX_RESULTS,
                                               sortOrder=self.SORT_ORDER_ASCENDING,
                                               query=None)
            current_page_json = request.execute()
            results.extend(current_page_json[KEY_CHROMEOSDEVICES])
            page_token = current_page_json.get(KEY_NEXTPAGETOKEN)
            if not page_token:
                break
        return results


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
