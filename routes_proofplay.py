from env_setup import setup

setup()

from os import path

basedir = path.abspath(path.dirname(__file__))

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
        BASE_URI + '/post_new_program_play',
        handler="proofplay.main.PostNewProgramPlay",
        name="PostNewProgramPlay"
    ),

    ################################################################
    # RUN QUERIES
    ################################################################
    ################################################################
    # BY RESOURCE
    ################################################################
    Route(
        BASE_URI + '/multi_resource_by_date/<start_date>/<end_date>/<resource_identifiers>/<tenant>/<distributor_key>',
        handler="proofplay.main.MultiResourceByDate",
        name="MultiResourceByDate"
    ),
    Route(
        BASE_URI + '/multi_resource_by_device/<start_date>/<end_date>/<resource_identifiers>/<tenant>/<distributor_key>',
        handler="proofplay.main.MultiResourceByDevice",
        name="MultiResourceByDevice"
    ),
    ################################################################
    # BY DEVICE
    ################################################################
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
    # BY LOCATION
    ################################################################
    Route(
        BASE_URI + '/multi_location_summarized/<start_date>/<end_date>/<locations>/<tenant>/<distributor_key>',
        handler="proofplay.main.MultiLocationSummarized",
        name="MultiLocationSummarized"
    ),

    Route(
        BASE_URI + '/multi_location_by_device/<start_date>/<end_date>/<locations>/<tenant>/<distributor_key>',
        handler="proofplay.main.MultiLocationByDevice",
        name="MultiLocationByDevice"
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
    Route(
        BASE_URI + '/retrieve_all_locations/<tenant>',
        handler="proofplay.main.RetrieveAllLocationsOfTenant",
        name="RetrieveAllLocationsOfTenant"
    ),

    ################################################################
    # Migrate DB
    ################################################################

    Route(
        BASE_URI + '/0730578567129494/make_migration',
        handler="proofplay.main.MakeMigration",
        name="MakeMigration"
    ),
]
)
