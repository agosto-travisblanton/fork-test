import json

from credential_creator import credential_creator, determine_env_string
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
                 int_credentials=False,
                 qa_credentials=False,
                 stage_credentials=False):

        env_string = determine_env_string(prod_credentials=prod_credentials,
                                          int_credentials=int_credentials,
                                          qa_credentials=qa_credentials,
                                          stage_credentials=stage_credentials)

        if prod_credentials or int_credentials or qa_credentials or stage_credentials:
            self.credentials = credential_creator(env_string, self.DIRECTORY_SERVICE_SCOPES,
                                                  admin_to_impersonate_email_address)

        else:
            self.credentials = SignedJwtAssertionCredentials(config.SERVICE_ACCOUNT_EMAIL,
                                                             private_key=config.PRIVATE_KEY,
                                                             scope=self.DIRECTORY_SERVICE_SCOPES,
                                                             sub=admin_to_impersonate_email_address)
        self.authorized_http = self.credentials.authorize(Http())
        self.discovery_service = discovery.build('admin', 'directory_v1', http=self.authorized_http)

    def patch_tenant_name(self, org_unit_path, new_tenant_code):
        ou_api = self.discovery_service.orgunits()
        request_body = {
            "name": new_tenant_code,
        }

        request = ou_api.insert(customerId=config.GOOGLE_CUSTOMER_ID, orgUnitPath=org_unit_path, body=request_body)
        try:
            response = request.execute()
        except HttpError, error:
            # Note: Directory API returns a 400 if OU exists w/ message "Invalid Ou Id"
            reason = json.loads(error.content)
            response = {'statusCode': error.resp.status, 'statusText': reason['error']['message']}
            return response
        return response

    # https://www.googleapis.com/admin/directory/v1/customer/my_customer/orgunits
    def insert(self, ou_container_name, parent_org_unit_path=None):
        if parent_org_unit_path is None:
            parent_org_unit_path = self.TOP_LEVEL_ORG_UNIT_PATH
        ou_api = self.discovery_service.orgunits()
        request_body = {
            "name": ou_container_name,
            "description": 'Organization unit for {0}'.format(ou_container_name),
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

        return response

    # GET https://www.googleapis.com/admin/directory/v1/customer/my_customer/orgunits/<org_unit_path>?key={API_KEY}
    def get(self, organization_unit_path):
        if organization_unit_path.startswith('/'):
            organization_unit_path = organization_unit_path[1:]
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
