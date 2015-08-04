from env_setup import setup
setup()

# DO NOT REMOVE
# Importing deferred is a work around to this bug.
# https://groups.google.com/forum/?fromgroups=#!topic/webapp2/sHb2RYxGDLc
# noinspection PyUnresolvedReferences
from google.appengine.ext import deferred

from webapp2 import Route, WSGIApplication

application = WSGIApplication(
    [
        Route(
            r'/_ah/start',
            handler='handlers.warmup.StartHandler',
            name='migration-start',
        ),

        Route(
            r'/migration/',
            handler='migration.migration.MigrationListingHandler',
            name='migration-listing',
            methods=['GET'],
        ),

        Route(
            r'/migration/migrate',
            handler='migration.migration.MigrationRunHandler',
            name='migration-run',
            methods=['POST'],
        ),
    ]
)


