import logging

from google.appengine.ext import ndb

from app_config import config
from restler.serializers import json_response


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


def api_token_required(handler_method):

    def authorize(self, *args, **kwargs):
        api_token = self.request.headers.get('Authorization')
        if api_token is None:
            logging.error('No API token supplied in the HTTP request.')
            json_response(self.response, {'error': 'No API token supplied in the HTTP request.'}, status_code=403)
            return
        elif not api_token == config.API_TOKEN:
            logging.error('HTTP request API token is invalid.')
            json_response(self.response, {'error': 'HTTP request API token is invalid.'}, status_code=403)
            return

        handler_method(self, *args, **kwargs)

    return authorize
