import json
import logging
from google.appengine.api import urlfetch

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class HttpClient(object):

    def set_default_fetch_deadline(self, limit_in_seconds):
        urlfetch.set_default_fetch_deadline(limit_in_seconds)

    def get(self, http_client_request):
        pass

    def post(self, http_client_request):
        response = None
        try:
            response = urlfetch.fetch(url=http_client_request.url,
                                      payload=http_client_request.payload,
                                      method=urlfetch.POST,
                                      headers=http_client_request.headers,
                                      validate_certificate=False)
        except Exception, e:
            logging.exception(e)
            raise e
        return HttpClientResponse(status_code=response.status_code)

    def put(self, http_client_request):
        response = None
        try:
            response = urlfetch.fetch(url=http_client_request.url,
                                      payload=http_client_request.payload,
                                      method=urlfetch.PUT,
                                      headers=http_client_request.headers,
                                      validate_certificate=False)
        except Exception, e:
            logging.exception(e)
            raise e
        return HttpClientResponse(status_code=response.status_code)

    def delete(self, http_client_request):
        response = None
        try:
            response = urlfetch.fetch(url=http_client_request.url,
                                      payload=http_client_request.payload,
                                      method=urlfetch.DELETE,
                                      headers=http_client_request.headers,
                                      validate_certificate=False)
        except Exception, e:
            logging.exception(e)
            raise e
        return HttpClientResponse(status_code=response.status_code)


class HttpClientRequest(object):
    """ Abstraction representing a HTTP request. """

    def __init__(self, url, payload=None, headers=None):
        self.url = url
        self.headers = headers
        self.payload = payload


class HttpClientResponse(object):
    """ Abstraction representing a HTTP response. """

    def __init__(self, status_code=200, content=None):
        self.status_code = status_code
        self.content = content

    def status_code(self):
        return self.status_code

    def json_content(self):
        return json.loads(self.content)

    def content(self):
        return self.content
