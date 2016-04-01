__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'
from models import Distributor

distributor_name = 'Agosto'

distributor = Distributor.query(Distributor.name == distributor_name).get()
if None == distributor:
    distributor = Distributor.create(name=distributor_name, active=True)
    distributor.put()
    print 'Distributor ' + distributor.name + ' has been added'
else:
    print 'Distributor ' + distributor.name + ' already exists.'