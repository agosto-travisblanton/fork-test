import logging

from google.appengine.ext import ndb
from google.appengine.ext.deferred import deferred

from app_config import config
from content_manager_api import ContentManagerApi
from googleapiclient import discovery
from httplib2 import Http
from model_entities.integration_events_log_model import IntegrationEventLog
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

                chrome_os_devices_api = self.discovery_service.chromeosdevices()
                request = chrome_os_devices_api.update(customerId=customer_id,
                                                       deviceId=device_id,
                                                       body=resource_json)
                request.execute()


def register_device(device_urlsafe_key=None, device_mac_address=None, gcm_registration_id=None,
                    correlation_id=None, page_token=None):
    """
    A function that is meant to be run asynchronously to update the device entity
    with ChromeOsDevice information from Directory API using the MAC address to match.
    """
    api_request_event = IntegrationEventLog.create(
            event_category='Registration',
            component_name='Chrome Directory API',
            workflow_step='Request for device information',
            mac_address=device_mac_address,
            gcm_registration_id=gcm_registration_id,
            correlation_identifier=correlation_id)
    api_request_event.put()
    if not device_urlsafe_key:
        error_message = 'register_device: The device URL-safe key parameter is None. It is required.'
        if api_request_event:
            api_request_event.details = error_message
            api_request_event.put()
        raise deferred.PermanentTaskFailure(error_message)
    if not device_mac_address:
        error_message = 'register_device: The device MAC address parameter is None. It is required.'
        if api_request_event:
            api_request_event.details = error_message
            api_request_event.put()
        raise deferred.PermanentTaskFailure(error_message)
    impersonation_admin_email_address = get_impersonation_email_from_device_key(device_urlsafe_key)
    if not impersonation_admin_email_address:
        error_message = 'register_device: Impersonation email not found for device with device key {0}.'.format(
            device_urlsafe_key)
        if api_request_event:
            api_request_event.details = error_message
            api_request_event.put()
        logging.error(error_message)
        return

    api_response_event = IntegrationEventLog.create(
            event_category='Registration',
            component_name='Chrome Directory API',
            workflow_step='Response for device information request',
            mac_address=device_mac_address,
            gcm_registration_id=gcm_registration_id,
            correlation_identifier=correlation_id)
    api_response_event.put()

    chrome_os_devices_api = ChromeOsDevicesApi(impersonation_admin_email_address)
    chrome_os_devices, new_page_token = chrome_os_devices_api.cursor_list(customer_id=config.GOOGLE_CUSTOMER_ID,
                                                                          next_page_token=page_token)
    if chrome_os_devices and len(chrome_os_devices) > 0:
        lowercase_device_mac_address = device_mac_address.lower()
        loop_comprehension = (x for x in chrome_os_devices if x.get('macAddress') == lowercase_device_mac_address or
                              x.get('ethernetMacAddress') == lowercase_device_mac_address)
        chrome_os_device = next(loop_comprehension, None)
        if chrome_os_device:
            device_key = ndb.Key(urlsafe=device_urlsafe_key)
            device = device_key.get()
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
            device.etag = chrome_os_device.get('etag')
            device.put()

            api_response_event.serial_number = device.serial_number
            api_response_event.details = 'Chrome Directory API call success! Notifying Content Manager.'
            api_response_event.put()

            info = 'register_device: retrieved directory API for MAC address = {0}. Notifying Content Manager.' \
                .format(lowercase_device_mac_address)
            logging.info(info)

            if ContentManagerApi().create_device(device_urlsafe_key, correlation_id):
                logging.info('CM returned 201 of create_device')
            else:
                logging.error('Error notifying CM of create_device')
            return device
        else:
            if new_page_token:
                api_response_event.details = 'new page token'
                api_response_event.put()
                deferred.defer(register_device,
                               device_urlsafe_key=device_urlsafe_key,
                               device_mac_address=device_mac_address,
                               gcm_registration_id=gcm_registration_id,
                               correlation_id=correlation_id,
                               page_token=new_page_token)
    else:
        api_response_event.details = 'No devices returned from Chrome Directory API.'
        api_response_event.put()


def refresh_device_by_mac_address(device_urlsafe_key=None, device_mac_address=None, page_token=None):
    """
    A function that is meant to be run asynchronously to update the device entity
    with ChromeOsDevice information from Directory API using the MAC address to match.
    """
    if device_urlsafe_key is None:
        raise deferred.PermanentTaskFailure('The device URL-safe key parameter is None. It is required.')
    if device_mac_address is None:
        raise deferred.PermanentTaskFailure('The device MAC address parameter is None. It is required.')
    impersonation_admin_email_address = get_impersonation_email_from_device_key(device_urlsafe_key)
    if None == impersonation_admin_email_address:
        logging.info('Impersonation email not found for device with device key {0}.'.format(device_urlsafe_key))
        return
    chrome_os_devices_api = ChromeOsDevicesApi(impersonation_admin_email_address)
    chrome_os_devices, new_page_token = chrome_os_devices_api.cursor_list(customer_id=config.GOOGLE_CUSTOMER_ID,
                                                                          next_page_token=page_token)
    if chrome_os_devices is not None and len(chrome_os_devices) > 0:
        lowercase_device_mac_address = device_mac_address.lower()
        loop_comprehension = (x for x in chrome_os_devices if x.get('macAddress') == lowercase_device_mac_address or
                              x.get('ethernetMacAddress') == lowercase_device_mac_address)
        chrome_os_device = next(loop_comprehension, None)
        if chrome_os_device is not None:
            device_key = ndb.Key(urlsafe=device_urlsafe_key)
            device = device_key.get()
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
            device.etag = chrome_os_device.get('etag')
            device.put()
            logging.info('Refreshed device_id = {0} by MAC address = {1}'.
                         format(device.device_id, lowercase_device_mac_address))

            return device
        else:
            if new_page_token is not None:
                deferred.defer(refresh_device_by_mac_address,
                               device_urlsafe_key=device_urlsafe_key,
                               device_mac_address=device_mac_address,
                               page_token=new_page_token)


def refresh_device(device_urlsafe_key=None):
    """
    A function that is meant to be run asynchronously to update the device entity
    with ChromeOsDevice information from Directory API using the device ID to match.
    """
    if device_urlsafe_key is None:
        raise deferred.PermanentTaskFailure('The device URL-safe key parameter is None. It is required.')
    device_key = ndb.Key(urlsafe=device_urlsafe_key)
    device = device_key.get()
    if None == device.device_id:
        logging.info('Did not refresh in refresh_device because no device_id available.')
        return
    impersonation_admin_email_address = get_impersonation_email_from_device_key(device_urlsafe_key)
    if None == impersonation_admin_email_address:
        logging.info('Impersonation email not found for device with device key {0}.'.format(device_urlsafe_key))
        return
    chrome_os_devices_api = ChromeOsDevicesApi(impersonation_admin_email_address)
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
        device.etag = chrome_os_device.get('etag')
        device.put()
        logging.info('Refreshed device_id = {0}, impersonating {1}'.
                     format(device.device_id, impersonation_admin_email_address))

    else:
        logging.info('Directory API lookup failure for device_id = {0}, impersonating {1}'.
                     format(device.device_id, impersonation_admin_email_address))


def refresh_chrome_os_device(device_urlsafe_key=None):
    """
    A function that is meant to be run asynchronously to update the device entity
    with ChromeOsDevice information from Directory API using the device ID to match.
    """
    if device_urlsafe_key is None:
        raise deferred.PermanentTaskFailure('The device url-safe key parameter is None. It is required.')
    device_key = ndb.Key(urlsafe=device_urlsafe_key)
    device = device_key.get()
    if None == device.device_id:
        logging.info('Did not refresh in refresh_chrome_os_device because no device_id available.')
        return
    impersonation_admin_email_address = get_impersonation_email_from_device_key(device_urlsafe_key)
    if None == impersonation_admin_email_address:
        logging.info('Impersonation email not found for device with device key {0}.'.format(device_urlsafe_key))
        return
    chrome_os_device = None
    chrome_os_devices_api = ChromeOsDevicesApi(impersonation_admin_email_address)
    try:
        chrome_os_device = chrome_os_devices_api.get(config.GOOGLE_CUSTOMER_ID, device.device_id)
    except Exception, e:
        logging.exception(e)
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
        device.etag = chrome_os_device.get('etag')
        device.put()
        logging.info('Refreshed device_id = {0}, impersonating {1}'.
                     format(device.device_id, impersonation_admin_email_address))
    else:
        logging.info('Directory API lookup failure for device_id = {0}, impersonating {1}'.
                     format(device.device_id, impersonation_admin_email_address))


def update_chrome_os_device(device_urlsafe_key=None):
    """
    A function that is meant to be run asynchronously to update the ChromeOsDevice
    information from Directory API with information found on the devie entity.
    """
    if device_urlsafe_key is None:
        raise deferred.PermanentTaskFailure('The device URL-safe key parameter is None.  It is required.')
    device = ndb.Key(urlsafe=device_urlsafe_key).get()
    impersonation_admin_email_address = get_impersonation_email_from_device(device)
    if None == impersonation_admin_email_address:
        logging.info('Impersonation email not found for device with device key {0}.'.format(device_urlsafe_key))
        return
    chrome_os_devices_api = ChromeOsDevicesApi(impersonation_admin_email_address)
    chrome_os_devices_api.update(config.GOOGLE_CUSTOMER_ID,
                                 device.device_id,
                                 annotated_user=device.annotated_user,
                                 annotated_location=device.annotated_location,
                                 notes=device.notes,
                                 org_unit_path=device.org_unit_path)


def get_impersonation_email_from_device(device):
    return device.get_tenant().get_domain().impersonation_admin_email_address


def get_impersonation_email_from_device_key(device_urlsafe_key):
    device = ndb.Key(urlsafe=device_urlsafe_key).get()
    return get_impersonation_email_from_device(device)
