from google.appengine.api.datastore_errors import BadValueError, BadRequestError
from google.appengine.ext import ndb
from google.net.proto.ProtocolBuffer import ProtocolBufferDecodeError

from app_config import config

INVALID_KEY_TYPE = 'INVALID_KEY_TYPE'
INVALID_KEY = 'INVALID_KEY'
INVALID_CURSOR = 'INVALID_CURSOR'


def string_to_int(s, default):
    try:
        return int(s)
    except:
        return default


class KeyValidatorMixin(object):
    """
    Validates urlsafe representation of an ndb.Key
    """

    def valid_key(self, urlsafe_key, kind_cls):
        '''
        Validates that urlsafe_key is an ndb.Key of type kind_cls
        :param urlsafe_key: an urlsafe key string
        :param kind_cls: a class object
        :return: (True, ndb.Key) tuple if the key is valid.  Aborts with a 400 error if the key is not of type kind_cls or is not a
        valid ndb.Key.  If key is None, (False, None) tuple is returned
        '''

        try:
            if urlsafe_key:
                key = ndb.Key(urlsafe=urlsafe_key)
                if key.kind() == kind_cls.__name__:
                    return True, key
                else:
                    self.abort(400, INVALID_KEY_TYPE)
        except ProtocolBufferDecodeError:
            self.abort(400, INVALID_KEY)

        return False, None

    def validate_and_get(self, urlsafe_key, kind_cls, abort_on_not_found=False, use_app_engine_memcache=True):
        '''
        Validates that urlsafe_key is an ndb.Key of type kind_cls, and if it is, retrieves and returns the object
        :param urlsafe_key: an urlsafe key string
        :param kind_cls: a class object
        :param abort_on_not_found: if the key is valid but the object is not found, True will cause this method to
        abort with a 404; False will cause None to be returned.
        :param use_app_engine_memcache: Passing False will bypass App Engine's standard caching service memcache.
        Default is True which is to use App Engine's memcache .
        :return: If the key is valid and the object exists, the object is returned.  If the key is invalid, the method
        will abort with a 400.
        '''
        obj = None
        valid, key = self.valid_key(urlsafe_key, kind_cls)
        if valid:
            obj = key.get(use_memcache=use_app_engine_memcache)
            if obj is None and abort_on_not_found:
                self.abort(404, "%s not found" % kind_cls.__name__)

        return obj



    def get_or_except(self, urlsafe_key, kind_cls, use_app_engine_memcache=True):
        obj = None
        valid, key = self.valid_key(urlsafe_key, kind_cls)
        if valid:
            obj = key.get(use_memcache=use_app_engine_memcache)
            if obj is None:
                raise ValueError("Bad urlsafe_key {}".format(urlsafe_key))

        return obj



class PagingListHandlerMixin(object):
    @property
    def page_size(self):
        """
        The requested ``page_size`` constrained between ``1`` and the configuration value ``app_MAX_PAGE_SIZE``.
        If ``page_size`` isn't passed in, it will default to the configuration value ``app_DEFAULT_PAGE_SIZE``.

        :return: The requested page size for fetching.
        """
        request_page_size = self.request.params.get('page_size', self.request.get('page_size'))
        page_size = string_to_int(request_page_size, config.DEFAULT_PAGE_SIZE)
        page_size = min(max(page_size, 1), config.MAX_PAGE_SIZE)
        return page_size

    @property
    def reverse_direction(self):
        to_reverse = self.request.params.get('reverse_direction', self.request.get('reverse_direction', 'false'))
        to_reverse = to_reverse.lower() == 'true' if to_reverse else False
        return to_reverse

    @property
    def cursor(self):
        request_cursor = self.request.params.get('cursor', self.request.get('cursor'))
        if request_cursor:
            try:
                request_cursor = ndb.Cursor(urlsafe=request_cursor)
            except (BadValueError, BadRequestError):
                self.abort(400, INVALID_CURSOR)
        else:
            request_cursor = None
        return request_cursor

    def fetch_page(self, query_forward, query_reverse):
        if self.reverse_direction:
            objects, result_cursor, has_prev = query_reverse.fetch_page(self.page_size, start_cursor=self.cursor)
            prev_cursor = result_cursor if has_prev else None
            if self.cursor:
                next_cursor = self.cursor.reversed()
                has_next = True
            else:
                next_cursor = None
                has_next = False
            objects = objects[::-1]  # reverse the list
        else:
            objects, result_cursor, has_next = query_forward.fetch_page(self.page_size, start_cursor=self.cursor)
            next_cursor = result_cursor if has_next else None
            if self.cursor:
                prev_cursor = self.cursor.reversed() if self.cursor else None
                has_prev = True
            else:
                prev_cursor = None
                has_prev = False

        result_data = {
            'objects': objects,
            'paging': {
                'has_next': has_next,
                'next_cursor': next_cursor.urlsafe() if next_cursor else None,
                'has_prev': has_prev,
                'prev_cursor': prev_cursor.urlsafe() if prev_cursor else None
            }
        }

        return result_data
