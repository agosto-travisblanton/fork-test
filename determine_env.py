"""
The ``agar.env`` module contains a number of constants to help determine which environment code is running in.
"""
import os

from google.appengine.api.app_identity import get_application_id
from google.appengine.api import apiproxy_stub_map

server_software = os.environ.get('SERVER_SOFTWARE', '')
have_appserver = bool(apiproxy_stub_map.apiproxy.GetStub('datastore_v3'))

appid = None
if have_appserver:
    appid = get_application_id()
else:
    try:
        project_dirname = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        project_dir = os.path.abspath(project_dirname)
        from google.appengine.tools import old_dev_appserver

        appconfig, matcher, from_cache = old_dev_appserver.LoadAppConfig(project_dir, {})
        appid = appconfig.application
    except ImportError:
        dev_appserver = None
        appid = None

#: ``True`` if running in the dev server, ``False`` otherwise.
on_development_server = bool(have_appserver and (not server_software or server_software.lower().startswith('devel')))

#: ``True`` if running on a google server, ``False`` otherwise.
on_server = bool(have_appserver and appid and server_software and not on_development_server)

#: ``True`` if running on a google server and the application ID ends in ``-int``, ``False`` otherwise.
on_integration_server = on_server and (appid.lower().endswith('-int') or appid.lower().endswith('-demo'))

#: ``True`` if running on a google server and the application ID does not end in ``-int``, ``False`` otherwise.
on_production_server = on_server and not on_integration_server


def get_env():
    if on_development_server:
        return "DEV"
    if on_integration_server:
        return "INT"
