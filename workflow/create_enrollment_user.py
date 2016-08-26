from integrations.directory_api.users_api import UsersApi

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


def create_enrollment_user(impersonation_email,
                           org_unit_path,
                           enrollment_email,
                           enrollment_password,
                           enrollment_family_name,
                           enrollment_given_name,
                           correlation_id):
    """
    A function that is meant to be run asynchronously to create an enrollment user in CDM
    :param impersonation_email: impersonation email that is tied to the domain
    :param org_unit_path: organization unit path in CDM
    :param enrollment_email: enrollment user email on the domain attached to the org_unit_path
    :param enrollment_password: provisioning generated password for the enrollment user account
    :param enrollment_family_name: enrollment user account family name
    :param enrollment_given_name: enrollment user account given name
    :param correlation_id: workflow identifier for integration event logging
    """
    users_api = UsersApi(admin_to_impersonate_email_address=impersonation_email, int_credentials=True)
    # TODO add integration event logging here using correlation_id for request including payload
    result = users_api.insert(
        family_name=enrollment_family_name,
        given_name=enrollment_given_name,
        password=enrollment_password,
        primary_email=enrollment_email,
        org_unit_path=org_unit_path)
    if 'statusCode' in result.keys() and 'statusText' in result.keys():
        status_code = result['statusCode']
        status_text = result['statusText']
        # TODO add integration event logging using correlation_id for failure response (status code and status text)
    else:
        # TODO add integration event logging using correlation_id for success!
        is_created = result['primaryEmail'].strip().lower() == enrollment_email

    return result
