import json

from app_config import config
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
