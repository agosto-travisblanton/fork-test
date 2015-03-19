import env_setup; env_setup.setup()

from webapp2 import RequestHandler

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class IndexHandler(RequestHandler):
    def get(self):
        self.response.out.write("Warmed Up")
