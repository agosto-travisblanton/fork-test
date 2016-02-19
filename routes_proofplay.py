from env_setup import setup

setup()

# DO NOT REMOVE
# Importing deferred is a work around to this bug.
# https://groups.google.com/forum/?fromgroups=#!topic/webapp2/sHb2RYxGDLc
# noinspection PyUnresolvedReferences
from google.appengine.ext import deferred
from webapp2 import Route, WSGIApplication

BASE_URI = r'/proofplay/api/v1'

application = WSGIApplication([

    Route(
            r'/_ah/start',
            handler='handlers.warmup.StartHandler',
            name='proof-of-play-start',
    ),

    ################################################################
    # POST NEW CONTENT
    ################################################################
    Route(
            BASE_URI + '/0ac1b95dc3f93d9132b796986ed11cd4/post_new_program_play',
            handler="proofplay.main.PostNewProgramPlay",
            name="PostNewProgramPlay"
    ),

    ################################################################
    # RUN QUERIES
    ################################################################
    Route(
            BASE_URI + '/multi_resource_by_date/<start_date>/<end_date>/<resources>/<tenant>/<distributor_key>',
            handler="proofplay.main.MultiResourceByDate",
            name="MultiResourceByDate"
    ),
    Route(
            BASE_URI + '/multi_resource_by_device/<start_date>/<end_date>/<resources>/<tenant>/<distributor_key>',
            handler="proofplay.main.MultiResourceByDevice",
            name="MultiResourceByDevice"
    ),

    Route(
            BASE_URI + '/multi_device_summarized/<start_date>/<end_date>/<devices>/<tenant>/<distributor_key>',
            handler="proofplay.main.MultiDeviceSummarized",
            name="MultiDeviceSummarized"
    ),

    Route(
            BASE_URI + '/multi_device_by_date/<start_date>/<end_date>/<devices>/<tenant>/<distributor_key>',
            handler="proofplay.main.MultiDeviceByDate",
            name="MultiDeviceByDate"
    ),

    ################################################################
    # REST DATA FOR UI
    ################################################################
    Route(
            BASE_URI + '/retrieve_all_resources/<tenant>',
            handler="proofplay.main.RetrieveAllResourcesOfTenant",
            name="RetrieveAllResources"
    ),
    Route(
            BASE_URI + '/retrieve_all_displays/<tenant>',
            handler="proofplay.main.RetrieveAllDevicesOfTenant",
            name="RetrieveAllDevicesOfTenant"
    ),
    Route(
            BASE_URI + '/retrieve_my_tenants',
            handler="proofplay.main.GetTenants",
            name="GetTenants"
    ),
]
)

