from models import Distributor, User, DistributorUser

USER = "thomas.blade@agosto.com"

def all_distributor_keys():
    distributor_keys_to_add_to_user = []
    d = Distributor.query().fetch()
    for e in d:
        distributor_keys_to_add_to_user.append(e.key)

    return distributor_keys_to_add_to_user


def filtered_distributor_keys():
    u = User.get_or_insert_by_email(USER)
    du = DistributorUser.query().fetch()
    distributor_keys_to_add_to_user = all_distributor_keys()

    for each_pair in du:
        if each_pair.user_key == u.key:
            distributor_keys_to_add_to_user.remove(each_pair.distributor_key)

    return distributor_keys_to_add_to_user


def add_user_to_remaining_keys():
    remaining_keys = filtered_distributor_keys()
    u = User.get_or_insert_by_email(USER)
    for each_key in remaining_keys:
        u.add_distributor(each_key)
    print "ALL DONE"


def kick_off():
    if not User.get_by_email(USER):
        print "ERROR: NO USER WITH THIS NAME"

    else:
        add_user_to_remaining_keys()


kick_off()