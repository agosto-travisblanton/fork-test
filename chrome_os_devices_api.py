import logging

from google.appengine.ext import ndb
from google.appengine.ext.deferred import deferred

from oauth2client.client import SignedJwtAssertionCredentials
from googleapiclient import discovery
from httplib2 import Http
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
    KEY_ANNOTATED_USER = 'annotatedUser'
    KEY_ORG_UNIT_PATH = 'orgUnitPath'
    KEY_ANNOTATED_LOCATION = 'annotatedLocation'
    KEY_NOTES = 'notes'
    KEY_CHROMEOSDEVICES = 'chromeosdevices'
    KEY_NEXTPAGETOKEN = 'nextPageToken'

    def __init__(self, admin_to_impersonate_email_address):
        self.credentials = SignedJwtAssertionCredentials(config.SERVICE_ACCOUNT_EMAIL,
                                                         private_key=config.PRIVATE_KEY,
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
        chromeosdevices_api = self.discovery_service.chromeosdevices()
        while True:
            # https://google-api-client-libraries.appspot.com/documentation/admin/directory_v1/python/latest/admin_directory_v1.chromeosdevices.html#list
            if page_token is None:
                request = chromeosdevices_api.list(customerId=customer_id,
                                                   orderBy='serialNumber',
                                                   projection=self.PROJECTION_FULL,
                                                   maxResults=self.MAX_RESULTS,
                                                   sortOrder=self.SORT_ORDER_ASCENDING)
            else:
                request = chromeosdevices_api.list(customerId=customer_id,
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
        chromeosdevices_api = self.discovery_service.chromeosdevices()
        # https://google-api-client-libraries.appspot.com/documentation/admin/directory_v1/python/latest/admin_directory_v1.chromeosdevices.html#list
        if next_page_token is None:
            request = chromeosdevices_api.list(customerId=customer_id,
                                               orderBy='serialNumber',
                                               projection=self.PROJECTION_FULL,
                                               maxResults=self.MAX_RESULTS,
                                               sortOrder=self.SORT_ORDER_ASCENDING)
        else:
            request = chromeosdevices_api.list(customerId=customer_id,
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
        chromeosdevices_api = self.discovery_service.chromeosdevices()
        request = chromeosdevices_api.get(customerId=customer_id, deviceId=device_id)
        return request.execute()

    # https://developers.google.com/admin-sdk/directory/v1/reference/chromeosdevices/update
    def update(self, customer_id, device_id, annotated_user=None, annotated_location=None, notes=None,
               org_unit_path=None):
        """
        Update a Chrome OS device with annotated user, location and notes information.

        :param customer_id:
        :param device_id:
        :param annotated_user:
        :param annotated_location:
        :param notes:
        :param org_unit_path:
        :return:
        """
        resource_json = self.get(customer_id, device_id)
        if resource_json is not None:
            chromeosdevices_api = self.discovery_service.chromeosdevices()
            if org_unit_path is not None:
                resource_json['orgUnitPath'] = org_unit_path
            if notes is not None:
                resource_json['notes'] = notes
            if annotated_location is not None:
                resource_json['annotatedLocation'] = annotated_location
            if annotated_user is not None:
                resource_json['annotatedUser'] = annotated_user
            request = chromeosdevices_api.update(customerId=customer_id,
                                                 deviceId=device_id,
                                                 body=resource_json)
            request.execute()


def refresh_display_by_mac_address(display_urlsafe_key=None, device_mac_address=None, page_token=None):
    """
    A function that is meant to be run asynchronously to update the Display entity
    with ChromeOsDevice information from Directory API using the MAC address to match.
    """
    if display_urlsafe_key is None:
        raise deferred.PermanentTaskFailure('The Display URL-safe key parameter is None.  It is required.')
    if device_mac_address is None:
        raise deferred.PermanentTaskFailure('The device MAC address parameter is None.  It is required.')
    chrome_os_devices_api = ChromeOsDevicesApi(config.IMPERSONATION_ADMIN_EMAIL_ADDRESS)
    chrome_os_devices, new_page_token = chrome_os_devices_api.cursor_list(customer_id=config.GOOGLE_CUSTOMER_ID,
                                                                          next_page_token=page_token)
    if chrome_os_devices is not None and len(chrome_os_devices) > 0:
        lowercase_device_mac_address = device_mac_address.lower()
        loop_comprehension = (x for x in chrome_os_devices if x.get('macAddress') == lowercase_device_mac_address or
                              x.get('ethernetMacAddress') == lowercase_device_mac_address)
        chrome_os_device = next(loop_comprehension, None)
        if chrome_os_device is not None:
            display_key = ndb.Key(urlsafe=display_urlsafe_key)
            display = display_key.get()
            display.device_id = chrome_os_device.get('deviceId')
            display.mac_address = chrome_os_device.get('macAddress')
            display.serial_number = chrome_os_device.get('serialNumber')
            display.status = chrome_os_device.get('status')
            display.last_sync = chrome_os_device.get('lastSync')
            display.kind = chrome_os_device.get('kind')
            display.ethernet_mac_address = chrome_os_device.get('ethernetMacAddress')
            display.org_unit_path = chrome_os_device.get('orgUnitPath')
            display.annotated_user = chrome_os_device.get('annotatedUser')
            display.annotated_location = chrome_os_device.get('annotatedLocation')
            display.notes = chrome_os_device.get('notes')
            display.boot_mode = chrome_os_device.get('bootMode')
            display.last_enrollment_time = chrome_os_device.get('lastEnrollmentTime')
            display.platform_version = chrome_os_device.get('platformVersion')
            display.model = chrome_os_device.get('model')
            display.os_version = chrome_os_device.get('osVersion')
            display.firmware_version = chrome_os_device.get('firmwareVersion')
            display.managed_display = True
            display.put()
            return display
        else:
            if new_page_token is not None:
                deferred.defer(refresh_display_by_mac_address,
                               display_urlsafe_key=display_urlsafe_key,
                               device_mac_address=device_mac_address,
                               page_token=new_page_token)


def refresh_display(display_urlsafe_key=None):
    """
    A function that is meant to be run asynchronously to update the Display entity
    with ChromeOsDevice information from Directory API using the device ID to match.
    """
    if display_urlsafe_key is None:
        raise deferred.PermanentTaskFailure('The Display URL-safe key parameter is None.  It is required.')
    display_key = ndb.Key(urlsafe=display_urlsafe_key)
    display = display_key.get()
    chrome_os_devices_api = ChromeOsDevicesApi(config.IMPERSONATION_ADMIN_EMAIL_ADDRESS)
    chrome_os_device = chrome_os_devices_api.get(config.GOOGLE_CUSTOMER_ID, display.device_id)
    if chrome_os_device is not None:
        display.device_id = chrome_os_device.get('deviceId')
        display.mac_address = chrome_os_device.get('macAddress')
        display.serial_number = chrome_os_device.get('serialNumber')
        display.status = chrome_os_device.get('status')
        display.last_sync = chrome_os_device.get('lastSync')
        display.kind = chrome_os_device.get('kind')
        display.ethernet_mac_address = chrome_os_device.get('ethernetMacAddress')
        display.org_unit_path = chrome_os_device.get('orgUnitPath')
        display.annotated_user = chrome_os_device.get('annotatedUser')
        display.annotated_location = chrome_os_device.get('annotatedLocation')
        display.notes = chrome_os_device.get('notes')
        display.boot_mode = chrome_os_device.get('bootMode')
        display.last_enrollment_time = chrome_os_device.get('lastEnrollmentTime')
        display.platform_version = chrome_os_device.get('platformVersion')
        display.model = chrome_os_device.get('model')
        display.os_version = chrome_os_device.get('osVersion')
        display.firmware_version = chrome_os_device.get('firmwareVersion')
        display.managed_display = True
        display.put()


def refresh_chrome_os_display(device_urlsafe_key=None):
    """
    A function that is meant to be run asynchronously to update the Display entity
    with ChromeOsDevice information from Directory API using the device ID to match.
    """
    if device_urlsafe_key is None:
        raise deferred.PermanentTaskFailure('The device url-safe key parameter is None. It is required.')
    device_key = ndb.Key(urlsafe=device_urlsafe_key)
    device = device_key.get()
    chrome_os_devices_api = ChromeOsDevicesApi(config.IMPERSONATION_ADMIN_EMAIL_ADDRESS)
    chrome_os_device = chrome_os_devices_api.get(config.GOOGLE_CUSTOMER_ID, device.device_id)
    if chrome_os_device is not None:
        device.device_id = chrome_os_device.get('deviceId')
        device.mac_address = chrome_os_device.get('macAddress')
        device.serial_number = chrome_os_device.get('serialNumber')
        device.status = chrome_os_device.get('status')
        device.last_sync = chrome_os_device.get('lastSync')
        device.kind = chrome_os_device.get('kind')
        device.ethernet_mac_address = chrome_os_device.get('ethernetMacAddress')
        device.org_unit_path = chrome_os_device.get('orgUnitPath')
        device.annotated_user = chrome_os_device.get('annotatedUser')
        device.annotated_location = chrome_os_device.get('annotatedLocation')
        device.notes = chrome_os_device.get('notes')
        device.boot_mode = chrome_os_device.get('bootMode')
        device.last_enrollment_time = chrome_os_device.get('lastEnrollmentTime')
        device.platform_version = chrome_os_device.get('platformVersion')
        device.model = chrome_os_device.get('model')
        device.os_version = chrome_os_device.get('osVersion')
        device.firmware_version = chrome_os_device.get('firmwareVersion')
        device.put()
    else:
        logging.debug('Directory API lookup failure for device_id = {0}, impersonating {1}'.
                      format(device.device_id, config.IMPERSONATION_ADMIN_EMAIL_ADDRESS))


def update_chrome_os_device(display_urlsafe_key=None):
    """
    A function that is meant to be run asynchronously to update the ChromeOsDevice
    information from Directory API with information found on the Display entity.
    """
    if display_urlsafe_key is None:
        raise deferred.PermanentTaskFailure('The Display URL-safe key parameter is None.  It is required.')
    display = ndb.Key(urlsafe=display_urlsafe_key).get()
    chrome_os_devices_api = ChromeOsDevicesApi(config.IMPERSONATION_ADMIN_EMAIL_ADDRESS)
    chrome_os_devices_api.update(config.GOOGLE_CUSTOMER_ID,
                                 display.device_id,
                                 annotated_user=display.annotated_user,
                                 annotated_location=display.annotated_location,
                                 notes=display.notes,
                                 org_unit_path=display.org_unit_path)
