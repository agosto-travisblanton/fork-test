import json

from webapp2 import RequestHandler

from integrations.directory_api.organization_units_api import OrganizationUnitsApi
from restler.serializers import json_response

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class TenantOrganizationUnitsHandler(RequestHandler):
    PARENT_ORG_UNIT_PATH = 'skykit'

    def get_by_ou_path(self):
        status = 200
        error_message = None
        organization_unit_path = self.request.get('organizationUnitPath')
        if organization_unit_path is None or organization_unit_path == '':
            status = 400
            error_message = 'The organizationUnitPath parameter is invalid.'
        impersonation_email = self.request.get('impersonationEmail')
        if impersonation_email is None or impersonation_email == '':
            status = 400
            error_message = 'The impersonationEmail parameter is invalid.'
        if status == 200:
            organization_units_api = OrganizationUnitsApi(
                admin_to_impersonate_email_address=impersonation_email,
                int_credentials=True)
            result = organization_units_api.get(organization_unit_path=organization_unit_path)
            if 'statusCode' in result.keys():
                self.response.set_status(result['statusCode'])
                return
            json_response(self.response, result)
        else:
            self.response.set_status(status, error_message)

    def get_ou_list(self):
        status = 200
        error_message = None
        impersonation_email = self.request.get('impersonationEmail')
        if impersonation_email is None or impersonation_email == '':
            status = 400
            error_message = 'The impersonationEmail parameter is invalid.'
        parent_organization_unit_path = self.request.get('parentOrganizationUnitPath')
        if parent_organization_unit_path is None or parent_organization_unit_path == '':
            parent_organization_unit_path = self.PARENT_ORG_UNIT_PATH
        if status == 200:
            organization_units_api = OrganizationUnitsApi(
                admin_to_impersonate_email_address=impersonation_email,
                int_credentials=True)
            result = organization_units_api.list(parent_organization_unit_path=parent_organization_unit_path)
            if 'statusCode' in result.keys():
                self.response.set_status(result['statusCode'])
                return
            json_response(self.response, result)
        else:
            self.response.set_status(status, error_message)

    def create(self):
        if self.request.body is not str('') and self.request.body is not None:
            status = 201
            error_message = None
            request_json = json.loads(self.request.body)
            impersonation_email = request_json.get('impersonationEmail')
            if impersonation_email is None or impersonation_email == '':
                status = 400
                error_message = 'The impersonationEmail parameter is invalid.'
            else:
                impersonation_email = impersonation_email.strip().lower()
            tenant_code = request_json.get('tenantCode')
            if tenant_code is None or tenant_code == '':
                status = 400
                error_message = 'The tenantCode parameter is invalid.'
            else:
                tenant_code = tenant_code.strip().lower()
            screen_rotation = request_json.get('screenRotation')
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
                if 'statusCode' in result.keys():
                    self.response.set_status(result['statusCode'])
                    return
            else:
                self.response.set_status(status, error_message)
        else:
            self.response.set_status(400, 'Did not receive request body.')
