﻿from datetime import datetime
from google.appengine.ext import ndb
import logging

MIGRATION_STATUS_QUEUED = 'Queued'
MIGRATION_STATUS_RUNNING = 'Running'
MIGRATION_STATUS_FAILED = 'Failed'
MIGRATION_STATUS_COMPLETED = 'Completed'
MIGRATION_STATUSES = [MIGRATION_STATUS_QUEUED, MIGRATION_STATUS_RUNNING, MIGRATION_STATUS_FAILED,
                      MIGRATION_STATUS_COMPLETED]


class MigrationOperation(ndb.Model):
    start_time = ndb.DateTimeProperty()
    finish_time = ndb.DateTimeProperty()
    status = ndb.StringProperty(required=True, choices=MIGRATION_STATUSES, default=MIGRATION_STATUS_QUEUED)
    debug_info = ndb.StringProperty()
    class_version = ndb.IntegerProperty()

    @property
    def name(self):
        return self.key.id()

    @classmethod
    def get_by_name(cls, name):
        return cls.get_by_id(name)

    @classmethod
    def get_or_insert_by_name(cls, name):
        return cls.get_or_insert(name)

    @classmethod
    @ndb.transactional
    def start(cls, name):
        migration = cls.get_or_insert_by_name(name)
        if migration.status == MIGRATION_STATUS_RUNNING:
            migration = None
        else:
            migration.status = MIGRATION_STATUS_RUNNING
            migration.start_time = datetime.utcnow()
            migration.finish_time = None
            migration.put()
        return migration

    @classmethod
    @ndb.transactional
    def fail(cls, name):
        migration = cls.get_by_name(name)
        if migration is None:
            logging.warning("Attempt to FAIL '{0}' which could not be retrieved from data store.".format(name))
        else:
            if migration.status != MIGRATION_STATUS_RUNNING:
                logging.warning("FAIL '{0}' with status '{1}'".format(migration.name, migration.status))
            migration.status = MIGRATION_STATUS_FAILED
            migration.finish_time = datetime.utcnow()
            migration.put()
        return migration

    @classmethod
    @ndb.transactional
    def complete(cls, name):
        migration = cls.get_by_name(name)
        if migration is None:
            logging.warning("Attempt to COMPLETE '{0}' which counld not be retrieved from data store.".format(name))
        elif migration.status != MIGRATION_STATUS_RUNNING:
            logging.warning("COMPLETE '{0}' with status '{1}'".format(migration.name, migration.status))
        else:
            migration.status = MIGRATION_STATUS_COMPLETED
            migration.finish_time = datetime.utcnow()
            migration.put()
        return migration

    @classmethod
    @ndb.transactional
    def set_debug_info(cls, name, debug_info):
        migration = cls.get_by_name(name)
        if migration is not None:
            migration.debug_info = debug_info
            migration.put()
        return migration

    def _pre_put_hook(self):
        self.class_version = 1
