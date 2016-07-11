from datetime import datetime
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb
from restler.decorators import ae_ndb_serializer


@ae_ndb_serializer
class PlayerCommandEvent(ndb.Model):
    device_urlsafe_key = ndb.StringProperty(required=True, indexed=True)
    payload = ndb.StringProperty(required=True, indexed=True)
    gcm_registration_id = ndb.StringProperty(required=True, indexed=True)
    gcm_message_id = ndb.StringProperty(required=False, indexed=True)
    user_identifier = ndb.StringProperty(required=False, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    posted = ndb.DateTimeProperty(required=True, indexed=True)
    confirmed = ndb.DateTimeProperty(required=False, indexed=True)
    player_has_confirmed = ndb.BooleanProperty(default=False, required=True, indexed=True)
    class_version = ndb.IntegerProperty()

    @classmethod
    def create(cls, device_urlsafe_key, payload, gcm_registration_id, player_has_confirmed=False, user_identifier='NA'):
        return cls(device_urlsafe_key=device_urlsafe_key,
                   payload=payload,
                   gcm_registration_id=gcm_registration_id,
                   player_has_confirmed=player_has_confirmed,
                   posted=datetime.utcnow(),
                   user_identifier=user_identifier)

    @classmethod
    def get_events_by_device_key(cls, device_urlsafe_key, fetch_size=25, prev_cursor_str=None,
                                 next_cursor_str=None):

        objects = None
        next_cursor = None
        prev_cursor = None

        if not prev_cursor_str and not next_cursor_str:
            objects, next_cursor, more = PlayerCommandEvent.query(
                PlayerCommandEvent.device_urlsafe_key == device_urlsafe_key).order(
                -PlayerCommandEvent.posted).fetch_page(
                page_size=fetch_size)

            prev_cursor = None
            next_cursor = next_cursor.urlsafe() if more else None

        elif next_cursor_str:
            cursor = Cursor(urlsafe=next_cursor_str)
            objects, next_cursor, more = PlayerCommandEvent.query(
                PlayerCommandEvent.device_urlsafe_key == device_urlsafe_key).order(
                -PlayerCommandEvent.posted).fetch_page(
                page_size=fetch_size,
                start_cursor=cursor
            )

            prev_cursor = next_cursor_str
            next_cursor = next_cursor.urlsafe() if more else None

        elif prev_cursor_str:
            cursor = Cursor(urlsafe=prev_cursor_str)
            objects, prev, more = PlayerCommandEvent.query(
                PlayerCommandEvent.device_urlsafe_key == device_urlsafe_key).order(
                PlayerCommandEvent.posted).fetch_page(
                page_size=fetch_size,
                start_cursor=cursor.reversed()
            )

            # needed because we are using a reverse cursor
            objects.reverse()

            next_cursor = prev_cursor_str
            prev_cursor = prev.urlsafe() if more else None

        to_return = {
            'objects': objects or [],
            'next_cursor': next_cursor,
            'prev_cursor': prev_cursor,
        }

        return to_return

    def _pre_put_hook(self):
        self.class_version = 1
