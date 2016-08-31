from oauth2client.client import SignedJwtAssertionCredentials
from app_config import config


def determine_env_string(prod_credentials=False,
                         int_credentials=False,
                         qa_credentials=False,
                         stage_credentials=False):
    if prod_credentials:
        return "prod_credentials"
    elif int_credentials:
        return 'int_credentials'
    elif qa_credentials:
        return 'qa_credentials'
    elif stage_credentials:
        return 'qa_credentials'

def credential_creator(env, scopes, admin_to_impersonate_email_address):
    credentials = None
    if env.lower() == 'prod_credentials':
        key_file = '{}/privatekeys/skykit-provisioning.pem'.format(config.APP_ROOT)
        with open(key_file) as f:
            private_key = f.read()
        credentials = SignedJwtAssertionCredentials(
            '613606096818-3hehucjfgbtj56pu8dduuo36uccccen0@developer.gserviceaccount.com',
            private_key=private_key,
            scope=scopes,
            sub=admin_to_impersonate_email_address)

    elif env.lower() == 'int_credentials':
        key_file = '{}/privatekeys/skykit-display-device-int.pem'.format(config.APP_ROOT)
        with open(key_file) as f:
            private_key = f.read()
        credentials = SignedJwtAssertionCredentials(
            '390010375778-87capuus77kispm64q27iah4kl0rorv4@developer.gserviceaccount.com',
            private_key=private_key,
            scope=scopes,
            sub=admin_to_impersonate_email_address)

    elif env.lower() == 'stage_credentials':
        key_file = '{}/privatekeys/skykit-provisioning-stage.pem'.format(config.APP_ROOT)
        with open(key_file) as f:
            private_key = f.read()
        credentials = SignedJwtAssertionCredentials(
            'service-247@skykit-provisioning-stage.iam.gserviceaccount.com',
            private_key=private_key,
            scope=scopes,
            sub=admin_to_impersonate_email_address)

    elif env.lower() == 'qa_credentials':
        key_file = '{}/privatekeys/skykit-provisioning-qa.pem'.format(config.APP_ROOT)
        with open(key_file) as f:
            private_key = f.read()
        credentials = SignedJwtAssertionCredentials(
            'service@skykit-provisioning-qa.iam.gserviceaccount.com',
            private_key=private_key,
            scope=scopes,
            sub=admin_to_impersonate_email_address)

    if not credentials:
        raise ValueError("You did not provide a valid environment")

    return credentials
