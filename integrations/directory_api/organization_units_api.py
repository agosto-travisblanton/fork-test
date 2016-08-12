import json

from app_config import config
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from httplib2 import Http
from oauth2client.client import SignedJwtAssertionCredentials

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class OrganizationUnitsApi(object):
    """ Facade encapsulating the Directory API Organization Units of the Admin SDK. """

    DIRECTORY_SERVICE_SCOPES = [
        'https://www.googleapis.com/auth/admin.directory.orgunit'
    ]

    TOP_LEVEL_ORG_UNIT_PATH = '/skykit'

    def __init__(self,
                 admin_to_impersonate_email_address,
                 prod_credentials=False,
                 int_credentials=False):

        if prod_credentials is True:
            key_file = '{}/privatekeys/skykit-provisioning.pem'.format(config.APP_ROOT)
            with open(key_file) as f:
                private_key = f.read()
            self.credentials = SignedJwtAssertionCredentials(
                '613606096818-3hehucjfgbtj56pu8dduuo36uccccen0@developer.gserviceaccount.com',
                private_key=private_key,
                scope=self.DIRECTORY_SERVICE_SCOPES,
                sub=admin_to_impersonate_email_address)
        elif int_credentials is True:
            key_file = '{}/privatekeys/skykit-display-device-int.pem'.format(config.APP_ROOT)
            with open(key_file) as f:
                private_key = f.read()
            self.credentials = SignedJwtAssertionCredentials(
                '390010375778-87capuus77kispm64q27iah4kl0rorv4@developer.gserviceaccount.com',
                private_key=private_key,
                scope=self.DIRECTORY_SERVICE_SCOPES,
                sub=admin_to_impersonate_email_address)
        else:
            self.credentials = SignedJwtAssertionCredentials(config.SERVICE_ACCOUNT_EMAIL,
                                                             private_key=config.PRIVATE_KEY,
                                                             scope=self.DIRECTORY_SERVICE_SCOPES,
                                                             sub=admin_to_impersonate_email_address)
        self.authorized_http = self.credentials.authorize(Http())
        self.discovery_service = discovery.build('admin', 'directory_v1', http=self.authorized_http)

    # GET https://www.googleapis.com/admin/directory/v1/customer/my_customer/orgunits/<org_unit_path>?key={API_KEY}
    def get(self, organization_unit_path):
        ou_api = self.discovery_service.orgunits()
        request = ou_api.get(customerId=config.GOOGLE_CUSTOMER_ID,
                             orgUnitPath=organization_unit_path)
        try:
            response = request.execute()
        except HttpError, err:
            response = {'statusCode': err.resp.status}
        return response

    # GET https://www.googleapis.com/admin/directory/v1/customer/my_customer/orgunits?orgUnitPath=skykit&key={API_KEY}
    def list(self, parent_organization_unit_path=None):
        if parent_organization_unit_path is None:
            parent_organization_unit_path = self.TOP_LEVEL_ORG_UNIT_PATH
        ou_api = self.discovery_service.orgunits()
        request = ou_api.list(customerId=config.GOOGLE_CUSTOMER_ID,
                              orgUnitPath=parent_organization_unit_path)
        try:
            response = request.execute()
        except HttpError, err:
            response = {'statusCode': err.resp.status}
        return response

    # https://www.googleapis.com/admin/directory/v1/customer/my_customer/orgunits
    def insert(self, tenant_code, screen_rotation=0):
        ou_api = self.discovery_service.orgunits()
        request_body = {
            "name": tenant_code,
            "description": 'OU for '.format(tenant_code),
            "parentOrgUnitPath": self.TOP_LEVEL_ORG_UNIT_PATH
        }
        request = ou_api.insert(customerId=config.GOOGLE_CUSTOMER_ID, body=request_body)
        try:
            response = request.execute()
        except HttpError, error:
            # Note: Directory API returns a 400 if OU exists w/ message "Invalid Ou Id"
            reason = json.loads(error.content)
            response = {'statusCode': error.resp.status, 'statusText': reason['error']['message']}
            return response

        sub_org_unit_name = self._get_sub_org_unit_name(screen_rotation=screen_rotation)
        self._add_sub_org_unit(ou_api=ou_api,
                               parent_org_unit_path='{0}/{1}'.format(self.TOP_LEVEL_ORG_UNIT_PATH, tenant_code),
                               sub_org_unit_name=sub_org_unit_name)

        return response

    @staticmethod
    def _add_sub_org_unit(ou_api, parent_org_unit_path, sub_org_unit_name):
        ou_api = ou_api
        request_body = {
            "name": sub_org_unit_name,
            "description": 'Display rotation sub OU for tenant '.format(parent_org_unit_path),
            "parentOrgUnitPath": parent_org_unit_path
        }
        request = ou_api.insert(customerId=config.GOOGLE_CUSTOMER_ID, body=request_body)
        try:
            response = request.execute()
        except HttpError, error:
            # Note: Directory API returns a 400 if OU exists w/ message "Invalid Ou Id"
            reason = json.loads(error.content)
            response = {'statusCode': error.resp.status, 'statusText': reason['error']['message']}
        return response

    @staticmethod
    def _get_sub_org_unit_name(screen_rotation=0):
        if screen_rotation in [90, 180, 270]:
            return 'screen_rotation_{0}'.format(screen_rotation)
        else:
            return 'screen_rotation_0'
