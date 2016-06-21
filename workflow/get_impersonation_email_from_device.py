__author__ = 'Bob MacNeal <bob.macneal@agosto.com>, Christopher Bartling <chris.bartling@agosto.com>'


def get_impersonation_email_from_device(device):
    return device.get_tenant().get_domain().impersonation_admin_email_address

