from agar.env import on_development_server
from agar.sessions import SessionRequestHandler
import base64
from cloudstorage import common, api_utils, storage_api, errors
import cloudstorage
from cloudstorage.common import LOCAL_GCS_ENDPOINT
from restler.serializers import json_response


# WARNING! HUGE KLUDGE!
# cloudstorage_api sets the api_url to os.environ.get('HTTP_HOST') which DOES NOT WORK when using forward*
# The following functions (local_stat and local_open) override the api_url and always use localhost:8080
def local_stat(filename, retry_params=None, _account_id=None):
    """Identical to cloudstorage_api.stat EXCEPT for changing api.api_url to localhost"""
    common.validate_file_path(filename)
    api = storage_api._get_storage_api(retry_params=retry_params, account_id=_account_id)
    api.api_url = 'http://{}{}'.format('localhost:8080', LOCAL_GCS_ENDPOINT)  # <----- HERE'S THE KLUDGE
    status, headers, content = api.head_object(api_utils._quote_filename(filename))
    errors.check_status(status, [200], filename, resp_headers=headers, body=content)
    file_stat = common.GCSFileStat(
        filename=filename,
        st_size=common.get_stored_content_length(headers),
        st_ctime=common.http_time_to_posix(headers.get('last-modified')),
        etag=headers.get('etag'),
        content_type=headers.get('content-type'),
        metadata=common.get_metadata(headers))

    return file_stat


def local_open(filename, mode='r', content_type=None, options=None,
               read_buffer_size=storage_api.ReadBuffer.DEFAULT_BUFFER_SIZE, retry_params=None, _account_id=None,
               offset=0):
    """Identical to cloudstorage_api.open EXCEPT for changing api.api_url to localhost"""
    common.validate_file_path(filename)
    api = storage_api._get_storage_api(retry_params=retry_params, account_id=_account_id)
    api.api_url = 'http://{}{}'.format('localhost:8080', LOCAL_GCS_ENDPOINT)  # <----- HERE'S THE KLUDGE
    filename = api_utils._quote_filename(filename)

    if mode == 'w':
        common.validate_options(options)
        return storage_api.StreamingBuffer(api, filename, content_type, options)
    elif mode == 'r':
        if content_type or options:
            raise ValueError('Options and content_type can only be specified for writing mode.')
        return storage_api.ReadBuffer(api, filename, buffer_size=read_buffer_size)
    else:
        raise ValueError('Invalid mode %s.' % mode)


class DownloadFileHandler(SessionRequestHandler):
    def get(self, base64_filename):
        # see notes at top of file as to why we are doing this:
        stat_func = local_stat if on_development_server else cloudstorage.stat

        filename = base64.b64decode(base64_filename)
        gcs_stat = stat_func(filename)
        if gcs_stat is None:
            error = 'Failed to stat {}'.format(filename)
            json_response(self.response, {'error': error}, status_code=400)
            return

        open_func = local_open if on_development_server else cloudstorage.open
        self.response.headers['Content-Type'] = gcs_stat.content_type
        with open_func(filename) as gcs_file:
            self.response.write(gcs_file.read())
