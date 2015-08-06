from env_setup import setup

setup()

from agar.django.templates import render_template
from google.appengine.ext import deferred
from migration_models import (
    MigrationOperation,
    MIGRATION_STATUS_QUEUED,
    MIGRATION_STATUS_COMPLETED,
    MIGRATION_STATUS_FAILED,
    MIGRATION_STATUS_RUNNING,
)
from utils.web_util import build_uri
from webapp2 import RequestHandler
import logging
import traceback
from device_to_display_conversion import DeviceToDisplayConversion

MIGRATIONS = [
    DeviceToDisplayConversion()
]

MIGRATIONS_MAP = {migration.name: migration for migration in MIGRATIONS}


def _get_migration_context(name):
    context = {
        'name': name,
        'running': False,
        'start_time': 'N/A',
        'finish_time': 'N/A',
    }
    migration_operation = MigrationOperation.get_by_name(name)
    if migration_operation is None:
        context['status'] = MIGRATION_STATUS_QUEUED
        context['running'] = False
        context['color'] = 'LightGrey'
    else:
        if migration_operation.start_time is not None:
            context['start_time'] = migration_operation.start_time.isoformat(' ')
        if migration_operation.finish_time is not None:
            context['finish_time'] = migration_operation.finish_time.isoformat(' ')
        context['status'] = migration_operation.status
        if migration_operation.status == MIGRATION_STATUS_RUNNING:
            context['running'] = True
            context['color'] = 'DarkSeaGreen'
        elif migration_operation.status == MIGRATION_STATUS_FAILED:
            context['color'] = 'Salmon'
        elif migration_operation.status == MIGRATION_STATUS_COMPLETED:
            context['color'] = 'Gold'
        else:
            context['color'] = 'LightGrey'
    return context


def _run_migration(migration_operation_key):
    migration_operation = migration_operation_key.get()
    name = migration_operation.name
    migration = MIGRATIONS_MAP[name]
    logging.info("Running migration '{}'".format(name))
    try:
        migration.run()
        migration.complete()
    except Exception, e:
        logging.exception(e)
        logging.error("Traceback for error on migration '{0}': {1}".format(name, traceback.format_exc()))
        MigrationOperation.fail(name)


class MigrationListingHandler(RequestHandler):
    def get(self):
        context = {
            'migrations': [_get_migration_context(migration.name) for migration in MIGRATIONS],
            'run_uri': build_uri('migration-run', module='migration')
        }
        render_template(self.response, 'migration/listing.html', context=context)


class MigrationRunHandler(RequestHandler):
    def post(self):
        name = self.request.get('name')
        if name in MIGRATIONS_MAP:
            migration_operation = MigrationOperation.start(name)
            if migration_operation is not None:
                _run_migration(migration_operation.key)
                # deferred.defer(_run_migration, migration_status.key, _queue='migrations', _target='migration')
            else:
                logging.warning("Migration '{0}' is already running".format(name))
        else:
            logging.error('Attempted to run invalid migration: {0}'.format(name))
        self.redirect(build_uri('migration-listing', module='migration'))
