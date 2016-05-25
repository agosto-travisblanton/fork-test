from env_setup import setup

setup()

from agar.django.templates import render_template
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

from hydrate_tenant_key_on_devices import HydrateTenantKeyOnDevices
from refresh_chrome_device_properties_from_directory_api import RefreshChromeDevicePropertiesFromDirectoryApi
from set_content_manager_base_url_on_tenant import SetContentManagerBaseUrlOnTenant
from hydrate_agosto_default_domain_key_on_tenant import HydrateAgostoDefaultDomainKeyOnTenant
from hydrate_default_user_role_on_distributer_user import HydrateDefaultUserRoleOnDistributerUser

MIGRATIONS = [
    HydrateTenantKeyOnDevices(),
    RefreshChromeDevicePropertiesFromDirectoryApi(),
    SetContentManagerBaseUrlOnTenant(),
    HydrateAgostoDefaultDomainKeyOnTenant(),
    HydrateDefaultUserRoleOnDistributerUser()
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
    logging.info("'{}' is running.".format(name))
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
        name = self.request.get('name').split("|", 2)
        if name[0] == 'rerun':
            migration_name = name[1]
            migration = MigrationOperation.get_by_name(migration_name)
            migration.status = 'Queued'
            migration.put()
        else:
            migration_name = name[0]
        if migration_name in MIGRATIONS_MAP:
            migration_operation = MigrationOperation.start(migration_name)
            if migration_operation is not None:
                logging.info("'{0}' is set to run".format(migration_name))
                _run_migration(migration_operation.key)
                # deferred.defer(_run_migration, migration_operation.key, _queue='migrations', _target='migration')
            else:
                logging.info("'{0}' is already running".format(migration_name))
        else:
            logging.error('Attempted to run invalid migration: {0}'.format(migration_name))
        self.redirect(build_uri('migration-listing', module='migration'))
