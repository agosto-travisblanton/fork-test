import json
import logging

from google.appengine.ext import ndb

from app_config import config
from decorators import requires_api_token
from extended_session_request_handler import ExtendedSessionRequestHandler
from integrations.content_manager.content_manager_api import ContentManagerApi
from integrations.directory_api.organization_units_api import OrganizationUnitsApi
from integrations.directory_api.users_api import UsersApi
from models import Tenant
from proofplay.database_calls import get_tenant_list_from_distributor_key
from restler.serializers import json_response
from strategy import TENANT_STRATEGY
from utils.iterable_util import delimited_string_to_list

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TenantsHandler(ExtendedSessionRequestHandler):
    @requires_api_token
    def get_tenants_paginated(self, offset, page_size):
        offset = int(offset)
        page_size = int(page_size)
        distributor_key = self.request.headers.get('X-Provisioning-Distributor')
        result = get_tenant_list_from_distributor_key(distributor_key=distributor_key)
        paginated_result = result[offset:page_size + offset]

        if paginated_result:
            is_first_page = offset == 0
            is_last_page = paginated_result[-1] == result[-1]

        else:
            is_first_page = True
            is_last_page = True

        json_response(
            self.response,
            {
                "tenants": paginated_result,
                "is_first_page": is_first_page,
                "is_last_page": is_last_page,
                "total": len(result)
            },
            strategy=TENANT_STRATEGY)

    @requires_api_token
    def get(self, tenant_key=None):
        distributor_urlsafe_key = self.request.headers.get('X-Provisioning-Distributor')
        if not tenant_key:
            tenant_search_code = self.request.get("tenant_name")
            if tenant_search_code:
                result = Tenant.find_by_partial_name(tenant_search_code, distributor_urlsafe_key)
            else:
                distributor_key = self.request.headers.get('X-Provisioning-Distributor')
                result = get_tenant_list_from_distributor_key(distributor_key=distributor_key)
        else:
            tenant_key = ndb.Key(urlsafe=tenant_key)
            tenant = tenant_key.get()
            if tenant.proof_of_play_url is None:
                tenant.proof_of_play_url = config.DEFAULT_PROOF_OF_PLAY_URL
                tenant.put()
            result = tenant

        json_response(self.response, result, strategy=TENANT_STRATEGY)

    @requires_api_token
    def post(self):
        if self.request.body is not str('') and self.request.body is not None:
            status = 201
            error_message = None
            request_json = json.loads(self.request.body)
            name = self.check_and_get_field('name')
            admin_email = self.check_and_get_field('admin_email')
            admin_email = admin_email.strip().lower()
            tenant_code = self.check_and_get_field('tenant_code')
            tenant_code = tenant_code.strip().lower()
            content_server_url = self.check_and_get_field('content_server_url')
            content_server_url = content_server_url.strip().lower()
            content_manager_base_url = self.check_and_get_field('content_manager_base_url')
            content_manager_base_url = content_manager_base_url.strip().lower()
            notification_emails = delimited_string_to_list(request_json.get('notification_emails'))
            domain_key_input = self.check_and_get_field('domain_key')
            try:
                domain_key = ndb.Key(urlsafe=domain_key_input)
            except Exception, e:
                logging.exception(e)
            if None is domain_key:
                status = 400
                error_message = 'The domain did not resolve.'
            active = self.check_and_get_field('active')
            if str(active).lower() != 'true' and str(active).lower() != 'false':
                status = 400
                error_message = 'The active parameter is invalid.'
            else:
                active = bool(active)
            proof_of_play_logging = self.check_and_get_field('proof_of_play_logging')
            if str(proof_of_play_logging).lower() != 'true' and str(proof_of_play_logging).lower() != 'false':
                status = 400
                error_message = 'The proof_of_play_logging parameter is invalid.'
            else:
                proof_of_play_logging = bool(proof_of_play_logging)
            proof_of_play_url = request_json.get('proof_of_play_url')
            if proof_of_play_url is None or proof_of_play_url == '':
                proof_of_play_url = config.DEFAULT_PROOF_OF_PLAY_URL
            else:
                proof_of_play_url = proof_of_play_url.strip().lower()
            default_timezone = request_json.get('default_timezone')
            if default_timezone is None or default_timezone == '':
                status = 400
                error_message = 'The default timezone is invalid.'
            else:
                default_timezone = default_timezone
            if status == 201:
                if Tenant.is_tenant_code_unique(tenant_code):  # could also check if tenant OU exists
                    tenant = Tenant.create(name=name,
                                           tenant_code=tenant_code,
                                           admin_email=admin_email,
                                           content_server_url=content_server_url,
                                           content_manager_base_url=content_manager_base_url,
                                           domain_key=domain_key,
                                           active=active,
                                           notification_emails=notification_emails,
                                           proof_of_play_logging=proof_of_play_logging,
                                           proof_of_play_url=proof_of_play_url,
                                           default_timezone=default_timezone)

                    # Bust out the tenant OU
                    impersonation_email = domain_key.get().impersonation_admin_email_address
                    organization_units_api = OrganizationUnitsApi(
                        admin_to_impersonate_email_address=impersonation_email,
                        int_credentials=True)
                    ou_result = organization_units_api.insert(ou_container_name=tenant.tenant_code)
                    if 'statusCode' in ou_result.keys() and 'statusText' in ou_result.keys():
                        status_code = ou_result['statusCode']
                        status_text = ou_result['statusText']
                        if status_text == 'Invalid Ou Id':
                            status_code = 412
                            error_message = 'Precondition Failed. {0}'.format(status_code, status_text)
                            # We return 412 Precondition Failed so UI knows error occurred due to dupe OU in CDM
                        else:
                            error_message = 'Unable to create tenant OU. {0} {1}'.format(status_code, status_text)
                        self.response.set_status(status_code, error_message)
                        # TODO add integration event logging using correlation_id for failure response
                        return
                    else:
                        tenant.organization_unit_id = ou_result['orgUnitId']
                        # Bust out the enrollment user
                        users_api = UsersApi(
                            admin_to_impersonate_email_address=impersonation_email,
                            int_credentials=True)
                        user_result = users_api.insert(
                            family_name=tenant.tenant_code,
                            given_name='enrollment',
                            password=tenant.enrollment_password,
                            primary_email=tenant.enrollment_email,
                            org_unit_path=tenant.organization_unit_path)
                        if 'statusCode' in user_result.keys() and 'statusText' in user_result.keys():
                            status_code = user_result['statusCode']
                            status_text = user_result['statusText']
                            error_message = 'Unable to create enrollment user. {0} {1}'.format(status_code, status_text)
                            self.response.set_status(status_code, error_message)
                            # TODO add integration event logging using correlation_id for failure response
                            return
                        else:
                            # TODO add integration event logging using correlation_id for success!
                            # is_created = ou_result['primaryEmail'].strip().lower() == tenant.enrollment_email
                            tenant_key = tenant.put()
                            content_manager_api = ContentManagerApi()
                            notify_content_manager = content_manager_api.create_tenant(tenant)
                            if not notify_content_manager:
                                logging.info('Failed to notify content manager about new tenant {0}'.format(name))

                            tenant_uri = self.request.app.router.build(None,
                                                                       'manage-tenant',
                                                                       None,
                                                                       {'tenant_key': tenant_key.urlsafe()})
                            self.response.headers['Location'] = tenant_uri
                            self.response.headers.pop('Content-Type', None)
                            self.response.set_status(201)
                else:
                    error_message = "Conflict. Tenant code \"{0}\" is already assigned to a tenant.".format(tenant_code)
                    self.response.set_status(409, error_message)
            else:
                self.response.set_status(status, error_message)
        else:
            logging.info("Problem creating Tenant. No request body.")
            self.response.set_status(400, 'Did not receive request body.')

    @requires_api_token
    def put(self, tenant_key):
        status = 204
        error_message = None
        key = ndb.Key(urlsafe=tenant_key)
        tenant = key.get()
        request_json = json.loads(self.request.body)
        name = request_json.get('name')
        if name is None or name == '':
            status = 400
            error_message = 'The name parameter is invalid.'
        else:
            tenant.name = name
        tenant_code = request_json.get('tenant_code')
        if tenant_code is None or tenant_code == '':
            status = 400
            error_message = 'The tenant code parameter is invalid.'
        else:
            tenant.tenant_code = tenant_code.strip().lower()
        admin_email = request_json.get('admin_email')
        if admin_email is None or admin_email == '':
            status = 400
            error_message = 'The admin email parameter is invalid.'
        else:
            tenant.admin_email = admin_email.strip().lower()
        content_server_url = request_json.get('content_server_url')
        if content_server_url is None or content_server_url == '':
            status = 400
            error_message = 'The content server url parameter is invalid.'
        else:
            tenant.content_server_url = content_server_url.strip().lower()
        content_manager_base_url = request_json.get('content_manager_base_url')
        if content_manager_base_url is None or content_manager_base_url == '':
            status = 400
            error_message = 'The content manager base url parameter is invalid.'
        else:
            tenant.content_manager_base_url = content_manager_base_url.strip().lower()
        default_timezone = request_json.get('default_timezone')
        if default_timezone is None or default_timezone == '':
            status = 400
            error_message = 'The default timezone parameter is invalid.'
        else:
            tenant.default_timezone = default_timezone
        email_list = delimited_string_to_list(request_json.get('notification_emails'))
        tenant.notification_emails = email_list
        domain_key_input = request_json.get('domain_key')
        tenant.active = request_json.get('active')
        proof_of_play_logging = request_json.get('proof_of_play_logging')
        proof_of_play_url = request_json.get('proof_of_play_url')
        Tenant.set_proof_of_play_options(
            tenant_code=tenant.tenant_code,
            proof_of_play_logging=proof_of_play_logging,
            proof_of_play_url=proof_of_play_url,
            tenant_key=key)
        try:
            domain_key = ndb.Key(urlsafe=domain_key_input)
        except Exception, e:
            logging.exception(e)
        if domain_key:
            tenant.domain_key = domain_key
        else:
            status = 400
            error_message = 'Error resolving domain from domain key.'
        if status == 204:
            tenant.put()
            self.response.headers.pop('Content-Type', None)
            self.response.set_status(status)
        else:
            self.response.set_status(status, error_message)

    @requires_api_token
    def delete(self, tenant_key):
        key = ndb.Key(urlsafe=tenant_key)
        tenant = key.get()
        if tenant:
            tenant.active = False
            tenant.put()
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)
