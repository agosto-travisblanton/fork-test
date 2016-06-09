from models import User, Distributor

distributor_name = 'FASTSIGNS'
user_email = 'daniel.ternyak@agosto.com'

user = User.get_or_insert_by_email(email=user_email)
distributor = Distributor.query(Distributor.name == distributor_name).get()

if distributor:

    user.add_distributor(distributor.key)
    print 'SUCCESS! ' + user.email + ' is linked to ' + distributor.name

else:
    print "THIS DISTRIBUTOR DOES NOT EXIST"
