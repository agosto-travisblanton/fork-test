import json
import logging
import re

from webapp2 import RequestHandler

from app_config import config
from decorators import has_admin_user_key
from models import IntegrationEventLog
from ndb_mixins import PagingListHandlerMixin, KeyValidatorMixin
from restler.serializers import json_response
from strategy import INTEGRATION_EVENT_LOG_STRATEGY

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class IntegrationEventsLogHandler(RequestHandler, PagingListHandlerMixin, KeyValidatorMixin):

    @has_admin_user_key
    def get_list(self):
        category_filter = config.INTEGRATION_EVENTS_DEFAULT_EVENTS_CATEGORY
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

