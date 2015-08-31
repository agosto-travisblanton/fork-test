from google.appengine.ext import deferred
from mapreduce import mapreduce_pipeline
from migration_models import MigrationOperation
import logging


class MigrationBase(object):
    def __init__(self, name):
        self.name = name

    def run(self):
        raise NotImplementedError()

    def complete(self):
        MigrationOperation.complete(self.name)
        logging.info("'{}' has completed.".format(self.name))


def _poll_for_mapreduce_pipeline_completion(migration_name, remaining_pipeline_ids, aborted_pipeline_ids=[]):
    remaining_pipeline_ids = set(remaining_pipeline_ids)
    completed_pipeline_ids = []
    for pipeline_id in remaining_pipeline_ids:
        pipeline = mapreduce_pipeline.MapreducePipeline.from_id(pipeline_id)
        if pipeline.was_aborted:  # FIXME: this condition is never hit; figure out how to detect mapreduce failure
            aborted_pipeline_ids.append(pipeline_id)
            logging.error("MapReduce migration '{}' pipeline '{}' was aborted".format(migration_name, pipeline_id))
        elif pipeline.has_finalized:
            completed_pipeline_ids.append(pipeline_id)
            logging.info("MapReduce migration '{}' pipeline '{}' has finalized".format(migration_name, pipeline_id))
    remaining_pipeline_ids = remaining_pipeline_ids.difference(completed_pipeline_ids)
    remaining_pipeline_ids = remaining_pipeline_ids.difference(aborted_pipeline_ids)

    if len(remaining_pipeline_ids) != 0:
        deferred.defer(_poll_for_mapreduce_pipeline_completion, migration_name, remaining_pipeline_ids,
                       aborted_pipeline_ids, _queue='migrations', _countdown=5)
    elif len(aborted_pipeline_ids) != 0:
        logging.error("MapReduce migration '{}' failed because the following pipelines were aborted: {}".
                      format(migration_name, ' '.join(aborted_pipeline_ids)))
        MigrationOperation.fail(migration_name)
    else:
        MigrationOperation.complete(migration_name)
        logging.info("Completed migration '{}'".format(migration_name))


class MapReduceMigration(MigrationBase):
    def complete(self):
        # Completion is signalled via pipeline completion.
        pass

    def poll_for_completion(self, pipeline_ids):
        deferred.defer(_poll_for_mapreduce_pipeline_completion, self.name, pipeline_ids, _queue='migrations',
                       _countdown=5)
