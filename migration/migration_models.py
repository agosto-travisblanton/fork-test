from datetime import datetime
from google.appengine.ext import ndb
import logging


MIGRATION_STATE_NONE = 'None'
MIGRATION_STATE_RUNNING = 'Running'
MIGRATION_STATE_FAILED = 'Failed'
MIGRATION_STATE_COMPLETE = 'Complete'
MIGRATION_STATES = [MIGRATION_STATE_NONE, MIGRATION_STATE_RUNNING, MIGRATION_STATE_FAILED, MIGRATION_STATE_COMPLETE]


class MigrationStatus(ndb.Model):
    start_date = ndb.DateTimeProperty()
    finish_date = ndb.DateTimeProperty()
    state = ndb.StringProperty(required=True, choices=MIGRATION_STATES, default=MIGRATION_STATE_NONE)
    debug_info = ndb.StringProperty()

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
        migration_status = cls.get_or_insert_by_name(name)
        if migration_status.state == MIGRATION_STATE_RUNNING:
            migration_status = None
        else:
            migration_status.state = MIGRATION_STATE_RUNNING
            migration_status.start_date = datetime.utcnow()
            migration_status.finish_date = None
            migration_status.put()
        return migration_status

    @classmethod
    @ndb.transactional
    def fail(cls, name):
        status = cls.get_by_name(name)
        if status is None:
            logging.warning("Attempted to fail invalid migration '{}'".format(name))
        else:
            if status.state != MIGRATION_STATE_RUNNING:
                logging.warning("Failed migration '{}' while in state '{}'".format(status.name, status.state))

            # 'Failed' state trumps all other states.
            status.state = MIGRATION_STATE_FAILED
            status.finish_date = datetime.utcnow()
            status.put()

    @classmethod
    @ndb.transactional
    def complete(cls, name):
        status = cls.get_by_name(name)
        if status is None:
            logging.warning("Attempted to complete invalid migration '{}'".format(name))
        elif status.state != MIGRATION_STATE_RUNNING:
            logging.warning("Completed migration '{}' while in state '{}'".format(status.name, status.state))
        else:
            status.state = MIGRATION_STATE_COMPLETE
            status.finish_date = datetime.utcnow()
            status.put()

    @classmethod
    @ndb.transactional
    def set_debug_info(cls, name, debug_info):
        status = cls.get_by_name(name)
        if status is not None:
            status.debug_info = debug_info
            status.put()

