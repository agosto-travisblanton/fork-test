from google.appengine.ext import ndb
from webapp2 import RequestHandler

from app_config import config
from decorators import has_admin_user_key, requires_api_token
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

    @requires_api_token
    def get_enrollment_events(self):
        device_key = self.request.get('deviceKey')
        if device_key:
            query_results = IntegrationEventLog.query(
                ndb.AND(IntegrationEventLog.event_category == 'Registration',
                        IntegrationEventLog.device_urlsafe_key == device_key)).order(
                IntegrationEventLog.utc_timestamp).fetch()
            json_response(self.response, query_results, strategy=INTEGRATION_EVENT_LOG_STRATEGY)
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
