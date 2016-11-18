import json
import logging

from google.appengine.ext import ndb
from webapp2 import RequestHandler

from app_config import config
from utils.auth_util import requires_auth
from integrations.directory_api.chrome_os_devices_api import ChromeOsDevicesApi
from integrations.directory_api.organization_units_api import OrganizationUnitsApi
from integrations.directory_api.users_api import UsersApi
from models import Domain
from ndb_mixins import KeyValidatorMixin
from oauth2client.client import AccessTokenRefreshError
from restler.serializers import json_response
from strategy import DOMAIN_STRATEGY
from extended_session_request_handler import ExtendedSessionRequestHandler

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class DomainsHandler(ExtendedSessionRequestHandler):
    DEVICES_SCOPE = 'https://www.googleapis.com/auth/admin.directory.device.chromeos'
    OU_SCOPE = 'https://www.googleapis.com/auth/admin.directory.orgunit'
    USERS_SCOPE = 'https://www.googleapis.com/auth/admin.directory.user'

    @requires_auth
    def get(self, domain_key=None):
        if None == domain_key:
            distributor_key = self.request.headers.get('X-Provisioning-Distributor')
            distributor = ndb.Key(urlsafe=distributor_key)
            domain_list = Domain.query(Domain.distributor_key == distributor).fetch(100)
            result = filter(lambda x: x.active is True, domain_list)
        else:
            result = self.validate_and_get(domain_key, Domain, abort_on_not_found=True, use_app_engine_memcache=False)
        json_response(self.response, result, strategy=DOMAIN_STRATEGY)

    @requires_auth
    def post(self):
        if self.request.body is not str('') and self.request.body is not None:
            status = 201
            error_message = None
            request_json = json.loads(self.request.body)
            name = request_json.get('name')
            if name is None or name == '':
                status = 400
                error_message = 'The name parameter is invalid.'
            else:
                if Domain.already_exists(name):
                    status = 409
                    error_message = "Conflict. Domain name \"{0}\" is in use.".format(name)
            active = request_json.get('active')
            if active is None or active == '' or (str(active).lower() != 'true' and str(active).lower() != 'false'):
                status = 400
                error_message = 'The active parameter is invalid.'
            else:
                active = bool(active)
            impersonation_admin_email_address = request_json.get('impersonation_admin_email_address')
            if impersonation_admin_email_address is None or impersonation_admin_email_address == '':
                status = 400
                error_message = 'The impersonation_admin_email_address parameter is invalid.'
            organization_unit_path = request_json.get('organization_unit_path')
            if organization_unit_path is None or organization_unit_path == '':
                organization_unit_path = config.DEFAULT_OU_PATH
            distributor_urlsafe_key = self.request.headers.get('X-Provisioning-Distributor')
            if distributor_urlsafe_key is None or distributor_urlsafe_key == '':
                status = 400
                error_message = 'The distributor_key parameter is invalid.'
            if status == 201:
                domain = Domain.create(distributor_key=ndb.Key(urlsafe=distributor_urlsafe_key),
                                       name=name,
                                       impersonation_admin_email_address=impersonation_admin_email_address,
                                       organization_unit_path=organization_unit_path,
                                       active=active)
                domain_key = domain.put()
                domain_uri = self.request.app.router.build(None,
                                                           'manage-domain',
                                                           None,
                                                           {'domain_key': domain_key.urlsafe()})
                self.response.headers['Location'] = domain_uri
                self.response.headers.pop('Content-Type', None)
                self.response.set_status(201)
            else:
                self.response.set_status(status, error_message)
        else:
            logging.info("Problem creating Domain. No request body.")
            self.response.set_status(400, 'Did not receive request body.')

    @requires_auth
    def put(self, domain_key):
        status = 204
        message = None
        domain = None
        try:
            domain = ndb.Key(urlsafe=domain_key).get()
        except Exception, e:
            logging.exception(e)
        if domain is None:
            status = 404
            message = 'Unrecognized domain with key: {0}'.format(domain_key)
            return self.response.set_status(status, message)
        else:
            request_json = json.loads(self.request.body)
            domain.active = request_json.get('active')
            organization_unit_path = request_json.get('organization_unit_path')
            if organization_unit_path is None or organization_unit_path == '':
                organization_unit_path = config.DEFAULT_OU_PATH
            domain.organization_unit_path = organization_unit_path
            domain.put()
            self.response.headers.pop('Content-Type', None)
            self.response.set_status(status, message)

    @requires_auth
    def delete(self, domain_key):
        key = ndb.Key(urlsafe=domain_key)
        device = key.get()
        if device:
            device.active = False
            device.put()
        self.response.set_status(204)
        self.response.headers.pop('Content-Type', None)

    @requires_auth
    def ping_directory_api(self, domain_key):
        domain = self.validate_and_get(domain_key, Domain, abort_on_not_found=True, use_app_engine_memcache=False)
        result = {'domainName': domain.name, 'impersonationEmail': domain.impersonation_admin_email_address}
        _check_devices_scope(self.DEVICES_SCOPE, domain.name, domain.impersonation_admin_email_address, result)
        _check_ou_scope(self.OU_SCOPE, domain.name, domain.impersonation_admin_email_address, result)
        _check_users_scope(self.USERS_SCOPE, domain.name, domain.impersonation_admin_email_address, result)
        json_response(self.response, result)


def _check_devices_scope(scope, domain_name, impersonation_email, result):
    try:
        chrome_os_devices_api = ChromeOsDevicesApi(admin_to_impersonate_email_address=impersonation_email)
        scopes = chrome_os_devices_api.DIRECTORY_SERVICE_SCOPES
        if any(scope in s for s in scopes):
            result['devicesAccess'] = True
        else:
            result['devicesAccess'] = False
    except AccessTokenRefreshError as exception:
        result['devicesAccess'] = False
        error_message = "'{0}' for {1} on {2}".format(
            exception.message,
            impersonation_email,
            domain_name
        )
        logging.info(error_message)
        result['devicesAccessException'] = error_message


def _check_ou_scope(scope, domain_name, impersonation_email, result):
    try:
        organization_units_api = OrganizationUnitsApi(admin_to_impersonate_email_address=impersonation_email)
        if organization_units_api:
            scopes = organization_units_api.DIRECTORY_SERVICE_SCOPES
            if any(scope in s for s in scopes):
                result['orgUnitsAccess'] = True
            else:
                result['orgUnitsAccess'] = False
    except AccessTokenRefreshError as exception:
        result['orgUnitsAccess'] = False
        error_message = "'{0}' for {1} on {2}".format(
            exception.message,
            impersonation_email,
            domain_name
        )
        logging.info(error_message)
        result['orgUnitsAccessException'] = error_message


def _check_users_scope(scope, domain_name, impersonation_email, result):
    try:
        users_api = UsersApi(admin_to_impersonate_email_address=impersonation_email)
        if users_api:
            scopes = users_api.DIRECTORY_SERVICE_SCOPES
            if any(scope in s for s in scopes):
                result['usersAccess'] = True
            else:
                result['usersAccess'] = False
    except AccessTokenRefreshError as exception:
        result['usersAccess'] = False
        error_message = "'{0}' for {1} on {2}".format(
            exception.message,
            impersonation_email,
            domain_name
        )
        logging.info(error_message)
        result['usersAccessException'] = error_message
