from google.appengine.ext import ndb

from workflow.get_impersonation_email_from_device import get_impersonation_email_from_device

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>, Christopher Bartling <chris.bartling@agosto.com>'


def get_impersonation_email_from_device_key(device_urlsafe_key):
    device = ndb.Key(urlsafe=device_urlsafe_key).get()
    return get_impersonation_email_from_device(device)

