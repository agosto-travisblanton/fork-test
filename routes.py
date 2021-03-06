from env_setup import setup
from provisioning_env import (
    on_development_server,
    on_integration_server,
    on_qa_server,
    on_test_harness
)

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
from provisioning_env import on_production_server

application = WSGIApplication(
    [
        ############################################################
        # WARMUP
        ############################################################

        Route(r'/_ah/warmup',
              handler='handlers.warmup.WarmupHandler',
              name='warmup',
              ),

        ############################################################
        # API (external endpoints)
        ############################################################

        # Player API - POST new device registration
        Route(r'/api/v1/devices',
              handler='handlers.api.player.device_handler.DeviceHandler',
              name='api-device-registration',
              handler_method='post',
              methods=['POST']
              ),

        # Player API - GET device by parameter
        Route(r'/api/v1/devices',
              handler='handlers.api.player.device_handler.DeviceHandler',
              name='api-device-by-parameter',
              handler_method='get_device_by_parameter',
              methods=['GET']
              ),

        # Player API - GET device by key
        Route(r'/api/v1/devices/<device_urlsafe_key>',
              handler='handlers.api.player.device_handler.DeviceHandler',
              name='api-device-get',
              handler_method='get',
              methods=['GET']
              ),

        # Player API - PUT device by key
        Route(r'/api/v1/devices/<device_urlsafe_key>',
              handler='handlers.api.player.device_handler.DeviceHandler',
              name='api-device-put',
              handler_method='put',
              methods=['PUT']
              ),

        # Player API - PUT heartbeat
        Route(r'/api/v1/devices/<device_urlsafe_key>/heartbeat',
              handler='handlers.api.player.device_handler.DeviceHandler',
              name='device-heartbeat',
              handler_method='heartbeat',
              methods=['PUT']
              ),

        # API - GET device pairing code
        Route(r'/api/v1/devices/<device_urlsafe_key>/pairing',
              handler='handlers.api.player.device_handler.DeviceHandler',
              name='device-pairing-code',
              handler_method='get_pairing_code',
              methods=['GET']
              ),

        # Player API - PUT to confirm receiving a command
        Route(r'/api/v1/player-command-events/<urlsafe_event_key>',
              handler='handlers.api.player.command_handler.CommandHandler',
              name='player-confirmation',
              handler_method='player_confirmation',
              methods=['PUT']
              ),

        # CM route secured by shared_secret
        Route(r'/api/v1/content-manager/devices/<device_urlsafe_key>',
              handler='handlers.api.content_manager.device_handler.DeviceHandler',
              name='update-content-manager',
              methods=['PUT']
              ),

        # CM route used to send change content requests to the Player via Provisioning
        Route(r'/api/v1/devices/<device_urlsafe_key>/commands',
              handler='handlers.api.content_manager.device_commands_handler.DeviceCommandsHandler',
              handler_method='post',
              methods=['POST'],
              name='device-commands',
              ),

        # report API
        Route(r'/api/reports/v1/chrome_os_device',
              handler='handlers.api.reports.device_handler.DeviceHandler',
              name='report-device-by-parameter',
              handler_method='get_device_by_parameters',
              methods=['GET']
              ),

        # report API - returns device list
        Route(r'/api/reports/v1/chrome_os_devices',
              handler='handlers.api.reports.device_handler.DeviceHandler',
              name='report-device-list',
              handler_method='get_device_list',
              methods=['GET']
              ),

        # report API - returns device count
        Route(r'/api/reports/v1/chrome_os_devices/count',
              handler='handlers.api.reports.device_handler.DeviceHandler',
              name='report-device-count',
              handler_method='get_devices_count',
              methods=['GET']
              ),

        ############################################################
        # DEVICES (Internal UI only)
        ############################################################

        Route(r'/internal/v1/devices/<device_urlsafe_key>',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='internal-device-get',
              handler_method='get',
              methods=['GET']
              ),

        Route(r'/internal/v1/devices/<device_urlsafe_key>',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='internal-device-put',
              handler_method='put',
              methods=['PUT']
              ),

        Route(r'/internal/v1/devices/<device_urlsafe_key>/panel-sleep',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='internal-panel-sleep',
              handler_method='update_panel_sleep',
              methods=['PUT']
              ),

        Route(r'/internal/v1/devices/<device_urlsafe_key>/controls-mode',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='internal-controls-mode',
              handler_method='update_controls_mode',
              methods=['PUT']
              ),

        Route(r'/internal/v1/devices/<device_urlsafe_key>/sleep-controller',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='internal-sleep-controller',
              handler_method='update_sleep_controller',
              methods=['PUT']
              ),

        Route(r'/internal/v1/devices/<device_urlsafe_key>',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='internal-device-delete',
              handler_method='delete',
              methods=['DELETE']
              ),

        ############################################################
        # VERSION
        ############################################################

        Route(r'/internal/v1/versions',
              handler='handlers.versions_handler.VersionsHandler',
              name='version-retrieval',
              handler_method='get',
              methods=['GET']
              ),

        ############################################################
        # LOGIN
        ############################################################

        Route(r'/internal/v1/identity',
              handler='handlers.identity_handler.IdentityHandler',
              name='identity',
              ),
        Route(r'/internal/v1/login',
              handler='handlers.login_handler.LoginHandler',
              name='login',
              ),

        ############################################################
        # LOCATIONS
        ############################################################

        Route(r'/internal/v1/locations/<location_urlsafe_key>',
              handler='handlers.locations_handler.LocationsHandler',
              name='internal-manage-location',
              methods=['GET', 'PUT', 'DELETE']
              ),

        Route(r'/internal/v1/locations',
              handler='handlers.locations_handler.LocationsHandler',
              name='internal-location-create',
              methods=['POST']
              ),

        Route(r'/internal/v1/tenants/<tenant_urlsafe_key>/<prev_cursor>/<next_cursor>/locations',
              handler='handlers.locations_handler.LocationsHandler',
              name='internal-get-locations-by-tenant-paginated',
              handler_method='get_locations_by_tenant_paginated',
              methods=['GET']
              ),

        Route(r'/internal/v1/tenants/<tenant_urlsafe_key>/locations',
              handler='handlers.locations_handler.LocationsHandler',
              name='internal-locations-list',
              handler_method='get_locations_by_tenant',
              methods=['GET']
              ),

        ############################################################
        # DEVICE (ADDITIONAL DEVICE ROUTES UNDER DISTRIBUTOR/TENANT)
        ############################################################

        Route(r'/internal/v1/devices/<prev_cursor_str>/<next_cursor_str>/<device_urlsafe_key>/issues',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='internal-device-issues',
              handler_method='get_latest_issues',
              methods=['GET']
              ),

        Route(r'/internal/v1/devices/<device_urlsafe_key>/commands/reset',
              handler='handlers.device_commands_handler.DeviceCommandsHandler',
              name='device-reset-command',
              handler_method='reset',
              methods=['POST']
              ),

        Route(r'/internal/v1/devices/<device_urlsafe_key>/commands/volume',
              handler='handlers.device_commands_handler.DeviceCommandsHandler',
              name='device-volume-command',
              handler_method='volume',
              methods=['POST']
              ),

        Route(r'/internal/v1/devices/<device_urlsafe_key>/commands/custom',
              handler='handlers.device_commands_handler.DeviceCommandsHandler',
              name='device-custom-command',
              handler_method='custom',
              methods=['POST']
              ),

        Route(r'/internal/v1/devices/<device_urlsafe_key>/commands/power-on',
              handler='handlers.device_commands_handler.DeviceCommandsHandler',
              name='device-power-on-command',
              handler_method='power_on',
              methods=['POST']
              ),

        Route(r'/internal/v1/devices/<device_urlsafe_key>/commands/power-off',
              handler='handlers.device_commands_handler.DeviceCommandsHandler',
              name='device-power-off-command',
              handler_method='power_off',
              methods=['POST']
              ),

        Route(r'/internal/v1/devices/<device_urlsafe_key>/commands/content-delete',
              handler='handlers.device_commands_handler.DeviceCommandsHandler',
              name='device-delete-content-command',
              handler_method='content_delete',
              methods=['POST']
              ),

        Route(r'/internal/v1/devices/<device_urlsafe_key>/commands/content-update',
              handler='handlers.device_commands_handler.DeviceCommandsHandler',
              name='device-update-content-command',
              handler_method='content_update',
              methods=['POST']
              ),

        Route(r'/internal/v1/devices/<device_urlsafe_key>/commands/refresh-device-representation',
              handler='handlers.device_commands_handler.DeviceCommandsHandler',
              name='refresh-device-representation-command',
              handler_method='refresh_device_representation',
              methods=['POST']
              ),

        Route(r'/internal/v1/devices/<device_urlsafe_key>/commands/diagnostics',
              handler='handlers.device_commands_handler.DeviceCommandsHandler',
              name='device-diagnostics-toggle-command',
              handler_method='diagnostics_toggle',
              methods=['POST']
              ),

        Route(r'/internal/v1/devices/<device_urlsafe_key>/commands/restart',
              handler='handlers.device_commands_handler.DeviceCommandsHandler',
              name='device-restart-command',
              handler_method='restart',
              methods=['POST']
              ),

        Route(r'/internal/v1/devices/<device_urlsafe_key>/commands/post-log',
              handler='handlers.device_commands_handler.DeviceCommandsHandler',
              name='device-post-log-command',
              handler_method='post_log',
              methods=['POST']
              ),

        Route(r'/internal/v1/devices/analytics/search-global',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='search_for_device_globally',
              handler_method='search_for_device_globally',
              methods=['GET']
              ),

        ############################################################
        # (DISTRIBUTOR) DEVICE ROUTES
        ############################################################
        # PAGINATED DEVICE LIST
        ############################################################

        Route(r'/internal/v1/distributors/<distributor_urlsafe_key>/devices',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='devices-by-distributor',
              handler_method='get_devices_by_distributor',
              methods=['GET']
              ),

        ############################################################
        # SEARCH
        ############################################################

        Route(r'/internal/v1/distributors/search/<distributor_urlsafe_key>/devices',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='search_for_device',
              handler_method='search_for_device',
              methods=['GET']
              ),

        ############################################################
        # TENANT ROUTES
        ############################################################
        # PAGINATED TENANT DEVICE LIST
        ############################################################

        Route(r'/internal/v1/tenants/<tenant_urlsafe_key>/devices',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='devices-by-tenant',
              handler_method='get_devices_by_tenant',
              methods=['GET']
              ),

        ############################################################
        # SEARCH
        ############################################################

        Route(r'/internal/v1/tenants/search/<tenant_urlsafe_key>/devices',
              handler='handlers.device_resource_handler.DeviceResourceHandler',
              name='search_for_device_by_tenant',
              handler_method='search_for_device_by_tenant',
              methods=['GET']
              ),

        ############################################################
        # GET, POST, PUT, DELETE
        ############################################################

        Route(
            r'/internal/v1/tenants',
            handler='handlers.tenants_handler.TenantsHandler',
            name='tenants',
            methods=['GET', 'POST']
        ),

        Route(
            r'/internal/v1/tenants/<tenant_key>',
            handler='handlers.tenants_handler.TenantsHandler',
            name='manage-tenant',
            methods=['GET', 'PUT', 'DELETE']
        ),

        Route(
            r'/internal/v1/tenants/paginated/<page_size>/<offset>',
            handler='handlers.tenants_handler.TenantsHandler',
            name='get_tenants_paginated',
            handler_method='get_tenants_paginated',
            methods=['GET']
        ),


        ############################################################
        # USERS
        ############################################################

        Route(
            r'/internal/v1/users',
            handler='handlers.users_handler.UsersHandler',
            methods=['POST']
        ),

        Route(
            r'/internal/v1/users/<user_urlsafe_key>/distributors',
            handler='handlers.users_handler.UsersHandler',
            handler_method='get_list_by_user',
            name='get-distributors-by-user',
            methods=['GET']
        ),

        ############################################################
        # DISTRIBUTORS
        ############################################################

        Route(r'/internal/v1/distributors',
              handler='handlers.distributors_handler.DistributorsHandler',
              name='distributors',
              handler_method='get_list',
              methods=['GET']
              ),

        Route(r'/internal/v1/distributors',
              handler='handlers.distributors_handler.DistributorsHandler',
              name='distributor-creator',
              methods=['POST']
              ),

        Route(r'/internal/v1/analytics/distributors/<distributor_key>/users',
              handler='handlers.distributors_handler.DistributorsHandler',
              handler_method='get_users',
              methods=['GET']
              ),

        Route(r'/internal/v1/distributors/<distributor_key>',
              handler='handlers.distributors_handler.DistributorsHandler',
              name='manage-distributor',
              methods=['GET', 'PUT', 'DELETE']
              ),

        Route(r'/internal/v1/distributors/<distributor_key>/domains',
              handler='handlers.distributors_handler.DistributorsHandler',
              name='distributor-domains',
              handler_method='get_domains',
              methods=['GET']
              ),

        ############################################################
        # DOMAINS
        ############################################################

        Route(r'/internal/v1/domains',
              handler='handlers.domains_handler.DomainsHandler',
              name='domains',
              methods=['GET', 'POST']
              ),

        Route(r'/internal/v1/domains/<domain_key>',
              handler='handlers.domains_handler.DomainsHandler',
              name='manage-domain',
              methods=['GET', 'PUT', 'DELETE']
              ),

        Route(r'/internal/v1/domains/<domain_key>/directory_api',
              handler='handlers.domains_handler.DomainsHandler',
              name='directory-api-ping',
              handler_method='ping_directory_api',
              methods=['GET']
              ),

        ############################################################
        # OVERLAY
        ############################################################

        Route(r'/internal/v1/overlay/device/<device_urlsafe_key>',
              handler='handlers.overlay_handler.OverlayHandler',
              name='post-overlay',
              handler_method='post',
              methods=['POST'],
              ),

        Route(r'/internal/v1/overlay/tenant/<tenant_urlsafe_key>',
              handler='handlers.overlay_handler.OverlayHandler',
              name='post_tenant_overlay',
              handler_method='post_tenant_overlay',
              methods=['POST'],
              ),

        Route(r'/internal/v1/overlay/tenant/<tenant_urlsafe_key>/apply',
              handler='handlers.overlay_handler.OverlayHandler',
              name='tenant_apply_overlay_to_devices',
              handler_method='tenant_apply_overlay_to_devices',
              methods=['POST'],
              ),

        ############################################################
        # IMAGE
        ############################################################

        Route(r'/internal/v1/image/<image_urlsafe_key>',
              handler='handlers.image_handler.ImageHandler',
              name='delete_image',
              handler_method='delete_image',
              methods=['DELETE'],
              ),

        Route(r'/internal/v1/image/<image_urlsafe_key>',
              handler='handlers.image_handler.ImageHandler',
              name='get_image_by_key',
              handler_method='get_image_by_key',
              methods=['GET'],
              ),

        Route(r'/internal/v1/image/tenant/<tenant_urlsafe_key>',
              handler='handlers.image_handler.ImageHandler',
              name='manage-image',
              methods=['POST', 'GET'],
              ),

        ############################################################
        # DEVICE MONITORING
        ############################################################

        # Route gets called as chron job (chron.yaml) every 4 minutes
        Route(r'/internal/v1/monitor/devices',
              handler='handlers.monitor_devices_handler.MonitorDevicesHandler',
              name='monitor-devices',
              handler_method='last_contact_check',
              methods=['GET'],
              ),

        ############################################################
        # PLAYER COMMAND EVENTS
        ############################################################

        Route(r'/internal/v1/player-command-events/<prev_cursor_str>/<next_cursor_str>/<device_urlsafe_key>',
              handler='handlers.command_events_handler.CommandEventsHandler',
              name='player-command-events',
              handler_method='get_player_command_events',
              methods=['GET']
              ),

        ############################################################
        # TIMEZONES
        ############################################################

        Route(r'/internal/v1/timezones/us',
              handler='handlers.timezones_handler.TimezonesHandler',
              name='us-timezones',
              handler_method='get_us_timezones',
              methods=['GET']
              ),

        Route(r'/internal/v1/timezones/all',
              handler='handlers.timezones_handler.TimezonesHandler',
              name='all-timezones',
              handler_method='get_all_common_timezones',
              methods=['GET']
              ),

        Route(r'/internal/v1/timezones/custom',
              handler='handlers.timezones_handler.TimezonesHandler',
              name='custom-timezones',
              handler_method='get_custom_timezones',
              methods=['GET']
              ),

        ############################################################
        # INTEGRATION EVENTS LOG
        ############################################################

        Route(r'/internal/v1/integrations_events',
              handler='handlers.integration_events_log_handler.IntegrationEventsLogHandler',
              name='integration-events-list',
              handler_method='get_by_event_category',
              methods=['GET']
              ),

        Route(r'/internal/v1/integration_events/enrollment',
              handler='handlers.integration_events_log_handler.IntegrationEventsLogHandler',
              name='enrollment-events-list',
              handler_method='get_enrollment_events',
              methods=['GET']
              ),

        Route(r'/internal/v1/integration_events/tenant_create',
              handler='handlers.integration_events_log_handler.IntegrationEventsLogHandler',
              name='get_tenant_create_events',
              handler_method='get_tenant_create_events',
              methods=['GET']
              ),

        ############################################################
        # Tenant OU
        ############################################################

        Route(r'/internal/v1/tenant_organizational_unit',
              handler='handlers.tenant_organization_units_handler.TenantOrganizationUnitsHandler',
              name='organization-unit-by-path',
              handler_method='get_by_ou_path',
              methods=['GET']
              ),

        Route(r'/internal/v1/tenant_organizational_units',
              handler='handlers.tenant_organization_units_handler.TenantOrganizationUnitsHandler',
              name='organization-units-list',
              handler_method='get_ou_list',
              methods=['GET']
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

if on_development_server or on_integration_server or on_qa_server:
    dev_routes = [
        Route(r'/api/v1/seed/<user_first>/<user_last>',
              handler="handlers.dev_handlers.SeedScript",
              name="Seed",
              methods=["GET"]
              ),
    ]

    for route in dev_routes:
        application.router.add(route)

if on_development_server or on_test_harness:
    application.router.add(Route(r'/_gcs/download/<base64_filename>',
                                 handler='handlers.gcs.DownloadFileHandler',
                                 name='gcs-download'
                                 ))
