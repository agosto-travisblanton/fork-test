from env_setup import setup
setup()

import os

from google.appengine.ext import ereporter

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
        # index
        ############################################################
        Route(
            r'/',
            handler="handlers.index.IndexHandler",
            name='index',
        ),

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
            handler='handlers.device_enrollment.DeviceEnrollmentHandler',
            name='devices',
        ),
        Route(
            r'/api/v1/devices/<device_id>',
            handler='handlers.device_enrollment.DeviceEnrollmentHandler',
            name='devices-mutator',
        ),
    ]
)

# if not on_production_server:
#     dev_routes = [
#
#         Route(
#             r'/dev/bootstrap',
#             handler='handlers.bootstrap.BootstrapHandler',
#             name='dev-bootstrap',
#         ),
#         Route(
#             r'/dev/load_bootstrap',
#             handler='handlers.dev.LoadBootstrap',
#             name='load-bootstrap',
#         ),
#         Route(
#             r'/dev',
#             handler='handlers.dev.DevIndex',
#             name='dev-index',
#         ),
#     ]
#
#     for route in dev_routes:
#         application.router.add(route)
