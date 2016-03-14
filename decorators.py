import logging

from google.appengine.ext import ndb

from app_config import config
from restler.serializers import json_response
from proofplay.database_calls import get_tenant_names_for_distributor


def identity_required(handler_method):
    def identify(self, *args, **kwargs):
        self.user_key = self.request.headers.get('X-Provisioning-User')
        self.user = None
        try:
            self.user = ndb.Key(urlsafe=self.user_key).get()
        except Exception, e:
            logging.exception(e)
            logging.error('API call is missing a user key in header.')
            json_response(self.response, {'error': 'No user logged in'}, status_code=403)
            return

        handler_method(self, *args, **kwargs)

    return identify


def distributor_required(handler_method):
    def distributor(self, *args, **kwargs):
        self.distributor_key = self.request.headers.get('X-Provisioning-Distributor')
        self.distributor = None
        try:
            self.distributor = ndb.Key(urlsafe=self.distributor_key).get()
        except Exception, e:
            logging.exception(e)
            logging.error('API call is missing a distributor key in header.')
            json_response(self.response, {'error': 'No distributor'}, status_code=403)
            return

        handler_method(self, *args, **kwargs)

    return distributor


#
# def gae_supported_numpy(test_method):
#     import numpy
#     from utils.print_utils import StderrLogger
#
#     def check_numpy(self, *args, **kwargs):
#         npv = numpy.version.full_version
#         if npv != '1.6.1':
#             logger = StderrLogger()
#             logger.warning("Found local numpy version {}. App engine only supports version 1.6.1. "
#                            "You may falsely green bar!".format(npv))
#         test_method(self, *args, **kwargs)
#
#     return check_numpy
#
#
# def no_in_context_cache(function):
#     """
#     Disables in-context caching. NOTE: Will not work on functions that get pickled.
#     :param function:
#     :return: function that wraps the existing function which disables ndb in-context caching.
#     """
#     from google.appengine.ext import ndb
#
#     def disable_cache(*args, **kwargs):
#         ctx = ndb.get_context()
#         ctx.set_cache_policy(lambda key: False)
#         return function(*args, **kwargs)
#
#     return disable_cache
#

def log_memory(function):
    """
    Decorator that prints memory usage of a function before and after it runs to logging.debug.
    WARNING! This will NOT work on functions or methods that will get Pickled!
    :param function:
    :return: function that wraps the existing function which does pre and post logging
    """
    from google.appengine.api import runtime
    from agar.env import on_server

    def log(*args, **kwargs):
        memory = "NOT SUPPORTED"
        if on_server:
            memory = runtime.memory_usage().current()
        start_msg = "START {} memory: {} MB".format(function.func_name, memory)
        logging.debug(start_msg)
        ret_value = function(*args, **kwargs)
        if on_server:
            memory = runtime.memory_usage().current()
        end_msg = "END   {} memory: {} MB".format(function.func_name, memory)
        logging.debug(end_msg)
        return ret_value

    return log


def requires_api_token(handler_method):
    def authorize(self, *args, **kwargs):
        self.is_unmanaged_device = False
        api_token = self.request.headers.get('Authorization')
        self.is_unmanaged_device = api_token == config.UNMANAGED_API_TOKEN
        if _token_missing(api_token):
            json_response(self.response, {'error': 'No API token supplied in the HTTP request.'}, status_code=403)
            return
        if _token_invalid(api_token=api_token, for_unmanaged_registration_token=False, for_registration_token=False):
            json_response(self.response, {'error': 'HTTP request API token is invalid.'}, status_code=403)
            return
        handler_method(self, *args, **kwargs)

    return authorize


def has_tenant_in_distributor_header(handler_method):
    def authorize(self, *args, **kwargs):
        distributor_key = self.request.headers.get('X-Provisioning-Distributor')
        tenants = get_tenant_names_for_distributor(distributor_key)
        tenant = kwargs['tenant']
        if tenant not in tenants:
            self.response.write("YOU ARE NOT ALLOWED TO QUERY THIS CONTENT")
            self.abort(403)
            return

        handler_method(self, *args, **kwargs)

    return authorize


def has_tenant_in_distributor_param(handler_method):
    def authorize(self, *args, **kwargs):
        distributor_key = kwargs['distributor_key']
        tenants = get_tenant_names_for_distributor(distributor_key)
        tenant = kwargs['tenant']
        if tenant not in tenants:
            self.response.write("YOU ARE NOT ALLOWED TO QUERY THIS CONTENT")
            self.abort(403)
            return

        handler_method(self, *args, **kwargs)

    return authorize


def has_distributor_key(handler_method):
    def authorize(self, *args, **kwargs):
        distributor_key = self.request.headers.get('X-Provisioning-Distributor')
        if not distributor_key:
            self.response.write("YOU ARE NOT ALLOWED TO QUERY THIS CONTENT")
            self.abort(403)
            return

        handler_method(self, *args, **kwargs)

    return authorize


def requires_registration_token(handler_method):
    def authorize(self, *args, **kwargs):
        self.is_unmanaged_device = False
        api_token = self.request.headers.get('Authorization')
        self.is_unmanaged_device = api_token == config.UNMANAGED_REGISTRATION_TOKEN
        if _token_missing(api_token):
            json_response(self.response, {'error': 'No API token supplied in the HTTP request.'}, status_code=403)
            return
        if _token_invalid(api_token=api_token, for_unmanaged_registration_token=False, for_registration_token=True):
            json_response(self.response, {'error': 'HTTP request API token is invalid.'}, status_code=403)
            return
        handler_method(self, *args, **kwargs)

    return authorize


def requires_unmanaged_registration_token(handler_method):
    def authorize(self, *args, **kwargs):
        self.is_unmanaged_device = True
        api_token = self.request.headers.get('Authorization')
        if _token_missing(api_token):
            json_response(self.response, {'error': 'No API token supplied in the HTTP request.'}, status_code=403)
            return
        if _token_invalid(api_token=api_token, for_unmanaged_registration_token=True, for_registration_token=False):
            json_response(self.response, {'error': 'HTTP request API token is invalid.'}, status_code=403)
            return
        handler_method(self, *args, **kwargs)

    return authorize


def _token_missing(api_token):
    if api_token is None:
        logging.error('No API token supplied in the HTTP request.')
        return True
    return False


def _token_invalid(api_token, for_unmanaged_registration_token=False, for_registration_token=False):
    if for_unmanaged_registration_token is True:
        valid_api_token = api_token == config.UNMANAGED_REGISTRATION_TOKEN
        if not valid_api_token:
            logging.error('HTTP request API token is invalid for unmanaged registration.')
            return True
    elif for_registration_token is True:
        valid_api_token = api_token == config.API_TOKEN
        unmanaged_registration_token = api_token == config.UNMANAGED_REGISTRATION_TOKEN
        if not valid_api_token and not unmanaged_registration_token:
            logging.error('HTTP request API token is invalid for registration.')
            return True
    else:
        valid_api_token = api_token == config.API_TOKEN
        unmanaged_api_token = api_token == config.UNMANAGED_API_TOKEN
        if not valid_api_token and not unmanaged_api_token:
            logging.error('HTTP request API token {0} is invalid. Expected token = {1}'.format(api_token, config.API_TOKEN))
            return True
    return False
