from app_config import config
from googleapiclient import discovery
from httplib2 import Http
from oauth2client.client import SignedJwtAssertionCredentials

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
    KEY_ANNOTATED_USER = 'annotatedUser'
    KEY_ORG_UNIT_PATH = 'orgUnitPath'
    KEY_ANNOTATED_LOCATION = 'annotatedLocation'
    KEY_ANNOTATED_ASSET_ID = 'annotatedAssetId'
    KEY_NOTES = 'notes'
    KEY_CHROMEOSDEVICES = 'chromeosdevices'
    KEY_NEXTPAGETOKEN = 'nextPageToken'

    def __init__(self, admin_to_impersonate_email_address, prod_credentials=False):
        if prod_credentials is True:
            self.credentials = SignedJwtAssertionCredentials(config.SERVICE_ACCOUNT_EMAIL,
                                                             private_key=config.PRIVATE_KEY,
                                                             scope=self.DIRECTORY_SERVICE_SCOPES,
                                                             sub=admin_to_impersonate_email_address)
        else:
            key_file = '{}/privatekeys/skykit-provisioning.pem'.format(config.APP_ROOT)
            with open(key_file) as f:
                private_key = f.read()
            self.credentials = SignedJwtAssertionCredentials(
                '613606096818-3hehucjfgbtj56pu8dduuo36uccccen0@developer.gserviceaccount.com',
                private_key=private_key,
                scope=self.DIRECTORY_SERVICE_SCOPES,
                sub=admin_to_impersonate_email_address)
        self.authorized_http = self.credentials.authorize(Http())
        self.discovery_service = discovery.build('admin', 'directory_v1', http=self.authorized_http)

    # https://developers.google.com/admin-sdk/directory/v1/reference/chromeosdevices/list
    def list(self, customer_id, page_token=None):
        """
        Obtain a list of Chrome OS devices associated with a customer.

        :param customer_id: An identifier for a customer.
        :return: An array of Chrome OS devices.
        """
        results = []
        chrome_os_devices_api = self.discovery_service.chromeosdevices()
        while True:
            # https://google-api-client-libraries.appspot.com/documentation/admin/directory_v1/python/latest/admin_directory_v1.chromeosdevices.html#list
            if page_token is None:
                request = chrome_os_devices_api.list(customerId=customer_id,
                                                     orderBy='serialNumber',
                                                     projection=self.PROJECTION_FULL,
                                                     maxResults=self.MAX_RESULTS,
                                                     sortOrder=self.SORT_ORDER_ASCENDING)
            else:
                request = chrome_os_devices_api.list(customerId=customer_id,
                                                     orderBy='serialNumber',
                                                     projection=self.PROJECTION_FULL,
                                                     pageToken=page_token,
                                                     maxResults=self.MAX_RESULTS,
                                                     sortOrder=self.SORT_ORDER_ASCENDING)
            current_page_json = request.execute()
            chrome_os_devices = current_page_json.get(self.KEY_CHROMEOSDEVICES)
            page_token = current_page_json.get(self.KEY_NEXTPAGETOKEN)
            if chrome_os_devices is not None:
                results.extend(chrome_os_devices)
            if page_token is None:
                break
        return results

    # https://developers.google.com/admin-sdk/directory/v1/reference/chromeosdevices/list
    def cursor_list(self, customer_id, next_page_token=None):
        """
        Obtain a list of Chrome OS devices associated with a customer.

        :param customer_id: An identifier for a customer.
        :return: An array of Chrome OS devices.
        """
        results = []
        chrome_os_devices_api = self.discovery_service.chromeosdevices()
        # https://google-api-client-libraries.appspot.com/documentation/admin/directory_v1/python/latest/admin_directory_v1.chromeosdevices.html#list
        if next_page_token is None:
            request = chrome_os_devices_api.list(customerId=customer_id,
                                                 orderBy='serialNumber',
                                                 projection=self.PROJECTION_FULL,
                                                 maxResults=self.MAX_RESULTS,
                                                 sortOrder=self.SORT_ORDER_ASCENDING)
        else:
            request = chrome_os_devices_api.list(customerId=customer_id,
                                                 orderBy='serialNumber',
                                                 projection=self.PROJECTION_FULL,
                                                 pageToken=next_page_token,
                                                 maxResults=self.MAX_RESULTS,
                                                 sortOrder=self.SORT_ORDER_ASCENDING)
        current_page_json = request.execute()
        chrome_os_devices = current_page_json.get(self.KEY_CHROMEOSDEVICES)
        next_page_token = current_page_json.get(self.KEY_NEXTPAGETOKEN)
        if chrome_os_devices is not None:
            results.extend(chrome_os_devices)
        return results, next_page_token

    # https://developers.google.com/admin-sdk/directory/v1/reference/chromeosdevices/get
    def get(self, customer_id, device_id):
        """
        Retrieve the metadata for a specific Chrome OS device.

        :param customer_id: The customer identifier.
        :param device_id: The device key value.
        :return:
        """
        chrome_os_devices_api = self.discovery_service.chromeosdevices()
        request = chrome_os_devices_api.get(customerId=customer_id, deviceId=device_id)
        return request.execute()

    # https://developers.google.com/admin-sdk/directory/v1/reference/chromeosdevices/update
    def update(self, customer_id, device_id, annotated_user=None, annotated_location=None, notes=None,
               org_unit_path=None, annotated_asset_id=None):
        """
        Update a Chrome OS device with annotated user, location and notes information.

        :param customer_id:
        :param device_id:
        :param annotated_user:
        :param annotated_location:
        :param notes:
        :param org_unit_path:
        :param annotated_asset_id:
        :return:
        """
        if device_id:
            resource_json = self.get(customer_id, device_id)
            if resource_json is not None:
                if org_unit_path is not None:
                    resource_json['orgUnitPath'] = org_unit_path
                if notes is not None:
                    resource_json['notes'] = notes
                if annotated_location is not None:
                    resource_json['annotatedLocation'] = annotated_location
                if annotated_user is not None:
                    resource_json['annotatedUser'] = annotated_user
                if annotated_asset_id is not None:
                    resource_json['annotatedAssetId'] = annotated_asset_id

                chrome_os_devices_api = self.discovery_service.chromeosdevices()
                request = chrome_os_devices_api.update(customerId=customer_id,
                                                       deviceId=device_id,
                                                       body=resource_json)
                request.execute()

