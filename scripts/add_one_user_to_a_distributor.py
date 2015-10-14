from models import User, Distributor

user = User.query(User.email == 'bob.macneal@agosto.com').get()

distributor = Distributor.query(Distributor.name == 'Agosto').get()
user.add_distributor(distributor.key)

print 'User ' + user.email + ' is now linked to ' + distributor.name
