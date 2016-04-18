from models import User, Distributor
__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'

distributor_name = 'Hardwired Local LLC'
user_email = 'marla.geary@agosto.com'
admin_email = 'skykit@hardwired.skykit.com'

user = User.get_or_insert_by_email(email=user_email)
distributor = Distributor.query(Distributor.name == distributor_name).get()

if None == distributor:
    distributor = Distributor.create(name=distributor_name, active=True)
    distributor.admin_email = admin_email
    distributor.put()
    print 'Distributor ' + distributor.name + ' created.'
else:
    distributor.admin_email = admin_email
    distributor.put()
    print distributor.name + ' found.'

if None == user:
    print 'User not found'
else:
    user.add_distributor(distributor.key)
    print 'SUCCESS! ' + user.email + ' is linked to ' + distributor.name
