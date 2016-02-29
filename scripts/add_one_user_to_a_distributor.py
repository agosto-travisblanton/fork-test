from models import User, Distributor
__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'

user = User.get_or_insert_by_email(email='bob.macneal@agosto.com')
distributor = Distributor.query(Distributor.name == 'Agosto').get()

if None == distributor:
    print 'Distributor not found'
else:
    if None == user:
        print 'User not found'
    else:
        user.add_distributor(distributor.key)
        print 'SUCCESS! ' + user.email + ' is linked to ' + distributor.name
