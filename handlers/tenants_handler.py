import httplib
import json
import logging

from google.appengine.ext import ndb
from google.appengine.ext.deferred import deferred

from app_config import config
from decorators import requires_auth
from extended_session_request_handler import ExtendedSessionRequestHandler
from integrations.content_manager.content_manager_api import ContentManagerApi
from integrations.directory_api.organization_units_api import OrganizationUnitsApi
from integrations.directory_api.users_api import UsersApi
from model_entities.domain_model import Domain
from models import IntegrationEventLog
from models import Tenant
from proofplay.database_calls import get_tenant_list_from_distributor_key
from restler.serializers import json_response
from strategy import TENANT_STRATEGY
from utils.iterable_util import delimited_string_to_list

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class TenantsHandler(ExtendedSessionRequestHandler):
    @requires_auth
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

    @requires_auth
    def get(self, tenant_key=None):
        distributor_urlsafe_key = self.request.headers.get('X-Provisioning-Distributor')
        tenant = self.validate_and_get(tenant_key, Tenant, abort_on_not_found=False)
        if not tenant:
            tenant_name_search = self.request.get("tenant_name")
            across_distributors_if_admin = self.request.get("allDistributors") == "true"
            if tenant_name_search and across_distributors_if_admin:
                user_key = self.request.headers.get("X-Provisioning-User")
                try:
                    user_entity = ndb.Key(urlsafe=user_key).get()
                except Exception, e:
                    user_entity = None
                    logging.exception(e)

                if user_entity and user_entity.is_administrator:
                    result = Tenant.find_by_partial_name_across_all_distributors(tenant_name_search)
                else:
                    error_message = 'Bad User Key'
                    self.response.set_status(httplib.BAD_REQUEST, error_message)
                    return

            elif tenant_name_search:
                result = Tenant.find_by_partial_name(tenant_name_search, distributor_urlsafe_key)
            else:
                distributor_key = self.request.headers.get('X-Provisioning-Distributor')
                result = get_tenant_list_from_distributor_key(distributor_key=distributor_key)

        else:
            # Todo: Move this to a one-time migration / data entered during new entity creation
            if tenant.proof_of_play_url == None:
                tenant.proof_of_play_url = config.DEFAULT_PROOF_OF_PLAY_URL
                tenant.put()
            result = tenant

        json_response(self.response, result, strategy=TENANT_STRATEGY)

    @requires_auth
    def post(self):
        correlation_id = IntegrationEventLog.generate_correlation_id()
        IntegrationEventLog.create(
            event_category='Tenant Creation',
            component_name='Provisioning',
            workflow_step='Initialize Tenant Creation',
            tenant_code=config.TENANT_CODE_UNKNOWN,
            details=self.request.body,
            correlation_identifier=correlation_id).put()
        if self.request.body is not str('') and self.request.body is not None:
            request_json = json.loads(self.request.body)
            name = self.check_and_get_field(key='name', abort_on_not_found=True)
            admin_email = self.check_and_get_field(key='admin_email', abort_on_not_found=True)
            admin_email = admin_email.strip().lower()
            tenant_code = self.check_and_get_field(key='tenant_code', abort_on_not_found=True)
            tenant_code = tenant_code.strip().lower()
            content_server_url = self.check_and_get_field(key='content_server_url', abort_on_not_found=True)
            content_server_url = content_server_url.strip().lower()
            content_manager_base_url = self.check_and_get_field(key='content_manager_base_url', abort_on_not_found=True)
            content_manager_base_url = content_manager_base_url.strip().lower()
            notification_emails = delimited_string_to_list(request_json.get('notification_emails'))
            domain_urlsafe_key = self.check_and_get_field(key='domain_key', abort_on_not_found=True)
            domain = self.validate_and_get(urlsafe_key=domain_urlsafe_key, kind_cls=Domain, abort_on_not_found=True)
            active = self.check_and_get_field(key='active', abort_on_not_found=True)
            if str(active).lower() == 'false':
                active = False
            else:
                active = True
            proof_of_play_logging = self.check_and_get_field(key='proof_of_play_logging', abort_on_not_found=True)
            if str(proof_of_play_logging).lower() == 'true':
                proof_of_play_logging = True
            else:
                proof_of_play_logging = False
            proof_of_play_url = request_json.get('proof_of_play_url')
            if proof_of_play_url is None or proof_of_play_url == '':
                proof_of_play_url = config.DEFAULT_PROOF_OF_PLAY_URL
            else:
                proof_of_play_url = proof_of_play_url.strip().lower()
            default_timezone = self.check_and_get_field(key='default_timezone', abort_on_not_found=True)
            ou_create = self.check_and_get_field(key='ou_create', abort_on_not_found=True)
            if str(ou_create).lower() == 'true':
                create_tenant_organization_unit = True
            else:
                create_tenant_organization_unit = False
            if Tenant.is_tenant_code_unique(tenant_code):
                tenant = Tenant.create(name=name,
                                       tenant_code=tenant_code,
                                       admin_email=admin_email,
                                       content_server_url=content_server_url,
                                       content_manager_base_url=content_manager_base_url,
                                       domain_key=domain.key,
                                       active=active,
                                       notification_emails=notification_emails,
                                       proof_of_play_logging=proof_of_play_logging,
                                       proof_of_play_url=proof_of_play_url,
                                       default_timezone=default_timezone,
                                       ou_create=ou_create)
                tenant_key = tenant.put()
                IntegrationEventLog.create(
                    event_category='Tenant Creation',
                    component_name='Provisioning',
                    workflow_step='Saved in DataStore',
                    tenant_code=tenant_code,
                    details='key: {0}, code: {1} '.format(tenant_key.urlsafe(), tenant_code),
                    correlation_identifier=correlation_id).put()

                if create_tenant_organization_unit:
                    IntegrationEventLog.create(
                        event_category='Tenant Creation',
                        component_name='Provisioning',
                        workflow_step='Tenant With OU Option',
                        tenant_code=tenant_code,
                        details='key: {0}, code: {1} '.format(tenant_key.urlsafe(), tenant_code),
                        correlation_identifier=correlation_id).put()
                    status_code, error_message = self.create_tenant_organization_unit_in_chrome_device_management(
                        domain, tenant, correlation_id)
                    if status_code != httplib.CREATED:
                        logging.error(error_message)
                        self.response.set_status(status_code, error_message)
                        return
                else:
                    IntegrationEventLog.create(
                        event_category='Tenant Creation',
                        component_name='Provisioning',
                        workflow_step='Tenant Without OU Option',
                        tenant_code=tenant_code,
                        details='key: {0}, code: {1} '.format(tenant_key.urlsafe(), tenant_code),
                        correlation_identifier=correlation_id).put()

                deferred.defer(ContentManagerApi().create_tenant,
                               tenant=tenant,
                               correlation_id=correlation_id,
                               _queue='content-server')

                tenant_uri = self.request.app.router.build(None, 'manage-tenant', None,
                                                           {'tenant_key': tenant_key.urlsafe()})
                success_message = 'Tenant {0} ({1}) created. Uri = {2}. Organization unit option = {3}.'.format(
                        tenant.name, tenant_code, tenant_uri, create_tenant_organization_unit)
                IntegrationEventLog.create(
                    event_category='Tenant Creation',
                    component_name='Provisioning',
                    workflow_step='Complete Success!',
                    tenant_code=tenant_code,
                    details=success_message,
                    correlation_identifier=correlation_id).put()
                logging.debug('Success creating Tenant: {0}'.format(success_message))

                # update initial tenant creation event to include then known tenant_code
                initial_tenant_creation_event = IntegrationEventLog.get_initial_tenant_creation_event(
                    correlation_identifier=correlation_id)
                initial_tenant_creation_event.tenant_code = tenant_code
                initial_tenant_creation_event.put()

                self.response.headers['Location'] = tenant_uri
                self.response.headers.pop('Content-Type', None)
                self.response.set_status(httplib.CREATED)
            else:
                error_message = "Conflict. Tenant code \"{0}\" is already assigned.".format(tenant_code)
                IntegrationEventLog.create(
                    event_category='Tenant Creation',
                    component_name='Provisioning',
                    workflow_step='Request to create a tenant',
                    tenant_code=tenant_code,
                    details=error_message,
                    correlation_identifier=correlation_id).put()
                logging.error('Failed creating Tenant: {0}'.format(error_message))
                self.response.set_status(httplib.CONFLICT, error_message)
        else:
            error_message = 'Did not receive request body.'
            IntegrationEventLog.create(
                event_category='Tenant Creation',
                component_name='Provisioning',
                workflow_step='Request to create a tenant',
                details=error_message,
                correlation_identifier=correlation_id).put()
            logging.error('Failed creating Tenant: {0}'.format(error_message))
            self.response.set_status(httplib.BAD_REQUEST, error_message)

    @requires_auth
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
        overlay_status = request_json.get('overlayStatus')
        if overlay_status != (None or ''):
            tenant.overlays_available = overlay_status
        else:
            tenant.overlays_available = False

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

    @requires_auth
    def delete(self, tenant_key):
        key = ndb.Key(urlsafe=tenant_key)
        tenant = key.get()
        if tenant:
            tenant.active = False
            tenant.put()
        self.response.headers.pop('Content-Type', None)
        self.response.set_status(204)

    @staticmethod
    def create_tenant_organization_unit_in_chrome_device_management(domain, tenant, correlation_id):
        tenant_code = tenant.tenant_code
        # 1. Check if the tenant OU exists in CDM
        impersonation_email = domain.impersonation_admin_email_address
        organization_units_api = OrganizationUnitsApi(
            admin_to_impersonate_email_address=impersonation_email)
        result = organization_units_api.get(organization_unit_path=tenant.organization_unit_path)
        if 'statusCode' in result.keys():
            if result['statusCode'] == httplib.NOT_FOUND:
                details = 'OU available. Attempting to create it.'
                logging.debug(details)
                IntegrationEventLog.create(
                    event_category='Tenant Creation',
                    component_name='Chrome Directory API',
                    workflow_step='CDM Tenant OU Request',
                    details=details,
                    tenant_code=tenant_code,
                    correlation_identifier=correlation_id).put()
                ou_result = organization_units_api.insert(ou_container_name=tenant_code)
                if 'statusCode' in ou_result.keys() and 'statusText' in ou_result.keys():
                    status_code = ou_result['statusCode']
                    status_text = ou_result['statusText']
                    if 'Invalid Ou Id' in status_text:
                        # We return 412 Precondition Failed so UI knows error occurred due to dupe OU in CDM
                        error_message = 'Precondition failed: {0} {1}'.format(
                            httplib.PRECONDITION_FAILED, status_text)
                        logging.error(error_message)
                    else:
                        error_message = 'Unable to create tenant OU: {0} {1}'.format(
                            status_code, status_text)
                        logging.error(error_message)

                    IntegrationEventLog.create(
                        event_category='Tenant Creation',
                        component_name='Chrome Directory API',
                        workflow_step='Response from CDM: OU Creation was unsuccessful',
                        tenant_code=tenant_code,
                        details=error_message,
                        correlation_identifier=correlation_id).put()
                    return status_code, error_message
                else:
                    tenant.organization_unit_id = ou_result['orgUnitId']
                    success_message = 'Success creating OU for {0} ({1}) with organization_unit_id set to {2}.'.format(
                        tenant.name, tenant_code, tenant.organization_unit_id)
                    IntegrationEventLog.create(
                        event_category='Tenant Creation',
                        component_name='Chrome Directory API',
                        workflow_step='CDM OU Created',
                        details=success_message,
                        tenant_code=tenant_code,
                        correlation_identifier=correlation_id).put()

                    tenant.put()
                    logging.debug(success_message)

                    message = 'Prepare enrollment user for {0} ({1}) with impersonation email {2}.'.format(
                        tenant.name, tenant_code, impersonation_email)
                    IntegrationEventLog.create(
                        event_category='Tenant Creation',
                        component_name='Chrome Directory API',
                        workflow_step='CDM Enrollment User Request',
                        tenant_code=tenant_code,
                        details=message,
                        correlation_identifier=correlation_id).put()
                    logging.debug(message)

                    users_api = UsersApi(admin_to_impersonate_email_address=impersonation_email)
                    user_result = users_api.insert(
                        family_name=tenant_code,
                        given_name='enrollment',
                        password=tenant.enrollment_password,
                        primary_email=tenant.enrollment_email,
                        org_unit_path=tenant.organization_unit_path)
                    if 'statusCode' in user_result.keys() and 'statusText' in user_result.keys():
                        status_code = user_result['statusCode']
                        status_text = user_result['statusText']
                        if 'Entity already exists' in status_text:
                            # Return 412 Precondition Failed so UI knows error is due to dupe user in CDM
                            error_message = 'Precondition failed for enrollment user. {0} {1}'.format(
                                httplib.PRECONDITION_FAILED, status_text)
                        else:
                            error_message = 'Unable to create enrollment user. {0} {1}'.format(status_code, status_text)

                        logging.error(error_message)
                        IntegrationEventLog.create(
                            event_category='Tenant Creation',
                            component_name='Chrome Directory API',
                            workflow_step='Response: Creating enrollment user unsuccessful',
                            tenant_code=tenant_code,
                            details=error_message,
                            correlation_identifier=correlation_id).put()

                        return status_code, error_message
                    else:
                        success_message = 'Success creating enrollment user for {0} on tenant {1} ({2}).'.format(
                            tenant.enrollment_email, tenant.name, tenant_code)
                        status_code = httplib.CREATED
                        IntegrationEventLog.create(
                            event_category='Tenant Creation',
                            component_name='Chrome Directory API',
                            workflow_step='CDM Created Enrollment User',
                            details=success_message,
                            tenant_code=tenant_code,
                            correlation_identifier=correlation_id).put()
                        logging.debug(success_message)
                    return status_code, 'Created'
        else:
            status_code = httplib.NOT_ACCEPTABLE
            status_text = 'Unable to create organization unit in CDM.'
            return status_code, status_text
