from app_config import config

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class ContentManagerApi(object):
    """ Facade around our Content Manager API. """

    HEADERS = {
        'Content-Type': 'application/json'
    }

    def __init__(self):
        self.HEADERS['Authorization'] = 'key={0}'.format(config.CONTENT_MANAGER_API_SERVER_KEY)

    def create_tenant(self):
        pass
