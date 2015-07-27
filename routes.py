from env_setup import setup
setup()

import os
from google.appengine.ext import ereporter
# This 'CURRENT_VERSION_ID' variable is not available when running tests
if os.environ.get('CURRENT_VERSION_ID'):
    # this makes ereporter capture exceptions on all your handlers
    ereporter.register_logger()

# DO NOT REMOVE
# Importing deferred is a work around to this bug.
# https://groups.google.com/forum/?fromgroups=#!topic/webapp2/sHb2RYxGDLc
from google.appengine.ext import deferred

from webapp2 import Route, WSGIApplication

# This 'CURRENT_VERSION_ID' variable is not available when running tests
if os.environ.get('CURRENT_VERSION_ID'):
    # this makes ereporter capture exceptions on all your handlers
    ereporter.register_logger()

application = WSGIApplication(
    [
        ############################################################
        # warmup
        ############################################################
        Route(
            r'/_ah/warmup',
            handler='handlers.warmup.WarmupHandler',
            name='warmup',
        ),

        ############################################################
        # device registration
        ############################################################
        Route(
            r'/api/v1/devices',
            handler='handlers.device_resource_handler.DeviceResourceHandler',
            name='devices',
            handler_method='get_list',
            methods=['GET']
        ),
        Route(
            r'/api/v1/devices',
            handler='handlers.device_resource_handler.DeviceResourceHandler',
            name='device-creator',
            handler_method='post',
            methods=['POST']
        ),
        Route(
            r'/api/v1/devices/<device_urlsafe_key>',
            handler='handlers.device_resource_handler.DeviceResourceHandler',
            name='manage-device',
            methods=['GET', 'PUT', 'DELETE']
        ),
        Route(
            r'/api/v1/devices/<device_urlsafe_key>/commands',
            handler='handlers.device_commands_handler.DeviceCommandsHandler',
            name='device-commands',
        ),
        Route(
            r'/api/v1/tenants/<tenant_urlsafe_key>/devices',
            handler='handlers.device_resource_handler.DeviceResourceHandler',
            name='devices-by-tenant',
            handler_method='get_devices_by_tenant',
            methods=['GET']
        ),

        ############################################################
        # Displays
        ############################################################
        Route(
            r'/api/v1/displays',
            handler='handlers.displays_handler.DisplaysHandler',
            name='displays-retrieval',
            handler_method='get_list',
            methods=['GET']
        ),
        Route(
            r'/api/v1/tenants/<tenant_urlsafe_key>/displays',
            handler='handlers.displays_handler.DisplaysHandler',
            name='displays-by-tenant',
            handler_method='get_displays_by_tenant',
            methods=['GET']
        ),
        Route(
            r'/api/v1/displays/<display_urlsafe_key>',
            handler='handlers.displays_handler.DisplaysHandler',
            name='manage-display',
            methods=['GET', 'PUT', 'DELETE']
        ),
        Route(
            r'/api/v1/displays',
            handler='handlers.displays_handler.DisplaysHandler',
            name='display-creator',
            handler_method='post',
            methods=['POST']
        ),

        ############################################################
        # Tenants
        ############################################################
        Route(
            r'/api/v1/tenants',
            handler='handlers.tenants_handler.TenantsHandler',
            name='tenants',
            methods=['GET', 'POST']
        ),
        Route(
            r'/api/v1/tenants/<tenant_key>',
            handler='handlers.tenants_handler.TenantsHandler',
            name='manage-tenant',
            methods=['GET', 'PUT', 'DELETE']
        ),
        ############################################################
        # Distributors
        ############################################################
        Route(
            r'/api/v1/distributors',
            handler='handlers.distributors_handler.DistributorsHandler',
            name='distributors',
            methods=['GET', 'POST']
        ),
        Route(
            r'/api/v1/distributors/<distributor_key>',
            handler='handlers.distributors_handler.DistributorsHandler',
            name='manage-distributor',
            methods=['GET', 'PUT', 'DELETE']
        )
    ]
)


