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
# from google.appengine.ext import deferred

from webapp2 import Route, WSGIApplication
from agar.env import on_production_server

application = WSGIApplication(
    [
        ############################################################
        # warmup
        ############################################################
        Route(r'/_ah/warmup',
              handler='handlers.warmup.WarmupHandler',
              name='warmup',
              ),

        ############################################################
        # version
        ############################################################
        Route(
            r'/api/v1/versions',
            handler='handlers.versions_handler.VersionsHandler',
            name='version-retrieval',
            handler_method='get',
            methods=['GET']
        ),

        ############################################################
        # login
        ############################################################
        Route(r'/api/v1/identity',
              handler='handlers.identity_handler.IdentityHandler',
              name='identity'
              ),

        Route(r'/login',
              handler='handlers.login_handler.LoginHandler',
              name='login',
              ),

        Route(r'/logout',
              handler='handlers.logout_handler.LogoutHandler',
              name='logout',
              ),

        ############################################################
        # device
        ############################################################
        Route(r'/api/v1/devices/<device_urlsafe_key>/heartbeat',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='devices-heartbeat',
              handler_method='heartbeat',
              methods=['PUT']
              ),
        Route(r'/api/v1/devices',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='devices-retrieval',
              handler_method='get_list',
              methods=['GET']
              ),
        Route(r'/api/v1/devices',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='device-creator',
              handler_method='post',
              methods=['POST']
              ),
        Route(r'/api/v1/devices/<device_urlsafe_key>',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='device',
              methods=['GET', 'PUT', 'DELETE']
              ),
        Route(r'/api/v1/devices/<device_urlsafe_key>/pairing',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='device-pairing-code',
              handler_method='get_pairing_code',
              methods=['GET']
              ),
        Route(r'/api/v1/devices/<device_urlsafe_key>/issues',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='device-issues',
              handler_method='get_latest_issues',
              methods=['GET']
              ),
        Route(r'/api/v1/devices/<device_urlsafe_key>/commands',
              handler='handlers.device_commands_handler.DeviceCommandsHandler',
              name='device-commands',
              ),
        Route(r'/api/v1/devices/<device_urlsafe_key>/commands/reset',
              handler='handlers.device_commands_handler.DeviceCommandsHandler',
              name='device-reset-command',
              handler_method='reset',
              methods=['POST']
              ),
        Route(r'/api/v1/devices/<device_urlsafe_key>/commands/volume',
              handler='handlers.device_commands_handler.DeviceCommandsHandler',
              name='device-volume-command',
              handler_method='volume',
              methods=['POST']
              ),
        Route(r'/api/v1/devices/<device_urlsafe_key>/commands/custom',
              handler='handlers.device_commands_handler.DeviceCommandsHandler',
              name='device-custom-command',
              handler_method='custom',
              methods=['POST']
              ),
        Route(r'/api/v1/tenants/<tenant_urlsafe_key>/devices',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='devices-by-tenant',
              handler_method='get_devices_by_tenant',
              methods=['GET']
              ),
        Route(r'/api/v1/distributors/<distributor_urlsafe_key>/devices',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='devices-by-distributor',
              handler_method='get_devices_by_distributor',
              methods=['GET']
              ),
        ############################################################
        # Tenants
        ############################################################
        Route(r'/api/v1/tenants',
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
            r'/api/v1/users/<user_urlsafe_key>/distributors',
            handler='handlers.distributors_handler.DistributorsHandler',
            handler_method='get_list_by_user',
            name='get-distributors-by-user',
            methods=['GET']
        ),
        Route(r'/api/v1/distributors',
              handler='handlers.distributors_handler.DistributorsHandler',
              name='distributors',
              handler_method='get_list',
              methods=['GET']
        ),
        Route(r'/api/v1/distributors',
              handler='handlers.distributors_handler.DistributorsHandler',
              name='distributor-creator',
              methods=['POST']
              ),
        Route(r'/api/v1/distributors/<distributor_key>',
              handler='handlers.distributors_handler.DistributorsHandler',
              name='manage-distributor',
              methods=['GET', 'PUT', 'DELETE']
              ),
        Route(r'/api/v1/distributors/<distributor_key>/domains',
              handler='handlers.distributors_handler.DistributorsHandler',
              name='distributor-domains',
              handler_method='get_domains',
              methods=['GET']
        ),

        ############################################################
        # Domains
        ############################################################
        Route(r'/api/v1/domains',
              handler='handlers.domains_handler.DomainsHandler',
              name='domains',
              methods=['GET', 'POST']
              ),
        Route(r'/api/v1/domains/<domain_key>',
              handler='handlers.domains_handler.DomainsHandler',
              name='manage-domain',
              methods=['GET', 'PUT', 'DELETE']
              ),

        ############################################################
        # Device Monitoring
        ############################################################
        Route(r'/api/v1/monitor/devices',
              handler='handlers.monitor_devices_handler.MonitorDevicesHandler',
              name='monitor-devices',
              handler_method='last_contact_check',
              methods=['GET'],
              ),

        ############################################################
        # Player Command Events
        ############################################################
        Route(r'/api/v1/player-command-events/<urlsafe_event_key>',
              handler='handlers.player_command_events_handler.PlayerCommandEventsHandler',
              name='manage-event',
              handler_method='command_confirmation',
              methods=['PUT']
              ),

        ############################################################
        # /dev/ routes secured by admin:required
        ############################################################
        Route(
            r'/dev/versions',
            handler='handlers.versions.VersionHandler',
            name='versions',
            methods=['GET'],
        ),

    ],
    debug=not on_production_server
)
