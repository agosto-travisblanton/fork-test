from env_setup import setup
setup()

import os

from google.appengine.ext import ereporter

# DO NOT REMOVE
# Importing deferred is a work around to this bug.
# https://groups.google.com/forum/?fromgroups=#!topic/webapp2/sHb2RYxGDLc
from google.appengine.ext import deferred

from goodyear_env import on_production_server
from webapp2 import Route, WSGIApplication

# This 'CURRENT_VERSION_ID' variable is not available when running tests
if os.environ.get('CURRENT_VERSION_ID'):
    # this makes ereporter capture exceptions on all your handlers
    ereporter.register_logger()

application = WSGIApplication(
    [
        Route(
            r'/',
            handler="handlers.index.IndexHandler",
            name='index',
        ),

        ############################################################
        # Customer
        ############################################################
        Route(
            r'/tenant/<key>/customers',
            handler='handlers.customer.CustomerListHandler',
            name='list-customers',
            methods=['GET']
        ),
        Route(
            r'/customer/<key>',
            handler='handlers.customer.CustomerHandler',
            name='manage-customer',
            methods=['GET', 'DELETE', 'PUT']
        ),
        Route(
            r'/tenant/<key>/customer',
            handler='handlers.customer.CustomerHandler',
            name='create-customer',
            methods=['POST']
        ),

        ############################################################
        # Dashboard
        ############################################################
        Route(
            r'/stats',
            handler='handlers.dashboard.DashboardStatsHandler',
            name='list-statistics',
            methods=['POST']
        ),
        Route(
            r'/stats/export',
            handler='handlers.dashboard.DashboardStatsExportHandler',
            name='export-statistics',
            methods=['POST']
        ),

        ############################################################
        # Events
        ############################################################
        Route(
            r'/events',
            handler='handlers.event.EventReadingListHandler',
            name='list-event-readings',
            methods=['GET']
        ),
        Route(
            r'/<filter:(customer|vehicle_group|vehicle)>/<key>/events',
            handler='handlers.event.EventReadingListHandler',
            name='list-filtered-event-readings',
            methods=['GET']
        ),
        Route(
            r'/event/<key>',
            handler='handlers.event.VehicleEventHandler',
            name='manage-event',
            methods=['GET']
        ),
        Route(
            r'/event/<key>/raw',
            handler='handlers.event.RawVehicleEventHandler',
            name='get-raw-event',
            methods=['GET']
        ),
        Route(
            r'/events',
            handler='handlers.event.VehicleEventHandler',
            name='create-event',
            methods=['POST']
        ),

        ############################################################
        # Incidents
        ############################################################
        Route(
            r'/incident/<key>',
            handler='handlers.incident.IncidentHandler',
            name='manage-incident',
            methods=['GET']
        ),
        Route(
            r'/incidents',
            handler='handlers.incident.IncidentHandler',
            name='list-incidents',
            methods=['GET']
        ),


        ############################################################
        # Report
        ############################################################
        Route(
            r'/reports',
            handler='handlers.report.ReportListHandler',
            name='list-reports',
            methods=['GET'],
        ),
        Route(
            r'/report/<key>',
            handler='handlers.report.DownloadReportHandler',
            name='get-report',
            methods=['GET'],
        ),

        ############################################################
        # TelemetryProvider
        ############################################################
        Route(
            r'/telemetry_providers',
            handler='handlers.telemetry_provider.TelemetryProviderHandler',
            name='list-telemetry_providers',
            methods=['GET'],
        ),
        Route(
            r'/telemetry_provider/<key>',
            handler='handlers.telemetry_provider.TelemetryProviderHandler',
            name='manage-telemetry_provider',
            methods=['GET','PUT','DELETE'],
        ),
        Route(
            r'/telemetry_provider',
            handler='handlers.telemetry_provider.TelemetryProviderHandler',
            name='create-telemetry_provider',
            methods=['POST'],
        ),

        ############################################################
        # Tenant
        ############################################################
        Route(
            r'/tenants',
            handler='handlers.tenant.TenantHandler',
            name='list-tenants',
            methods=['GET'],
        ),
        Route(
            r'/tenant/<key>',
            handler='handlers.tenant.TenantHandler',
            name='manage-tenant',
            methods=['GET','PUT','DELETE'],
        ),
        Route(
            r'/tenant',
            handler='handlers.tenant.TenantHandler',
            name='create-tenant',
            methods=['POST'],
        ),

        ############################################################
        # Threshold Sets
        ############################################################
        Route(
            r'/<owner:(tenant|customer|vehicle_group|vehicle)>/<owner_key>/vehicle_template/<vehicle_template_key>/threshold_set',
            handler='handlers.threshold.ThresholdSetHandler',
            name='manage-threshold-set',
            methods=['GET', 'PUT'],
        ),

        ############################################################
        # User
        ############################################################
        Route(
            r'/identity',
            handler='handlers.user.IdentityHandler',
            name='identity',
        ),
        Route(
            r'/login_form',
            handler='handlers.user.LoginHandler',
            name='login',
        ),
        Route(
            r'/logout',
            handler='handlers.user.Logout',
            name='logout',
        ),
        Route(
            r'/user/password_reset',
            handler='handlers.user.PasswordHandler',
            name='reset-password',
            methods=['POST'],
        ),
        Route(
            r'/users',
            handler='handlers.user.UserHandler',
            name='list-users',
            methods=['GET'],
        ),
        Route(
            r'/user/<key>',
            handler='handlers.user.UserHandler',
            name='manage-user',
            methods=['GET', 'PUT'],
        ),
        Route(
            r'/user',
            handler='handlers.user.UserHandler',
            name='create-user',
            methods=['POST'],
        ),

        ############################################################
        # Unregistered Vehicle
        ############################################################
        Route(
            r'/<filter:(customer)>/<key>/unregistered_vehicles',
            handler='handlers.unregistered_vehicle.UnregisteredVehicleHandler',
            name='list-filtered-unregistered-vehicles',
            methods=['GET']
        ),

        Route(
            r'/unregistered_vehicles',
            handler='handlers.unregistered_vehicle.UnregisteredVehicleHandler',
            name='list-unregistered-vehicles',
            methods=['GET'],
        ),
        Route(
            r'/unregistered_vehicle/<key>',
            handler='handlers.unregistered_vehicle.UnregisteredVehicleHandler',
            name='manage-unregistered-vehicle',
            methods=['GET', 'DELETE', 'POST'],
        ),

        ############################################################
        # Vehicle
        ############################################################
        Route(
            r'/vehicle_group/<key>/vehicles',
            handler='handlers.vehicle.VehicleListHandler',
            name='list-vehicles',
            methods=['GET'],
        ),
        Route(
            r'/vehicle/<key>',
            handler='handlers.vehicle.VehicleHandler',
            name='manage-vehicle',
            methods=['GET', 'PUT', 'DELETE'],
        ),
        Route(
            r'/vehicle_group/<key>/vehicle',
            handler='handlers.vehicle.VehicleHandler',
            name='create-vehicle',
            methods=['POST'],
        ),

        ############################################################
        # Vehicle Group
        ############################################################
        Route(
            r'/customer/<key>/vehicle_groups',
            handler='handlers.vehicle_group.VehicleGroupListHandler',
            name='list-vehicle-groups',
            methods=['GET'],
        ),
        Route(
            r'/vehicle_group/<key>',
            handler='handlers.vehicle_group.VehicleGroupHandler',
            name='manage-vehicle-group',
            methods=['GET', 'PUT', 'DELETE'],
        ),
        Route(
            r'/customer/<key>/vehicle_group',
            handler='handlers.vehicle_group.VehicleGroupHandler',
            name='create-vehicle-group',
            methods=['POST'],
        ),


        ############################################################
        # Vehicle Template
        ############################################################
        Route(
            r'/vehicle_templates',
            handler='handlers.vehicle_template.VehicleTemplateHandler',
            name='list-vehicle-templates',
            methods=['GET'],
        ),
        Route(
            r'/vehicle_template/<key>',
            handler='handlers.vehicle_template.VehicleTemplateHandler',
            name='manage-vehicle-template',
            methods=['GET', 'PUT', 'DELETE'],
        ),
        Route(
            r'/tenant/<key>/vehicle_template',
            handler='handlers.vehicle_template.VehicleTemplateHandler',
            name='create-vehicle-template',
            methods=['POST'],
        ),
        Route(
            r'/<filter:(telemetry_provider)>/<key>/vehicle_templates',
            handler='handlers.vehicle_template.VehicleTemplateHandler',
            name='list-telemetry-provider-vehicle-templates',
            methods=['GET'],
        ),

        ############################################################
        # Wheel Schematic Images ALWAYS PUBLIC
        ############################################################
        Route(
            r'/wheel-schematic/<wheel_schematic_info>',
            handler='handlers.wheel_schematic.WheelSchematicHandler',
            name='wheel-schematic-png',
            methods=['GET'],
        ),

        ############################################################
        # Embedded Google Maps Page ALWAYS PUBLIC
        ############################################################
        Route(
            r'/google-map/<lat>/<lon>/<zoom>',
            handler='handlers.geomap.GoogleMapsAPIHandler',
            name='geomap',
            methods=['GET'],
        ),

        ############################################################
        # warmup
        ############################################################
        Route(
            r'/_ah/warmup',
            handler='handlers.warmup.WarmupHandler',
            name='warmup',
        ),
    ]
)

if not on_production_server:
    dev_routes = [

        Route(
            r'/dev/bootstrap',
            handler='handlers.bootstrap.BootstrapHandler',
            name='dev-bootstrap',
        ),
        Route(
            r'/dev/load_bootstrap',
            handler='handlers.dev.LoadBootstrap',
            name='load-bootstrap',
        ),
        Route(
            r'/dev',
            handler='handlers.dev.DevIndex',
            name='dev-index',
        ),
    ]

    for route in dev_routes:
        application.router.add(route)
