from app_config import config
from models import Distributor
__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'

distributors = Distributor.query().fetch(100)
print 'Distributor count = ' + str(len(distributors))
for distributor in distributors:
    distributor.content_manager_url = config.DEFAULT_CONTENT_MANAGER_URL
    distributor.player_content_url = config.DEFAULT_PLAYER_CONTENT_URL
    distributor.put()
    print distributor.name + ' content_manager_url and player_content_url have been updated'
