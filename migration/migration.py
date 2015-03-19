from env_setup import setup
setup()

from agar.django.templates import render_template
from google.appengine.ext import deferred
from migration_models import (
    MigrationStatus,
    MIGRATION_STATE_NONE,
    MIGRATION_STATE_COMPLETE,
    MIGRATION_STATE_FAILED,
    MIGRATION_STATE_RUNNING,
)
from utils.web_util import build_uri
from webapp2 import RequestHandler
import logging
import traceback

from entity_toucher import DbEntityToucher
from migration_example import MigrationExample
from migration_example_exception import MigrationExampleException
import migration_elf_913
import migration_elf_1048


MIGRATIONS = [
    MigrationExample(),
    MigrationExampleException(),
    DbEntityToucher(name='Touch all SensorReadings', kind_name='SensorReading'),
    DbEntityToucher(name='Touch all Customers', kind_name='Customer'),
    migration_elf_913.DbEntityToucher(name='ELF-913', kind_name='SensorReading'),
    migration_elf_1048.Migration1(name='ELF-1048-1 (touch all SensorReadings within past 30 days)'),
    migration_elf_1048.Migration2(name='ELF-1048-2 (touch all SensorReadings older than ~30 days)'),
]

MIGRATIONS_MAP = {migration.name: migration for migration in MIGRATIONS}


def _get_migration_context(name):
    context = {
        'name': name,
        'running': False,
        'start_date': 'N/A',
        'finish_date': 'N/A',
    }
    migration_status = MigrationStatus.get_by_name(name)
    if migration_status is None:
        context['state'] = MIGRATION_STATE_NONE
        context['running'] = False
        context['color'] = 'LightCyan'
    else:
        if migration_status.start_date is not None:
            context['start_date' ] = migration_status.start_date.isoformat(' ')
        if migration_status.finish_date is not None:
            context['finish_date'] = migration_status.finish_date.isoformat(' ')
        context['state'] = migration_status.state
        if migration_status.state == MIGRATION_STATE_RUNNING:
            context['running'] = True
            context['color'] = 'Lime'
        elif migration_status.state == MIGRATION_STATE_FAILED:
            context['color'] = 'Red'
        elif migration_status.state == MIGRATION_STATE_COMPLETE:
            context['color'] = 'Silver'
        else:
            context['color'] = 'LightCyan'
    return context


def _run_migration(migration_status_key):
    migration_status = migration_status_key.get()
    name = migration_status.name
    migration = MIGRATIONS_MAP[name]
    logging.info("Running migration '{}'".format(name))
    try:
        migration.run()
        migration.complete()
    except:
        MigrationStatus.fail(name)
        logging.error("Exception while running migration '{}': {}".format(name, traceback.format_exc()))


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
            migration_status = MigrationStatus.start(name)
            if migration_status is not None:
                deferred.defer(_run_migration, migration_status.key, _queue='migrations', _target='migration')
            else:
                logging.warning("Migration '{}' already running".format(name))
        else:
            logging.error('Attempted to run invalid migration: {}'.format(name))
        self.redirect(build_uri('migration-listing', module='migration'))
