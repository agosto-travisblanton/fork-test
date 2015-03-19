import logging
import random
import string

from stormpath.error import Error as SpError
from stormpath.client import Client

from app_config import config


def create_initial_password():
    upper = ''.join(random.choice(string.ascii_uppercase) for i in range(4))
    lower = ''.join(random.choice(string.ascii_lowercase) for i in range(4))
    number = random.choice(range(10))
    special = random.choice(['/', '$', '^'])
    password = '%s%s%s%s' % (upper, lower, number, special)
    password = list(password)
    random.shuffle(password)
    return ''.join(password)


def get_client():
    client = Client(api_key={
        'id': config.STORMPATH_APIKEY_ID,
        'secret': config.STORMPATH_APIKEY_SECRET
    })

    return client


def get_auth_application():
    client = get_client()
    auth_app = None
    for app in client.applications:
        if app.name and app.name.lower() == config.STORMPATH_AUTH_APP:
            auth_app = app
            break
    return auth_app


def get_account_group_memberships(account):
    group_memberships_details = []

    for item in account.group_memberships.items:
        group_details = {
            'description': item.group.description,
            'href': item.group.href,
            'name': item.group.name,
            'status': item.group.status
        }
        group_memberships_details.append(group_details)

    return group_memberships_details


def login(username, password, tenant):
    stormpath_username = '%s/%s' % (tenant.lower(), username)
    auth_app = get_auth_application()

    try:
        return auth_app.authenticate_account(stormpath_username, password)
    except SpError as e:
        logging.exception(e)
        raise


def get_directory_by_tenant(tenant_name):
    tenant_name = tenant_name.lower()

    client = get_client()
    directory = None
    for dir_item in client.directories.items:
        if dir_item.name.lower() == tenant_name:
            directory = dir_item
            break

    return directory


def get_groups_by_tenant(tenant_name):
    tenant_name = tenant_name.lower()

    directory = get_directory_by_tenant(tenant_name)
    return directory.groups.items


def create_role_group_by_iss_tenant(tenant_name, role_group_details):
    tenant_name = tenant_name.lower()

    directory = get_directory_by_tenant(tenant_name)
    new_role = directory.groups.create(role_group_details)
    return new_role


def get_accounts(tenant):
    directory = get_directory_by_tenant(tenant)
    return directory.accounts.query(username='%s/*' % tenant, limit=100)


def create_account(tenant_name, email, password, first_name, middle_name, last_name, user_status, username):
    valid_status = ['enabled', 'disabled']
    status_code = 200

    if user_status:
        user_status = user_status.lower()

    if not email:
        raise Exception('email is required.')

    if not username:
        raise Exception('username is required.')

    if user_status and user_status not in valid_status:
        raise Exception('user_status must be one of: %s' % valid_status)

    directory = get_directory_by_tenant(tenant_name)

    if username.lower().find(tenant_name.lower()) != 0:
        username = '%s/%s' % (tenant_name.lower(), username.lower())

    params = {
        'username': username,
        'email': email,
        'password': password,
        'surname': last_name,
        'given_name': first_name,
        'middle_name': middle_name,
        'status': user_status
    }

    try:
        account = directory.accounts.create(params)
    except SpError as e:
        status_code = 400
        logging.exception(e)
        account = {'error_message': e.message}
    return status_code, account


def update_account(
        href,
        tenant_name,
        email,
        user_status=None,
        username=None,
        password=None,
        first_name=None,
        middle_name=None,
        last_name=None):

    status_code = 200
    valid_status = ['enabled', 'disabled']

    if user_status:
        user_status = user_status.lower()

    if not email:
        raise Exception('email is required.')

    if user_status is not None and user_status not in valid_status:
        raise Exception('user_status must be one of: %s' % valid_status)

    directory = get_directory_by_tenant(tenant_name)
    account = directory.accounts.get(href)

    account.middle_name = middle_name

    if user_status:
        account.status = user_status

    if username:
        if username.lower().find(tenant_name.lower()) != 0:
            username = '%s/%s' % (tenant_name.lower(), username)

    account.username = username

    if email:
        account.email = email

    if password:
        account.password = password

    if first_name:
        account.given_name = first_name

    if last_name:
        account.surname = last_name

    try:
        account.save()
        account = directory.accounts.get(account.href)
    except SpError as e:
        status_code = 400
        logging.exception(e)
        account = {'error_message': e.message}
    return status_code, account


def send_password_reset_email(email):
    try:
        auth_app = get_auth_application()
        auth_app.send_password_reset_email(email)
        status_code = 200
        message = {'message': 'Password reset instructions sent to %s.' % email}
    except SpError as e:
        status_code = 400
        message = {'error_message': e.message}

    return status_code, message


def stormpath_ping():
    try:
        auth_app = get_auth_application()
        return auth_app is not None
    except Exception:
        return False
