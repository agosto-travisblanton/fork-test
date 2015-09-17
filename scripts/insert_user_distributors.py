from models import Distributor, User, DistributorUser

names = ['Agosto, Inc.', 'Tierney Bros., Inc.', 'Samsung Company']
for name in names:
    matching = Distributor.query(Distributor.name == name).fetch(1)
    if len(matching) == 0:
        distributor = Distributor(name=name)
        distributor_key = distributor.put()
    else:
        distributor_key = matching[0].key

    users = User.query().fetch(10)
    for user in users:
        distributor_user = DistributorUser(user_key=user.key, distributor_key=distributor_key)
        distributor_user.put()
