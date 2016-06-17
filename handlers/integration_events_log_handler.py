from google.appengine.ext import ndb
from webapp2 import RequestHandler

from app_config import config
from decorators import has_admin_user_key
from models import IntegrationEventLog
from ndb_mixins import PagingListHandlerMixin, KeyValidatorMixin
from restler.serializers import json_response
from strategy import INTEGRATION_EVENT_LOG_STRATEGY

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class IntegrationEventsLogHandler(RequestHandler, PagingListHandlerMixin, KeyValidatorMixin):
    INTEGRATION_EVENTS_DEFAULT_EVENTS_CATEGORY = 'Registration'

    @has_admin_user_key
    def get_by_event_category(self):
        category_filter = self.INTEGRATION_EVENTS_DEFAULT_EVENTS_CATEGORY
        event_category = self.request.get('eventCategory')
        if event_category:
            category_filter = event_category
        fetch_size = config.INTEGRATION_EVENTS_DEFAULT_FETCH_SIZE
        page_size = self.request.get('pageSize')
        if page_size:
            fetch_size = int(page_size)
        query_results = IntegrationEventLog.query(IntegrationEventLog.event_category == category_filter).order(
            IntegrationEventLog.utc_timestamp).fetch(fetch_size)
        json_response(self.response, query_results, strategy=INTEGRATION_EVENT_LOG_STRATEGY)

    @has_admin_user_key
    def get_registration_events(self):
        gcm_registration_id = self.request.get('gcmRegistrationId')
        if gcm_registration_id:
            query_results = IntegrationEventLog.query(
                ndb.AND(IntegrationEventLog.event_category == 'Registration',
                        IntegrationEventLog.gcm_registration_id == gcm_registration_id)).order(
                IntegrationEventLog.utc_timestamp).fetch()
            if len(query_results) > 0:
                json_response(self.response, query_results, strategy=INTEGRATION_EVENT_LOG_STRATEGY)
                return
            else:
                error_message = "Unable to find registration events with GCM registration ID: {0}".format(
                    gcm_registration_id)
                self.response.set_status(404, error_message)
                return
        else:
            query_results = IntegrationEventLog.query(IntegrationEventLog.event_category == 'Registration').order(
                IntegrationEventLog.utc_timestamp).fetch()
            if len(query_results) > 0:
                json_response(self.response, query_results, strategy=INTEGRATION_EVENT_LOG_STRATEGY)
                return
            else:
                error_message = 'Unable to find registration events'
                self.response.set_status(404, error_message)
                return
