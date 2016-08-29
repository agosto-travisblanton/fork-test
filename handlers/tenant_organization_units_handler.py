from uuid import uuid4

from extended_session_request_handler import ExtendedSessionRequestHandler
from integrations.directory_api.organization_units_api import OrganizationUnitsApi
from restler.serializers import json_response
from workflow.create_tenant_org_unit import create_tenant_org_unit

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
            ou_container_name = self.check_and_get_field('tenantCode')
            ou_container_name = ou_container_name.strip().lower()
            org_unit_path = self.check_and_get_field('orgUnitPath').strip()
            enrollment_email = self.check_and_get_field('enrollmentEmail').strip().lower()
            enrollment_password = 'pwd12345'  # This will be 10 character uuid we generate, persist and display on ui
            enrollment_family_name = self.check_and_get_field('enrollmentFamilyName').strip()
            enrollment_given_name = self.check_and_get_field('enrollmentGivenName').strip()
            correlation_id = str(uuid4())
            if status == 201:
                result = create_tenant_org_unit(impersonation_email=impersonation_email,
                                                ou_container_name=ou_container_name,
                                                org_unit_path=org_unit_path,
                                                enrollment_email=enrollment_email,
                                                enrollment_password=enrollment_password,
                                                enrollment_family_name=enrollment_family_name,
                                                enrollment_given_name=enrollment_given_name,
                                                correlation_id=correlation_id)
                if 'statusCode' in result.keys() and 'statusText' in result.keys():
                    self.response.set_status(result['statusCode'], result['statusText'])
            else:
                self.response.set_status(status, error_message)
        else:
            self.response.set_status(400, 'Did not receive request body.')

    # def create_enrollment_user(self):
    #     if self.request.body is not str('') and self.request.body is not None:
    #         status = 201
    #         error_message = None
    #         impersonation_email = self.check_and_get_field('impersonationEmail').strip().lower()
    #         family_name = self.check_and_get_field('familyName').strip()
    #         given_name = self.check_and_get_field('givenName').strip()
    #         org_unit_path = self.check_and_get_field('orgUnitPath').strip()
    #         password = 'pwd12345'  # This will be 10 character uuid we generate, persist w/ tenant, and display on ui
    #         primary_email = self.check_and_get_field('primaryEmail').strip().lower()
    #         if status == 201:
    #             users_api = UsersApi(admin_to_impersonate_email_address=impersonation_email, int_credentials=True)
    #             result = users_api.insert(
    #                 family_name=family_name,
    #                 given_name=given_name,
    #                 password=password,
    #                 primary_email=primary_email,
    #                 org_unit_path=org_unit_path)
    #             if 'statusCode' in result.keys() and 'statusText' in result.keys():
    #                 self.response.set_status(result['statusCode'], result['statusText'])
    #         else:
    #             self.response.set_status(status, error_message)
    #     else:
    #         self.response.set_status(400, 'Did not receive request body.')
