__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'
from models import Distributor

distributor = Distributor.query(Distributor.name == 'Agosto').get()
if None == distributor:
    distributor = Distributor.create(name='Agosto',active=True)
    distributor_key = distributor.put()
    print 'Distributor ' + distributor.name + ' has been added'
else:
    print 'Distributor ' + distributor.name + ' already exists.'
