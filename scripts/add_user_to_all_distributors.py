from models import Distributor, User, DistributorUser


def all_distributor_keys():
    distributor_keys_to_add_to_user = []
    d = Distributor.query().fetch()
    for e in d:
        distributor_keys_to_add_to_user.append(e.key)

    return distributor_keys_to_add_to_user


def filtered_distributor_keys(user):
    u = User.get_or_insert_by_email(user)
    du = DistributorUser.query().fetch()
    distributor_keys_to_add_to_user = all_distributor_keys()

    for each_pair in du:
        if each_pair.user_key == u.key:
            distributor_keys_to_add_to_user.remove(each_pair.distributor_key)

    return distributor_keys_to_add_to_user


def add_user_to_remaining_keys(user):
    remaining_keys = filtered_distributor_keys(user)
    u = User.get_or_insert_by_email(user)
    for each_key in remaining_keys:
        u.add_distributor(each_key)
    print "ALL DONE"


def kick_off(user):
    if not User.get_by_email(user):
        print "ERROR: NO USER WITH THIS NAME"

    else:
        add_user_to_remaining_keys(user)


if __name__ == '__main__':
    kick_off("daniel.ternyak@agosto.com")
