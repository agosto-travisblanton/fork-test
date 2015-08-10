import env_setup;

env_setup.setup()

import logging
from google.appengine.api import modules
from webapp2 import RequestHandler


class WarmupHandler(RequestHandler):
    def get(self):
        logging.info('Warmed up!')
        self.response.out.write("Warmed Up")


class StartHandler(RequestHandler):
    def get(self):
        logging.info('{} started successfully.'.format(modules.get_current_module_name()))
