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
                    name='proof-of-play-start',
            ),
            Route(
                    r'/proofplay/api/v1/0ac1b95dc3f93d9132b796986ed11cd4/post_new_program_play',
                    handler="proofplay.main.PostNewProgramPlay",
                    name="PostNewProgramPlay"
            ),
            Route(
                    r'/proofplay/api/v1/one_resource_by_date/<start_date>/<end_date>/<resource>/<tenant>',
                    handler="proofplay.main.OneResourceByDate",
                    name="OneResourceByDate"
            ),
            Route(
                    r'/proofplay/api/v1/multi_resource_by_date/<start_date>/<end_date>/<resources>/<tenant>',
                    handler="proofplay.main.MultiResourceByDate",
                    name="MultiResourceByDate"
            ),
            Route(
                    r'/proofplay/api/v1/one_resource_by_device/<start_date>/<end_date>/<resource>/<tenant>',
                    handler="proofplay.main.OneResourceByDevice",
                    name="OneResourceByDevice"
            ),
            Route(
                    r'/proofplay/api/v1/retrieve_all_resources/<tenant>',
                    handler="proofplay.main.RetrieveAllResourcesOfTenant",
                    name="RetrieveAllResources"
            ),
            Route(
                    r'/proofplay/api/v1/retrieve_my_tenants',
                    handler="proofplay.main.GetTenants",
                    name="GetTenants"
            ),
        ]
)
