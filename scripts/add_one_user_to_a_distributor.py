from models import User, Distributor
__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'

distributor_name = 'Agosto'
user_email = 'bob.macneal@agosto.com'

user = User.get_or_insert_by_email(email=user_email)
distributor = Distributor.query(Distributor.name == distributor_name).get()

if None == distributor:
    distributor = Distributor.create(name=distributor_name, active=True)
    distributor.put()
    print 'Distributor ' + distributor.name + ' created.'
else:
    print distributor.name + ' found.'

if None == user:
    print 'User not found'
else:
    user.add_distributor(distributor.key)
    print 'SUCCESS! ' + user.email + ' is linked to ' + distributor.name