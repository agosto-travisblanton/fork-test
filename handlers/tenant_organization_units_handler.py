from extended_session_request_handler import ExtendedSessionRequestHandler

from integrations.directory_api.organization_units_api import OrganizationUnitsApi
from restler.serializers import json_response

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TenantOrganizationUnitsHandler(ExtendedSessionRequestHandler):
    PARENT_ORG_UNIT_PATH = 'skykit'

    def get_by_ou_path(self):
        organization_unit_path = self.check_and_get_query_param('organizationUnitPath')
        impersonation_email = self.check_and_get_query_param('impersonationEmail')
        organization_units_api = OrganizationUnitsApi(
            admin_to_impersonate_email_address=impersonation_email,
            int_credentials=True)
        result = organization_units_api.get(organization_unit_path=organization_unit_path)
        if 'statusCode' in result.keys():
            self.response.set_status(result['statusCode'])
            return
        json_response(self.response, result)

    def get_ou_list(self):
        impersonation_email = self.check_and_get_query_param('impersonationEmail')
        parent_organization_unit_path = self.check_and_get_query_param('parentOrganizationUnitPath')

        organization_units_api = OrganizationUnitsApi(
            admin_to_impersonate_email_address=impersonation_email,
            int_credentials=True)
        result = organization_units_api.list(parent_organization_unit_path=parent_organization_unit_path)
        if 'statusCode' in result.keys():
            self.response.set_status(result['statusCode'])
            return
        json_response(self.response, result)

    def create(self):
        if self.request.body is not str('') and self.request.body is not None:
            status = 201
            error_message = None
            impersonation_email = self.check_and_get_field('impersonationEmail')
            impersonation_email = impersonation_email.strip().lower()
            tenant_code = self.check_and_get_field('tenantCode')
            tenant_code = tenant_code.strip().lower()

            screen_rotation = self.check_and_get_field('screenRotation')
            try:
                int(screen_rotation)
            except ValueError as exception:
                status = 400
                error_message = 'The screenRotation parameter is invalid. Error = {0}'.format(exception.message)
            screen_rotation = int(screen_rotation)
            if screen_rotation != 0 and screen_rotation != 90 and screen_rotation != 180 and screen_rotation != 270:
                status = 400
                error_message = 'The screenRotation parameter is an unexpected value.'
            if status == 201:
                organization_units_api = OrganizationUnitsApi(
                    admin_to_impersonate_email_address=impersonation_email, int_credentials=True)
                result = organization_units_api.insert(tenant_code=tenant_code,
                                                       screen_rotation=screen_rotation)
                if 'statusCode' in result.keys() and 'statusText' in result.keys():
                    self.response.set_status(result['statusCode'], result['statusText'])
            else:
                self.response.set_status(status, error_message)
        else:
            self.response.set_status(400, 'Did not receive request body.')
