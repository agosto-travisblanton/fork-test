import httplib
import inspect
import logging

from google.appengine.api.datastore_errors import BadRequestError
from google.appengine.ext import ndb
from google.net.proto.ProtocolBuffer import ProtocolBufferDecodeError

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


def resolve_device(urlsafe_key):
    status = httplib.OK
    message = 'OK'
    try:
        device_key = ndb.Key(urlsafe=urlsafe_key)
        chrome_os_device = device_key.get()
    except TypeError, type_error:
        logging.exception(type_error.message)
        message = 'Invalid input (Type Error). {0} in urlsafe key'.format(type_error.message)
        status = httplib.BAD_REQUEST
        return status, message, None
    except BadRequestError, bad_request_error:
        logging.exception(bad_request_error.message)
        message = 'Invalid input. (Bad Request Error) {0} in urlsafe key'.format(bad_request_error.message)
        status = httplib.BAD_REQUEST
        return status, message, None
    except ProtocolBufferDecodeError, protocol_buffer_decode_error:
        logging.exception(protocol_buffer_decode_error.message)
        message = 'Invalid urlsafe string (Protocol Buffer Decode Error): {0}'.format(
            protocol_buffer_decode_error.message)
        status = httplib.BAD_REQUEST
        return status, message, None
    except Exception, exception:
        logging.exception(exception)
        message = exception.message
        status = httplib.BAD_REQUEST
        return status, message, None
    if None is chrome_os_device:
        status = httplib.NOT_FOUND
        calling_method_name = inspect.stack()[1][3]
        message = '{0} method not executed because device unresolvable with urlsafe key: {1}'.format(
            calling_method_name, urlsafe_key)
        logging.warning(message)
    return status, message, chrome_os_device
