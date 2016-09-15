import json

from app_config import config
from credential_creator import credential_creator, determine_env_string
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from httplib2 import Http
from oauth2client.client import SignedJwtAssertionCredentials

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class UsersApi(object):
    """ Facade encapsulating the Directory API Users of the Admin SDK. """

    DIRECTORY_SERVICE_SCOPES = [
        'https://www.googleapis.com/auth/admin.directory.user'
    ]

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

    # POST https://www.googleapis.com/admin/directory/v1/users
    def insert(self, family_name, given_name, password, primary_email, org_unit_path):
        user_api = self.discovery_service.users()
        request_body = {
            "name":
                {
                    "familyName": family_name,
                    "givenName": given_name,
                },
            "password": password,
            "primaryEmail": primary_email,
            "orgUnitPath": org_unit_path
        }
        request = user_api.insert(body=request_body)
        try:
            response = request.execute()
        except HttpError, error:
            # Note: Directory API returns a 409 Conflict 'Entity already exists.' when the user exists.
            reason = json.loads(error.content)
            response = {'statusCode': error.resp.status, 'statusText': reason['error']['message']}
            return response

        return response
