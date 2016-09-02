from extended_session_request_handler import ExtendedSessionRequestHandler
from integrations.directory_api.organization_units_api import OrganizationUnitsApi
from restler.serializers import json_response

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TenantOrganizationUnitsHandler(ExtendedSessionRequestHandler):

    def get_by_ou_path(self):
        organization_unit_path = self.check_and_get_query_param('organizationUnitPath')
        if organization_unit_path.startswith('/'):
            organization_unit_path =  organization_unit_path[1:]
        impersonation_email = self.check_and_get_query_param('impersonationEmail')
        organization_units_api = OrganizationUnitsApi(
            admin_to_impersonate_email_address=impersonation_email)
        result = organization_units_api.get(organization_unit_path=organization_unit_path)
        if 'statusCode' in result.keys():
            self.response.set_status(result['statusCode'])
            return
        json_response(self.response, result)

    def get_ou_list(self):
        impersonation_email = self.check_and_get_query_param('impersonationEmail')
        parent_organization_unit_path = self.check_and_get_query_param('parentOrganizationUnitPath')
        organization_units_api = OrganizationUnitsApi(
            admin_to_impersonate_email_address=impersonation_email)
        result = organization_units_api.list(parent_organization_unit_path=parent_organization_unit_path)
        if 'statusCode' in result.keys():
            self.response.set_status(result['statusCode'])
            return
        json_response(self.response, result)
