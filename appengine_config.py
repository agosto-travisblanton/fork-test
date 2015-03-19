"""
The configuration file used by :py:mod:`agar.config` implementations and other libraries using the
`google.appengine.api.lib_config`_ configuration library. Configuration overrides go in this file.
"""
from env_setup import setup
setup()

from agar.env import on_development_server, on_integration_server

##############################################################################
# AGAR SETTINGS
##############################################################################

# Root level WSGI application modules that 'agar.url.uri_for()' will search
agar_url_APPLICATIONS = ['main']

##############################################################################
# APPSTATS SETTINGS
##############################################################################

appstats_SHELL_OK = on_development_server or on_integration_server

