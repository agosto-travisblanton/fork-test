from migration_base import MapReduceMigration
from google.appengine.ext import ndb
from mapreduce import mapreduce_pipeline, base_handler
from migration_models import MigrationOperation
import logging
from mapreduce import operation as op
import models  # DO NOT REMOVE; needed for mapper


class DbEntityToucher(MapReduceMigration):
    def __init__(self, name, kind_name):
        super(DbEntityToucher, self).__init__(name)
        self.name = name
        self.kind_name = kind_name

    def run(self):
        pipeline = DbEntityToucherPipeline(self.name, self.kind_name)
        pipeline.start(queue_name='migrations')
        logging.info('DbEntityToucher started for {}'.format(self.kind_name))
        MigrationOperation.set_debug_info(self.name, 'pipeline_id={}'.format(pipeline.pipeline_id))
        self.poll_for_completion([pipeline.pipeline_id])


def db_entity_toucher_mapper(db_entity):
    ndb_entity = ndb.Key.from_old_key(db_entity.key()).get()
    if ndb_entity is not None:
        yield op.db.Put(ndb_entity)


class DbEntityToucherPipeline(base_handler.PipelineBase):
    def run(self, migration_name, kind_name):
        yield mapreduce_pipeline.MapperPipeline(
            "EntityToucher",
            "migration.entity_toucher.db_entity_toucher_mapper",
            "mapreduce.input_readers.DatastoreInputReader",
            params={
                "input_reader": {
                    "entity_kind": 'models_db.{}'.format(kind_name),
                    'batch_size': 500,
                },
            },
            shards=32
        )
