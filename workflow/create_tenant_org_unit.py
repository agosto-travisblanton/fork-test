from integrations.directory_api.organization_units_api import OrganizationUnitsApi
from workflow.create_enrollment_user import create_enrollment_user

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


def create_tenant_org_unit(impersonation_email,
                           ou_container_name,
                           org_unit_path,
                           enrollment_email,
                           enrollment_password,
                           enrollment_family_name,
                           enrollment_given_name,
                           correlation_id):
    """
    A function that is meant to be run asynchronously to create a tenant OU in CDM
    :param impersonation_email: impersonation email that is tied to the domain
    :param ou_container_name: typically this is tenant_code
    :param org_unit_path: organization unit path in CDM
    :param enrollment_email: enrollment user email on the domain attached to the org_unit_path
    :param enrollment_password: provisioning generated password for the enrollment user account
    :param enrollment_family_name: enrollment user account family name
    :param enrollment_given_name: enrollment user account given name
    :param correlation_id: workflow identifier for integration event logging
    """
    ou_api = OrganizationUnitsApi(admin_to_impersonate_email_address=impersonation_email, int_credentials=True)
    # TODO add integration event logging here using correlation_id for request including payload
    result = ou_api.insert(ou_container_name=ou_container_name)
    if 'statusCode' in result.keys() and 'statusText' in result.keys():
        status_code = result['statusCode']
        status_text = result['statusText']
        # TODO add integration event logging here using correlation_id for response (status code and status text)

    # TODO create_enrollment_user should be done on a deferred thread
    enrollment_user_result = create_enrollment_user(impersonation_email=impersonation_email,
                                                    org_unit_path=org_unit_path,
                                                    primary_email=enrollment_email,
                                                    password=enrollment_password,
                                                    enrollment_family_name=enrollment_family_name,
                                                    enrollment_given_name=enrollment_given_name,
                                                    correlation_id=correlation_id)
    return result

